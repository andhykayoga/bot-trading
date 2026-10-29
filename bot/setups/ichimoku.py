"""Ichimoku Rafał Zuchowicz (rulebook 06 bagian B): ICH-01, ICH-02, ICH-03, dan target
Hosoda ICH-04 untuk TP. Juga AFS-14 (Ichimoku Alvesting) yang memakai perhitungan sama.

Pergeseran (Q-36): Kumo di candle t = Senkou yang dihitung di t−25; Chikou candle t =
close[t] dibandingkan dengan harga & Kumo 25 candle sebelumnya.
"""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan

SHIFT = 25


def hosoda_targets(sw: ind.SwingState, t: int, direction: int) -> list[float]:
    """Target V, N, E, NT (ICH-04) dari swing A–B–C terakhir yang sudah diakui di candle t.
    Naik: A = swing low, B = swing high, C = swing low lebih tinggi dari A. Turun: cerminan."""
    if direction > 0:
        c_p, c_i = sw.lp[t, 0], sw.li[t, 0]
        hs = [(sw.hp[t, k], sw.hi[t, k]) for k in range(3) if 0 <= sw.hi[t, k] < c_i]
        if c_i < 0 or not hs:
            return []
        b_p, b_i = hs[0]
        ls = [(sw.lp[t, k], sw.li[t, k]) for k in range(1, 3) if 0 <= sw.li[t, k] < b_i]
        if not ls:
            return []
        a_p = ls[0][0]
        if not (a_p < c_p < b_p):
            return []
        return sorted({b_p + (b_p - c_p), c_p + (b_p - a_p), b_p + (b_p - a_p), c_p + (c_p - a_p)})
    c_p, c_i = sw.hp[t, 0], sw.hi[t, 0]
    ls = [(sw.lp[t, k], sw.li[t, k]) for k in range(3) if 0 <= sw.li[t, k] < c_i]
    if c_i < 0 or not ls:
        return []
    b_p, b_i = ls[0]
    hs = [(sw.hp[t, k], sw.hi[t, k]) for k in range(1, 3) if 0 <= sw.hi[t, k] < b_i]
    if not hs:
        return []
    a_p = hs[0][0]
    if not (a_p > c_p > b_p):
        return []
    return sorted({b_p - (c_p - b_p), c_p - (a_p - b_p), b_p - (a_p - b_p), c_p - (a_p - c_p)}, reverse=True)


def pick_tp(targets: list[float], entry: float, sl: float, direction: int, min_rr: float):
    """TP = target terdekat yang RR-nya ≥ minimum (Q-08); tp2 = target sesudahnya."""
    risk = (entry - sl) * direction
    if risk <= 0:
        return None, None
    ok = [x for x in targets if (x - entry) * direction >= min_rr * risk]
    if not ok:
        return None, None
    ok.sort(key=lambda x: (x - entry) * direction)
    return ok[0], (ok[1] if len(ok) > 1 else None)


class _IchiBase(Setup):
    mentor = "Rafał Zuchowicz (Ichimoku, forex_3)"
    priority = 1
    category = "trend"
    defaults = {"sl_atr": 1.0, "sl_mode": "kijun", "partial": False}

    def plan(self) -> TestPlan:
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]},
                        comparisons={"sl_mode": ["kijun", "swing"], "partial": [False, True]})

    def _sl(self, ctx: Ctx, t: int, direction: int, p) -> float:
        a = ctx.atr[t] * p["sl_atr"]
        if p["sl_mode"] == "kijun":
            lvl = ctx.ichi["kijun"][t]
        else:
            lvl = ctx.sw.lp[t, 0] if direction > 0 else ctx.sw.hp[t, 0]
        return lvl - a if direction > 0 else lvl + a

    def _order(self, sym, ctx: Ctx, t: int, direction: int, p, tf: str):
        b = ctx.b
        entry = b.c[t]
        sl = self._sl(ctx, t, direction, p)
        if np.isnan(sl) or (entry - sl) * direction <= 0:
            return None
        tp, tp2 = pick_tp(hosoda_targets(ctx.sw, t, direction), entry, sl, direction, 1.5)
        if tp is None:
            return None
        partial = bool(p["partial"]) and tp2 is not None
        return Order(self.id, sym, direction, int(b.t_close[t]), "market", sl=float(sl), tp=float(tp),
                     min_rr=1.5, entry_tf=tf, tp2=float(tp2) if partial else np.nan, partial=partial)


def _bias(ctx_hi: Ctx, idx: np.ndarray, t: int, direction: int) -> bool:
    """Harga timeframe besar (candle terakhir yang sudah close) di luar Kumo searah."""
    j = idx[t]
    if j < 0:
        return False
    c = ctx_hi.b.c[j]
    top, bot = ctx_hi.ichi["kumo_top"][j], ctx_hi.ichi["kumo_bot"][j]
    if np.isnan(top):
        return False
    return c > top if direction > 0 else c < bot


