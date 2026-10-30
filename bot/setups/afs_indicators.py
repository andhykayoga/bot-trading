"""Setup indikator Alvesting (rulebook 01 bagian F): AFS-12 – AFS-21."""
from __future__ import annotations

import numpy as np

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, pivots, swing_levels, swing_sl, zone_tp
from bot.setups.ichimoku import SHIFT

RETEST = 10   # D-05: retest ditunggu maksimal 10 candle


def _nearest_rr(levels, entry, sl, d, min_rr):
    """Target terdekat dari daftar level yang RR-nya ≥ minimum (Q-08)."""
    risk = (entry - sl) * d
    if risk <= 0:
        return np.nan
    ok = [x for x in levels if not np.isnan(x) and (x - entry) * d >= min_rr * risk]
    if not ok:
        return np.nan
    return float(min(ok) if d > 0 else max(ok))


def _limit_each_bar(setup_id, sym, b, t, d, price, sl, tp, min_rr, tf, tp_rr=np.nan):
    """Order limit di garis yang bergerak: dipasang ulang tiap candle, berlaku 1 candle."""
    if t + 1 >= len(b):
        return None
    return Order(setup_id, sym, d, int(b.t_close[t]), "limit", sl=float(sl), price=float(price), tp=float(tp),
                 tp_rr=tp_rr, min_rr=min_rr, expiry=int(b.t_close[t + 1]), entry_tf=tf)


