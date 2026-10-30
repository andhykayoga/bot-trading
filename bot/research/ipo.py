"""Uji saham IPO (reports/RENCANA_IPO_BACKDOOR.md bagian A).

A1/A5: dapat jatah di harga IPO, jual di penutupan hari ke-1/ke-5.
B: beli di penutupan hari pertama yang tidak terkunci ARA, tahan 20/60/250 hari bursa, dibanding IHSG.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
IPO = ROOT / "data" / "ipo"
BELI, JUAL = 0.0015, 0.0025
MULAI, AKHIR = pd.Timestamp("2022-01-01"), pd.Timestamp("2025-10-29")
TAHAN = (20, 60, 250)
SUSPENSI = 126                       # ±6 bulan bursa tanpa transaksi di akhir masa tahan → nilai 0

# Papan pencatatan yang kosong di dataset, dari berita (Bisnis 23 Sep 2025; Katadata/Databoks 8–10 Jul 2025).
PAPAN_KOSONG = {"EMAS": "Pengembangan", "PSAT": "Utama", "BLOG": "Utama", "ASPR": "Pengembangan",
                "CDIA": "Pengembangan", "COIN": "Pengembangan", "CHEK": "Pengembangan", "MERI": "Pengembangan",
                "PMUI": "Pengembangan"}


def baca_daftar() -> pd.DataFrame:
    d = pd.read_csv(IPO / "e-IPO Data.csv")
    d = d[d["IPO Status"] == "Closed"]
    out = pd.DataFrame({
        "kode": d["Ticker Code"], "harga_ipo": d["Final Price (Rp)"], "saham": d["Number of shares offered"],
        "papan": d["Listing Board"], "listing": pd.to_datetime(d["Listing Date"], format="mixed"),
        "d1_dataset": d["Return D1"]})
    out["papan"] = out.papan.fillna(out.kode.map(PAPAN_KOSONG))
    out["dana_miliar"] = out.saham * out.harga_ipo / 1e9
    return out[out.listing >= "2021-01-01"].sort_values("listing").reset_index(drop=True)


def harga(kode: str) -> pd.DataFrame:
    return pd.read_parquet(IPO / "harga" / f"{kode}.parquet").set_index("t")


def faktor_split(split: pd.DataFrame, tanggal: pd.DatetimeIndex) -> np.ndarray:
    """Yahoo menyesuaikan harga lama dengan split sesudahnya. Faktor = hasil kali rasio split setelah tiap tanggal;
    harga mentah = harga Yahoo × faktor."""
    f = np.ones(len(tanggal))
    for t, rasio in zip(pd.to_datetime(split.tanggal), split.nilai):
        f[tanggal < t] *= rasio
    return f


def batas_ara(harga_mentah: float, papan: str) -> float:
    if papan == "Akselerasi":
        return 0.10
    return 0.35 if harga_mentah <= 200 else 0.25 if harga_mentah <= 5000 else 0.20


def hari_ara(c: np.ndarray, h: np.ndarray, sebelum: np.ndarray, mentah: np.ndarray, papan: str) -> np.ndarray:
    """Terkunci ARA: tutup = tertinggi dan naik ≥ batas ARA − 1,5 poin dari penutupan sebelumnya."""
    batas = np.array([batas_ara(m, papan) for m in mentah])
    return (c >= h * (1 - 1e-9)) & (c / sebelum - 1 >= batas - 0.015)


def satu(r: pd.Series, ihsg: pd.Series, aksi: pd.DataFrame) -> dict:
    p = harga(r.kode)
    p = p[p.index >= r.listing]
    split = aksi[(aksi.kode == r.kode) & (aksi.jenis == "splits")]
    f_harian = faktor_split(split, p.index)
    ipo_adj = r.harga_ipo / f_harian[0]
    c, h = p.c.to_numpy(), p.h.to_numpy()
    sebelum = np.r_[ipo_adj, c[:-1]]
    ara = hari_ara(c, h, sebelum, sebelum * f_harian, r.papan)
    out = {"kode": r.kode, "listing": r.listing, "papan": r.papan, "harga_ipo": r.harga_ipo,
           "dana_miliar": r.dana_miliar, "hari_pertama": p.index[0], "d1_yahoo": c[0] / ipo_adj - 1,
           "d1_dataset": r.d1_dataset, "ara_d1": bool(ara[0])}
    lengkap = p.index[0] == r.listing           # Yahoo kadang tidak punya hari listing (KRYA): A1/A5 tidak dihitung
    out["A1"] = c[0] / ipo_adj * (1 - JUAL) / (1 + BELI) - 1 if lengkap else np.nan
    out["A5"] = c[4] / ipo_adj * (1 - JUAL) / (1 + BELI) - 1 if lengkap and len(c) >= 5 else np.nan
    kal0 = ihsg.index[ihsg.index >= p.index[0]]
    out["B250_dari_ipo"] = nilai_akhir(p, ihsg, p.index[0], kal0[min(250, len(kal0) - 1)]) * c[0] / ipo_adj - 1
    i = int(np.argmax(~ara)) if (~ara).any() else len(c) - 1
    masuk = p.index[i]
    out.update(hari_ara_beruntun=i, masuk=masuk, harga_masuk_mentah=c[i] * f_harian[i])
    out.update(tahan(p, ihsg, masuk))
    return out


def nilai_akhir(p: pd.DataFrame, ihsg: pd.Series, masuk: pd.Timestamp, keluar: pd.Timestamp) -> float:
    """Kelipatan nilai (termasuk dividen, tanpa biaya) dari penutupan `masuk` sampai `keluar`; 0 kalau di akhir masa
    tahan saham tidak bertransaksi lebih dari SUSPENSI hari bursa (disuspensi/dihapus)."""
    s = p.adj[p.adj.index <= keluar]
    ada = p.v[(p.v.index <= keluar)] > 0
    terakhir = ada[ada].index.max()
    if ihsg.index[(ihsg.index > terakhir) & (ihsg.index <= keluar)].size > SUSPENSI:
        return 0.0
    return s.iloc[-1] / p.adj.loc[masuk]


def tahan(p: pd.DataFrame, ihsg: pd.Series, masuk: pd.Timestamp, hari: tuple[int, ...] = TAHAN) -> dict:
    kal = ihsg.index[ihsg.index >= masuk]
    out = {}
    for n in hari:
        keluar = kal[min(n, len(kal) - 1)]
        x = nilai_akhir(p, ihsg, masuk, keluar)
        out[f"B{n}"] = x * (1 - JUAL) / (1 + BELI) - 1
        out[f"B{n}_ihsg"] = ihsg.loc[keluar] / ihsg.loc[masuk] - 1
        out[f"B{n}_lebih"] = out[f"B{n}"] - out[f"B{n}_ihsg"]
        out[f"B{n}_penuh"] = kal.size > n
        out[f"B{n}_nol"] = x == 0
    return out


def hitung_semua() -> pd.DataFrame:
    daftar = baca_daftar()
    aksi = pd.read_csv(IPO / "harga" / "aksi_korporasi.csv")
    ihsg = harga("IHSG").c
    return pd.DataFrame([satu(r, ihsg, aksi) for r in daftar.itertuples()])


def kelompok(h: pd.DataFrame) -> dict[str, pd.DataFrame]:
    u = h[(h.listing >= MULAI) & (h.listing <= AKHIR)]
    return {"Semua IPO": u, "F1 Papan Utama": u[u.papan == "Utama"],
            "F2 Dana ≥ Rp500 miliar": u[u.dana_miliar >= 500], "F3 Harga IPO ≥ Rp200": u[u.harga_ipo >= 200]}


def ringkas(x: pd.Series) -> dict:
    x = x.dropna()
    return {"n": len(x), "rata": x.mean(), "median": x.median(), "positif": (x > 0).mean()}


def kohort(d: pd.DataFrame, kol: str) -> tuple[float, float]:
    a = d[d.listing.dt.year <= 2023][kol].median()
    b = d[d.listing.dt.year >= 2024][kol].median()
    return a, b


def lolos_a(d: pd.DataFrame, kol: str) -> dict:
    s, (a, b) = ringkas(d[kol]), kohort(d, kol)
    return {**s, "kohort_22_23": a, "kohort_24_25": b,
            "lolos": s["rata"] > 0 and s["median"] > 0 and s["positif"] >= 0.6 and a > 0 and b > 0}


def lolos_b(d: pd.DataFrame, n: int = 250) -> dict:
    kol = f"B{n}_lebih"
    s, (a, b) = ringkas(d[kol]), kohort(d, kol)
    return {**s, "hasil_median": d[f"B{n}"].median(), "hasil_rata": d[f"B{n}"].mean(),
            "kohort_22_23": a, "kohort_24_25": b, "nol": int(d[f"B{n}_nol"].sum()),
            "lolos": s["rata"] > 0 and s["median"] > 0 and s["positif"] >= 0.5 and a > 0 and b > 0}


def jatah_ilustrasi(d: pd.DataFrame, porsi_ramai: float = 0.05) -> float:
    """Rata-rata A1 tertimbang jatah: penuh di IPO yang tidak ARA hari pertama, `porsi_ramai` di IPO yang ARA."""
    w = np.where(d.ara_d1, porsi_ramai, 1.0)
    return float(np.average(d.A1, weights=w))
