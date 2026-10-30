"""Technical Research 5 tahap Alvesting (rulebook 01 bagian A): AFS-01, AFS-02, AFS-03."""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, pivots, swing_levels, swing_sl, zone_hit, zone_tp


def _trigger_arrays(ctx: Ctx):
    """Pemicu syarat 4: candle D-06 atau Stochastic 5,3,3 silang di area jenuh (D-08)."""
    def build():
        bull, bear = ctx.patterns
        k, d = ctx.stoch
        return bull | ind.stoch_cross(k, d, "oversold"), bear | ind.stoch_cross(k, d, "overbought")
    return ctx._memo("trig", build)


def _trendline_ok(ctx: Ctx):
    """Poin 3 (D1): garis lewat 2 swing low terakhir (naik) / 2 swing high (turun), belum ada
    close yang menembus garis sejak swing kedua. Mengembalikan (ok_long, ok_short) per candle."""
    def build():
        sw, c = ctx.sw, ctx.b.c
        n = len(c)
        okl = np.zeros(n, bool)
        oks = np.zeros(n, bool)
        for t in range(n):
            i1, i2, p1, p2 = sw.li[t, 1], sw.li[t, 0], sw.lp[t, 1], sw.lp[t, 0]
            if i1 >= 0 and p2 > p1:
                x = np.arange(i2, t + 1)
                line = p1 + (p2 - p1) * (x - i1) / (i2 - i1)
                okl[t] = bool((c[i2:t + 1] >= line).all())
            i1, i2, p1, p2 = sw.hi[t, 1], sw.hi[t, 0], sw.hp[t, 1], sw.hp[t, 0]
            if i1 >= 0 and p2 < p1:
                x = np.arange(i2, t + 1)
                line = p1 + (p2 - p1) * (x - i1) / (i2 - i1)
                oks[t] = bool((c[i2:t + 1] <= line).all())
        return okl, oks
    return ctx._memo("tl_ok", build)


def _equal(a, b, tol):
    return abs(a - b) <= tol


def area_hit(actx: Ctx, ia: int, lo: float, hi: float, close: float, d: int, piv: dict) -> bool:
    """Syarat 2: range candle pemicu menyentuh minimal satu area (5 cara mentor)."""
    a = actx.atr[ia]
    if np.isnan(a):
        return False
    half = 0.5 * a
    b, sw = actx.b, actx.sw
    # 1. zona horizontal dari swing timeframe area (support di bawah/di harga untuk long)
    lv = np.r_[swing_levels(actx, ia, "low", 150)[:5], swing_levels(actx, ia, "high", 150)[:5]]
    lv = lv[lv <= close + half] if d > 0 else lv[lv >= close - half]
    if any(zone_hit(lo, hi, x, half) for x in lv):
        return True
    # 2. trendline lewat 2 swing terakhir sebagai support/resistance diagonal
    if d > 0:
        i1, i2, p1, p2 = sw.li[ia, 1], sw.li[ia, 0], sw.lp[ia, 1], sw.lp[ia, 0]
        ok = i1 >= 0 and p2 > p1
    else:
        i1, i2, p1, p2 = sw.hi[ia, 1], sw.hi[ia, 0], sw.hp[ia, 1], sw.hp[ia, 0]
        ok = i1 >= 0 and p2 < p1
    if ok:
        line = p1 + (p2 - p1) * (ia - i1) / (i2 - i1)
        if zone_hit(lo, hi, line, half):
            return True
    # 3. pita EMA 13–21
    e13, e21 = actx._memo("ema13", lambda: ind.ema(b.c, 13)), actx._memo("ema21", lambda: ind.ema(b.c, 21))
    top, bot = max(e13[ia], e21[ia]), min(e13[ia], e21[ia])
    if lo <= top and hi >= bot:
        return True
    # 4. pivot P, S1–S3 (long) atau P, R1–R3 (short)
    keys = ("P", "S1", "S2", "S3") if d > 0 else ("P", "R1", "R2", "R3")
    if any(zone_hit(lo, hi, piv[k], half) for k in keys if not np.isnan(piv[k])):
        return True
    # 5. golden pocket 0,5–0,618 dari impuls terakhir
    if d > 0 and 0 <= sw.li[ia, 0] < sw.hi[ia, 0]:
        H, L = sw.hp[ia, 0], sw.lp[ia, 0]
        if lo <= H - 0.5 * (H - L) and hi >= H - 0.618 * (H - L):
            return True
    if d < 0 and 0 <= sw.hi[ia, 0] < sw.li[ia, 0]:
        H, L = sw.hp[ia, 0], sw.lp[ia, 0]
        if lo <= L + 0.618 * (H - L) and hi >= L + 0.5 * (H - L):
            return True
    return False


