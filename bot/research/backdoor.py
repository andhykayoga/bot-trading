"""Uji saham backdoor / ganti pengendali (reports/RENCANA_IPO_BACKDOOR.md bagian B).

Beli di penutupan hari bursa pertama setelah publik tahu siapa pengendali barunya, tahan 250 (dan 500) hari bursa,
dibanding IHSG. Daftar peristiwa di bot/research/backdoor_peristiwa.csv (dari berita, dibekukan sebelum harga diunduh).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from bot.research import ipo

ROOT = Path(__file__).resolve().parents[2]
PERISTIWA = ROOT / "bot" / "research" / "backdoor_peristiwa.csv"
HARGA = ROOT / "data" / "backdoor" / "harga"
MULAI, AKHIR = pd.Timestamp("2019-01-01"), pd.Timestamp("2025-10-29")


def baca_peristiwa() -> pd.DataFrame:
    d = pd.read_csv(PERISTIWA, parse_dates=["tanggal"])
    return d[(d.tanggal >= MULAI) & (d.tanggal <= AKHIR)].sort_values("tanggal").reset_index(drop=True)


def siap() -> bool:
    return PERISTIWA.exists() and (HARGA / "IHSG.parquet").exists()


def harga(kode: str) -> pd.DataFrame | None:
    f = HARGA / f"{kode}.parquet"
    return pd.read_parquet(f).set_index("t") if f.exists() else None


def satu(r, ihsg: pd.Series) -> dict:
    out = {"kode": r.kode, "tanggal": r.tanggal, "pengendali_baru": r.pengendali_baru, "kuat": bool(r.kuat)}
    p = harga(r.kode)
    if p is None or p.empty:
        return {**out, "ada_harga": False}
    setelah = p[(p.index > r.tanggal) & (p.v > 0)]             # disuspensi saat itu: tunggu transaksi pertama
    if setelah.empty:
        return {**out, "ada_harga": False}
    masuk = setelah.index[0]
    return {**out, "ada_harga": True, "masuk": masuk, "harga_masuk": setelah.c.iloc[0],
            **ipo.tahan(p, ihsg, masuk, (250, 500))}


def hitung_semua() -> pd.DataFrame:
    ihsg = harga("IHSG").c
    return pd.DataFrame([satu(r, ihsg) for r in baca_peristiwa().itertuples()])


def lolos(d: pd.DataFrame, n: int = 250) -> dict:
    kol = f"B{n}_lebih"
    x = d[kol].dropna()
    a = d[d.tanggal.dt.year <= 2021][kol].median()
    b = d[d.tanggal.dt.year >= 2022][kol].median()
    return {"n": len(x), "hasil_median": d[f"B{n}"].median(), "median": x.median(), "rata": x.mean(),
            "positif": (x > 0).mean(), "kohort_19_21": a, "kohort_22_25": b, "nol": int(d[f"B{n}_nol"].sum()),
            "lolos": x.mean() > 0 and x.median() > 0 and (x > 0).mean() >= 0.5 and a > 0 and b > 0}
