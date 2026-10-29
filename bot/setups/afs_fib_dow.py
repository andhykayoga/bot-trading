"""Fibonacci, area dinamis, Dow, dan ABCD Alvesting: AFS-04, AFS-05, AFS-09, AFS-10."""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, swing_levels, swing_sl, trigger_ok

BTC_ATR_PCT = 3.36   # ATR BTC (%) yang disebut mentor; dasar faktor k di forex (D-09, Q-50)
EXT = (1.0, 1.618, 2.618, 3.618, 4.236)


def daily_atr_on(ctx: Ctx) -> np.ndarray:
    """ATR(14) harian (candle D1 terakhir yang sudah close) untuk tiap candle ctx (D-09)."""
    def build():
        d1 = Ctx.get(ctx.d, "D1")
        i = ctx.htf_index("D1")
        return np.where(i >= 0, d1.atr[np.clip(i, 0, None)], np.nan)
    return ctx._memo("datr", build)


class AFS04(Setup):
    id = "AFS-04"
    name = "Pantulan Fibonacci golden pocket 0,5–0,618 (D1 & W1)"
    mentor = "Alvesting (Akademi Crypto) — Fibonacci Secret"
    category = "trend"
    entry_tf = "D1"
    defaults = {"mode": "confirm", "k_mult": 1.0, "sl_atr": 1.0, "partial": False}

    def plan(self):
        return TestPlan(tested={"k_mult": [0.5, 1.0, 1.5], "sl_atr": [0.5, 1.0, 1.5]},
                        comparisons={"mode": ["confirm", "anticipate"], "partial": [False, True]})

    def signals_for(self, sym, d, p):
        out = []
        for tf in ("D1", "W1"):
            out += self._tf(sym, d, p, tf)
        out.sort(key=lambda o: o.created)
        return out

    def _tf(self, sym, d, p, tf):
        ctx = Ctx.get(d, tf)
        b, sw, a = ctx.b, ctx.sw, ctx.atr
        ma100 = ctx._memo("ma100", lambda: ind.sma(b.c, 100))
        datr = daily_atr_on(ctx)
        k = 3.0 / BTC_ATR_PCT * p["k_mult"]       # pantulan 3% di kripto → k × ATR harian
        out = []
        used = set()
        for t in range(5, len(b)):
            if np.isnan(a[t]):
                continue
            for dirn in (1, -1):
                if sw.trend[t] != dirn:
                    continue
                if dirn > 0:
                    lo_i, hi_i = sw.li[t, 0], sw.hi[t, 0]
                    if not (0 <= lo_i < hi_i):
                        continue
                    L, H = sw.lp[t, 0], sw.hp[t, 0]
                    pk_top, pk_bot = H - 0.5 * (H - L), H - 0.618 * (H - L)
                    seg = slice(hi_i + 1, t + 1)
                    if hi_i + 1 > t:
                        continue
                    corr_low = b.l[seg].min()
                    if corr_low <= L:            # batal: low impuls (level 0) tertembus
                        continue
                    if corr_low > pk_top:        # belum masuk golden pocket
                        continue
                else:
                    hi_i, lo_i = sw.hi[t, 0], sw.li[t, 0]
                    if not (0 <= hi_i < lo_i):
                        continue
                    H, L = sw.hp[t, 0], sw.lp[t, 0]
                    pk_bot, pk_top = L + 0.5 * (H - L), L + 0.618 * (H - L)
                    seg = slice(lo_i + 1, t + 1)
                    if lo_i + 1 > t:
                        continue
                    corr_high = b.h[seg].max()
                    if corr_high >= H:
                        continue
                    if corr_high < pk_bot:
                        continue
                key = (dirn, int(lo_i), int(hi_i))
                if key in used:
                    continue
                # wajib confluence: zona horizontal, trendline, atau MA100 di dalam golden pocket
                half = 0.5 * a[t]
                lv = np.r_[swing_levels(ctx, t, "low", 300), swing_levels(ctx, t, "high", 300)]
                conf = bool(((lv >= pk_bot - half) & (lv <= pk_top + half)).any())
                if not np.isnan(ma100[t]) and pk_bot - half <= ma100[t] <= pk_top + half:
                    conf = True
                if dirn > 0 and sw.li[t, 1] >= 0 and sw.lp[t, 0] > sw.lp[t, 1]:
                    i1, i2, p1, p2 = sw.li[t, 1], sw.li[t, 0], sw.lp[t, 1], sw.lp[t, 0]
                    line = p1 + (p2 - p1) * (t - i1) / (i2 - i1)
                    conf |= pk_bot - half <= line <= pk_top + half
                if dirn < 0 and sw.hi[t, 1] >= 0 and sw.hp[t, 0] < sw.hp[t, 1]:
                    i1, i2, p1, p2 = sw.hi[t, 1], sw.hi[t, 0], sw.hp[t, 1], sw.hp[t, 0]
                    line = p1 + (p2 - p1) * (t - i1) / (i2 - i1)
                    conf |= pk_bot - half <= line <= pk_top + half
                if not conf:
                    continue
                entry = b.c[t]
                if p["mode"] == "confirm":
                    if np.isnan(datr[t]):
                        continue
                    if dirn > 0 and entry < corr_low + k * datr[t]:
                        continue
                    if dirn < 0 and entry > corr_high - k * datr[t]:
                        continue
                else:
                    if not trigger_ok(ctx, t, dirn):
                        continue
                    if dirn > 0 and not (b.l[t] <= pk_top and b.h[t] >= pk_bot):
                        continue
                    if dirn < 0 and not (b.h[t] >= pk_bot and b.l[t] <= pk_top):
                        continue
                sl = corr_low - p["sl_atr"] * a[t] if dirn > 0 else H + p["sl_atr"] * a[t]
                levels = [L + r * (H - L) for r in EXT] if dirn > 0 else [H - r * (H - L) for r in EXT]
                risk = (entry - sl) * dirn
                if risk <= 0:
                    continue
                ok = [x for x in levels if (x - entry) * dirn >= 1.5 * risk]
                if not ok:
                    continue
                tp = ok[0]
                tp2 = ok[1] if len(ok) > 1 and p["partial"] else np.nan
                used.add(key)
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=float(sl), tp=float(tp),
                                 min_rr=1.5, entry_tf=tf, tp2=float(tp2), partial=not np.isnan(tp2)))
        return out


