"""Membentuk candle semua timeframe dari data 5 menit, dengan batas hari D-12.

- Data mentah: candle M5 OANDA (harga tengah bid/ask, tick volume), waktu UTC.
- Forex: hari mulai 17.00 New York; H4 dimulai dari batas hari itu
  (17, 21, 01, 05, 09, 13 waktu New York); minggu mulai Minggu 17.00 New York.
- Setiap candle punya `t_open` dan `t_close` (UTC, nanodetik). Candle baru boleh
  dipakai setelah `t_close` (D-01, D-10: sinyal dari candle yang sudah close).
- Semua instrumen satu pasar dipasang di satu grid M5 bersama, supaya mesin
  backtest bisa menghitung equity akun gabungan (G-08, G-15).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from bot.markets import INSTRUMENTS, MARKETS, Market

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CACHE = DATA / "cache"

TF_MINUTES = {"M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440, "W1": 10080}
NS_MIN = 60 * 10**9


@dataclass
class Bars:
    """Candle satu timeframe, disimpan sebagai array numpy supaya cepat."""
    tf: str
    t_open: np.ndarray    # int64 ns UTC
    t_close: np.ndarray   # int64 ns UTC: waktu candle selesai
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    v: np.ndarray
    day: np.ndarray       # tanggal hari trading (int, hari sejak epoch) sesuai D-12

    def __len__(self) -> int:
        return len(self.c)

    def idx_at(self, t_ns) -> np.ndarray:
        """Indeks candle terakhir yang SUDAH close pada waktu t (−1 kalau belum ada)."""
        return np.searchsorted(self.t_close, t_ns, side="right") - 1


@dataclass
class InstrumentData:
    symbol: str
    bars: dict[str, Bars] = field(default_factory=dict)

    def __getitem__(self, tf: str) -> Bars:
        return self.bars[tf]


def load_m5_raw(symbol: str) -> pd.DataFrame:
    files = sorted((DATA / "raw" / symbol).glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"Data {symbol} belum diunduh. Jalankan: python -m bot.data.download")
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    df = df.drop_duplicates("time").sort_values("time").reset_index(drop=True)
    df["time"] = df["time"].astype("int64") * 10**9
    return df


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Buang candle yang jelas rusak: harga ≤ 0 atau open/close di luar high–low.
    Lonjakan saat berita (NFP, FOMC) tetap dipakai karena itu harga sungguhan."""
    px = df[["open", "high", "low", "close"]]
    ok = (px > 0).all(axis=1) & (df["high"] >= df[["open", "close"]].max(axis=1)) \
        & (df["low"] <= df[["open", "close"]].min(axis=1))
    return df[ok].reset_index(drop=True)


def _drop_weekend(df: pd.DataFrame, market: Market) -> pd.DataFrame:
    """Forex: buang kutipan akhir pekan (Jumat 17.00 – Minggu 17.00 New York), supaya
    minggu trading mulai Minggu 17.00 dan D1 berisi 5 candle hari kerja (D-12)."""
    if not market.weekend_closed:
        return df
    ny = pd.to_datetime(df["time"].to_numpy(), utc=True).tz_convert("America/New_York")
    wd, hr = ny.dayofweek.to_numpy(), ny.hour.to_numpy()
    weekend = ((wd == 4) & (hr >= 17)) | (wd == 5) | ((wd == 6) & (hr < 17))
    return df[~weekend].reset_index(drop=True)


def _trading_keys(t_ns: np.ndarray, market: Market) -> tuple[np.ndarray, np.ndarray]:
    """Kembalikan (waktu lokal yang digeser sehingga hari trading mulai 00:00, hari trading)."""
    ts = pd.to_datetime(t_ns, utc=True).tz_convert(market.day_start_tz).tz_localize(None)
    shifted = ts + pd.Timedelta(hours=24 - market.day_start_hour) if market.day_start_hour else ts
    shifted_ns = shifted.as_unit("ns").to_numpy().astype("int64")
    day = shifted_ns // (86400 * 10**9)
    return shifted_ns, day


