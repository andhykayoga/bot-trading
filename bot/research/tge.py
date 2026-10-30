"""Uji aturan token baru / TGE (LIVE-02) — reports/RENCANA_ORDERFLOW_TGE.md bagian B.

Hari 0 = candle harian pertama token di Binance spot; harga listing = close hari 0 (porsi 30% dibeli di situ).
Keputusan di close hari t, eksekusi di open hari t+1. Uang yang belum terpakai tidak berbunga. Data token berhenti
di jeda > 7 hari pertama (delisting); posisi yang masih ada dinilai di close terakhir.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "tge"
VALUASI = ROOT / "bot" / "research" / "tge_valuasi.csv"
JENDELA = ("2023-01-01", "2025-06-30")
AKHIR = "2026-10-28"
BIAYA, BIAYA_BTC = 0.002, 0.0011
PORSI_AWAL = 0.3                  # sisanya (70%) untuk base
TURUN_BASE = 0.5                  # base: close ≤ 50% harga listing
DEKAT_LANTAI = 1.3                # base: close ≤ 1,3 × lantai
UMUR_LOW = 14                     # base: low terendah sejak listing berumur ≥ 14 hari
CUT = 0.833                       # cut loss: close < 0,833 × lantai ($1,25 ÷ $1,5 contoh mentor)
TARGET = 3.33                     # target: close ≥ 3,33 × lantai ($5 ÷ $1,5 contoh mentor)
BATAS_HARI = 730
TAHAN_PEMBANDING = 365


def _potong(d: pd.DataFrame) -> pd.DataFrame:
    putus = np.flatnonzero(d["t"].diff().dt.days.to_numpy() > 7)
    if len(putus):
        d = d.iloc[:putus[0]]
    d = d.set_index(d["t"].dt.normalize())[["o", "h", "l", "c"]]
    return d.loc[:AKHIR]


@lru_cache(maxsize=None)
def harga(coin: str) -> pd.DataFrame:
    return _potong(pd.read_parquet(DATA / "harian" / f"{coin}.parquet"))


@lru_cache(maxsize=None)
def btc() -> pd.Series:
    return pd.read_parquet(ROOT / "data" / "kripto_harian" / "BTC.parquet").pipe(_potong)["c"]


def simulasi(d: pd.DataFrame, lantai: float) -> dict:
    """Aturan mentor + pelengkap pada candle harian `d` (baris 0 = hari listing). Modal 1."""
    o, lo, c = d["o"].to_numpy(), d["l"].to_numpy(), d["c"].to_numpy()
    listing = c[0]
    akhir = min(len(d) - 1, BATAS_HARI)
    unit, kas = PORSI_AWAL * (1 - BIAYA) / listing, 1.0 - PORSI_AWAL
    i_low, base, keluar = 0, None, None
    for t in range(1, akhir):
        if lo[t] < lo[i_low]:
            i_low = t
        if c[t] < CUT * lantai:
            keluar = (t + 1, o[t + 1], "cut loss")
        elif c[t] >= TARGET * lantai:
            keluar = (t + 1, o[t + 1], "target")
        if keluar:
            break
        if base is None and c[t] <= TURUN_BASE * listing and c[t] <= DEKAT_LANTAI * lantai and t - i_low >= UMUR_LOW:
            base = (t + 1, o[t + 1])
            unit += kas * (1 - BIAYA) / o[t + 1]
            kas = 0.0
    if keluar is None:
        keluar = (akhir, c[akhir], "batas 730 hari" if akhir == BATAS_HARI else "data habis")
    i, px, alasan = keluar
    return {"hasil": kas + unit * px * (1 - BIAYA) - 1, "alasan": alasan, "hari_keluar": i,
            "tgl_keluar": d.index[i].date(), "harga_keluar": px,
            "tgl_base": d.index[base[0]].date() if base else None, "harga_base": base[1] if base else np.nan}


def tahan(d: pd.DataFrame, hari: int, biaya: float = BIAYA) -> float:
    c = d["c"].to_numpy()
    i = min(hari, len(c) - 1)
    return c[i] / c[0] * (1 - biaya) ** 2 - 1


def satu(row: pd.Series) -> dict:
    d = harga(row["coin"])
    lantai = row["valuasi_usd"] / row["supply"]
    r = simulasi(d, lantai)
    b = btc().loc[d.index[0]:]
    c = d["c"].iloc[:BATAS_HARI + 1]
    return {"coin": row["coin"], "status": row["status"], "listing": d.index[0].date(), "harga_listing": d["c"].iloc[0],
            "lantai": lantai, "listing_per_lantai": d["c"].iloc[0] / lantai, **r,
            "terendah_per_lantai": c.min() / lantai, "akhir_per_lantai": c.iloc[-1] / lantai,
            "tahan_365": tahan(d, TAHAN_PEMBANDING), "tahan_730": tahan(d, BATAS_HARI),
            "btc_365": tahan(b.to_frame("c"), TAHAN_PEMBANDING, BIAYA_BTC),
            "hari_data": len(d) - 1}


def ringkas(df: pd.DataFrame) -> dict:
    s = {"n": len(df), "rata": df["hasil"].mean(), "median": df["hasil"].median(),
         "positif": int((df["hasil"] > 0).sum()), "rata_tahan_365": df["tahan_365"].mean(),
         "median_tahan_365": df["tahan_365"].median(), "rata_btc_365": df["btc_365"].mean(),
         "rata_tahan_730": df["tahan_730"].mean(), "median_tahan_730": df["tahan_730"].median()}
    s["lolos"] = bool(s["n"] >= 20 and s["rata"] > 0 and s["median"] > 0 and s["rata"] > s["rata_tahan_365"])
    return s


def jalankan_semua() -> dict:
    val = pd.read_csv(VALUASI)
    lst = pd.read_csv(DATA / "listing_binance.csv", parse_dates=["listing"])
    di_jendela = lst[lst["listing"].between(*JENDELA)]
    tok = pd.DataFrame([satu(r) for _, r in val.iterrows()])
    cek = di_jendela.set_index("coin")["listing"].dt.date
    salah = [c for c, t in zip(tok["coin"], tok["listing"]) if cek.get(c) != t]
    if salah:
        raise ValueError(f"tanggal listing tidak cocok / di luar jendela: {salah}")
    hasil = {"token": tok, "semua": ringkas(tok), "ketat": ringkas(tok[tok["status"] == "ketat"]),
             "jumlah_listing_jendela": len(di_jendela)}
    print(tok[["coin", "listing_per_lantai", "alasan", "tgl_base", "hasil", "tahan_365"]].round(3).to_string())
    print("semua:", {k: round(v, 3) if isinstance(v, float) else v for k, v in hasil["semua"].items()})
    print("ketat:", {k: round(v, 3) if isinstance(v, float) else v for k, v in hasil["ketat"].items()})
    return hasil
