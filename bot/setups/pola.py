"""Pola grafik yang ditunda di versi pertama (Q-23): AFS-11 harmonic dan AFS-23 pola klasik.

Titik pola = swing berselang-seling (D-01, fractal 2–2; swing berurutan yang sejenis diambil yang paling ekstrem).
Sinyal dihitung saat swing terakhir diakui (2 candle sesudahnya). SL = sl_atr × ATR di luar titik terakhir,
TP RR 1:2. Detail tiap pola dan bagian yang merupakan pilihan saya ada di reports/RENCANA_MODUL_BARU.md.
"""
from __future__ import annotations

import numpy as np

from bot.engine.orders import Order
from bot.setups.base import Ctx, Setup, TestPlan, trigger_ok

TOL = 0.05


def zigzag_events(ctx: Ctx):
    """Urutan swing berselang-seling, dibangun bertahap. Hasil: daftar (t_diakui, seq) dengan seq =
    daftar (indeks, harga, jenis: +1 high / −1 low) yang diketahui saat candle t_diakui close."""
    def build():
        b, sw = ctx.b, ctx.sw
        ev = []
        for i in np.flatnonzero(sw.sh | sw.sl):
            for jenis in ((1, -1) if sw.sh[i] and sw.sl[i] else ((1,) if sw.sh[i] else (-1,))):
                ev.append((int(i), jenis))
        seq, out = [], []
        for i, jenis in ev:
            harga = float(b.h[i] if jenis > 0 else b.l[i])
            if seq and seq[-1][2] == jenis:
                if (harga - seq[-1][1]) * jenis > 0:
                    seq[-1] = (i, harga, jenis)
                else:
                    continue
            else:
                seq.append((i, harga, jenis))
            out.append((i + 2, list(seq[-6:])))
        return out
    return ctx._memo("zigzag", build)


def _near(x: float, target: float) -> bool:
    return abs(x - target) <= TOL


def _within(x: float, lo: float, hi: float) -> bool:
    return lo <= x <= hi


class _Pola(Setup):
    mentor = "Alvesting (Akademi Crypto) — pola grafik, ditunda di versi pertama (Q-23)"
    label = "trading"
    entry_tf = "H4"
    defaults = {"tf": "H4", "sl_atr": 1.0}

    def plan(self):
        return TestPlan(tf=["H4", "D1"], tested={"sl_atr": [0.5, 1.0, 1.5]})

    def cocok(self, seq, ctx: Ctx, t: int):
        """Kembalikan arah (+1/−1) kalau pola terbentuk saat swing terakhir diakui di candle t, selain itu 0."""
        raise NotImplementedError

    def entry(self, seq, ctx: Ctx, t: int, arah: int) -> int | None:
        """Candle tempat masuk (default: candle t, saat titik terakhir diakui)."""
        return t

    def signals_for(self, sym, d, p):
        tf = p["tf"]
        ctx = Ctx.get(d, tf)
        b, a = ctx.b, ctx.atr
        out = []
        for t, seq in zigzag_events(ctx):
            if t >= len(b) or np.isnan(a[t]):
                continue
            arah = self.cocok(seq, ctx, t)
            if not arah:
                continue
            j = self.entry(seq, ctx, t, arah)
            if j is None or j >= len(b):
                continue
            titik = seq[-1][1]
            sl = titik - arah * p["sl_atr"] * a[j]
            if (b.c[j] - sl) * arah <= 0:
                continue
            out.append(Order(self.id, sym, arah, int(b.t_close[j]), "market", sl=float(sl), tp_rr=2.0, min_rr=2.0,
                             label="trading", entry_tf=tf))
        out.sort(key=lambda o: o.created)
        return out


# ---------------------------------------------------------------- AFS-11 harmonic

class _Harmonic(_Pola):
    category = "reversal"

    def rasio_ok(self, b_ret, ac, d_xa, bd) -> bool:
        raise NotImplementedError

    def cocok(self, seq, ctx, t):
        if len(seq) < 5:
            return 0
        (_, X, _), (_, A, _), (_, B, _), (_, C, _), (_, D, jd) = seq[-5:]
        s = -jd                                 # D swing low → pola bullish (long)
        xa = s * (A - X)
        if xa <= 0 or s * (A - B) <= 0 or s * (C - B) <= 0 or s * (C - D) <= 0:
            return 0
        b_ret, ac = s * (A - B) / xa, s * (C - B) / (s * (A - B))
        d_xa, bd = s * (A - D) / xa, s * (C - D) / (s * (C - B))
        if not self.rasio_ok(b_ret, ac, d_xa, bd):
            return 0
        # menunggu pemicu (mentor: "tunggu kepastian") di salah satu dari 2 candle sesudah D
        return s if (trigger_ok(ctx, t, s) or trigger_ok(ctx, t - 1, s)) else 0


