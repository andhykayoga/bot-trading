"""Uji valuasi Ko Andri (reports/RENCANA_SAHAM_KO_ANDRI.md) dan tulis reports/LAPORAN_SAHAM_KO_ANDRI.md.

    python -m bot.data.download idx          # harga, dividen, split dari Yahoo
    python scripts/run_saham.py              # butuh data/saham/financials_45.xlsx (+ baris EPS & BVPS)
"""
from __future__ import annotations

import math
import pickle
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import saham as s  # noqa: E402
from scripts.laporan_modul_baru import md_table, num, pc  # noqa: E402

OUT = ROOT / "reports" / "hasil_saham"
REPORT = ROOT / "reports" / "LAPORAN_SAHAM_KO_ANDRI.md"
NAMA = ["Ko Andri (5 syarat)", "45 saham bobot sama", "IHSG (tanpa dividen)", "Deposito 4%", "Ko Andri (≥ 4 syarat)"]


def cek_data(fin: pd.DataFrame) -> list[str]:
    kurang = fin[(fin.tahun >= 2014) & (fin.eps.isna() | fin.bvps.isna())]
    if "saham_kr" in fin:                                      # BVPS × jumlah saham harus = ekuitas induk
        sel = (fin.bvps * fin.saham_kr / (fin.ekuitas - fin.nci) - 1).abs()
        beda = fin[(fin.tahun >= 2014) & (sel > 0.03)]
    else:
        beda = fin.iloc[:0]
    neraca = fin[(fin.tahun >= 2014) & ((fin.liabilitas + fin.ekuitas - fin.aset).abs() > 0.01 * fin.aset.abs())]
    out = [f"- Baris EPS/BVPS kosong (2014–2025): {len(kurang)} dari {len(fin[fin.tahun >= 2014])} saham-tahun"
           + (f" ({', '.join(sorted(kurang.kode.unique()))})" if len(kurang) else "") + ".",
           f"- BVPS × jumlah saham ≠ ekuitas milik induk (selisih > 3%): {len(beda)} saham-tahun"
           + (f" ({', '.join(sorted(beda.kode.unique()))})" if len(beda) else "") + ".",
           f"- Aset ≠ liabilitas + ekuitas (selisih > 1%): {len(neraca)} saham-tahun "
           f"({', '.join(sorted(neraca.kode.unique())) or '–'}); BJBR wajar karena dana syirkah temporer dicatat di "
           "antara liabilitas dan ekuitas."]
    return out


def tabel_ringkas(r: dict, tgl: list) -> list[str]:
    lbl = [f"{a.year}–{b.year}" if b.year > a.year else f"{a.year}" for a, b in
           zip(tgl, [*tgl[1:], s.AKHIR])]
    rows = []
    for n in NAMA:
        x = r[n]
        rows.append([n, pc(100 * x["cagr"]), pc(100 * x["dd"], 0), *[pc(100 * v, 0) for v in x["periode"]]])
    return md_table(["Strategi", "Per tahun", "Turun terdalam", *lbl[:len(r[NAMA[0]]["periode"])]], rows)


def tabel_pilihan(h: dict) -> list[str]:
    rows = []
    for t, m in h["metrik"].items():
        sel = m[m.skor == 5]
        if sel.empty:
            rows.append([str(t.date()), "– (deposito)", "", "", "", "", ""])
        for _, r in sel.iterrows():
            rows.append([str(t.date()), r.kode, r.sektor, num(r.pbv), num(r.per, 1), pc(100 * r.roe, 1, False),
                         num(r.der, 2)])
    return md_table(["Tanggal pilih", "Saham", "Sektor", "PBV", "PER", "ROE", "DER"], rows)