class AFS12(Setup):
    id = "AFS-12"
    name = "Pivot point: entry di garis P"
    mentor = "Alvesting (Akademi Crypto) — pivot point"
    category = "trend"
    defaults = {"tf": "H1", "sl_mode": "P", "sl_atr": 1.0}

    def plan(self):
        # Timeframe H1 (pivot mingguan, trading) / M15 & M5 (pivot harian, scalping) diuji setara.
        return TestPlan(tf=["H1", "M15", "M5"], setara={"sl_mode": ["P", "S1"]},
                        tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        period = "W1" if tf == "H1" else "D1"
        label = "trading" if tf == "H1" else "scalping"
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        pv = pivots(ctx, period)
        P = pv["P"]
        out = []
        armed = {1: -2, -1: -2}     # periode pivot saat setup dipersenjatai
        done = {1: -2, -1: -2}
        for t in range(1, len(b) - 1):
            per = pv["period"][t]
            if per < 0 or np.isnan(a[t]) or np.isnan(P[t]):
                continue
            # long: harga di atas P dan berkonsolidasi di area R1 → tunggu turun ke P
            if b.c[t] > P[t] and b.h[t] >= pv["R1"][t] - 0.5 * a[t]:
                armed[1] = per
            # short: harga close di bawah P → tunggu naik kembali ke P
            if b.c[t] < P[t]:
                armed[-1] = per
            for dirn in (1, -1):
                if armed[dirn] != per or done[dirn] == per:
                    continue
                if (dirn > 0 and b.c[t] <= P[t]) or (dirn < 0 and b.c[t] >= P[t]):
                    continue
                if dirn > 0:
                    base = P[t] if p["sl_mode"] == "P" else pv["S1"][t]
                    sl = base - p["sl_atr"] * a[t]
                    tp = _nearest_rr([pv["R1"][t], pv["R2"][t], pv["R3"][t]], P[t], sl, 1, 1.5)
                else:
                    base = P[t] if p["sl_mode"] == "P" else pv["R1"][t]
                    sl = base + p["sl_atr"] * a[t]
                    tp = _nearest_rr([pv["S1"][t], pv["S2"][t]], P[t], sl, -1, 1.5)
                if np.isnan(tp):
                    continue
                o = Order(self.id, sym, dirn, int(b.t_close[t]), "limit", sl=float(sl), price=float(P[t]),
                          tp=tp, min_rr=1.5, expiry=int(b.t_close[t + 1]), label=label, entry_tf=tf)
                out.append(o)
        return out


class AFS13A(Setup):
    id = "AFS-13A"
    name = "Keltner Channel mode tren (retest garis tengah)"
    mentor = "Alvesting (Akademi Crypto) — Keltner Channel"
    category = "trend"
    defaults = {"tf": "H4", "sl_atr": 1.0, "retest": RETEST}

    def plan(self):
        return TestPlan(tf=["H1", "H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5], "retest": [5, 10, 15]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        mid, up, lo = ctx._memo("kc", lambda: ind.keltner(b.h, b.l, b.c, 20, 10, 2.0))
        bear_trig = ctx.patterns[1]
        out = []
        cross_up = cross_dn = -10**9
        for t in range(21, len(b) - 1):
            if np.isnan(mid[t]) or np.isnan(a[t]):
                continue
            if b.c[t] > mid[t] and b.c[t - 1] <= mid[t - 1]:
                cross_up = t
            if b.c[t] < mid[t] and b.c[t - 1] >= mid[t - 1]:
                cross_dn = t
            # long: sudah tembus ke atas garis tengah, pasang limit tepat di garis tengah selama masa retest
            if 0 < t - cross_up <= p["retest"] and b.c[t] > mid[t]:
                sl = mid[t] - p["sl_atr"] * a[t]
                o = _limit_each_bar(self.id, sym, b, t, 1, mid[t], sl, up[t], 2.0, tf)
                if o:
                    out.append(o)
            # short: retest garis tengah dari bawah + candle pemicu melemah → order pasar
            if 0 < t - cross_dn <= p["retest"] and b.h[t] >= mid[t] and b.c[t] < mid[t] and bear_trig[t]:
                sl = mid[t] + p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, -1, int(b.t_close[t]), "market", sl=float(sl), tp=float(lo[t]),
                                 min_rr=2.0, entry_tf=tf))
        return out


class AFS13B(Setup):
    id = "AFS-13B"
    name = "Keltner Channel mode pantulan (pita luar)"
    mentor = "Alvesting (Akademi Crypto) — Keltner Channel"
    category = "reversal"
    defaults = {"tf": "H4", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H1", "H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        mid, up, lo = ctx._memo("kc", lambda: ind.keltner(b.h, b.l, b.c, 20, 10, 2.0))
        out = []
        for t in range(21, len(b) - 1):
            if np.isnan(mid[t]) or np.isnan(a[t]):
                continue
            # long: limit tepat di pita bawah; SL di bawah swing low terakhir (di bawah pita)
            if b.c[t] > lo[t]:
                sl = swing_sl(ctx, t, 1, lo[t], p["sl_atr"])
                tp = _nearest_rr([mid[t], up[t]], lo[t], sl, 1, 1.5) if not np.isnan(sl) else np.nan
                if not np.isnan(tp):
                    out.append(_limit_each_bar(self.id, sym, b, t, 1, lo[t], sl, tp, 1.5, tf))
            if b.c[t] < up[t]:
                sl = swing_sl(ctx, t, -1, up[t], p["sl_atr"])
                tp = _nearest_rr([mid[t], lo[t]], up[t], sl, -1, 1.5) if not np.isnan(sl) else np.nan
                if not np.isnan(tp):
                    out.append(_limit_each_bar(self.id, sym, b, t, -1, up[t], sl, tp, 1.5, tf))
        return [o for o in out if o is not None]


class AFS14(Setup):
    id = "AFS-14"
    name = "Ichimoku di atas/bawah semua garis (D1)"
    mentor = "Alvesting (Akademi Crypto) — Ichimoku"
    category = "trend"
    entry_tf = "D1"
    defaults = {"sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, a, ic = ctx.b, ctx.atr, ctx.ichi
        c = b.c
        c25 = ind.shift(c, SHIFT)
        top25, bot25 = ind.shift(ic["kumo_top"], SHIFT), ind.shift(ic["kumo_bot"], SHIFT)
        above = (c > ic["kumo_top"]) & (c > ic["tenkan"]) & (c > ic["kijun"]) & (c > c25) & (c > top25)
        below = (c < ic["kumo_bot"]) & (c < ic["tenkan"]) & (c < ic["kijun"]) & (c < c25) & (c < bot25)
        out = []
        for t in range(1, len(c)):
            if np.isnan(a[t]):
                continue
            if above[t] and not above[t - 1]:
                sl = ic["kumo_bot"][t] - p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=float(sl), tp_rr=3.0,
                                 min_rr=3.0, entry_tf="D1"))
            if below[t] and not below[t - 1] and t + RETEST < len(c):
                # short: tunggu retest Kumo dari bawah → limit di tepi bawah Kumo, batal setelah 10 candle
                lvl = ic["kumo_bot"][t]
                sl = ic["kumo_top"][t] + p["sl_atr"] * a[t]
                out.append(Order(self.id, sym, -1, int(b.t_close[t]), "limit", sl=float(sl), price=float(lvl),
                                 tp_rr=3.0, min_rr=3.0, expiry=int(b.t_close[t + RETEST]), entry_tf="D1"))
        return out


class AFS15(Setup):
    id = "AFS-15"
    name = "Parabolic SAR titik ke-2"
    mentor = "Alvesting (Akademi Crypto) — Parabolic SAR"
    category = "reversal"
    defaults = {"tf": "H4", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H1", "H4"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        sar, trend = ctx._memo("psar", lambda: ind.psar(b.h, b.l))
        rr = 2.0 if tf == "H1" else 3.0
        out = []
        for t in range(3, len(b)):
            if np.isnan(a[t]):
                continue
            # titik ke-2 searah: arah baru dimulai di t−1, t adalah titik kedua
            if trend[t] != 0 and trend[t] == trend[t - 1] and trend[t - 2] == -trend[t]:
                dirn = int(trend[t])
                sl = swing_sl(ctx, t, dirn, b.c[t], p["sl_atr"])
                if np.isnan(sl):
                    continue
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=rr, min_rr=rr,
                                 entry_tf=tf))
        return out