class AFS11G(_Harmonic):
    id, name = "AFS-11G", "Harmonic Gartley"

    def rasio_ok(self, b_ret, ac, d_xa, bd):
        return _within(b_ret, 0.5, 0.618) and ac < 1 and _near(d_xa, 0.786)


class AFS11B(_Harmonic):
    id, name = "AFS-11B", "Harmonic Bat"

    def rasio_ok(self, b_ret, ac, d_xa, bd):
        return _within(b_ret, 0.5, 0.618) and ac < 1 and _within(d_xa, 0.85, 0.92)


class AFS11C(_Harmonic):
    id, name = "AFS-11C", "Harmonic Crab"

    def rasio_ok(self, b_ret, ac, d_xa, bd):
        return _within(b_ret, 0.5, 0.618) and ac < 1 and _near(d_xa, 1.618)


class AFS11F(_Harmonic):
    id, name = "AFS-11F", "Harmonic Butterfly"

    def rasio_ok(self, b_ret, ac, d_xa, bd):
        return _near(b_ret, 0.786) and _within(ac, 0.382, 0.886) and _within(bd, 1.618, 2.24) and _near(d_xa, 1.27)


# ---------------------------------------------------------------- AFS-23 pola klasik

class AFS23H(_Pola):
    id, name = "AFS-23H", "Head & shoulders (dan kebalikannya), tembus neckline"
    category = "both"

    def cocok(self, seq, ctx, t):
        if len(seq) < 5:
            return 0
        p1, p3, p5 = seq[-5][1], seq[-3], seq[-1]
        s = -p5[2]                              # bahu kanan high → short; low → long (inverse)
        kepala_ok = (p3[1] - p1) * -s > 0 and (p3[1] - p5[1]) * -s > 0
        if not kepala_ok or abs(p1 - p5[1]) > ctx.atr[t]:
            return 0
        return s

    def entry(self, seq, ctx, t, arah):
        b = ctx.b
        (i2, n2, _), (i4, n4, _), (_, p5, _) = seq[-4], seq[-2], seq[-1]
        for j in range(t, min(t + 20, len(b))):
            if (arah < 0 and b.h[j] > p5) or (arah > 0 and b.l[j] < p5):
                return None                     # bahu kanan tertembus dulu: pola batal
            neck = n2 + (n4 - n2) * (j - i2) / (i4 - i2)
            if (b.c[j] - neck) * arah > 0:
                return j
        return None


class AFS23T(_Pola):
    id, name = "AFS-23T", "Ascending/descending triangle, masuk sebelum breakout"
    category = "trend"

    def cocok(self, seq, ctx, t):
        if len(seq) < 4:
            return 0
        (_, x1, _), (_, y1, _), (_, x2, _), (_, y2, j) = seq[-4:]
        s = -j                                  # titik terakhir low → ascending (long)
        if abs(x1 - x2) > 0.5 * ctx.atr[t] or (y2 - y1) * s <= 0:
            return 0
        batas = max(x1, x2) if s > 0 else min(x1, x2)
        return s if (batas - ctx.b.c[t]) * s > 0 else 0


class AFS23W(_Pola):
    id, name = "AFS-23W", "Rising/falling wedge, 3 sentuhan"
    category = "reversal"

    def cocok(self, seq, ctx, t):
        if len(seq) < 5:
            return 0
        (i1, a1, j), (k1, b1, _), (i2, a2, _), (k2, b2, _), (i3, a3, _) = seq[-5:]
        s = -j                                  # sentuhan ke-3 di high → rising wedge → short
        if s < 0:   # rising wedge: high naik 3×, low naik, garis bawah lebih curam (menyempit)
            if not (a1 < a2 < a3 and b1 < b2):
                return 0
            sh, sl_ = (a3 - a1) / (i3 - i1), (b2 - b1) / (k2 - k1)
            return -1 if 0 < sh < sl_ else 0
        if not (a1 > a2 > a3 and b1 > b2):      # falling wedge: low turun 3×, high turun, low lebih landai
            return 0
        sl_, sh = (a3 - a1) / (i3 - i1), (b2 - b1) / (k2 - k1)
        return 1 if sh < sl_ < 0 else 0


class AFS23B(_Pola):
    id, name = "AFS-23B", "Broadening (megaphone), 3 sentuhan, masuk di sisi luar"
    category = "reversal"

    def cocok(self, seq, ctx, t):
        if len(seq) < 5:
            return 0
        (_, a1, j), (_, b1, _), (_, a2, _), (_, b2, _), (_, a3, _) = seq[-5:]
        s = -j                                  # sentuhan ke-3 di low → long; di high → short
        if s > 0:
            return 1 if a1 > a2 > a3 and b1 < b2 else 0
        return -1 if a1 < a2 < a3 and b1 > b2 else 0


ALL_POLA = [AFS11G, AFS11B, AFS11C, AFS11F, AFS23H, AFS23T, AFS23W, AFS23B]
