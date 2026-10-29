"""Versi perbaikan terbatas (rencana cadangan tahap 1, lihat reports/RENCANA_CADANGAN.md).

Empat versi, dikunci sebelum diuji, tanpa pencarian parameter (semua angka = nilai awal
rulebook). Perubahan yang diizinkan: timeframe lebih besar, filter kondisi pasar, atau
menggabungkan beberapa setup menjadi satu sinyal.

- V1  ICH-01 dipindah ke D1 (bias W1).                                  → timeframe lebih besar
- V2  Konsensus tren D1 (struktur D-02 + Kumo + MA21) + pullback EMA 13/21 (AFS-05) di D1. → gabungan
- V3  AFS-05 di H4, hanya searah struktur D1 (D-02).                    → filter kondisi pasar
- V4  AFS-06 (stop hunt + BMS) di H1, hanya searah struktur D1.         → timeframe lebih besar + filter

Catatan G-11: V2 memakai dua indikator tren (Ichimoku dan MA21) karena memang menggabungkan
beberapa setup mentor menjadi satu sinyal, sesuai instruksi rencana cadangan.
"""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.afs_smc import AFS06
from bot.setups.base import Ctx, Setup, TestPlan, swing_sl, trigger_ok
from bot.setups.ichimoku import SHIFT, _bias, hosoda_targets, pick_tp


class _Fixed(Setup):
    """Versi perbaikan: satu konfigurasi terkunci, tidak ada varian."""
    priority = 3

    def plan(self):
        return TestPlan()


def _d1_trend_on(ctx: Ctx) -> np.ndarray:
    """Struktur D1 (D-02) candle D1 terakhir yang sudah close, untuk tiap candle ctx."""
    def build():
        d1 = Ctx.get(ctx.d, "D1")
        i = ctx.htf_index("D1")
        return np.where(i >= 0, d1.sw.trend[np.clip(i, 0, None)], 0)
    return ctx._memo("d1trend", build)


class V1(_Fixed):
    id = "V1"
    name = "ICH-01 di timeframe D1 (bias W1)"
    mentor = "Perbaikan dari Rafał (Ichimoku) — timeframe lebih besar"
    category = "trend"
    entry_tf = "D1"
    defaults = {"sl_atr": 1.0}

    def signals_for(self, sym, d, p):
        ctx, cw = Ctx.get(d, "D1"), Ctx.get(d, "W1")
        idx_w = ctx.htf_index("W1")
        b, ic, a = ctx.b, ctx.ichi, ctx.atr
        c = b.c
        c25 = ind.shift(c, SHIFT)
        top25, bot25 = ind.shift(ic["kumo_top"], SHIFT), ind.shift(ic["kumo_bot"], SHIFT)
        long_ok = (c > ic["kumo_top"]) & (c > top25) & (c > c25) & (ic["tenkan"] > ic["kijun"])
        short_ok = (c < ic["kumo_bot"]) & (c < bot25) & (c < c25) & (ic["tenkan"] < ic["kijun"])
        out = []
        for t in range(1, len(c)):
            for dirn, ok in ((1, long_ok), (-1, short_ok)):
                if not (ok[t] and not ok[t - 1] and _bias(cw, idx_w, t, dirn)) or np.isnan(a[t]):
                    continue
                sl = ic["kijun"][t] - dirn * p["sl_atr"] * a[t]
                if (c[t] - sl) * dirn <= 0:
                    continue
                tp, _ = pick_tp(hosoda_targets(ctx.sw, t, dirn), c[t], sl, dirn, 1.5)
                if tp is None:
                    continue
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=float(sl), tp=float(tp),
                                 min_rr=1.5, entry_tf="D1"))
        return out


class V2(_Fixed):
    id = "V2"
    name = "Konsensus tren D1 (struktur + Kumo + MA21) + pullback EMA 13/21"
    mentor = "Gabungan Ko Hengki/Alvesting (struktur), Rafał (Kumo), Alvesting (Dow MA21, EMA 13/21)"
    category = "trend"
    entry_tf = "D1"
    defaults = {"sl_atr": 1.0}

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, a, sw, ic = ctx.b, ctx.atr, ctx.sw, ctx.ichi
        ma21 = ctx._memo("ma21", lambda: ind.sma(b.c, 21))
        e13 = ctx._memo("ema13", lambda: ind.ema(b.c, 13))
        e21 = ctx._memo("ema21", lambda: ind.ema(b.c, 21))
        top, bot = np.fmax(e13, e21), np.fmin(e13, e21)
        out = []
        for t in range(25, len(b)):
            if np.isnan(a[t]) or np.isnan(ic["kumo_top"][t]) or np.isnan(ma21[t]):
                continue
            c = b.c[t]
            if sw.trend[t] == 1 and c > ic["kumo_top"][t] and c > ma21[t]:
                dirn = 1
            elif sw.trend[t] == -1 and c < ic["kumo_bot"][t] and c < ma21[t]:
                dirn = -1
            else:
                continue
            if not (b.l[t] <= top[t] and b.h[t] >= bot[t]) or not trigger_ok(ctx, t, dirn):
                continue
            sl = swing_sl(ctx, t, dirn, c, p["sl_atr"])
            if np.isnan(sl):
                continue
            out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                             entry_tf="D1"))
        return out


class V3(_Fixed):
    id = "V3"
    name = "AFS-05 EMA 13/21 di H4, hanya searah struktur D1"
    mentor = "Perbaikan dari Alvesting (money magnet) — filter kondisi pasar"
    category = "trend"
    entry_tf = "H4"
    defaults = {"sl_atr": 1.0}

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "H4")
        b, sw, a = ctx.b, ctx.sw, ctx.atr
        e13 = ctx._memo("ema13", lambda: ind.ema(b.c, 13))
        e21 = ctx._memo("ema21", lambda: ind.ema(b.c, 21))
        top, bot = np.fmax(e13, e21), np.fmin(e13, e21)
        d1 = _d1_trend_on(ctx)
        out = []
        for t in range(25, len(b)):
            dirn = int(sw.trend[t])
            if dirn == 0 or d1[t] != dirn or np.isnan(a[t]):
                continue
            if not (b.l[t] <= top[t] and b.h[t] >= bot[t]) or not trigger_ok(ctx, t, dirn):
                continue
            sl = swing_sl(ctx, t, dirn, b.c[t], p["sl_atr"])
            if np.isnan(sl):
                continue
            out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                             entry_tf="H4"))
        return out


class V4(_Fixed):
    id = "V4"
    name = "AFS-06 stop hunt + BMS di H1, hanya searah struktur D1"
    mentor = "Perbaikan dari Alvesting (Smart Money) — timeframe lebih besar + filter kondisi pasar"
    category = "reversal"
    entry_tf = "H1"
    defaults = dict(AFS06.defaults, tf="H1", dir_tf="D1", dir_mode="same")

    def signals_for(self, sym, d, p):
        orders = AFS06().signals_for(sym, d, p)
        for o in orders:
            o.setup = self.id
        return orders


IMPROVED = [V1, V2, V3, V4]
