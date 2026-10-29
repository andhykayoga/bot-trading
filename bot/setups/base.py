"""Kerangka setup. Setiap setup = satu kelas di folder ini, bisa dinyalakan sendiri
lewat `config/setups.toml` (daftar `enabled`).

Setup hanya membaca candle yang sudah close dan menghasilkan daftar `Order`.
Aturan global, ukuran posisi, dan biaya diurus mesin (backtest sekarang, broker nanti).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from bot.data.candles import InstrumentData
from bot.engine.orders import Order
from bot import indicators as ind


@dataclass
class TestPlan:
    """Rencana uji G-17 untuk satu setup.

    tf:          pilihan timeframe yang setara, diuji paling dulu (Q-47).
    setara:      parameter yang pilihannya setara (tanpa default), diuji sesudah timeframe.
    tested:      parameter "uji dulu": daftar nilai, nilai default ada di `Setup.defaults`.
    comparisons: varian pembanding: daftar nilai, nilai pertama = default.
    """
    tf: list[str] = field(default_factory=list)
    setara: dict[str, list] = field(default_factory=dict)
    tested: dict[str, list] = field(default_factory=dict)
    comparisons: dict[str, list] = field(default_factory=dict)


class Setup:
    id: str = ""
    name: str = ""
    mentor: str = ""            # sumber, untuk laporan
    priority: int = 2           # 1 = setup forex (Pola N, Ichimoku Rafał); 2 = mentor saham–kripto
    category: str = "trend"     # "reversal" | "breakout" | "both" | "trend" (untuk filter waktu 07)
    label: str = "trading"
    entry_tf: str = "H1"
    uses_volume: bool = False   # punya aturan volume (diuji tick volume vs dimatikan, D-07)
    volume_only: bool = False   # seluruhnya bergantung volume: tidak dijalankan kalau volume dimatikan
    defaults: dict = {}

    def plan(self) -> TestPlan:
        return TestPlan()

    def params(self, **override) -> dict:
        p = dict(self.defaults)
        p.update(override)
        return p

    def entry_tf_of(self, p: dict) -> str:
        return p.get("tf", self.entry_tf)

    def category_of(self, p: dict) -> str:
        """Kelompok untuk filter waktu 07: pembalikan / breakout / keduanya / tren."""
        return self.category

    def signals(self, data: dict[str, InstrumentData], p: dict) -> list[Order]:
        orders: list[Order] = []
        if self.volume_only and p.get("volume") == "off":
            return orders
        for sym, d in data.items():
            orders.extend(self.signals_for(sym, d, p))
        return orders

    def signals_for(self, sym: str, d: InstrumentData, p: dict) -> list[Order]:
        raise NotImplementedError


# ---------------------------------------------------------------- bantuan bersama

class Ctx:
    """Indikator yang sering dipakai untuk satu instrumen & timeframe (dihitung sekali)."""

    _cache: dict = {}

    def __init__(self, d: InstrumentData, tf: str):
        self.d, self.tf = d, tf
        self.b = d[tf]

    @classmethod
    def get(cls, d: InstrumentData, tf: str) -> "Ctx":
        key = (d.symbol, tf)
        if key not in cls._cache:
            cls._cache[key] = cls(d, tf)
        return cls._cache[key]

    def _memo(self, name, fn):
        if not hasattr(self, "_m"):
            self._m = {}
        if name not in self._m:
            self._m[name] = fn()
        return self._m[name]

    @property
    def atr(self):
        b = self.b
        return self._memo("atr", lambda: ind.atr(b.h, b.l, b.c, 14))

    @property
    def sw(self) -> ind.SwingState:
        b = self.b
        return self._memo("sw", lambda: ind.SwingState(b.h, b.l, b.c))

    @property
    def stoch(self):
        b = self.b
        return self._memo("stoch", lambda: ind.stochastic(b.h, b.l, b.c, 5, 3, 3))

    @property
    def patterns(self):
        b = self.b
        return self._memo("pat", lambda: ind.candle_patterns(b.o, b.h, b.l, b.c))

    @property
    def ichi(self):
        b = self.b
        return self._memo("ichi", lambda: ind.ichimoku(b.h, b.l))

    @property
    def vol_high(self):
        b = self.b
        return self._memo("volhi", lambda: ind.volume_high(b.v, 20))

    def htf_index(self, htf: str) -> np.ndarray:
        """Untuk tiap candle di timeframe ini: indeks candle `htf` terakhir yang sudah
        close saat candle ini close (−1 kalau belum ada)."""
        return self._memo(f"htf_{htf}", lambda: self.d[htf].idx_at(self.b.t_close))


def swing_levels(ctx: Ctx, t: int, kind: str, lookback: int = 150) -> np.ndarray:
    """Harga semua swing high/low yang sudah diakui pada candle t (swing di j diakui di j+2),
    dalam `lookback` candle terakhir, urut dari yang terbaru."""
    sw = ctx.sw
    key = "_sh_idx" if kind == "high" else "_sl_idx"
    idx = ctx._memo(key, lambda: np.flatnonzero(sw.sh if kind == "high" else sw.sl))
    hi = np.searchsorted(idx, t - 2, side="right")
    lo = np.searchsorted(idx, t - lookback, side="left")
    sel = idx[lo:hi][::-1]
    arr = ctx.b.h if kind == "high" else ctx.b.l
    return arr[sel]


def swing_sl(ctx: Ctx, t: int, direction: int, entry: float, mult: float, lookback: int = 150) -> float:
    """SL G-02: swing low terakhir yang berada di bawah entry − mult × ATR (long); cerminan untuk short."""
    lv = swing_levels(ctx, t, "low" if direction > 0 else "high", lookback)
    lv = lv[lv < entry] if direction > 0 else lv[lv > entry]
    if len(lv) == 0 or np.isnan(ctx.atr[t]):
        return np.nan
    return float(lv[0] - mult * ctx.atr[t]) if direction > 0 else float(lv[0] + mult * ctx.atr[t])


def zone_tp(ctx: Ctx, t: int, direction: int, entry: float, sl: float, min_rr: float,
            lookback: int = 150) -> float:
    """TP di zona lawan terdekat (D-04, D-10 butir 5) yang RR-nya ≥ minimum (Q-08).
    Long: tepi bawah zona resistance (swing high − 0,5 ATR); short: tepi atas zona support."""
    a = ctx.atr[t]
    risk = (entry - sl) * direction
    if risk <= 0 or np.isnan(a):
        return np.nan
    lv = swing_levels(ctx, t, "high" if direction > 0 else "low", lookback)
    edges = lv - 0.5 * a if direction > 0 else lv + 0.5 * a
    ok = edges[(edges - entry) * direction >= min_rr * risk]
    if len(ok) == 0:
        return np.nan
    return float(ok.min() if direction > 0 else ok.max())


def pivots(ctx: Ctx, period: str) -> dict[str, np.ndarray]:
    """Pivot Points Standard tipe Traditional (TradingView) dari periode sebelumnya
    (`period` = "D1" harian atau "W1" mingguan), selaras dengan candle ctx (AFS-12)."""
    def build():
        pb = ctx.d[period]
        i = ctx.htf_index(period)
        ok = i >= 0
        j = np.clip(i, 0, None)
        H = np.where(ok, pb.h[j], np.nan)
        L = np.where(ok, pb.l[j], np.nan)
        C = np.where(ok, pb.c[j], np.nan)
        P = (H + L + C) / 3
        return {"P": P, "R1": 2 * P - L, "S1": 2 * P - H, "R2": P + (H - L), "S2": P - (H - L),
                "R3": H + 2 * (P - L), "S3": L - 2 * (H - P), "period": np.where(ok, i, -1)}
    return ctx._memo(f"piv_{period}", build)


def zone_hit(lo: float, hi: float, level: float, half: float) -> bool:
    """Range candle [lo, hi] menyentuh zona level ± half (D-04)."""
    return lo <= level + half and hi >= level - half


def trigger_ok(ctx: Ctx, i: int, direction: int) -> bool:
    """Pemicu AFS-01 syarat 4: candle pemicu D-06 atau Stochastic 5,3,3 silang di area jenuh."""
    bull, bear = ctx.patterns
    k, dd = ctx.stoch
    if i < 1 or np.isnan(k[i]) or np.isnan(k[i - 1]):
        return bool(bull[i]) if direction > 0 else bool(bear[i])
    if direction > 0:
        return bool(bull[i]) or (k[i - 1] <= dd[i - 1] and k[i] > dd[i] and k[i] < 20)
    return bool(bear[i]) or (k[i - 1] >= dd[i - 1] and k[i] < dd[i] and k[i] > 80)