class AFS05(Setup):
    id = "AFS-05"
    name = "Money magnet EMA 13 & 21"
    mentor = "Alvesting (Akademi Crypto) — area dinamis"
    category = "trend"
    defaults = {"tf": "H4", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H1", "H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, sw, a = ctx.b, ctx.sw, ctx.atr
        e13 = ctx._memo("ema13", lambda: ind.ema(b.c, 13))
        e21 = ctx._memo("ema21", lambda: ind.ema(b.c, 21))
        top, bot = np.fmax(e13, e21), np.fmin(e13, e21)
        rr = 2.0 if tf == "H1" else 3.0
        out = []
        for t in range(25, len(b)):
            dirn = int(sw.trend[t])
            if dirn == 0 or np.isnan(a[t]):
                continue
            if not (b.l[t] <= top[t] and b.h[t] >= bot[t]):
                continue
            if not trigger_ok(ctx, t, dirn):
                continue
            entry = b.c[t]
            sl = swing_sl(ctx, t, dirn, entry, p["sl_atr"])
            if np.isnan(sl):
                continue
            out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=rr, min_rr=rr,
                             entry_tf=tf))
        return out


class AFS09(Setup):
    id = "AFS-09"
    name = "Validasi tembus 3% Dow Theory (MA21, D1)"
    mentor = "Alvesting (Akademi Crypto) — Dow Theory"
    category = "both"
    entry_tf = "D1"
    uses_volume = True       # AFS-F2: candle breakout harus bervolume
    defaults = {"k_mult": 1.0, "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"k_mult": [0.5, 1.0, 1.5], "sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, sw, a = ctx.b, ctx.sw, ctx.atr
        ma = ctx._memo("ma21", lambda: ind.sma(b.c, 21))
        k = 3.0 / BTC_ATR_PCT * p["k_mult"]
        use_vol = p.get("volume", "tick") == "tick"
        volhi = ctx.vol_high
        out = []
        state = 0       # +1: sudah close di atas MA21 dari tren turun, menunggu validasi
        for t in range(22, len(b)):
            if np.isnan(ma[t]) or np.isnan(a[t]):
                continue
            c = b.c[t]
            if state == 0:
                if c > ma[t] and b.c[t - 1] <= ma[t - 1] and sw.trend[t - 1] == -1:
                    state = 1
                elif c < ma[t] and b.c[t - 1] >= ma[t - 1] and sw.trend[t - 1] == 1:
                    state = -1
                else:
                    continue
            if state == 1 and c < ma[t]:
                state = 0; continue
            if state == -1 and c > ma[t]:
                state = 0; continue
            if (state == 1 and c >= ma[t] + k * a[t]) or (state == -1 and c <= ma[t] - k * a[t]):
                dirn = state
                state = 0
                if use_vol and not volhi[t]:
                    continue
                sl = swing_sl(ctx, t, dirn, c, p["sl_atr"])
                if np.isnan(sl):
                    continue
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                                 entry_tf="D1"))
        return out


