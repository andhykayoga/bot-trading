"""Nilai jurnal sinyal (jurnal/sinyal.csv) dengan bahasa sederhana: berapa sinyal yang keluar dan yang diambil,
hasil setelah biaya, sinyal yang diambil dibanding semua sinyal, dan dibanding hasil uji (per transaksi, diukur
dengan cara yang sama: dari harga penutupan sinyal beli ke harga penutupan sinyal jual).

    python scripts/nilai_jurnal.py

Aturan sinyal tidak diubah berdasarkan hasil ini. Di bawah 30 transaksi selesai, hasilnya belum bisa disimpulkan.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot import jurnal  # noqa: E402
from bot.research import kripto_investasi as ki  # noqa: E402

CUKUP = 30                                  # transaksi selesai minimal sebelum boleh menyimpulkan
POSISI = ("TS10", "TS5", "MA200")


def transaksi(d: pd.DataFrame) -> pd.DataFrame:
    """Pasangkan BELI → JUAL per aturan dan koin. Transaksi dihitung diambil kalau sinyal BELI-nya diambil."""
    rows = []
    for (kode, aset), g in d[d.singkat.isin(POSISI)].groupby(["singkat", "aset"]):
        buka = None
        for r in g.sort_values("tanggal").itertuples():
            if r.aksi == "BELI":
                buka = r
            elif r.aksi == "JUAL" and buka is not None:
                fee = ki.biaya(aset)
                hasil = float(r.harga) / float(buka.harga) * (1 - fee) / (1 + fee) - 1
                rows.append({"aturan": kode, "aset": aset, "beli": buka.tanggal, "jual": r.tanggal, "hasil": hasil,
                             "diambil": buka.diambil == "ya"})
                buka = None
    return pd.DataFrame(rows, columns=["aturan", "aset", "beli", "jual", "hasil", "diambil"])


def uji(kode: str, aset: str) -> pd.Series:
    """Hasil per transaksi di data sejarah 2018–sekarang, diukur sama dengan jurnal (close ke close, setelah biaya)."""
    c = ki.harga(aset)["c"].loc[ki.MULAI:]
    if kode == "MA200":
        pos = (ki.harga(aset)["c"] > ki.harga(aset)["c"].rolling(200).mean()).loc[ki.MULAI:].astype(float)
    else:
        tinggi20 = ki.harga(aset)["c"].rolling(20).max().shift(1)
        pos = ki.trailing(c, tinggi20, 0.10 if kode == "TS10" else 0.05)[0]
    ubah = pos.diff().fillna(0)
    beli, jual = c[ubah > 0], c[ubah < 0]
    fee, out = ki.biaya(aset), []
    for t, px in beli.items():
        nanti = jual[jual.index > t]
        if len(nanti):
            out.append(nanti.iloc[0] / px * (1 - fee) / (1 + fee) - 1)
    return pd.Series(out, dtype=float)


def ipo_hari_pertama(d: pd.DataFrame) -> pd.DataFrame:
    """Hasil hari pertama IPO yang dipesan (harga IPO → penutupan hari pertama, setelah biaya), dari Yahoo."""
    rows = []
    for r in d[(d.singkat == "IPO") & (d.aksi == "PESAN")].itertuples():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{r.aset}.JK?range=1y&interval=1d"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            q = json.loads(urllib.request.urlopen(req, timeout=30).read())["chart"]["result"][0]
            tutup = [x for x in q["indicators"]["quote"][0]["close"] if x is not None]
            rows.append({"kode": r.aset, "hasil": tutup[0] / float(r.harga) * (1 - 0.0025) / (1 + 0.0015) - 1,
                         "diambil": r.diambil == "ya"})
        except Exception:  # noqa: BLE001 - belum listing atau data belum ada
            continue
    return pd.DataFrame(rows, columns=["kode", "hasil", "diambil"])


def p(x: float) -> str:
    return "–" if pd.isna(x) else f"{100 * x:+.1f}%".replace(".", ",")


def laporan() -> str:
    d = jurnal.baca()
    if d.empty:
        return ("Jurnal masih kosong: belum ada sinyal yang keluar sejak bot berjalan. Belum bisa disimpulkan.\n"
                "Saran: lanjutkan seperti biasa dengan porsi yang sama, jangan menambah modal, jangan mengubah aturan.")
    d["singkat"] = d.id.str.split("-").str[-1]
    out = [f"Sejak {d.tanggal.min()}: {len(d)} sinyal keluar, {int((d.diambil == 'ya').sum())} Anda ambil, "
           f"{int((d.diambil == 'tidak').sum())} Anda lewati, {int((d.diambil == '').sum())} belum dijawab.", ""]
    for nama, g in d.groupby("strategi"):
        out.append(f"- {nama} (skor {g.skor.iloc[0]}): {len(g)} sinyal, {int((g.diambil == 'ya').sum())} diambil")
    t = transaksi(d)
    out += ["", "Kripto (transaksi beli → jual yang sudah selesai, setelah biaya 0,11% per sisi):"]
    cukup = False
    for kode in POSISI:
        g = t[t.aturan == kode]
        if g.empty:
            out.append(f"- {jurnal_nama(kode)}: belum ada transaksi selesai.")
            continue
        sejarah = pd.concat([uji(kode, a) for a in g.aset.unique()])
        ambil = g[g.diambil]
        out.append(f"- {jurnal_nama(kode)}: {len(g)} transaksi, rata-rata {p(g.hasil.mean())}, "
                   f"{100 * (g.hasil > 0).mean():.0f}% untung. Yang Anda ambil: {len(ambil)} transaksi, rata-rata "
                   f"{p(ambil.hasil.mean())}. Di uji 2018–sekarang: rata-rata {p(sejarah.mean())} per transaksi, "
                   f"{100 * (sejarah > 0).mean():.0f}% untung.")
        cukup |= len(g) >= CUKUP
    ipo = ipo_hari_pertama(d)
    if len(ipo):
        out += ["", f"IPO yang dipesan: {len(ipo)}, hasil hari pertama rata-rata {p(ipo.hasil.mean())} (belum termasuk "
                    "jatah yang lebih kecil dari pesanan). Di uji: median +20,5%."]
    out += ["", "Kesimpulan:"]
    if not cukup:
        out += [f"Belum bisa disimpulkan: belum ada aturan dengan {CUKUP} transaksi selesai. Hasil beberapa minggu "
                "atau bulan masih sangat dipengaruhi kebetulan.",
                "Saran: lanjutkan dengan porsi yang sama, jangan menambah modal, dan jangan mengubah aturan."]
    else:
        out += ["Sudah ada aturan dengan cukup transaksi. Bandingkan rata-rata jurnal dengan rata-rata uji di atas: "
                "kalau jauh lebih buruk (lebih dari separuhnya), kurangi porsi; kalau rugi melewati turun terdalam di "
                "uji (38–61%), berhenti; kalau mirip atau lebih baik, lanjut. Tambah modal hanya kalau hasilnya mirip "
                "uji selama minimal setahun."]
    return "\n".join(out)


def jurnal_nama(kode: str) -> str:
    return {"TS10": "Trailing stop 10%", "TS5": "Trailing stop 5%", "MA200": "Rata-rata 200 hari"}[kode]


if __name__ == "__main__":
    np.seterr(all="ignore")
    print(laporan())