def pattern_ok(actx: Ctx, ia: int, d: int, recent: int = 20) -> bool:
    """Syarat 3: double/triple bottom (top) atau ABCD searah bias di timeframe pola (Q-23)."""
    sw, a, b = actx.sw, actx.atr[ia], actx.b
    if np.isnan(a):
        return False
    tol = 0.5 * a
    if d > 0:
        p0, p1, i0 = sw.lp[ia, 0], sw.lp[ia, 1], sw.li[ia, 0]
        if i0 >= ia - recent and _equal(p0, p1, tol):
            return True
        # ABCD bullish: A = swing high, B = swing low, C = swing high < A, D = low sejak C
        A, iA, B, iB, C, iC = sw.hp[ia, 1], sw.hi[ia, 1], sw.lp[ia, 0], sw.li[ia, 0], sw.hp[ia, 0], sw.hi[ia, 0]
        if not (0 <= iA < iB < iC):
            B, iB = sw.lp[ia, 1], sw.li[ia, 1]
            if not (0 <= iA < iB < iC):
                return False
        if C >= A or iC < ia - recent:
            return False
        D = b.l[iC: ia + 1].min()
        ab, bc, cd = A - B, C - B, C - D
        return ab > 0 and bc > 0 and 0.382 <= bc / ab <= 0.886 and 1.13 <= cd / bc <= 2.618
    p0, p1, i0 = sw.hp[ia, 0], sw.hp[ia, 1], sw.hi[ia, 0]
    if i0 >= ia - recent and _equal(p0, p1, tol):
        return True
    A, iA, B, iB, C, iC = sw.lp[ia, 1], sw.li[ia, 1], sw.hp[ia, 0], sw.hi[ia, 0], sw.lp[ia, 0], sw.li[ia, 0]
    if not (0 <= iA < iB < iC):
        B, iB = sw.hp[ia, 1], sw.hi[ia, 1]
        if not (0 <= iA < iB < iC):
            return False
    if C <= A or iC < ia - recent:
        return False
    D = b.h[iC: ia + 1].max()
    ab, bc, cd = B - A, B - C, D - C
    return ab > 0 and bc > 0 and 0.382 <= bc / ab <= 0.886 and 1.13 <= cd / bc <= 2.618


class AFS01(Setup):
    id = "AFS-01"
    name = "Technical Research 5 tahap, versi swing (D1 / H4 / M15)"
    mentor = "Alvesting (Akademi Crypto) — Technical Research"
    category = "trend"
    tfs = ("D1", "H4", "M15")       # tren, area & pola, pemicu
    entry_tf = "M15"
    pivot_period = "W1"
    min_rr = 1.5
    defaults = {"points": "4of5", "pattern": True, "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]},
                        comparisons={"points": ["4of5", "5of5"], "pattern": [True, False]})

    def _extra(self, o: Order, p: dict) -> Order:
        return o

    def signals_for(self, sym, d, p):
        ttf, atf, gtf = self.tfs
        tctx, actx, gctx = Ctx.get(d, ttf), Ctx.get(d, atf), Ctx.get(d, gtf)
        g = gctx.b
        it = gctx.htf_index(ttf)
        ia_arr = gctx.htf_index(atf)
        trend = np.where(it >= 0, tctx.sw.trend[np.clip(it, 0, None)], 0)
        tl_l, tl_s = _trendline_ok(tctx)
        tl_long = np.where(it >= 0, tl_l[np.clip(it, 0, None)], False)
        tl_short = np.where(it >= 0, tl_s[np.clip(it, 0, None)], False)
        bull_t, bear_t = _trigger_arrays(gctx)
        k, _ = gctx.stoch
        piv = pivots(actx, self.pivot_period)
        cand = np.flatnonzero(((trend == 1) & bull_t) | ((trend == -1) & bear_t))
        out = []
        for t in cand:
            ia = ia_arr[t]
            if ia < 30:
                continue
            dirn = int(trend[t])
            pv = {kk: piv[kk][ia] for kk in ("P", "S1", "S2", "S3", "R1", "R2", "R3")}
            if not area_hit(actx, ia, g.l[t], g.h[t], g.c[t], dirn, pv):
                continue
            p3 = bool(tl_long[t] if dirn > 0 else tl_short[t])
            p5 = bool(k[t] < 20 if dirn > 0 else k[t] > 80)
            if p["points"] == "5of5" and not (p3 and p5):
                continue
            if p["points"] == "4of5" and not (p3 or p5):
                continue
            if p["pattern"] and not pattern_ok(actx, ia, dirn):
                continue
            entry = g.c[t]
            sl = swing_sl(actx, ia, dirn, entry, p["sl_atr"])
            if np.isnan(sl):
                continue
            tp = zone_tp(actx, ia, dirn, entry, sl, self.min_rr)
            if np.isnan(tp):
                continue
            o = Order(self.id, sym, dirn, int(g.t_close[t]), "market", sl=sl, tp=tp, min_rr=self.min_rr,
                      label=self.label, entry_tf=gtf)
            out.append(self._extra(o, p))
        return out


