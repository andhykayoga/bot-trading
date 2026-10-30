"""Pembagian data 60/20/20 menurut tanggal, per pasar (G-17 bagian 1, Q-42, Q-50)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from bot.data.candles import load_grid
from bot.markets import MARKETS


@dataclass(frozen=True)
class Splits:
    start: int
    dev_end: int     # = awal data pemilihan
    sel_end: int     # = awal uji akhir
    end: int

    def seg(self, name: str) -> tuple[int, int]:
        return {"dev": (self.start, self.dev_end), "sel": (self.dev_end, self.sel_end),
                "final": (self.sel_end, self.end), "full": (self.start, self.end)}[name]

    def describe(self) -> dict:
        f = lambda x: str(pd.Timestamp(x, tz="UTC").tz_convert("Asia/Jakarta").strftime("%Y-%m-%d %H:%M WIB"))
        return {"penyusunan": (f(self.start), f(self.dev_end)), "pemilihan": (f(self.dev_end), f(self.sel_end)),
                "uji akhir": (f(self.sel_end), f(self.end))}


def market_splits(market: str = "forex") -> Splits:
    g = load_grid(market)
    m = MARKETS[market]
    # batas hari trading: indeks grid pertama tiap hari
    first = np.r_[0, np.flatnonzero(np.diff(g.day)) + 1]
    t_first = g.t[first]
    start_i = int(np.searchsorted(t_first, pd.Timestamp(m.data_start, tz="UTC").value))
    # hari terakhir yang lengkap = hari sebelum hari terakhir di data
    end_i = len(first) - 1
    start, end = int(t_first[start_i]), int(t_first[end_i])

    def cut(frac):
        x = start + frac * (end - start)
        return int(t_first[np.searchsorted(t_first, x)])
    return Splits(start, cut(0.6), cut(0.8), end)
