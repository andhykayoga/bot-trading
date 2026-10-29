"""AFS-22 order flow (Alvesting), dilengkapi riset — reports/RENCANA_ORDERFLOW_TGE.md.

Delta candle = volume beli taker − volume jual taker (candle 1 jam spot Binance, digabung ke 4 jam pada 00.00 UTC).
Rasio delta = delta ÷ volume. Data: data/orderflow/<SIMBOL>USDT_1h.parquet.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, swing_levels, zone_hit

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "orderflow"


@lru_cache(maxsize=None)
def rasio_delta(symbol: str, tf: str) -> pd.Series:
    d = pd.read_parquet(DATA / f"{symbol.replace('USD', '')}USDT_1h.parquet")
    if tf == "H4":
        d = d.groupby(d["t"].dt.floor("4h")).agg(v=("v", "sum"), tbv=("tbv", "sum")).reset_index()
    elif tf != "H1":
        raise ValueError(tf)
    r = (2 * d["tbv"] - d["v"]) / d["v"].replace(0, np.nan)
    return pd.Series(r.to_numpy(), index=d["t"].astype("datetime64[ns]").astype("int64").to_numpy())


def rasio_untuk(ctx: Ctx, symbol: str, tf: str) -> np.ndarray:
    def build():
        s = rasio_delta(symbol, tf)
        return s.reindex(ctx.b.t_open).to_numpy()
    return ctx._memo(f"delta_{tf}", build)


class AFS22D(Setup):
    id = "AFS-22D"
    name = "Divergensi delta di zona support/resistance"
    mentor = "Alvesting (Akademi Crypto) — order flow (Q-51), dilengkapi riset"
    category = "reversal"
    entry_tf = "H1"
    defaults = {"tf": "H1", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H1", "H4"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        rd = rasio_untuk(ctx, sym, tf)
        out = []
        for t in range(30, len(b)):
            if np.isnan(a[t]) or np.isnan(rd[t]):
                continue
            half = 0.5 * a[t]
            if b.c[t] < b.o[t] and rd[t] > 0:          # candle merah, delta positif → bullish di support
                zona = swing_levels(ctx, t, "low", 150)[:3]
                if any(zone_hit(b.l[t], b.h[t], z, half) for z in zona):
                    sl = b.l[t] - p["sl_atr"] * a[t]
                    out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=float(sl), tp_rr=2.0,
                                     min_rr=2.0, label="trading", entry_tf=tf))
            elif b.c[t] > b.o[t] and rd[t] < 0:        # candle hijau, delta negatif → bearish di resistance
                zona = swing_levels(ctx, t, "high", 150)[:3]
                if any(zone_hit(b.l[t], b.h[t], z, half) for z in zona):
                    sl = b.h[t] + p["sl_atr"] * a[t]
                    out.append(Order(self.id, sym, -1, int(b.t_close[t]), "market", sl=float(sl), tp_rr=2.0,
                                     min_rr=2.0, label="trading", entry_tf=tf))
        return out


class DeltaFilter(Setup):
    """AFS-22F: setup dasar, tetapi long hanya kalau rasio delta candle sinyal > 0, short hanya kalau < 0."""

    def __init__(self, base: Setup):
        self.base = base
        self.id = f"{base.id}+delta"
        self.name = f"{base.name} + filter delta"
        self.mentor = base.mentor
        self.category = base.category
        self.entry_tf = base.entry_tf
        self.defaults = base.defaults
        self.uses_volume = base.uses_volume

    def plan(self):
        return self.base.plan()

    def plan_for(self, market):
        return self.base.plan_for(market)

    def entry_tf_of(self, p):
        return self.base.entry_tf_of(p)

    def category_of(self, p):
        return self.base.category_of(p)

    def signals(self, data, p):
        orders = self.base.signals(data, p)
        tf = self.base.entry_tf_of(p)
        tf = tf if tf in ("H1", "H4") else "H4" if tf in ("D1", "W1") else "H1"
        out = []
        cache = {}
        for o in orders:
            if o.symbol not in cache:
                s = rasio_delta(o.symbol, tf)
                cache[o.symbol] = (s.index.to_numpy(), s.to_numpy(), 3600 * 10**9 * (4 if tf == "H4" else 1))
            idx, val, dur = cache[o.symbol]
            k = np.searchsorted(idx, o.created - dur, side="right") - 1   # candle sinyal yang close di o.created
            if k < 0 or np.isnan(val[k]):
                continue
            if val[k] * o.direction > 0:
                out.append(o)
        return out