class AFS02(AFS01):
    id = "AFS-02"
    name = "Technical Research 5 tahap, versi scalping (H1 / M15 / M5)"
    tfs = ("H1", "M15", "M5")
    entry_tf = "M5"
    label = "scalping"
    pivot_period = "D1"
    min_rr = 2.0
    defaults = {"points": "4of5", "pattern": True, "sl_atr": 1.0, "hold_hours": 3}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]},
                        comparisons={"points": ["4of5", "5of5"], "pattern": [True, False],
                                     "hold_hours": [3, 24]})

    def _extra(self, o, p):
        o.hold_hours = float(p["hold_hours"])
        return o


class AFS03(Setup):
    id = "AFS-03"
    name = "Double/triple top-bottom + tembus neckline (M15, scalping)"
    mentor = "Alvesting (Akademi Crypto) — pola scalping"
    category = "both"           # pembalikan; versi konfirmasi juga breakout (07)
    label = "scalping"
    entry_tf = "M15"
    uses_volume = True          # AFS-F2 untuk versi konfirmasi
    defaults = {"tol": 0.5, "mode": "confirm", "sl_atr": 1.0, "hold_hours": 3}

    def category_of(self, p):
        return "both" if p.get("mode") == "confirm" else "reversal"

    def plan(self):
        return TestPlan(tested={"tol": [0.25, 0.5, 0.75], "sl_atr": [0.5, 1.0, 1.5]},
                        comparisons={"mode": ["confirm", "anticipate"], "hold_hours": [3, 24]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "M15")
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        volhi = ctx.vol_high
        use_vol = p.get("volume", "tick") == "tick"
        out = []
        n = len(b)
        last_sig = {1: -1, -1: -1}
        for t in range(10, n):
            if np.isnan(a[t]):
                continue
            tol = p["tol"] * a[t]
            for dirn in (-1, 1):  # −1: double top → short; +1: double bottom → long
                if dirn < 0:
                    peaks = swing_levels(ctx, t, "high", 200)[:4]
                    idxs = ctx._memo("_sh_idx", lambda: np.flatnonzero(sw.sh))
                else:
                    peaks = swing_levels(ctx, t, "low", 200)[:4]
                    idxs = ctx._memo("_sl_idx", lambda: np.flatnonzero(sw.sl))
                if len(peaks) < 2:
                    continue
                k_hi = np.searchsorted(idxs, t - 2, side="right")
                pidx = idxs[max(0, k_hi - 4):k_hi][::-1]
                # jumlah puncak yang sama tinggi (2 atau 3); puncak ke-4 yang sama → batal
                m = 1
                while m < len(peaks) and _equal(peaks[m], peaks[0], tol) and all(_equal(peaks[m], q, tol) for q in peaks[:m]):
                    m += 1
                if m < 2 or m > 3:
                    continue
                first, last = pidx[m - 1], pidx[0]
                top = peaks[:m].max() if dirn < 0 else peaks[:m].min()
                seg = slice(first, t + 1)
                # puncak gagal ditembus: tidak ada harga di luar puncak sejak puncak pertama
                if (dirn < 0 and b.h[seg].max() > top) or (dirn > 0 and b.l[seg].min() < top):
                    continue
                neck = b.l[first:last + 1].min() if dirn < 0 else b.h[first:last + 1].max()
                sl = top + p["sl_atr"] * a[t] if dirn < 0 else top - p["sl_atr"] * a[t]
                if last_sig[dirn] == last:
                    continue
                if p["mode"] == "confirm":
                    if t < last + 2:
                        continue
                    closes = b.c[last + 1: t + 1]
                    brk = closes < neck if dirn < 0 else closes > neck
                    # tembus pertama kali sekarang, atau sudah tembus sebelum puncak terakhir diakui
                    if not brk[-1] or (brk[:-1].any() and t != last + 2):
                        continue
                    first_brk = last + 1 + int(np.argmax(brk))
                    if use_vol and not volhi[first_brk]:
                        continue
                    o = Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=float(sl), tp_rr=2.0,
                              min_rr=2.0, label="scalping", hold_hours=float(p["hold_hours"]), entry_tf="M15")
                else:
                    if t != last + 2:
                        continue
                    if (dirn < 0 and b.c[t] <= neck) or (dirn > 0 and b.c[t] >= neck):
                        continue
                    tp = neck - 2 * (sl - neck) if dirn < 0 else neck + 2 * (neck - sl)
                    o = Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=float(sl), tp=float(tp),
                              min_rr=2.0, label="scalping", hold_hours=float(p["hold_hours"]), entry_tf="M15")
                last_sig[dirn] = last
                out.append(o)
        out.sort(key=lambda o: o.created)
        return out
