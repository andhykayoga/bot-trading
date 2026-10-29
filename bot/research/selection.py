"""Pemilihan varian dan uji akhir sesuai G-17.

Urutan per setup:
1. Timeframe (kalau diuji, setara) → pilih yang memenuhi syarat dengan Recovery Factor
   terbaik di data pemilihan.
2. Parameter setara lain (mis. RR 1:1,5 vs 1:2, tick volume vs volume dimatikan) → sama.
3. Nilai awal vs varian (satu parameter diubah sekali): nilai awal tetap dipakai kecuali
   ada varian yang memenuhi syarat dan Recovery Factor-nya lebih baik di data penyusunan
   DAN pemilihan.
4. Matikan instrumen yang rugi di data penyusunan dan pemilihan.
5. Uji akhir sekali dengan pilihan yang sudah dikunci.
Syarat ikut dibandingkan: ≥30 transaksi di data pemilihan dan untung bersih di
penyusunan maupun pemilihan.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np

from bot.data.candles import load_instrument
from bot.engine.backtest import Simulator
from bot.engine.metrics import by_symbol, summarize
from bot.engine.orders import Order
from bot.filters import astro
from bot.research.splits import Splits, market_splits
from bot.setups.base import Setup

MIN_TRADES = 30


def key_of(p: dict) -> str:
    return json.dumps(p, sort_keys=True, default=str)


def eligible(r: dict) -> bool:
    return r["sel"]["trades"] >= MIN_TRADES and r["dev"]["net"] > 0 and r["sel"]["net"] > 0


def rf(r: dict, seg: str) -> float:
    x = r[seg]["recovery"]
    return -np.inf if x is None or (isinstance(x, float) and np.isnan(x)) else x


@dataclass
class AstroFilter:
    """Efek filter waktu kalau dinyalakan (07, Q-38, Q-41): pada tanggal kandidat hanya setup
    pembalikan yang boleh masuk (hanya entry H4 ke atas); setup breakout tidak masuk saat
    Merkurius retrograde."""
    adef: astro.AstroDef
    use_retro: bool = True
    cand: dict = field(default_factory=dict)   # symbol -> set hari kandidat
    retro: set = field(default_factory=set)

    @classmethod
    def build(cls, adef: astro.AstroDef, symbols, use_retro=True) -> "AstroFilter":
        f = cls(adef, use_retro)
        for s in symbols:
            f.cand[s] = astro.candidate_day_set(load_instrument(s)["D1"], adef)
        f.retro = astro.retro_day_set()
        return f

    def allows(self, setup: Setup, p: dict, o: Order, day: int) -> bool:
        cat = setup.category_of(p)
        if o.entry_tf in ("H4", "D1", "W1") and cat not in ("reversal", "both") \
                and day in self.cand.get(o.symbol, ()):
            return False
        if self.use_retro and cat in ("breakout", "both") and day in self.retro:
            return False
        return True


class Evaluator:
    def __init__(self, market: str = "forex"):
        self.market = market
        self.sim = Simulator(market)
        self.splits: Splits = market_splits(market)
        self.data = {s: load_instrument(s) for s in self.sim.syms}
        self._sig: dict[str, list[Order]] = {}

    def orders(self, setup: Setup, p: dict) -> list[Order]:
        k = setup.id + key_of(p)
        if k not in self._sig:
            self._sig[k] = setup.signals(self.data, p)
        return self._sig[k]

    def entry_day(self, o: Order) -> int:
        g = self.sim.g
        i = min(int(np.searchsorted(g.t, o.created, side="left")), len(g.t) - 1)
        return int(g.day[i])

    def run(self, setup: Setup, p: dict, seg: str, symbols=None, afilter: AstroFilter | None = None):
        orders = self.orders(setup, p)
        if symbols is not None:
            orders = [o for o in orders if o.symbol in symbols]
        if afilter is not None:
            orders = [o for o in orders if afilter.allows(setup, p, o, self.entry_day(o))]
        a, b = self.splits.seg(seg)
        return self.sim.run(orders, a, b)

    def evaluate(self, setup: Setup, p: dict, segs=("dev", "sel"), symbols=None, afilter=None) -> dict:
        out = {"params": p}
        for s in segs:
            res = self.run(setup, p, s, symbols, afilter)
            out[s] = summarize(res)
            out[s + "_sym"] = by_symbol(res)
            out[s + "_res"] = res
        return out


def _strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if not k.endswith("_res")}


def select(ev: Evaluator, setup: Setup, log=print) -> dict:
    plan = setup.plan_for(ev.market)
    tried: dict[str, dict] = {}

    def run(p):
        k = key_of(p)
        if k not in tried:
            tried[k] = ev.evaluate(setup, p)
            r = tried[k]
            log(f"  {setup.id} {k}: dev {r['dev']['trades']} trx net {r['dev']['net_pct']:.1f}% "
                f"RF {r['dev']['recovery']:.2f} | sel {r['sel']['trades']} trx net {r['sel']['net_pct']:.1f}% "
                f"RF {r['sel']['recovery']:.2f}")
        return tried[k]

    def pick_setara(cands: list[dict]) -> dict:
        res = [run(p) for p in cands]
        ok = [r for r in res if eligible(r)]
        pool = ok if ok else res
        return max(pool, key=lambda r: rf(r, "sel"))["params"]

    base = setup.params()
    stages = []
    if plan.tf:
        base = pick_setara([dict(base, tf=t) for t in plan.tf])
        stages.append(("timeframe", plan.tf, base.get("tf")))
    setara = dict(plan.setara)
    if setup.uses_volume and ev.market != "crypto":   # tick volume vs dimatikan hanya untuk forex (D-07)
        setara["volume"] = ["tick", "off"]
    for name, opts in setara.items():
        base = pick_setara([dict(base, **{name: v}) for v in opts])
        stages.append((name, opts, base[name]))
    # nilai awal vs varian
    variants = []
    for name, vals in list(plan.tested.items()) + list(plan.comparisons.items()):
        for v in vals:
            if v != base.get(name):
                variants.append(dict(base, **{name: v}))
    r0 = run(base)
    rv = [run(p) for p in variants]
    better = [r for r in rv if eligible(r) and rf(r, "dev") > rf(r0, "dev") and rf(r, "sel") > rf(r0, "sel")]
    if eligible(r0):
        chosen = max(better, key=lambda r: rf(r, "sel")) if better else r0
        why = "varian lebih baik di penyusunan & pemilihan" if better else "nilai awal / versi mentor dipertahankan"
    else:
        ok = [r for r in [r0] + rv if eligible(r)]
        if not ok:
            ok = [r for r in tried.values() if eligible(r)]
        chosen = max(ok, key=lambda r: rf(r, "sel")) if ok else None
        why = "nilai awal tidak memenuhi syarat; dipilih varian terbaik di data pemilihan" if ok else \
            "tidak ada varian yang memenuhi syarat"
    result = {
        "id": setup.id, "name": setup.name, "mentor": setup.mentor, "priority": setup.priority,
        "category": setup.category, "trials": len(tried), "stages": stages,
        "tried": [_strip(r) for r in tried.values()],
    }
    if chosen is None:
        best = max(tried.values(), key=lambda r: rf(r, "sel"))
        result.update(status="belum bisa dinilai", why=why, chosen=_strip(best))
        return result
    p = chosen["params"]
    active = [s for s in ev.sim.syms
              if not (chosen["dev_sym"][s]["net"] < 0 and chosen["sel_sym"][s]["net"] < 0)]
    disabled = [s for s in ev.sim.syms if s not in active]
    result.update(chosen=_strip(chosen), why=why, active=active, disabled=disabled)
    return result


def final_test(ev: Evaluator, setup: Setup, sel: dict, afilter: AstroFilter | None) -> dict:
    """Uji akhir sekali dengan pilihan terkunci, lalu versi dengan filter Astronacci."""
    if "active" not in sel or not sel["active"]:
        return sel
    p, act = sel["chosen"]["params"], sel["active"]
    r = ev.evaluate(setup, p, segs=("dev", "sel", "final"), symbols=act)
    fin = r["final"]
    sel["final"] = _strip(r)
    sel["status"] = "lolos" if fin["net"] > 0 and fin["trades"] >= MIN_TRADES else "tidak lolos"
    sel["equity"] = {s: _daily_equity(r[s + "_res"]) for s in ("dev", "sel", "final")}
    sel["trades_final"] = r["final_res"].frame()
    g = ev.sim.g
    # untuk uji WKT-04: hari entry dan apakah kena SL
    sel["sl_flags"] = {s: [{"day": int(g.day[t.entry_idx]), "sl": t.exit_reason.startswith("SL")}
                           for t in r[s + "_res"].trades] for s in ("sel", "final")}
    if afilter is not None:
        ra = ev.evaluate(setup, p, segs=("dev", "sel", "final"), symbols=act, afilter=afilter)
        sel["astro"] = _strip(ra)
        fa = ra["final"]
        sel["astro_status"] = "lolos" if fa["net"] > 0 and fa["trades"] >= MIN_TRADES else "tidak lolos"
    return sel


def _daily_equity(res) -> list[tuple[str, float]]:
    import pandas as pd
    eq = res.equity()
    g = res.sim.g
    t = g.t[res.i_start:res.i_end]
    s = pd.Series(eq, index=pd.to_datetime(t, utc=True)).resample("1D").last().dropna()
    return [(str(i.date()), float(v)) for i, v in s.items()]