def laporan(h: dict, fin: pd.DataFrame) -> None:
    u, t = h["utama"], h["tambahan_2015_2019"]
    lu = u["lolos"]
    hasil = "**LOLOS**" if lu["lolos"] else "**TIDAK LOLOS**"
    ka, ew = u["ringkas"]["Ko Andri (5 syarat)"], u["ringkas"]["45 saham bobot sama"]
    lines = [
        "# Laporan: uji valuasi Ko Andri di 45 saham BEI",
        "",
        "Aturan dikunci lebih dulu di `reports/RENCANA_SAHAM_KO_ANDRI.md` (di-commit sebelum data laporan keuangan "
        "diterima). Data laporan keuangan dari ekspor Stockbit pengguna; harga, dividen, dan split dari Yahoo Finance.",
        "",
        "## Hasil",
        "",
        f"Periode utama April 2019 – Oktober 2026: {hasil}. Portofolio Ko Andri {pc(100 * ka['cagr'])} per tahun "
        f"(turun terdalam {pc(100 * ka['dd'], 0)}), dibanding 45 saham bobot sama {pc(100 * ew['cagr'])} per tahun "
        f"(turun terdalam {pc(100 * ew['dd'], 0)}). Menang di {lu['jumlah_menang']} dari {lu['jumlah_periode']} "
        "periode tahunan.",
        "",
        "Syarat lolos: (1) hasil per tahun lebih tinggi dari 45 saham bobot sama "
        f"{'✓' if lu['cagr'] else '✗'}; (2) menang di ≥ 5 dari 8 periode tahunan {'✓' if lu['menang'] else '✗'}; "
        f"(3) turun terdalam tidak lebih buruk dari pembanding + 10 poin {'✓' if lu['dd'] else '✗'}.",
        "",
        *tabel_ringkas(u["ringkas"], u["tanggal"]),
        "",
        "Hasil termasuk dividen dan setelah biaya (beli 0,15%, jual 0,25%), kecuali IHSG yang hanya indeks harga.",
        "",
        "## Saham yang terpilih tiap tahun (lolos kelima syarat)",
        "",
        *tabel_pilihan(u),
        "",
        "## Tambahan (tidak menentukan lolos): April 2015 – April 2019",
        "",
        "Periode ini memakai daftar saham yang baru ditetapkan Juli 2018, jadi ada bias pengetahuan masa depan.",
        "",
        *tabel_ringkas(t["ringkas"], t["tanggal"]),
        "",
        *tabel_pilihan(t),
        "",
        "## Pemeriksaan data",
        "",
        *cek_data(fin),
        "- Baris \"Laba Bersih Yang Dapat Diatribusikan\" di ekspor ternyata berisi laba total (termasuk kepentingan "
        "non-pengendali), sehingga laba dan nilai buku per saham diambil dari EPS dan BVPS Key Ratio Stockbit.",
        "- EPS/BVPS disesuaikan dengan stock split (Yahoo) dengan memeriksa jumlah saham tersirat (ekuitas induk ÷ BVPS).",
        "- SRIL dan WSKT: harga akhir April dari Stockbit, dividen dan tanggal suspensi dari berita "
        "(`bot/research/saham_manual.csv`). Di antara tanggal itu harganya dianggap tetap, jadi turun terdalam harian "
        "untuk dua saham ini tidak terlihat. SRIL bernilai 0 sejak suspensi 18 Mei 2021 (pailit), WSKT sejak 8 Mei 2023 "
        "(suspensi lebih dari 24 bulan).",
        "",
        "## Cara mengulang",
        "",
        "```bash",
        "python -m bot.data.download idx",
        "python scripts/run_saham.py",
        "```",
    ]
    REPORT.write_text("\n".join(lines) + "\n")
    print("tulis", REPORT.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fin = s.baca_keuangan()
    h = s.jalankan_semua(fin)
    (OUT / "hasil.pkl").write_bytes(pickle.dumps({k: {kk: vv for kk, vv in v.items() if kk != "kurva"}
                                                  for k, v in h.items()}))
    rows = [m.assign(tanggal=str(t.date())) for t, m in h["utama"]["metrik"].items()]
    pd.concat(rows).round(4).to_csv(s.SAHAM / "metrik_per_tahun.csv", index=False)   # turunan data Stockbit: tidak di git
    laporan(h, fin)
    if not all(math.isfinite(h["utama"]["ringkas"][n]["cagr"]) for n in NAMA):
        print("PERINGATAN: ada kurva yang tidak lengkap")
