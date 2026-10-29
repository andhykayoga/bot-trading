"""KMS-02 (Kalimasada, Wyckoff) dan HKI-01 (Ko Hengki, tren sekunder & minor)."""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.afs_fib_dow import BTC_ATR_PCT
from bot.setups.base import Ctx, Setup, TestPlan, swing_levels, swing_sl

RETEST = 10


class KMS02(Setup):
    id = "KMS-02"
    name = "Wyckoff breakout range + retest (D1)"
    mentor = "Kalimasada (Akademi Crypto) — Wyckoff"
    category = "breakout"
    entry_tf = "D1"
    uses_volume = True
    volume_only = True       # Wyckoff tanpa volume tidak dipakai (Q-48)
    defaults = {"sl_atr": 1.0, "retest": RETEST}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5], "retest": [5, 10, 15]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, a = ctx.b, ctx.atr
        volhi = ctx.vol_high
        k = 20.0 / BTC_ATR_PCT          # lebar range maks 20% kripto → 5,95 × ATR(14) D1 (D-09, Q-48)
        out = []
        n = len(b)
        for t in range(21, n - p["retest"]):
            if np.isnan(a[t]):
                continue
            rh, rl = b.h[t - 20:t].max(), b.l[t - 20:t].min()
            if rh - rl > k * a[t - 1]:
                continue
            half = 0.5 * a[t]
            for dirn in (1, -1):
                brk = b.c[t] > rh if dirn > 0 else b.c[t] < rl
                if not brk or not volhi[t]:
                    continue
                lvl = rh if dirn > 0 else rl
                entry = lvl + half if dirn > 0 else lvl - half        # tepi zona batas range (LPS / LPSY)
                # SL: swing terakhir di dalam range ± ATR
                inside = swing_levels(ctx, t, "low" if dirn > 0 else "high", 25)
                inside = inside[(inside >= rl) & (inside <= rh)]
                if len(inside) == 0:
                    continue
                sl = inside[0] - p["sl_atr"] * a[t] if dirn > 0 else inside[0] + p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "limit", sl=float(sl), price=float(entry),
                                 tp_rr=3.0, min_rr=3.0, expiry=int(b.t_close[t + p["retest"]]), entry_tf="D1"))
        return out


class _HKI01(Setup):
    mentor = "Ko Hengki (Remora) — harga & volume, tren"
    uses_volume = True
    tf = "D1"
    defaults = {"style": "weakness", "sl_atr": 1.0}

    def plan(self):
        # buy on weakness vs buy on breakout: keduanya sah menurut Ko Hengki (setara, Q-09)
        return TestPlan(setara={"style": ["weakness", "breakout"]}, tested={"sl_atr": [0.5, 1.0, 1.5]})

    category = "trend"

    def category_of(self, p):
        return "breakout" if p.get("style") == "breakout" else "trend"

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, self.tf)
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        v = b.v
        vavg = ind.shift(ind.sma(v, 20), 1)
        volhi = ctx.vol_high
        use_vol = p.get("volume", "tick") == "tick"
        # keluar paksa: struktur patah = candle close di bawah higher low terakhir (G-07 pengecualian 3)
        brk_t = b.t_close[(b.c < sw.lp[:, 0])]
        out = []
        for t in range(25, len(b) - 1):
            if sw.trend[t] != 1 or np.isnan(a[t]):
                continue
            half = 0.5 * a[t]
            if p["style"] == "weakness":
                sup = sw.lp[t, 0]
                top = sup + half
                if b.c[t] <= top:
                    continue
                # koreksi tanpa volume (HKI-F1): rata-rata volume candle sejak swing high terakhir < rata-rata 20
                i0 = sw.hi[t, 0]
                if use_vol:
                    if i0 < 0 or i0 >= t or v[i0 + 1: t + 1].mean() >= vavg[t]:
                        continue
                sl = sup - p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, 1, int(b.t_close[t]), "limit", sl=float(sl), price=float(top),
                                 tp_rr=3.0, min_rr=3.0, expiry=int(b.t_close[t + 1]), entry_tf=self.tf,
                                 exit_times=brk_t))
            else:
                res = swing_levels(ctx, t - 1, "high", 150)
                res = res[res + half >= b.c[t - 1]]
                if len(res) == 0:
                    continue
                lvl = res.min() + half
                if not (b.c[t] > lvl and b.c[t - 1] <= lvl):
                    continue
                if use_vol and not volhi[t]:      # HKI-F2: breakout harus bervolume
                    continue
                sl = swing_sl(ctx, t, 1, b.c[t], p["sl_atr"])
                if np.isnan(sl):
                    continue
                out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                                 entry_tf=self.tf, exit_times=brk_t))
        return out


class HKI01D1(_HKI01):
    id = "HKI-01-D1"
    name = "Ikuti tren sekunder (D1), keluar saat struktur patah"
    tf = "D1"
    entry_tf = "D1"


class HKI01H4(_HKI01):
    id = "HKI-01-H4"
    name = "Ikuti tren minor (H4), keluar saat struktur patah"
    tf = "H4"
    entry_tf = "H4"
