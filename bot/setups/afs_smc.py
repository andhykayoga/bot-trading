"""Smart Money Concept Alvesting (rulebook 01 bagian C): AFS-06, AFS-07, AFS-08.

Aturan bersama (Q-20): pola & entry di M15, arah tidak melawan struktur H4, TP =
likuiditas terdekat di sisi lawan (PDH/PDL, PWH/PWL, swing M15) dengan RR ≥ 1:2,
SL di swing invalidasi ± 1 × ATR(14) M15.
"""
from __future__ import annotations

import numpy as np

from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, swing_levels

TF = "M15"


def _smc_ctx(d):
    ctx = Ctx.get(d, TF)
    def build():
        b = ctx.b
        i_d, i_w, i_m = (d[x].idx_at(b.t_close) for x in ("D1", "W1", "MN"))
        pick = lambda arr, i: np.where(i >= 0, arr[np.clip(i, 0, None)], np.nan)
        h4 = Ctx.get(d, "H4")
        i_h4 = ctx.htf_index("H4")
        return {
            "pdh": pick(d["D1"].h, i_d), "pdl": pick(d["D1"].l, i_d),
            "pwh": pick(d["W1"].h, i_w), "pwl": pick(d["W1"].l, i_w),
            "pmh": pick(d["MN"].h, i_m), "pml": pick(d["MN"].l, i_m),
            "h4trend": np.where(i_h4 >= 0, h4.sw.trend[np.clip(i_h4, 0, None)], 0),
            # ambang "Auto" FVG LuxAlgo: rata-rata kumulatif (high − low) / low
            "fvg_thr": np.cumsum((b.h - b.l) / b.l) / np.arange(1, len(b) + 1),
        }
    return ctx, ctx._memo("smc", build)


def liquidity_tp(ctx: Ctx, L: dict, t: int, direction: int, entry: float, sl: float, min_rr: float = 2.0):
    """TP = likuiditas terdekat di sisi lawan; masuk hanya kalau RR ke sana ≥ min_rr (Q-20).
    Likuiditas yang sudah dilewati harga sekarang (close candle sinyal) sudah tersapu, jadi
    hanya level di luar harga entry dan harga sekarang yang dihitung."""
    ref = ctx.b.c[t]
    if direction > 0:
        cands = np.r_[L["pdh"][t], L["pwh"][t], swing_levels(ctx, t, "high", 200)]
        cands = cands[cands > max(entry, ref)]
        if len(cands) == 0:
            return np.nan
        tp = cands.min()
    else:
        cands = np.r_[L["pdl"][t], L["pwl"][t], swing_levels(ctx, t, "low", 200)]
        cands = cands[cands < min(entry, ref)]
        if len(cands) == 0:
            return np.nan
        tp = cands.max()
    risk = (entry - sl) * direction
    if risk <= 0 or (tp - entry) * direction < min_rr * risk:
        return np.nan
    return float(tp)


def find_fvg(b, thr, a: int, t: int, direction: int):
    """FVG terbaru (definisi LuxAlgo, Q-21) di candle a..t. Kembalikan tepi yang pertama
    disentuh saat harga kembali: bullish = tepi atas (low[k]), bearish = tepi bawah (high[k])."""
    for k in range(t, max(a + 2, 2) - 1, -1):
        if direction > 0:
            if b.l[k] > b.h[k - 2] and b.c[k - 1] > b.h[k - 2] and (b.l[k] - b.h[k - 2]) / b.h[k - 2] > thr[k]:
                return float(b.l[k])
        else:
            if b.h[k] < b.l[k - 2] and b.c[k - 1] < b.l[k - 2] and (b.l[k - 2] - b.h[k]) / b.h[k] > thr[k]:
                return float(b.h[k])
    return None


