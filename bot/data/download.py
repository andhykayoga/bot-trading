"""Unduh data mentah ke folder data/ (tidak disimpan di git).

Sumber:
- Candle 5 menit OANDA (harga tengah + tick volume) dari dataset Hugging Face
  `bunqi/OANDA_*`, satu file parquet per bulan. Dukascopy menolak akses (429).
- Kripto: candle 5 menit spot Binance (volume asli exchange) dari data.binance.vision.
- Kalender ekonomi Forex Factory 2007-01 s.d. 2025-04 (dataset Hugging Face
  `Ehsanrs2/Forex_Factory_Calendar`).
- Jadwal rilis AS (BLS/BEA/Census/Fed) 2021-2028 (dataset `XOOMAR/us-economic-release-calendar`),
  untuk menutup periode setelah 2025-04.

- Data riset jangka panjang (Damodaran, Kenneth French, FRED) untuk rencana investasi.

Jalankan: python -m bot.data.download [forex forex_uji crypto riset]
"""
from __future__ import annotations

import io
import json
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from bot.markets import INSTRUMENTS, MARKETS

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
HF = "https://huggingface.co"


def _get(url: str, retries: int = 5) -> bytes:
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - jaringan: coba lagi dengan jeda
            if i == retries - 1:
                raise
            print(f"  gagal ({e}), coba lagi...", file=sys.stderr)
            time.sleep(2 ** (i + 1))
    raise RuntimeError("unreachable")


def list_files(dataset: str) -> list[str]:
    meta = json.loads(_get(f"{HF}/api/datasets/{dataset}"))
    return [s["rfilename"] for s in meta.get("siblings", [])]


def download_candles(symbol: str, first_year: int = 2009) -> None:
    inst = INSTRUMENTS[symbol]
    if inst.source == "binance":
        return download_binance(symbol)
    dataset = f"bunqi/{inst.source_name}"
    out = DATA / "raw" / symbol
    out.mkdir(parents=True, exist_ok=True)
    files = [f for f in list_files(dataset) if f.startswith("5/") and f.endswith(".parquet")]
    files = [f for f in files if int(f.split("_5_")[1][:4]) >= first_year]
    print(f"{symbol}: {len(files)} file bulanan")
    for f in sorted(files):
        name = f.split("/")[-1]
        dest = out / name
        # File bulan berjalan selalu diunduh ulang karena masih bertambah.
        if dest.exists() and f"_5_{time.strftime('%Y-%m')}" not in name:
            continue
        dest.write_bytes(_get(f"{HF}/datasets/{dataset}/resolve/main/{f}"))
        print("  ", name)


def download_calendars() -> None:
    out = DATA / "calendar"
    out.mkdir(parents=True, exist_ok=True)
    sources = {
        "forex_factory.csv": "Ehsanrs2/Forex_Factory_Calendar/resolve/main/forex_factory_cache.csv",
        "us_releases.csv": "XOOMAR/us-economic-release-calendar/resolve/main/us-economic-release-calendar.csv",
    }
    for name, path in sources.items():
        dest = out / name
        if not dest.exists():
            dest.write_bytes(_get(f"{HF}/datasets/{path}"))
            print("kalender:", name)


def _binance_zip_to_parquet(raw: bytes, dest: Path) -> None:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        df = pd.read_csv(z.open(z.namelist()[0]), header=None)
    if not str(df.iloc[0, 0]).isdigit():          # sebagian file punya baris judul
        df = df.iloc[1:]
    t = df[0].astype("int64")
    t = np.where(t > 10**14, t // 10**6, t // 10**3)   # sejak 2025 Binance memakai mikrodetik
    out = pd.DataFrame({"time": t, "open": df[1].astype(float), "high": df[2].astype(float),
                        "low": df[3].astype(float), "close": df[4].astype(float), "volume": df[5].astype(float)})
    out.to_parquet(dest)


def download_binance(symbol: str, first: str = "2017-08") -> None:
    pair = INSTRUMENTS[symbol].source_name
    out = DATA / "raw" / symbol
    out.mkdir(parents=True, exist_ok=True)
    base = "https://data.binance.vision/data/spot"
    today = pd.Timestamp.utcnow().normalize().tz_localize(None)
    months = pd.period_range(first, today.to_period("M") - 1, freq="M")
    for m in months:
        dest = out / f"{pair}-5m-{m}.parquet"
        if dest.exists():
            continue
        try:
            raw = _get(f"{base}/monthly/klines/{pair}/5m/{pair}-5m-{m}.zip", retries=2)
        except Exception:  # noqa: BLE001 - bulan sebelum pair terdaftar
            continue
        _binance_zip_to_parquet(raw, dest)
        print("  ", dest.name)
    # bulan berjalan: file harian sampai kemarin
    for d in pd.date_range(today.replace(day=1), today - pd.Timedelta(days=1)):
        dest = out / f"{pair}-5m-{d.date()}.parquet"
        if dest.exists():
            continue
        try:
            raw = _get(f"{base}/daily/klines/{pair}/5m/{pair}-5m-{d.date()}.zip", retries=2)
        except Exception:  # noqa: BLE001 - file hari terakhir mungkin belum terbit
            continue
        _binance_zip_to_parquet(raw, dest)
    print(f"{symbol}: selesai")


RISET = {
    # Return tahunan AS 1928–2025 (saham termasuk dividen, obligasi 10 th, T-bill, emas, inflasi)
    "histretSP.xls": "https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls",
    # Return harian pasar saham AS (termasuk dividen) dan bunga T-bill, sejak 1926
    "ff_daily.zip": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
                    "F-F_Research_Data_Factors_daily_CSV.zip",
    # Imbal hasil obligasi pemerintah AS 10 tahun, harian
    "dgs10.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10",
    # Kurs USD/IDR dan indeks harga konsumen Indonesia (OECD lewat FRED), bulanan
    "usdidr.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CCUSMA02IDM618N",
    "idcpi.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IDNCPIALLMINMEI",
}


def download_riset() -> None:
    """Data jangka panjang untuk rencana investasi (scripts/rencana_untung.py)."""
    out = DATA / "riset"
    out.mkdir(parents=True, exist_ok=True)
    for name, url in RISET.items():
        (out / name).write_bytes(_get(url))
        print(f"riset: {name}")


def main(markets: list[str] | None = None) -> None:
    if markets and "riset" in markets:
        download_riset()
        markets = [m for m in markets if m != "riset"]
        if not markets:
            return
    for name, market in MARKETS.items():
        if markets and name not in markets:
            continue
        for sym in market.instruments:
            download_candles(sym)
    download_calendars()


if __name__ == "__main__":
    main(sys.argv[1:] or None)
