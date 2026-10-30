"""Order yang dihasilkan setup. Setup hanya menghasilkan order; mesin (backtest atau
nanti live) yang menerapkan aturan global, ukuran posisi, dan biaya."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

NEVER = np.iinfo(np.int64).max


@dataclass
class Order:
    setup: str
    symbol: str
    direction: int            # +1 long, −1 short
    created: int              # ns UTC: waktu candle sinyal close (order aktif mulai candle berikutnya)
    kind: str                 # "market" | "limit" | "stop"
    sl: float
    price: float = np.nan     # harga limit/stop
    tp: float = np.nan        # TP harga tetap; kalau NaN dipakai tp_rr
    tp_rr: float = np.nan     # TP = entry ± tp_rr × jarak entry–SL (dihitung dari harga isi sebenarnya)
    min_rr: float = 1.5       # RR minimum (G-03); dicek ulang dengan harga isi sebenarnya
    expiry: int = NEVER       # order limit/stop batal kalau belum terisi sampai waktu ini
    cancel_above: float = np.nan  # order menunggu batal kalau harga menyentuh level ini sebelum terisi
    cancel_below: float = np.nan
    label: str = "trading"    # "trading" | "scalping" (D-11)
    hold_hours: float = np.nan  # batas waktu scalping (default 3 jam dari Rules; pembanding 24 jam)
    entry_tf: str = "H1"      # timeframe entry (filter waktu hanya untuk H4 ke atas, Q-39)
    exit_times: np.ndarray | None = None  # waktu keluar paksa (mis. struktur patah HKI-01)
    tp2: float = np.nan       # target kedua untuk varian "50% di TP1, sisanya SL ke titik impas"
    partial: bool = False
    tags: dict = field(default_factory=dict)
