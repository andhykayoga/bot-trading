"""Uji saham IPO dan backdoor (reports/RENCANA_IPO_BACKDOOR.md) dan tulis reports/LAPORAN_IPO_BACKDOOR.md.

    python -m bot.data.download ipo backdoor
    python scripts/run_ipo_backdoor.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import backdoor, ipo  # noqa: E402
from scripts.laporan_modul_baru import md_table, pc  # noqa: E402

OUT = ROOT / "reports" / "hasil_ipo_backdoor"
REPORT = ROOT / "reports" / "LAPORAN_IPO_BACKDOOR.md"


def p(x, nd=1):
    return pc(100 * x, nd)


def ya(b) -> str:
    return "✓" if b else "✗"


def tabel_a(g: dict) -> list[str]:
    rows = []
    for nama, d in g.items():
        for kol, label in [("A1", "jual hari ke-1"), ("A5", "jual hari ke-5")]:
            r = ipo.lolos_a(d, kol)
            rows.append([nama, label, str(r["n"]), p(r["rata"]), p(r["median"]), pc(100 * r["positif"], 0, False),
                         f"{p(r['kohort_22_23'])} / {p(r['kohort_24_25'])}", ya(r["lolos"])])
    return md_table(["Kelompok", "Jual", "IPO", "Rata-rata", "Median", "Untung", "Median 2022–23 / 2024–25",
                     "Lolos"], rows)


def tabel_b(g: dict) -> list[str]:
    rows = []
    for nama, d in g.items():
        r = ipo.lolos_b(d, 250)
        rows.append([nama, str(r["n"]), p(r["hasil_median"]), p(r["median"]), p(r["rata"]),
                     pc(100 * r["positif"], 0, False), f"{p(r['kohort_22_23'])} / {p(r['kohort_24_25'])}",
                     ya(r["lolos"])])
    return md_table(["Kelompok", "IPO", "Hasil median", "Median vs IHSG", "Rata-rata vs IHSG", "Kalahkan IHSG",
                     "Median vs IHSG 2022–23 / 2024–25", "Lolos"], rows)


def bagian_ipo(h: pd.DataFrame) -> list[str]:
    g = ipo.kelompok(h)
    u = g["Semua IPO"]
    a1, b = ipo.lolos_a(u, "A1"), ipo.lolos_b(u, 250)
    ara, sepi = u[u.ara_d1], u[~u.ara_d1]
    b20, b60 = ipo.lolos_b(u, 20), ipo.lolos_b(u, 60)
    dari_ipo = u.B250_dari_ipo
    top = u.sort_values("B250", ascending=False).head(5)
    t21 = h[h.listing < ipo.MULAI]
    return [
        "## A. Saham IPO",
        "",
        f"**Hasil singkat:** dapat jatah lalu jual di hari pertama **lolos** syarat (rata-rata {p(a1['rata'])}, median "
        f"{p(a1['median'])}, {pc(100 * a1['positif'], 0, False)} IPO untung). Membeli di pasar setelah listing lalu "
        f"menahan setahun **tidak lolos** (median {p(b['hasil_median'])}; hanya {pc(100 * b['positif'], 0, False)} "
        "yang mengalahkan IHSG). Persis seperti kata Ko Andri: IPO hanya untuk trading cepat, bukan untuk ditahan.",
        "",
        f"Data: {len(u)} IPO e-IPO yang listing 1 Januari 2022 – 29 Oktober 2025 (lengkap, termasuk yang ambruk), "
        "harga setelah listing dari Yahoo Finance. Biaya beli 0,15% dan jual 0,25% sudah dihitung.",
        "",
        "### Dapat jatah di harga IPO, lalu cepat dijual",
        "",
        *tabel_a(g),
        "",
        "### Beli di pasar setelah listing, tahan setahun (250 hari bursa)",
        "",
        "Dibeli di penutupan hari pertama yang tidak terkunci ARA (rata-rata hari ke-"
        f"{u.hari_ara_beruntun.mean() + 1:.1f}".replace(".", ",") + "). \"Vs IHSG\" = hasil saham dikurangi kenaikan IHSG di tanggal yang sama.",
        "",
        *tabel_b(g),
        "",
        f"Ditahan lebih pendek juga kalah: 20 hari bursa median {p(b20['hasil_median'])} "
        f"({pc(100 * b20['positif'], 0, False)} mengalahkan IHSG), 60 hari bursa median {p(b60['hasil_median'])} "
        f"({pc(100 * b60['positif'], 0, False)}).",
        "",
        "### Kenapa rata-rata dan median sangat berbeda",
        "",
        f"- Dari harga IPO, setahun kemudian: median {p(dari_ipo.median())}, rata-rata {p(dari_ipo.mean())}. "
        f"{pc(100 * (dari_ipo < 0).mean(), 0, False)} IPO sudah di bawah harga IPO, dan "
        f"{pc(100 * (dari_ipo < -0.5).mean(), 0, False)} turun lebih dari separuh.",
        f"- Rata-rata terangkat oleh segelintir saham: {', '.join(f'{r.kode} ({p(r.B250, 0)})' for r in top.itertuples())}"
        f". Sebanyak {(u.B250 > 1).sum()} dari {len(u)} IPO naik lebih dari 2 kali lipat dalam setahun setelah dibeli, "
        f"tetapi {(u.B250 < -0.5).sum()} turun lebih dari separuh. Mirip membeli lotre: yang menang besar ada, tetapi "
        "kebanyakan kalah, dan tidak ada ciri sebelum listing (papan, besar dana, harga IPO) yang bisa memilih "
        "pemenangnya dengan andal.",
        "",
        "### Masalah jatah (yang membuat hasil hari pertama terlihat lebih bagus dari kenyataan)",
        "",
        f"- {len(ara)} dari {len(u)} IPO ({pc(100 * len(ara) / len(u), 0, False)}) ARA di hari pertama, rata-rata "
        f"{p(ara.A1.mean())}. Justru IPO seperti ini yang kelebihan permintaan puluhan sampai ratusan kali, sehingga "
        "pemesan ritel hanya dapat beberapa lot (misalnya pesan 100 lot, dapat 0–1 lot).",
        f"- {len(sepi)} IPO lainnya rata-rata hanya {p(sepi.A1.mean())} (median {p(sepi.A1.median())}; "
        f"{pc(100 * (sepi.A1 > 0).mean(), 0, False)} untung, terburuk {p(sepi.A1.min(), 0)}). IPO yang sepi inilah yang "
        "biasanya memberi jatah penuh.",
        f"- Ilustrasi: kalau jatah penuh di IPO sepi tetapi hanya 5% dari pesanan di IPO yang ARA, rata-rata hasil per "
        f"rupiah yang benar-benar dibelikan turun dari {p(a1['rata'])} menjadi {p(ipo.jatah_ilustrasi(u.dropna(subset=['A1'])))}"
        f" (dengan jatah 1%: {p(ipo.jatah_ilustrasi(u.dropna(subset=['A1']), 0.01))}). Dana juga terkunci beberapa hari "
        "selama masa penawaran.",
        "",
        "### Pemeriksaan data",
        "",
        "- Daftar IPO cocok dengan jumlah IPO resmi BEI per tahun (2022: 59, 2023: 79, 2024: 41).",
        "- Cek silang: per 22 Desember 2023, 51 dari 79 IPO 2023 di bawah harga IPO menurut data ini, sama persis dengan "
        "Bisnis.com (\"51 saham baru membukukan kinerja negatif\"). Hasil setahun dari harga IPO juga mirip penelitian "
        "Economina (Mei 2026, 190 IPO 2022–2025: rata-rata +44%, median −22,5%).",
        "- Kolom \"Return D1\" di dataset salah untuk saham yang kemudian split (misalnya CUAN); yang dipakai harga "
        "Yahoo yang sudah dicocokkan dengan split. KRYA tidak punya harga hari listing di Yahoo, jadi tidak ikut A1/A5.",
        f"- IPO di periode utama yang disuspensi lebih dari 6 bulan pada akhir masa tahan setahun (dihitung 0): "
        f"{int(u.B250_nol.sum())}.",
        f"- Tambahan 2021 ({len(t21)} IPO, tidak menentukan): jual hari pertama median {p(t21.A1.median())}; beli setelah "
        f"listing dan tahan setahun median {p(t21.B250.median())}, hasilnya searah.",
        "",
    ]


def bagian_backdoor() -> list[str]:
    if not backdoor.siap():
        return ["## B. Saham backdoor (ganti pengendali)", "", "Daftar peristiwa sedang dikumpulkan.", ""]
    h = backdoor.hitung_semua()
    h.to_csv(OUT / "backdoor_per_peristiwa.csv", index=False)
    return backdoor.laporan(h)


def laporan(h: pd.DataFrame) -> None:
    lines = [
        "# Laporan: saham IPO dan saham backdoor",
        "",
        "Aturan dikunci lebih dulu di `reports/RENCANA_IPO_BACKDOOR.md` (di-commit sebelum harga diunduh).",
        "",
        *bagian_ipo(h),
        *bagian_backdoor(),
        "## Cara mengulang",
        "",
        "```bash",
        "python -m bot.data.download ipo backdoor",
        "python scripts/run_ipo_backdoor.py",
        "```",
    ]
    REPORT.write_text("\n".join(lines) + "\n")
    print("tulis", REPORT.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    h = ipo.hitung_semua()
    kol = ["kode", "listing", "papan", "harga_ipo", "dana_miliar", "d1_yahoo", "ara_d1", "A1", "A5",
           "hari_ara_beruntun", "masuk", "B20", "B60", "B250", "B250_ihsg", "B250_lebih", "B250_dari_ipo"]
    h[kol].round(4).to_csv(OUT / "ipo_per_saham.csv", index=False, date_format="%Y-%m-%d")
    laporan(h)