def build_bars(m5: pd.DataFrame, market: Market) -> dict[str, Bars]:
    t = m5["time"].to_numpy()
    o, h, l, c = (m5[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    v = m5["volume"].to_numpy(float)
    shifted, day = _trading_keys(t, market)
    out: dict[str, Bars] = {}
    out["M5"] = Bars("M5", t, t + 5 * NS_MIN, o, h, l, c, v, day)
    offset = shifted - t  # selisih waktu lokal-geser terhadap UTC (berubah saat DST)
    for tf in ("M15", "H1", "H4", "D1", "W1"):
        mins = TF_MINUTES[tf]
        if tf == "W1":
            # Hari trading ke-0 epoch (1970-01-01) = Kamis. Minggu trading mulai Senin.
            key = (day + 3) // 7
            start_shifted = (key * 7 - 3) * 86400 * 10**9
        else:
            step = mins * NS_MIN
            key = shifted // step
            start_shifted = key * step
        # batas grup = perubahan key
        brk = np.flatnonzero(np.diff(key)) + 1
        starts = np.r_[0, brk]
        ends = np.r_[brk, len(key)] - 1
        t_open = start_shifted[starts] - offset[starts]
        dur = (market.week_days * 1440 if tf == "W1" else mins) * NS_MIN
        t_close = t_open + dur
        bo = o[starts]
        bc = c[ends]
        bh = np.maximum.reduceat(h, starts)
        bl = np.minimum.reduceat(l, starts)
        bv = np.add.reduceat(v, starts)
        out[tf] = Bars(tf, t_open, t_close, bo, bh, bl, bc, bv, day[starts])
    # Bulan (untuk PMH/PML, AFS-06 – 08): mulai hari trading pertama bulan kalender (D-12)
    d1 = out["D1"]
    ym = pd.to_datetime(d1.day * 86400 * 10**9).to_period("M").astype("int64").to_numpy()
    starts = np.r_[0, np.flatnonzero(np.diff(ym)) + 1]
    ends = np.r_[starts[1:], len(ym)] - 1
    out["MN"] = Bars("MN", d1.t_open[starts], d1.t_close[ends], d1.o[starts],
                     np.maximum.reduceat(d1.h, starts), np.minimum.reduceat(d1.l, starts), d1.c[ends],
                     np.add.reduceat(d1.v, starts), d1.day[starts])
    return out


@lru_cache(maxsize=None)
def load_instrument(symbol: str) -> InstrumentData:
    market = MARKETS[INSTRUMENTS[symbol].market]
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{symbol}_m5.parquet"
    raw_files = sorted((DATA / "raw" / symbol).glob("*.parquet"))
    if cache.exists() and raw_files and cache.stat().st_mtime > max(f.stat().st_mtime for f in raw_files):
        m5 = pd.read_parquet(cache)
    else:
        m5 = _drop_weekend(_clean(load_m5_raw(symbol)), market)
        start = pd.Timestamp(market.data_start, tz="UTC").value - 400 * 86400 * 10**9  # pemanasan indikator
        m5 = m5[m5["time"] >= start].reset_index(drop=True)
        m5.to_parquet(cache)
    return InstrumentData(symbol, build_bars(m5, market))


@dataclass
class Grid:
    """Grid M5 bersama untuk semua instrumen satu pasar (harga tengah, diisi maju)."""
    t: np.ndarray                     # int64 ns, waktu buka candle M5
    o: dict[str, np.ndarray]
    h: dict[str, np.ndarray]
    l: dict[str, np.ndarray]
    c: dict[str, np.ndarray]
    live: dict[str, np.ndarray]       # True kalau instrumen punya candle asli di slot ini
    day: np.ndarray                   # hari trading (D-12)
    week: np.ndarray                  # minggu trading (D-12)

    def index_at_or_after(self, t_ns) -> np.ndarray:
        return np.searchsorted(self.t, t_ns, side="left")


@lru_cache(maxsize=None)
def load_grid(market_name: str) -> Grid:
    market = MARKETS[market_name]
    datas = {s: load_instrument(s)["M5"] for s in market.instruments}
    t = np.unique(np.concatenate([b.t_open for b in datas.values()]))
    o, h, l, c, live = {}, {}, {}, {}, {}
    for s, b in datas.items():
        pos = np.searchsorted(t, b.t_open)
        cc = np.full(len(t), np.nan)
        cc[pos] = b.c
        # slot tanpa candle asli: harga diam di close sebelumnya (open=high=low=close)
        cc = pd.Series(cc).ffill().bfill().to_numpy()
        oo = cc.copy(); hh = cc.copy(); ll = cc.copy()
        oo[pos] = b.o; hh[pos] = b.h; ll[pos] = b.l
        lv = np.zeros(len(t), bool); lv[pos] = True
        o[s], h[s], l[s], c[s], live[s] = oo, hh, ll, cc, lv
    _, day = _trading_keys(t, market)
    week = (day + 3) // 7
    return Grid(t, o, h, l, c, live, day, week)


def ts(x) -> int:
    """Ubah tanggal/teks ke int64 ns UTC."""
    return pd.Timestamp(x, tz="UTC").value if not isinstance(x, (int, np.integer)) else int(x)