class _SMC(Setup):
    mentor = "Alvesting (Akademi Crypto) — Smart Money Concept"
    entry_tf = TF

    def _make(self, sym, ctx, L, t, d, entry_kind, entry, sl, p, expiry_bars):
        b = ctx.b
        tp = liquidity_tp(ctx, L, t, d, entry, sl, 2.0)
        if np.isnan(tp) or np.isnan(sl):
            return None
        if entry_kind == "market":
            return Order(self.id, sym, d, int(b.t_close[t]), "market", sl=float(sl), tp=tp, min_rr=2.0, entry_tf=TF)
        e = min(t + expiry_bars, len(b) - 1)
        return Order(self.id, sym, d, int(b.t_close[t]), "limit", sl=float(sl), price=float(entry), tp=tp,
                     min_rr=2.0, expiry=int(b.t_close[e]), entry_tf=TF,
                     cancel_above=tp if d > 0 else np.nan, cancel_below=tp if d < 0 else np.nan)


class AFS06(_SMC):
    id = "AFS-06"
    name = "Stop hunt + break of structure"
    category = "reversal"
    defaults = {"sh_pen": 0.1, "sh_bars": 3, "entry": "market", "limit_bars": 20, "sl_atr": 1.0}

    def plan(self):
        return TestPlan(setara={"entry": ["market", "fvg"]},
                        tested={"sh_pen": [0.05, 0.1, 0.15], "sh_bars": [2, 3, 4],
                                "limit_bars": [10, 20, 30], "sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx, L = _smc_ctx(d)
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        out = []
        n = len(b)
        refs_hi = np.c_[L["pdh"], L["pwh"], L["pmh"]]
        refs_lo = np.c_[L["pdl"], L["pwl"], L["pml"]]
        for dirn in (-1, 1):
            st = None  # keadaan: dict(ref, pen_bar, peak, peak_i, rto, hl)
            for t in range(3, n):
                if np.isnan(a[t]):
                    continue
                if st is not None:
                    # batal kalau harga membuat ekstrem baru di luar puncak stop hunt sebelum BMS
                    ext = b.h[t] if dirn < 0 else b.l[t]
                    if (ext > st["peak"]) if dirn < 0 else (ext < st["peak"]):
                        if not st["rto"] and t - st["pen"] + 1 <= p["sh_bars"]:
                            st["peak"], st["peak_i"] = ext, t   # masih dalam fase tembus
                        else:
                            st = None
                if st is not None and not st["rto"]:
                    back = b.c[t] < st["ref"] if dirn < 0 else b.c[t] > st["ref"]
                    if back and t - st["pen"] + 1 <= p["sh_bars"]:
                        st["rto"] = True
                    elif t - st["pen"] + 1 > p["sh_bars"]:
                        st = None
                if st is not None and st["rto"]:
                    bms = b.c[t] < st["hl"] if dirn < 0 else b.c[t] > st["hl"]
                    if bms:
                        h4 = L["h4trend"][t]
                        if not ((dirn < 0 and h4 == 1) or (dirn > 0 and h4 == -1)):
                            sl = st["peak"] + p["sl_atr"] * a[t] if dirn < 0 else st["peak"] - p["sl_atr"] * a[t]
                            if p["entry"] == "market":
                                o = self._make(sym, ctx, L, t, dirn, "market", b.c[t], sl, p, 0)
                            else:
                                lvl = find_fvg(b, L["fvg_thr"], st["peak_i"], t, dirn)
                                o = self._make(sym, ctx, L, t, dirn, "limit", lvl, sl, p, p["limit_bars"]) \
                                    if lvl is not None else None
                            if o:
                                out.append(o)
                        st = None
                        continue
                if st is None:
                    # stop hunt baru: tembus likuiditas acuan minimal sh_pen × ATR
                    if dirn < 0:
                        refs = np.r_[refs_hi[t - 1], sw.hp[t - 1, 0]]
                        hl_ok = sw.lp[t, 0] > sw.lp[t, 1]           # harga sedang naik: higher low
                        pen = refs[(b.h[t] >= refs + p["sh_pen"] * a[t]) & (b.o[t] < refs)]
                    else:
                        refs = np.r_[refs_lo[t - 1], sw.lp[t - 1, 0]]
                        hl_ok = sw.hp[t, 0] < sw.hp[t, 1]           # harga sedang turun: lower high
                        pen = refs[(b.l[t] <= refs - p["sh_pen"] * a[t]) & (b.o[t] > refs)]
                    pen = pen[~np.isnan(pen)]
                    if len(pen) and hl_ok:
                        ref = pen.max() if dirn < 0 else pen.min()
                        st = {"ref": ref, "pen": t, "peak": b.h[t] if dirn < 0 else b.l[t], "peak_i": t,
                              "rto": False, "hl": sw.lp[t, 0] if dirn < 0 else sw.hp[t, 0]}
                        back = b.c[t] < ref if dirn < 0 else b.c[t] > ref
                        if back:
                            st["rto"] = True
        out.sort(key=lambda o: o.created)
        return out


class AFS07(_SMC):
    id = "AFS-07"
    name = "Change of character (CHoCH) + retest"
    category = "reversal"
    defaults = {"retest_bars": 10, "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"retest_bars": [5, 10, 15], "sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx, L = _smc_ctx(d)
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        out = []
        for t in range(2, len(b)):
            if np.isnan(a[t]):
                continue
            h4 = L["h4trend"][t]
            # CHoCH bearish: struktur bullish lalu close di bawah higher low terakhir
            if sw.trend[t - 1] == 1 and b.c[t] < sw.lp[t, 0] and h4 != 1:
                lvl = sw.lp[t, 0]
                entry = lvl - 0.5 * a[t]                       # tepi bawah zona (D-10)
                sl = sw.hp[t, 0] + p["sl_atr"] * a[t]
                o = self._make(sym, ctx, L, t, -1, "limit", entry, sl, p, p["retest_bars"])
                if o:
                    out.append(o)
            if sw.trend[t - 1] == -1 and b.c[t] > sw.hp[t, 0] and h4 != -1:
                lvl = sw.hp[t, 0]
                entry = lvl + 0.5 * a[t]
                sl = sw.lp[t, 0] - p["sl_atr"] * a[t]
                o = self._make(sym, ctx, L, t, 1, "limit", entry, sl, p, p["retest_bars"])
                if o:
                    out.append(o)
        return out


class AFS08(_SMC):
    id = "AFS-08"
    name = "Revisit fair value gap setelah BOS"
    category = "trend"
    defaults = {"limit_bars": 20, "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"limit_bars": [10, 20, 30], "sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx, L = _smc_ctx(d)
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        out = []
        for t in range(3, len(b)):
            if np.isnan(a[t]):
                continue
            h4 = L["h4trend"][t]
            for dirn in (1, -1):
                lvl_prev, lvl = (sw.hp[t - 1, 0], sw.hp[t, 0]) if dirn > 0 else (sw.lp[t - 1, 0], sw.lp[t, 0])
                if np.isnan(lvl):
                    continue
                bos = (b.c[t] > lvl and b.c[t - 1] <= lvl_prev) if dirn > 0 else (b.c[t] < lvl and b.c[t - 1] >= lvl_prev)
                if not bos or (dirn > 0 and h4 == -1) or (dirn < 0 and h4 == 1):
                    continue
                start_i = sw.li[t, 0] if dirn > 0 else sw.hi[t, 0]    # awal gerakan penyebab BOS
                if start_i < 0:
                    continue
                edge = find_fvg(b, L["fvg_thr"], int(start_i), t, dirn)
                if edge is None:
                    continue
                sl = sw.lp[t, 0] - p["sl_atr"] * a[t] if dirn > 0 else sw.hp[t, 0] + p["sl_atr"] * a[t]
                o = self._make(sym, ctx, L, t, dirn, "limit", edge, sl, p, p["limit_bars"])
                if o:
                    out.append(o)
        return out
