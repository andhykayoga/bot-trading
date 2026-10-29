"""Ambil harga harian, dividen, dan stock split saham BEI dari Yahoo Finance.

Dijalankan di KOMPUTER ANDA (server bot tidak bisa mengakses Yahoo/IDX):

    pip install yfinance pandas
    python ambil_data_idx.py

Hasilnya file data_idx.zip di folder yang sama. Kirim file itu (lihat reports/PANDUAN_DATA_STOCKBIT.md).
Daftar saham = 45 konstituen LQ45 periode Agustus 2018 – Januari 2019 (daftar tetap sejak awal, termasuk saham
yang kemudian ambruk atau disuspensi, supaya hasil uji tidak bias "hanya pemenang"), plus IHSG.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd
import yfinance as yf

SAHAM = ["ADHI", "ADRO", "AKRA", "ANTM", "ASII", "BBCA", "BBNI", "BBRI", "BBTN", "BJBR", "BKSL", "BMRI", "BRPT",
         "BSDE", "ELSA", "EXCL", "GGRM", "HMSP", "ICBP", "INCO", "INDF", "INDY", "INKP", "INTP", "ITMG", "JSMR", "KLBF",
         "LPKR", "LPPF", "MEDC", "MNCN", "PGAS", "PTBA", "PTPP", "SCMA", "SMGR", "SRIL", "SSMS", "TLKM", "TPIA", "UNTR",
         "UNVR", "WIKA", "WSBP", "WSKT"]
OUT = Path("data_idx")


def ambil(yahoo: str, nama: str, gagal: list) -> None:
    try:
        h = yf.Ticker(yahoo).history(start="2014-01-01", auto_adjust=False, actions=True)
    except Exception as e:  # noqa: BLE001 - catat lalu lanjut ke saham berikutnya
        gagal.append(f"{nama}: {e}")
        return
    if h.empty:
        gagal.append(f"{nama}: data kosong")
        return
    h.index = pd.to_datetime(h.index).tz_localize(None).date
    h.index.name = "Date"
    h.to_csv(OUT / f"{nama}.csv")
    print(f"{nama}: {len(h)} hari, {h.index[0]} s.d. {h.index[-1]}")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    gagal: list[str] = []
    ambil("^JKSE", "IHSG", gagal)
    for kode in SAHAM:
        ambil(f"{kode}.JK", kode, gagal)
    (OUT / "gagal.txt").write_text("\n".join(gagal) or "semua berhasil")
    with zipfile.ZipFile("data_idx.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()):
            z.write(f, f.name)
    print("selesai: data_idx.zip")
    if gagal:
        print("gagal:", *gagal, sep="\n  ")


if __name__ == "__main__":
    main()