class AFS10(Setup):
    id = "AFS-10"
    name = "Pola ABCD (M15 & H1)"
    mentor = "Alvesting (Akademi Crypto) — pola harmonic"
    category = "reversal"
    entry_tf = "M15"
    defaults = {"sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        out = []
        for tf in ("M15", "H1"):
            out += self._tf(sym, d, p, tf)
        out.sort(key=lambda o: o.created)
        return out

    def _tf(self, sym, d, p, tf):
        ctx = Ctx.get(d, tf)
        b, sw, a = ctx.b, ctx.sw, ctx.atr
        bull, bear = ctx.patterns
        out = []
        used = set()
        for t in range(10, len(b)):
            if np.isnan(a[t]):
                continue
            for dirn in (1, -1):
                if dirn > 0:   # A swing high, B swing low, C swing high < A, D di bawah B
                    A, iA, B, iB, C, iC = sw.hp[t, 1], sw.hi[t, 1], sw.lp[t, 0], sw.li[t, 0], sw.hp[t, 0], sw.hi[t, 0]
                    if not (0 <= iA < iB < iC) or not (C < A):
                        continue
                    ab, bc = A - B, C - B
                    Dx = C - ab                                  # AB = CD (pasangan resiprok)
                    trig = bull[t]
                    seg_ext = b.l[iC + 1: t + 1].min() if iC + 1 <= t else np.inf
                    if seg_ext < C - 2.618 * bc:                 # batal: lewat CD = 2,618 × BC
                        continue
                    in_zone = Dx - 0.5 * a[t] <= b.c[t] <= Dx + 0.5 * a[t]
                else:
                    A, iA, B, iB, C, iC = sw.lp[t, 1], sw.li[t, 1], sw.hp[t, 0], sw.hi[t, 0], sw.lp[t, 0], sw.li[t, 0]
                    if not (0 <= iA < iB < iC) or not (C > A):
                        continue
                    ab, bc = B - A, B - C
                    Dx = C + ab
                    trig = bear[t]
                    seg_ext = b.h[iC + 1: t + 1].max() if iC + 1 <= t else -np.inf
                    if seg_ext > C + 2.618 * bc:
                        continue
                    in_zone = Dx - 0.5 * a[t] <= b.c[t] <= Dx + 0.5 * a[t]
                if ab <= 0 or bc <= 0 or not (0.382 <= bc / ab <= 0.886):
                    continue
                cd_ratio = ab / bc                               # CD/BC dengan CD = AB
                if not (1.13 <= cd_ratio <= 2.618) or not trig or not in_zone:
                    continue
                key = (dirn, int(iC))
                if key in used:
                    continue
                used.add(key)
                ext = b.l[iC: t + 1].min() if dirn > 0 else b.h[iC: t + 1].max()
                sl = ext - p["sl_atr"] * a[t] if dirn > 0 else ext + p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=float(sl), tp_rr=2.0,
                                 min_rr=2.0, entry_tf=tf))
        return out