class AFS16P(Setup):
    id = "AFS-16P"
    name = "Donchian Channel mode pantulan"
    mentor = "Alvesting (Akademi Crypto) — Donchian Channel"
    category = "reversal"
    defaults = {"tf": "H4", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H1", "H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        up, mid, lo = ctx._memo("dc", lambda: ind.donchian(b.h, b.l, 20))
        out = []
        for t in range(21, len(b)):
            if np.isnan(a[t]):
                continue
            # pita dari 20 candle sebelumnya; "menyentuh" = low ≤ pita bawah
            if b.l[t] <= lo[t - 1]:
                sl = b.l[t] - p["sl_atr"] * a[t]
                tp = _nearest_rr([mid[t - 1], up[t - 1]], b.c[t], sl, 1, 1.5)
                if not np.isnan(tp):
                    out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=float(sl), tp=tp,
                                     min_rr=1.5, entry_tf=tf))
            if b.h[t] >= up[t - 1]:
                sl = b.h[t] + p["sl_atr"] * a[t]
                tp = _nearest_rr([mid[t - 1], lo[t - 1]], b.c[t], sl, -1, 1.5)
                if not np.isnan(tp):
                    out.append(Order(self.id, sym, -1, int(b.t_close[t]), "market", sl=float(sl), tp=tp,
                                     min_rr=1.5, entry_tf=tf))
        return out


class AFS16T(Setup):
    id = "AFS-16T"
    name = "Donchian Channel mode tren (silang garis tengah)"
    mentor = "Alvesting (Akademi Crypto) — Donchian Channel"
    category = "trend"
    defaults = {"tf": "H4", "sl_atr": 1.0, "retest": RETEST}

    def plan(self):
        return TestPlan(tf=["H1", "H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5], "retest": [5, 10, 15]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        up, mid, lo = ctx._memo("dc", lambda: ind.donchian(b.h, b.l, 20))
        out = []
        cross_dn = -10**9
        for t in range(21, len(b) - 1):
            if np.isnan(a[t]):
                continue
            if b.c[t] > mid[t] and b.c[t - 1] <= mid[t - 1]:
                sl = swing_sl(ctx, t, 1, b.c[t], p["sl_atr"])
                if not np.isnan(sl):
                    out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                                     entry_tf=tf))
            if b.c[t] < mid[t] and b.c[t - 1] >= mid[t - 1]:
                cross_dn = t
            if 0 < t - cross_dn <= p["retest"] and b.c[t] < mid[t]:
                sl = swing_sl(ctx, t, -1, mid[t], p["sl_atr"])
                if not np.isnan(sl):
                    o = _limit_each_bar(self.id, sym, b, t, -1, mid[t], sl, lo[t], 1.5, tf)
                    if o:
                        out.append(o)
        return out