class ICH01(_IchiBase):
    id = "ICH-01"
    name = "Ichimoku tren penuh (harga, Tenkan–Kijun, Kumo, Chikou), bias W1 & D1"
    entry_tf = "H4"

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "H4")
        cd, cw = Ctx.get(d, "D1"), Ctx.get(d, "W1")
        idx_d, idx_w = ctx.htf_index("D1"), ctx.htf_index("W1")
        b, ic = ctx.b, ctx.ichi
        c = b.c
        c25 = ind.shift(c, SHIFT)
        top25, bot25 = ind.shift(ic["kumo_top"], SHIFT), ind.shift(ic["kumo_bot"], SHIFT)
        long_ok = (c > ic["kumo_top"]) & (c > top25) & (c > c25) & (ic["tenkan"] > ic["kijun"])
        short_ok = (c < ic["kumo_bot"]) & (c < bot25) & (c < c25) & (ic["tenkan"] < ic["kijun"])
        out = []
        for t in range(1, len(c)):
            for dirn, ok in ((1, long_ok), (-1, short_ok)):
                if ok[t] and not ok[t - 1] and _bias(cd, idx_d, t, dirn) and _bias(cw, idx_w, t, dirn):
                    o = self._order(sym, ctx, t, dirn, p, "H4")
                    if o:
                        out.append(o)
        return out


class ICH02(_IchiBase):
    id = "ICH-02"
    name = "Ichimoku retest Kijun (arah D1, entry H4)"
    entry_tf = "H4"

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "H4")
        cd = Ctx.get(d, "D1")
        idx_d = ctx.htf_index("D1")
        b, kj = ctx.b, ctx.ichi["kijun"]
        kd = cd.ichi["kijun"]
        out = []
        for t in range(2, len(b)):
            j = idx_d[t]
            if j < 0 or np.isnan(kj[t]) or np.isnan(kd[j]):
                continue
            # long: candle sebelumnya close di atas Kijun dan belum menyentuhnya; candle ini
            # menyentuh Kijun tetapi tidak close di bawahnya
            if b.c[t - 1] > kj[t - 1] and b.l[t - 1] > kj[t - 1] and b.l[t] <= kj[t] and b.c[t] >= kj[t] \
                    and cd.b.c[j] > kd[j]:
                o = self._order(sym, ctx, t, 1, p, "H4")
                if o:
                    out.append(o)
            if b.c[t - 1] < kj[t - 1] and b.h[t - 1] < kj[t - 1] and b.h[t] >= kj[t] and b.c[t] <= kj[t] \
                    and cd.b.c[j] < kd[j]:
                o = self._order(sym, ctx, t, -1, p, "H4")
                if o:
                    out.append(o)
        return out


class ICH03(_IchiBase):
    id = "ICH-03"
    name = "Ichimoku pullback ke Tenkan dalam tren kuat (D1)"
    entry_tf = "D1"

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, tk = ctx.b, ctx.ichi["tenkan"]
        o_, h, l, c = b.o, b.h, b.l, b.c
        strong = ind.strong_candle(o_, h, l, c, 0.7)
        # silang close terhadap Tenkan (untuk mendeteksi sideways)
        side = np.sign(c - tk)
        cross = np.r_[False, (side[1:] != side[:-1]) & (side[1:] != 0) & (side[:-1] != 0)]
        out = []
        state = 0  # +1 tren naik aktif, −1 tren turun aktif
        for t in range(3, len(c)):
            if np.isnan(tk[t - 2]):
                continue
            # tanda berakhir: 2 close kuat berturut-turut di sisi lawan Tenkan, atau sideways
            if state > 0 and strong[t] and strong[t - 1] and c[t] < tk[t] and c[t - 1] < tk[t - 1]:
                state = 0
            if state < 0 and strong[t] and strong[t - 1] and c[t] > tk[t] and c[t - 1] > tk[t - 1]:
                state = 0
            if state != 0 and cross[max(0, t - 9): t + 1].sum() >= 3:
                state = 0
            # sinyal awal: candle kuat close di atas Tenkan dan Tenkan mulai naik (sebelumnya datar/turun)
            if strong[t] and c[t] > o_[t] and c[t] > tk[t] and tk[t] > tk[t - 1] and tk[t - 1] <= tk[t - 2]:
                state = 1
                continue
            if strong[t] and c[t] < o_[t] and c[t] < tk[t] and tk[t] < tk[t - 1] and tk[t - 1] >= tk[t - 2]:
                state = -1
                continue
            # entry: pullback menyentuh Tenkan dan bertahan
            if state > 0 and l[t] <= tk[t] and c[t] >= tk[t] and l[t - 1] > tk[t - 1]:
                od = self._order(sym, ctx, t, 1, p, "D1")
                if od:
                    out.append(od)
            if state < 0 and h[t] >= tk[t] and c[t] <= tk[t] and h[t - 1] < tk[t - 1]:
                od = self._order(sym, ctx, t, -1, p, "D1")
                if od:
                    out.append(od)
        return out
