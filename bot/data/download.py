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

- Candle harian multi-aset OANDA (folder D/), candle harian spot Binance untuk altcoin/meme
  (data-api.binance.vision), Fear & Greed Index (alternative.me).

- Candle 1 jam BTC/ETH dengan volume beli taker (order flow) dan data token baru Binance (TGE).

Jalankan: python -m bot.data.download [forex forex_uji forex_riset crypto riset harian kripto_harian orderflow tge]
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


MULTI_ASET = [
    "SPX500USD_US-SPX-500", "NAS100USD_US-Nas-100", "US2000USD_US-Russ-2000", "DE30EUR_Germany-30",
    "UK100GBP_UK-100", "FR40EUR_France-40", "EU50EUR_Europe-50", "JP225USD_Japan-225", "AU200AUD_Australia-200",
    "HK33HKD_Hong-Kong-33",
    "USB02YUSD_US-2Y-T-Note", "USB05YUSD_US-5Y-T-Note", "USB10YUSD_US-10Y-T-Note", "USB30YUSD_US-T-Bond",
    "DE10YBEUR_Bund", "UK10YBGBP_UK-10Y-Gilt",
    "XAUUSD_Gold", "XAGUSD_Silver", "XPTUSD_Platinum", "XCUUSD_Copper", "WTICOUSD_West-Texas-Oil",
    "BCOUSD_Brent-Crude-Oil", "NATGASUSD_Natural-Gas", "CORNUSD_Corn", "SOYBNUSD_Soybeans", "WHEATUSD_Wheat",
    "SUGARUSD_Sugar",
    "EURUSD_EURUSD", "GBPUSD_GBPUSD", "USDJPY_USDJPY", "AUDUSD_AUDUSD", "USDCAD_USDCAD", "USDCHF_USDCHF",
    "NZDUSD_NZDUSD",
]
ALTCOIN = ["ETH", "BNB", "XRP", "ADA", "SOL", "DOT", "LTC", "BCH", "EOS", "TRX", "XLM", "LINK", "ETC", "NEO", "IOTA",
           "VET", "ATOM", "AVAX", "MATIC", "FIL", "UNI", "NEAR", "ICP", "APT", "ARB", "OP", "SUI", "TON", "XMR", "ZEC",
           "DASH", "ALGO", "AAVE", "SAND", "MANA", "AXS", "LUNA", "FTT", "XTZ", "HBAR"]
MEME = ["DOGE", "SHIB", "PEPE", "FLOKI", "BONK", "WIF"]


def download_harian() -> None:
    """Candle harian OANDA untuk trend-following multi-aset (folder D/ dataset bunqi)."""
    out = DATA / "harian"
    out.mkdir(parents=True, exist_ok=True)
    for name in MULTI_ASET:
        dataset = f"bunqi/OANDA_{name}"
        parts = []
        for f in sorted(x for x in list_files(dataset) if x.startswith("D/") and x.endswith(".parquet")):
            parts.append(pd.read_parquet(io.BytesIO(_get(f"{HF}/datasets/{dataset}/resolve/main/{f}"))))
        df = pd.concat(parts).drop_duplicates("time").sort_values("time")
        df.to_parquet(out / f"{name.split('_')[0]}.parquet", index=False)
        print(f"harian: {name} {len(df)} hari")


BINANCE_API = "https://data-api.binance.vision/api/v3"


def _klines(symbol: str, interval: str = "1d", start: int = 0) -> pd.DataFrame | None:
    """Semua candle spot Binance sejak `start` (ms). Kolom t o h l c v qv n tbv (tbv = volume beli taker)."""
    step = {"1d": 86400_000, "1h": 3600_000}[interval]
    rows = []
    while True:
        chunk = json.loads(_get(f"{BINANCE_API}/klines?symbol={symbol}&interval={interval}&limit=1000"
                                f"&startTime={start}", retries=3))
        if not isinstance(chunk, list) or not chunk:
            break
        rows.extend(chunk)
        if len(chunk) < 1000:
            break
        start = chunk[-1][0] + step
    if not rows:
        return None
    df = pd.DataFrame([r[:10] for r in rows], columns=["t", "o", "h", "l", "c", "v", "t_close", "qv", "n", "tbv"])
    df = df.astype({c: float for c in ["o", "h", "l", "c", "v", "qv", "tbv"]})
    df["t"] = pd.to_datetime(df["t"], unit="ms")
    return df[["t", "o", "h", "l", "c", "v", "qv", "n", "tbv"]]


def download_kripto_harian() -> None:
    """Candle harian spot Binance (BTC, ETH, altcoin, meme) lewat data-api.binance.vision, plus Fear & Greed."""
    out = DATA / "kripto_harian"
    out.mkdir(parents=True, exist_ok=True)
    for coin in ["BTC", *ALTCOIN, *MEME]:
        df = _klines(f"{coin}USDT")
        if df is None:
            print(f"kripto: {coin} tidak ada")
            continue
        df[["t", "o", "h", "l", "c", "v", "qv"]].to_parquet(out / f"{coin}.parquet", index=False)
        print(f"kripto: {coin} {len(df)} hari sejak {df.t.iloc[0].date()}")
    fng = json.loads(_get("https://api.alternative.me/fng/?limit=0&format=json"))["data"]
    pd.DataFrame(fng).to_csv(DATA / "riset" / "fng.csv", index=False)
    print(f"fear & greed: {len(fng)} hari")


def download_orderflow() -> None:
    """Candle 1 jam BTCUSDT & ETHUSDT dengan volume beli taker, untuk uji order flow (AFS-22)."""
    out = DATA / "orderflow"
    out.mkdir(parents=True, exist_ok=True)
    for sym in ["BTCUSDT", "ETHUSDT"]:
        df = _klines(sym, "1h")
        df[["t", "o", "h", "l", "c", "v", "n", "tbv"]].to_parquet(out / f"{sym}_1h.parquet", index=False)
        print(f"orderflow: {sym} {len(df)} jam sejak {df.t.iloc[0]}")


def download_tge() -> None:
    """Tanggal listing semua pasangan USDT di Binance spot + candle harian token yang punya valuasi (LIVE-02)."""
    out = DATA / "tge"
    (out / "harian").mkdir(parents=True, exist_ok=True)
    info = json.loads(_get(f"{BINANCE_API}/exchangeInfo"))["symbols"]
    pairs = sorted(s["baseAsset"] for s in info if s["quoteAsset"] == "USDT" and s["symbol"].isascii())
    rows = []
    for coin in pairs:
        k = json.loads(_get(f"{BINANCE_API}/klines?symbol={coin}USDT&interval=1d&limit=1&startTime=0", retries=3))
        if k:
            rows.append((coin, pd.to_datetime(k[0][0], unit="ms").date(), float(k[0][1]), float(k[0][4])))
    pd.DataFrame(rows, columns=["coin", "listing", "open1", "close1"]).to_csv(out / "listing_binance.csv", index=False)
    print(f"tge: {len(rows)} pasangan USDT")
    valuasi = pd.read_csv(ROOT / "bot" / "research" / "tge_valuasi.csv")
    for coin in valuasi["coin"]:
        _klines(f"{coin}USDT").to_parquet(out / "harian" / f"{coin}.parquet", index=False)
    print(f"tge: candle harian {len(valuasi)} token")


def main(markets: list[str] | None = None) -> None:
    for nama, fungsi in [("riset", download_riset), ("harian", download_harian),
                         ("kripto_harian", download_kripto_harian), ("orderflow", download_orderflow),
                         ("tge", download_tge)]:
        if markets and nama in markets:
            fungsi()
            markets = [m for m in markets if m != nama]
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