class AFS17(Setup):
    id = "AFS-17"
    name = "KST silang di garis nol (D1)"
    mentor = "Alvesting (Akademi Crypto) — KST"
    category = "reversal"
    entry_tf = "D1"
    defaults = {"sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, a = ctx.b, ctx.atr
        k, s = ctx._memo("kst", lambda: ind.kst(b.c))
        out = []
        for t in range(1, len(b)):
            if np.isnan(s[t]) or np.isnan(s[t - 1]) or np.isnan(a[t]):
                continue
            up = k[t - 1] <= s[t - 1] and k[t] > s[t] and k[t] < 0
            dn = k[t - 1] >= s[t - 1] and k[t] < s[t] and k[t] > 0
            for dirn, ok in ((1, up), (-1, dn)):
                if ok:
                    sl = swing_sl(ctx, t, dirn, b.c[t], p["sl_atr"])
                    if not np.isnan(sl):
                        out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0,
                                         min_rr=3.0, entry_tf="D1"))
        return out


class AFS18(Setup):
    id = "AFS-18"
    name = "Konfirmasi Chaikin Money Flow (breakout & divergensi)"
    mentor = "Alvesting (Akademi Crypto) — Chaikin Money Flow"
    category = "both"
    uses_volume = True
    volume_only = True       # tanpa volume setup ini tidak dijalankan di forex (D-07)
    defaults = {"tf": "D1", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a, sw = ctx.b, ctx.atr, ctx.sw
        cm = ctx._memo("cmf", lambda: ind.cmf(b.h, b.l, b.c, b.v, 20))
        out = []
        for t in range(25, len(b)):
            if np.isnan(a[t]):
                continue
            half = 0.5 * a[t]
            res = swing_levels(ctx, t - 1, "high", 150)
            sup = swing_levels(ctx, t - 1, "low", 150)
            # breakout: close di atas zona resistance (yang sebelumnya di atas harga) + CMF > 0
            r = res[res + half >= b.c[t - 1]]
            if len(r) and b.c[t] > r.min() + half and b.c[t - 1] <= r.min() + half and cm[t] > 0:
                sl = swing_sl(ctx, t, 1, b.c[t], p["sl_atr"])
                if not np.isnan(sl):
                    out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                                     entry_tf=tf, tags={"jenis": "breakout"}))
            s_ = sup[sup - half <= b.c[t - 1]]
            if len(s_) and b.c[t] < s_.max() - half and b.c[t - 1] >= s_.max() - half and cm[t] < 0:
                sl = swing_sl(ctx, t, -1, b.c[t], p["sl_atr"])
                if not np.isnan(sl):
                    out.append(Order(self.id, sym, -1, int(b.t_close[t]), "market", sl=sl, tp_rr=3.0, min_rr=3.0,
                                     entry_tf=tf, tags={"jenis": "breakout"}))
            # divergensi: swing kedua baru diakui di candle ini (t = indeks swing + 2)
            j = t - 2
            if j >= 0 and sw.sl[j] and sw.li[t, 1] >= 0 and sw.li[t, 0] == j:
                i1 = sw.li[t, 1]
                if b.l[j] < b.l[i1] and cm[j] > cm[i1]:
                    sl = b.l[j] - p["sl_atr"] * a[t]
                    out.append(Order(self.id, sym, 1, int(b.t_close[t]), "market", sl=float(sl), tp_rr=3.0,
                                     min_rr=3.0, entry_tf=tf, tags={"jenis": "divergensi"}))
            if j >= 0 and sw.sh[j] and sw.hi[t, 1] >= 0 and sw.hi[t, 0] == j:
                i1 = sw.hi[t, 1]
                if b.h[j] > b.h[i1] and cm[j] < cm[i1]:
                    sl = b.h[j] + p["sl_atr"] * a[t]
                    out.append(Order(self.id, sym, -1, int(b.t_close[t]), "market", sl=float(sl), tp_rr=3.0,
                                     min_rr=3.0, entry_tf=tf, tags={"jenis": "divergensi"}))
        return out


