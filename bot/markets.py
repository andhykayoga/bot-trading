"""Definisi pasar dan instrumen.

Satu "pasar" = satu akun bot (G-16, Q-49): forex dan kripto punya saldo, batas
hari, dan batas risiko masing-masing.

- `forex`     : EURUSD, XAUUSD — instrumen bot (G-09).
- `forex_uji` : GBPUSD, USDJPY — hanya untuk menilai versi baru di data yang belum
                pernah disentuh (rencana cadangan); bukan instrumen trading bot.
- `forex_riset`: AUDUSD, USDCAD, USDCHF, NZDUSD — hanya untuk uji forex cepat (bukan instrumen bot).
- `crypto`    : BTC, ETH (spot Binance), pasar asal setup mentor saham–kripto.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Instrument:
    symbol: str                 # nama di bot, mis. "EURUSD"
    market: str                 # nama pasar (akun)
    source: str                 # "oanda" (Hugging Face bunqi/OANDA_*) atau "binance"
    source_name: str            # nama dataset OANDA atau simbol Binance
    base_ccy: str
    quote_ccy: str              # akun dalam USD; kalau kuotasi bukan USD, untung/rugi dikonversi
    min_units: float            # ukuran minimum order (G-01 butir 4)
    news_ccys: tuple[str, ...]  # mata uang berita yang diperhatikan (G-13)
    # Biaya (D-10 butir 6). Spread = max(spread_min, spread_pct × harga); untuk kripto
    # "spread" ini juga memuat komisi exchange (biaya per sisi = spread / 2).
    spread_min: float
    spread_pct: float
    swap_markup: float          # biaya admin swap per tahun (pecahan nilai posisi)
    swap: bool = True           # kripto spot: tidak ada swap
    news_events: tuple[str, ...] | None = None  # kalau diisi, hanya berita yang namanya memuat kata ini (G-13 kripto)

    def spread(self, price):
        """Spread dalam satuan harga; `price` boleh angka atau array."""
        return np.maximum(self.spread_min, self.spread_pct * np.asarray(price, dtype=float))

    def usd_per_quote(self, price: float) -> float:
        """Nilai 1 satuan harga dalam USD untuk 1 unit (USDJPY: 1 yen = 1/harga USD)."""
        if self.quote_ccy == "USD":
            return 1.0
        if self.base_ccy == "USD":
            return 1.0 / price
        raise ValueError(f"konversi {self.symbol} ke USD belum didukung")

    def notional_usd(self, units: float, price: float) -> float:
        return units * price * self.usd_per_quote(price)


@dataclass(frozen=True)
class Market:
    name: str
    instruments: tuple[str, ...]
    day_start_tz: str            # zona waktu batas hari (D-12)
    day_start_hour: int          # jam mulai hari di zona itu
    week_days: int               # jumlah hari dalam minggu trading (forex 5, kripto 7)
    data_start: str              # awal data backtest (G-17 bagian 1)
    long_only_live: bool = False  # kripto spot versi pertama: short tidak dieksekusi di live (G-16)
    leverage_cap: float = 10.0    # total nilai posisi terbuka / saldo (G-16)
    weekend_closed: bool = True   # forex: kutipan Jumat 17.00 – Minggu 17.00 New York dibuang


_CRYPTO_NEWS = ("FOMC", "Federal Funds Rate", "CPI", "Non-Farm", "Nonfarm")

INSTRUMENTS: dict[str, Instrument] = {
    # EURUSD: spread 1,4 pip (setara akun standar ritel, sudah termasuk komisi).
    "EURUSD": Instrument("EURUSD", "forex", "oanda", "OANDA_EURUSD_EURUSD", "EUR", "USD", 1000, ("USD", "EUR"),
                         spread_min=0.00014, spread_pct=0.0, swap_markup=0.01),
    # XAUUSD: spread minimal 0,30 USD, ikut melebar saat harga emas tinggi (0,015% harga).
    "XAUUSD": Instrument("XAUUSD", "forex", "oanda", "OANDA_XAUUSD_Gold", "XAU", "USD", 1, ("USD",),
                         spread_min=0.30, spread_pct=0.00015, swap_markup=0.025),
    # Pair uji (data belum pernah disentuh): spread ritel tipikal GBPUSD 1,8 pip, USDJPY 1,4 pip.
    "GBPUSD": Instrument("GBPUSD", "forex_uji", "oanda", "OANDA_GBPUSD_GBPUSD", "GBP", "USD", 1000, ("USD", "GBP"),
                         spread_min=0.00018, spread_pct=0.0, swap_markup=0.01),
    "USDJPY": Instrument("USDJPY", "forex_uji", "oanda", "OANDA_USDJPY_USDJPY", "USD", "JPY", 1000, ("USD", "JPY"),
                         spread_min=0.014, spread_pct=0.0, swap_markup=0.01),
    # Pair riset (uji forex cepat, reports/RENCANA_FOREX_CEPAT.md); spread ritel standar tipikal.
    "AUDUSD": Instrument("AUDUSD", "forex_riset", "oanda", "OANDA_AUDUSD_AUDUSD", "AUD", "USD", 1000, ("USD",),
                         spread_min=0.00016, spread_pct=0.0, swap_markup=0.01),
    "USDCAD": Instrument("USDCAD", "forex_riset", "oanda", "OANDA_USDCAD_USDCAD", "USD", "CAD", 1000, ("USD",),
                         spread_min=0.00020, spread_pct=0.0, swap_markup=0.01),
    "USDCHF": Instrument("USDCHF", "forex_riset", "oanda", "OANDA_USDCHF_USDCHF", "USD", "CHF", 1000, ("USD",),
                         spread_min=0.00018, spread_pct=0.0, swap_markup=0.01),
    "NZDUSD": Instrument("NZDUSD", "forex_riset", "oanda", "OANDA_NZDUSD_NZDUSD", "NZD", "USD", 1000, ("USD",),
                         spread_min=0.00020, spread_pct=0.0, swap_markup=0.01),
    # Kripto spot Binance: komisi 0,1% per sisi + setengah spread 0,01% → biaya pulang-pergi 0,22%.
    "BTCUSD": Instrument("BTCUSD", "crypto", "binance", "BTCUSDT", "BTC", "USD", 0.0001, ("USD",),
                         spread_min=0.0, spread_pct=0.0022, swap_markup=0.0, swap=False, news_events=_CRYPTO_NEWS),
    "ETHUSD": Instrument("ETHUSD", "crypto", "binance", "ETHUSDT", "ETH", "USD", 0.001, ("USD",),
                         spread_min=0.0, spread_pct=0.0022, swap_markup=0.0, swap=False, news_events=_CRYPTO_NEWS),
}

MARKETS: dict[str, Market] = {
    # Forex & emas: hari mulai 17.00 New York, minggu mulai Minggu 17.00 New York (D-12).
    "forex": Market("forex", ("EURUSD", "XAUUSD"), "America/New_York", 17, 5, "2010-01-01"),
    "forex_uji": Market("forex_uji", ("GBPUSD", "USDJPY"), "America/New_York", 17, 5, "2010-01-01"),
    "forex_riset": Market("forex_riset", ("AUDUSD", "USDCAD", "USDCHF", "NZDUSD"), "America/New_York", 17, 5,
                          "2014-01-01"),
    # Kripto: hari mulai 00.00 UTC, minggu mulai Senin; data sejak BTC & ETH sama-sama ada di Binance (Q-50).
    "crypto": Market("crypto", ("BTCUSD", "ETHUSD"), "UTC", 0, 7, "2017-09-01",
                     long_only_live=True, leverage_cap=1.0, weekend_closed=False),
}


def market_of(symbol: str) -> Market:
    return MARKETS[INSTRUMENTS[symbol].market]


def is_crypto(symbol: str) -> bool:
    return INSTRUMENTS[symbol].market == "crypto"
