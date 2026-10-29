"""Definisi pasar dan instrumen.

Satu "pasar" = satu akun bot (G-16, Q-49): forex dan kripto punya saldo, batas
hari, dan batas risiko masing-masing. Tahap sekarang hanya forex yang aktif
(G-09). Kripto sudah didefinisikan supaya nanti tinggal mengisi data dan biaya.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Instrument:
    symbol: str                 # nama di bot, mis. "EURUSD"
    market: str                 # "forex" atau "crypto"
    oanda_dataset: str | None   # nama dataset candle OANDA di Hugging Face (sumber data forex)
    quote_ccy: str              # mata uang kuotasi; akun dalam USD
    base_ccy: str
    min_units: float            # ukuran minimum order (G-01 butir 4)
    news_ccys: tuple[str, ...]  # mata uang berita yang diperhatikan (G-13)
    # Biaya (D-10 butir 6). Spread = max(spread_min, spread_pct * harga).
    spread_min: float
    spread_pct: float
    swap_markup: float          # biaya admin swap per tahun (pecahan nilai posisi)

    def spread(self, price):
        """Spread dalam satuan harga; `price` boleh angka atau array."""
        return np.maximum(self.spread_min, self.spread_pct * np.asarray(price, dtype=float))


@dataclass(frozen=True)
class Market:
    name: str
    instruments: tuple[str, ...]
    day_start_tz: str            # zona waktu batas hari (D-12)
    day_start_hour: int          # jam mulai hari di zona itu
    week_start_weekday: int      # 0=Senin ... 6=Minggu, hari batas minggu di zona itu
    data_start: str              # awal data backtest (G-17 bagian 1)
    long_only_live: bool = False  # kripto spot versi pertama: short tidak dieksekusi di live (G-16)
    leverage_cap: float = 10.0    # total nilai posisi terbuka / saldo (G-16)
    active: bool = True


INSTRUMENTS: dict[str, Instrument] = {
    # EURUSD: spread 1,4 pip (setara akun standar ritel, sudah termasuk komisi).
    "EURUSD": Instrument("EURUSD", "forex", "OANDA_EURUSD_EURUSD", "USD", "EUR",
                         min_units=1000, news_ccys=("USD", "EUR"),
                         spread_min=0.00014, spread_pct=0.0, swap_markup=0.01),
    # XAUUSD: spread minimal 0,30 USD, ikut melebar saat harga emas tinggi (0,015% harga).
    "XAUUSD": Instrument("XAUUSD", "forex", "OANDA_XAUUSD_Gold", "USD", "XAU",
                         min_units=1, news_ccys=("USD",),
                         spread_min=0.30, spread_pct=0.00015, swap_markup=0.025),
    # Kripto (belum aktif, Q-50/Q-51): data dan biaya diisi saat kripto ditambahkan.
    "BTCUSD": Instrument("BTCUSD", "crypto", "OANDA_BTCUSD_Bitcoin", "USD", "BTC",
                         min_units=0.0001, news_ccys=("USD",),
                         spread_min=0.0, spread_pct=0.0005, swap_markup=0.0),
    "ETHUSD": Instrument("ETHUSD", "crypto", "OANDA_ETHUSD_Ether", "USD", "ETH",
                         min_units=0.001, news_ccys=("USD",),
                         spread_min=0.0, spread_pct=0.0005, swap_markup=0.0),
}

MARKETS: dict[str, Market] = {
    # Forex & emas: hari mulai 17.00 New York, minggu mulai Minggu 17.00 New York (D-12).
    "forex": Market("forex", ("EURUSD", "XAUUSD"), "America/New_York", 17, 6, "2010-01-01"),
    # Kripto: hari mulai 00.00 UTC, minggu mulai Senin (D-12). Belum aktif (G-09).
    "crypto": Market("crypto", ("BTCUSD", "ETHUSD"), "UTC", 0, 0, "2017-09-01",
                     long_only_live=True, leverage_cap=1.0, active=False),
}


def market_of(symbol: str) -> Market:
    return MARKETS[INSTRUMENTS[symbol].market]