def volume_poc(m5, t_from: int, t_to: int, rows: int = 24) -> float:
    """POC (harga dengan volume terbanyak) dari candle M5 di [t_from, t_to); volume tiap
    candle dibagi rata ke baris harga yang dilaluinya."""
    a = np.searchsorted(m5.t_open, t_from)
    b = np.searchsorted(m5.t_open, t_to)
    if b - a < 10:
        return np.nan
    h, l, v = m5.h[a:b], m5.l[a:b], m5.v[a:b]
    lo, hi = l.min(), h.max()
    if hi <= lo:
        return np.nan
    edges = np.linspace(lo, hi, rows + 1)
    vol = np.zeros(rows)
    i0 = np.clip(np.searchsorted(edges, l, side="right") - 1, 0, rows - 1)
    i1 = np.clip(np.searchsorted(edges, h, side="right") - 1, 0, rows - 1)
    span = i1 - i0 + 1
    for k in range(len(v)):
        vol[i0[k]: i1[k] + 1] += v[k] / span[k]
    j = int(np.argmax(vol))
    return float((edges[j] + edges[j + 1]) / 2)


class AFS19(Setup):
    id = "AFS-19"
    name = "Pantulan POC volume profile"
    mentor = "Alvesting (Akademi Crypto) — volume profile"
    category = "trend"
    uses_volume = True
    volume_only = True
    defaults = {"poc": "week", "sl_atr": 1.0}

    def plan(self):
        # POC minggu lalu (chart H1) vs POC bulan lalu (chart H4) — setara (Q-24)
        return TestPlan(setara={"poc": ["week", "month"]}, tested={"sl_atr": [0.5, 1.0, 1.5]})

    def entry_tf_of(self, p):
        return "H1" if p.get("poc") == "week" else "H4"

    def signals_for(self, sym, d, p):
        tf = self.entry_tf_of(p)
        period = "W1" if p["poc"] == "week" else "MN"
        rr = 2.0 if tf == "H1" else 3.0
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        pb = d[period]
        poc_by_period = ctx._memo(f"poc_{period}", lambda: np.array(
            [volume_poc(d["M5"], int(pb.t_open[i]), int(pb.t_close[i])) for i in range(len(pb))]))
        ip = ctx.htf_index(period)
        out = []
        for t in range(1, len(b) - 1):
            if ip[t] < 0 or np.isnan(a[t]):
                continue
            poc = poc_by_period[ip[t]]
            if np.isnan(poc):
                continue
            if b.c[t] > poc:         # harga di atas POC → limit long di POC
                sl = poc - p["sl_atr"] * a[t]
                o = _limit_each_bar(self.id, sym, b, t, 1, poc, sl, np.nan, rr, tf, tp_rr=rr)
                if o:
                    out.append(o)
            elif b.c[t] < poc:       # harga di bawah POC → limit short di POC, TP zona support terdekat
                sl = poc + p["sl_atr"] * a[t]
                tp = zone_tp(ctx, t, -1, poc, sl, 2.0)
                if not np.isnan(tp):
                    o = _limit_each_bar(self.id, sym, b, t, -1, poc, sl, tp, 2.0, tf)
                    if o:
                        out.append(o)
        return out


class AFS20R(Setup):
    id = "AFS-20R"
    name = "Linear Regression Channel mode range (H4)"
    mentor = "Alvesting (Akademi Crypto) — Linear Regression Channel"
    category = "trend"
    entry_tf = "H4"
    defaults = {"sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "H4")
        b, a = ctx.b, ctx.atr
        mid, up, lo = ctx._memo("lrc", lambda: ind.linreg_channel(b.c, 100, 2.0))
        out = []
        for t in range(100, len(b) - 1):
            if np.isnan(up[t]) or np.isnan(a[t]):
                continue
            if lo[t] < b.c[t] < up[t]:
                sl = swing_sl(ctx, t, 1, lo[t], p["sl_atr"])
                if not np.isnan(sl):
                    o = _limit_each_bar(self.id, sym, b, t, 1, lo[t], sl, up[t], 1.5, "H4")
                    if o:
                        out.append(o)
                sl = swing_sl(ctx, t, -1, up[t], p["sl_atr"])
                if not np.isnan(sl):
                    o = _limit_each_bar(self.id, sym, b, t, -1, up[t], sl, lo[t], 1.5, "H4")
                    if o:
                        out.append(o)
        return out


class AFS20B(Setup):
    id = "AFS-20B"
    name = "Linear Regression Channel mode breakout + retest (H4)"
    mentor = "Alvesting (Akademi Crypto) — Linear Regression Channel"
    category = "breakout"
    entry_tf = "H4"
    uses_volume = True
    defaults = {"sl_atr": 1.0, "retest": RETEST}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5], "retest": [5, 10, 15]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "H4")
        b, a = ctx.b, ctx.atr
        mid, up, lo = ctx._memo("lrc", lambda: ind.linreg_channel(b.c, 100, 2.0))
        use_vol = p.get("volume", "tick") == "tick"
        volhi = ctx.vol_high
        out = []
        for t in range(101, len(b) - p["retest"]):
            if np.isnan(up[t]) or np.isnan(a[t]):
                continue
            half = 0.5 * a[t]
            for dirn in (-1, 1):
                brk = (b.c[t] < lo[t] and b.c[t - 1] >= lo[t - 1]) if dirn < 0 else \
                      (b.c[t] > up[t] and b.c[t - 1] <= up[t - 1])
                if not brk or (use_vol and not volhi[t]):
                    continue
                lvl = lo[t] if dirn < 0 else up[t]
                entry = lvl - half if dirn < 0 else lvl + half     # tepi zona yang pertama disentuh saat retest
                sl = swing_sl(ctx, t, dirn, entry, p["sl_atr"])
                if np.isnan(sl):
                    continue
                out.append(Order(self.id, sym, dirn, int(b.t_close[t]), "limit", sl=sl, price=float(entry),
                                 tp_rr=3.0, min_rr=3.0, expiry=int(b.t_close[t + p["retest"]]), entry_tf="H4"))
        return out


def renko(c: np.ndarray, box: np.ndarray):
    """Renko klasik dari harga close dengan ukuran bata ATR(14) saat bata dibentuk.
    Mengembalikan daftar bata: (indeks candle selesai, arah +1/−1, low/high terendah sejak bata sebelumnya)."""
    bricks = []
    if len(c) == 0:
        return bricks
    start = np.flatnonzero(~np.isnan(box))
    if len(start) == 0:
        return bricks
    i0 = start[0]
    base = c[i0]
    last_dir = 0
    ext_lo, ext_hi = c[i0], c[i0]
    for i in range(i0 + 1, len(c)):
        bx = box[i]
        ext_lo, ext_hi = min(ext_lo, c[i]), max(ext_hi, c[i])
        while True:
            up_need = bx if last_dir >= 0 else 2 * bx
            dn_need = bx if last_dir <= 0 else 2 * bx
            if c[i] >= base + up_need:
                base = base + up_need          # bata baru: close = base lama + 1 bata (lanjut) / 2 bata (balik)
                bricks.append((i, 1, ext_lo))
                last_dir = 1
                ext_lo, ext_hi = c[i], c[i]
            elif c[i] <= base - dn_need:
                base = base - dn_need
                bricks.append((i, -1, ext_hi))
                last_dir = -1
                ext_lo, ext_hi = c[i], c[i]
            else:
                break
    return bricks


class AFS21(Setup):
    id = "AFS-21"
    name = "Renko reversal (D1)"
    mentor = "Alvesting (Akademi Crypto) — Renko"
    category = "reversal"
    entry_tf = "D1"
    defaults = {"sl_atr": 1.0}

    def plan(self):
        return TestPlan(tested={"sl_atr": [0.5, 1.0, 1.5]})

    def signals_for(self, sym, d, p):
        ctx = Ctx.get(d, "D1")
        b, a = ctx.b, ctx.atr
        bricks = ctx._memo("renko", lambda: renko(b.c, a))
        out = []
        for k in range(2, len(bricks)):
            i, dirn, ext = bricks[k]
            if bricks[k - 1][1] == -dirn and bricks[k - 2][1] == -dirn:
                prev_close = b.c[bricks[k - 1][0]]
                wick = ext < prev_close if dirn > 0 else ext > prev_close   # ada "wick" sebelum berbalik
                if not wick or i + 1 >= len(b):
                    continue
                entry = b.c[i]
                sl = swing_sl(ctx, i, dirn, entry, p["sl_atr"])
                if np.isnan(sl):
                    continue
                tp = zone_tp(ctx, i, dirn, entry, sl, 1.5)
                if np.isnan(tp):
                    continue
                out.append(Order(self.id, sym, dirn, int(b.t_close[i]), "market", sl=sl, tp=tp, min_rr=1.5,
                                 entry_tf="D1"))
        return out
