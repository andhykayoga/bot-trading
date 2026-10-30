"""Rencana supaya uang bertambah, dengan kalkulasi untung per minggu, bulan, dan tahun.

    python scripts/rencana_untung.py            # tulis reports/RENCANA_UNTUNG.md + grafik (angka contoh)
    python scripts/rencana_untung.py --layar    # hitung dengan angka di config/rencana.toml, tampil di layar
    python scripts/rencana_untung.py --layar --modal 25000000 --setoran 2000000 --porto agresif

Butuh data riset sekali saja: python -m bot.data.download riset
Model dan asumsinya dijelaskan di bot/research/investasi.py.
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import investasi as iv  # noqa: E402
from scripts.make_report import BLUE, GRID, INK, INK2, RED, SURF  # noqa: E402

REPORT = ROOT / "reports" / "RENCANA_UNTUNG.md"
GRAFIK = ROOT / "reports" / "grafik"
MINGGU_PER_TAHUN = 365.25 / 7
TAHUN_TABEL = [1, 2, 3, 5, 10, 15, 20]
TAHUN_RENTANG = [1, 3, 5, 10, 20]


def rp(x: float) -> str:
    s, a = ("-" if x < 0 else ""), abs(x)
    if a >= 1e9:
        return f"{s}Rp {a / 1e9:.2f} miliar".replace(".", ",")
    if a >= 1e6:
        return f"{s}Rp {a / 1e6:.1f} juta".replace(".", ",")
    if a >= 1e3:
        return f"{s}Rp {a / 1e3:.0f} ribu"
    return f"{s}Rp {a:.0f}"


def pc(x: float, nd: int = 1, plus: bool = False) -> str:
    return (f"{x:+.{nd}f}%" if plus else f"{x:.{nd}f}%").replace(".", ",")


def nominal(real: float) -> float:
    return (1 + real) * (1 + iv.INFLASI_ID) - 1


def kurs_teks(d: dict, periode: str) -> str:
    arah = "lebih lemah" if d["riil"] > 0 else "lebih kuat"
    return f"{periode} rupiah {pc(100 * abs(d['riil']))} per tahun {arah} dari perkiraan selisih inflasi"


def md_table(head: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    return out + ["| " + " | ".join(r) + " |" for r in rows]


# ---------------------------------------------------------------- perhitungan

class Model:
    def __init__(self):
        self.tahunan = iv.load_tahunan()
        self.r, self.geser = iv.riil(self.tahunan)
        self.port = {n: iv.return_portofolio(self.r, n) for n in iv.PORTOFOLIO}

    def skenario(self, nama: str, tahun: int = 10) -> dict:
        """Hasil per tahun (riil) di 10 tahun: 1-dari-10 terburuk, tengah, 1-dari-10 terbaik."""
        c = iv.cagr_jalur(iv.bootstrap(self.port[nama].values, tahun))
        p10, p50, p90 = np.percentile(c, [10, 50, 90])
        return {"buruk": p10, "tengah": p50, "bagus": p90}

    def tabel_tetap(self, real: float, modal: float, setoran: float, tahun_list=TAHUN_TABEL) -> list[dict]:
        th = max(tahun_list)
        sal = iv.proyeksi(np.full((1, th), real), modal, setoran)[0]
        out = []
        for t in tahun_list:
            akhir, awal = sal[12 * t], sal[12 * (t - 1)]
            untung_thn = akhir - awal - 12 * setoran
            disetor = iv.total_setoran(modal, setoran, 12 * t)
            out.append({"tahun": t, "disetor": disetor, "saldo": akhir, "untung": akhir - disetor,
                        "per_bulan": untung_thn / 12, "per_minggu": untung_thn / MINGGU_PER_TAHUN,
                        "daya_beli": akhir / (1 + iv.INFLASI_ID) ** t})
        return out

    def rentang(self, nama: str, modal: float, setoran: float, tahun_list=TAHUN_RENTANG) -> list[dict]:
        p = self.port[nama].values
        out = []
        for t in tahun_list:
            sal = iv.proyeksi(iv.bootstrap(p, t), modal, setoran)[:, -1]
            hist = iv.proyeksi(iv.jendela(p, t), modal, setoran)[:, -1]
            disetor = iv.total_setoran(modal, setoran, 12 * t)
            q = np.percentile(sal, [10, 50, 90])
            out.append({"tahun": t, "disetor": disetor, "buruk": q[0], "tengah": q[1], "bagus": q[2],
                        "rugi": 100 * (sal < disetor).mean(), "hist_min": hist.min(),
                        "hist_rugi": 100 * (hist < disetor).mean(), "hist_n": len(hist)})
        return out

    def jalur(self, nama: str, modal: float, setoran: float, tahun: int = 20) -> dict:
        sal = iv.proyeksi(iv.bootstrap(self.port[nama].values, tahun), modal, setoran)
        q = np.percentile(sal, [10, 50, 90], axis=0)
        disetor = modal + setoran * np.arange(12 * tahun + 1)
        return {"buruk": q[0], "tengah": q[1], "bagus": q[2], "disetor": disetor}


# ---------------------------------------------------------------- grafik

def grafik_proyeksi(j: dict, nama: str, out: Path) -> None:
    th = np.arange(len(j["tengah"])) / 12
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
    ax.fill_between(th, j["buruk"] / 1e6, j["bagus"] / 1e6, color=BLUE, alpha=0.15, lw=0)
    ax.plot(th, j["tengah"] / 1e6, color=BLUE, lw=2)
    ax.plot(th, j["disetor"] / 1e6, color=INK2, lw=1.2, ls="--")
    end = th[-1]
    for key, label, color in [("bagus", "1 dari 10 terbaik", INK2), ("tengah", "Tengah", INK),
                              ("buruk", "1 dari 10 terburuk", INK2), ("disetor", "Total uang disetor", INK2)]:
        ax.annotate(label, (end, j[key][-1] / 1e6), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8, color=color)
    ax.set_xlim(0, end * 1.22)
    ax.set_xlabel("Tahun", color=INK2, fontsize=9)
    ax.set_ylabel("Saldo (juta rupiah)", color=INK2, fontsize=9)
    ax.set_title(f"{iv.NAMA[nama]}: Rp 10 juta + Rp 1 juta/bulan (10.000 simulasi)",
                 color=INK, fontsize=11, loc="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def grafik_tahunan(p, nama: str, out: Path) -> None:
    v = 100 * ((1 + p) * (1 + iv.INFLASI_ID) - 1)
    turun = int((v < 0).sum())
    fig, ax = plt.subplots(figsize=(7.5, 3.4), dpi=150)
    ax.bar(v.index, v.values, color=[BLUE if x >= 0 else RED for x in v.values], width=0.75)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_title(f"{iv.NAMA[nama]}, hasil per tahun 1928–2025 (setara rupiah, setelah biaya): "
                 f"turun di {turun} dari {len(v)} tahun", color=INK, fontsize=9.5, loc="left")
    ax.set_ylabel("% per tahun", color=INK2, fontsize=9)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


# ---------------------------------------------------------------- tampilan layar

def layar(m: Model, cfg: dict) -> None:
    modal, setoran, nama = cfg["modal"], cfg["setoran_bulanan"], cfg["portofolio"]
    sk = m.skenario(nama)
    print(f"\n{iv.NAMA[nama]} — modal {rp(modal)}, setoran {rp(setoran)}/bulan")
    print(f"Hasil per tahun dalam rupiah (setelah biaya): 1-dari-10 terburuk {pc(100 * nominal(sk['buruk']))}, "
          f"tengah {pc(100 * nominal(sk['tengah']))}, 1-dari-10 terbaik {pc(100 * nominal(sk['bagus']))}\n")
    print("Skenario tengah:")
    rows = [[str(x["tahun"]), rp(x["disetor"]), rp(x["saldo"]), rp(x["untung"]), rp(x["per_bulan"]),
             rp(x["per_minggu"])] for x in m.tabel_tetap(sk["tengah"], modal, setoran)]
    print("\n".join(md_table(["Tahun ke", "Total disetor", "Saldo", "Total untung", "Untung/bulan (tahun itu)",
                              "Untung/minggu (tahun itu)"], rows)))
    print("\nRentang hasil (10.000 simulasi):")
    rows = [[str(x["tahun"]), rp(x["disetor"]), rp(x["buruk"]), rp(x["tengah"]), rp(x["bagus"]), pc(x["rugi"])]
            for x in m.rentang(nama, modal, setoran)]
    print("\n".join(md_table(["Tahun ke", "Total disetor", "1 dari 10 terburuk", "Tengah", "1 dari 10 terbaik",
                              "Peluang saldo < uang disetor"], rows)))


# ---------------------------------------------------------------- laporan

def laporan(m: Model, cfg: dict) -> None:
    modal, setoran = 10_000_000, 1_000_000
    GRAFIK.mkdir(parents=True, exist_ok=True)
    sk = {n: m.skenario(n) for n in iv.PORTOFOLIO}
    s = sk["seimbang"]
    tetap = m.tabel_tetap(s["tengah"], modal, setoran)
    rent = {n: m.rentang(n, modal, setoran) for n in iv.PORTOFOLIO}
    sekali = m.rentang("seimbang", 100_000_000, 0)
    t10 = {n: next(x for x in rent[n] if x["tahun"] == 10) for n in rent}
    r1 = rent["seimbang"][0]
    t10s = t10["seimbang"]
    tetap10 = next(x for x in tetap if x["tahun"] == 10)
    tetap1 = tetap[0]
    mg = {n: iv.statistik_mingguan(iv.mingguan(n)) for n in iv.PORTOFOLIO}
    akhir_mg = min(iv._french_daily().index[-1], iv.obligasi_harian().index[-1])
    dep = {k: iv.pelemahan_rupiah_riil(a, 2024) for k, a in [("2000", 2000), ("2010", 2010)]}
    geo = {c: 100 * iv.geo(m.r[c]) for c in ["saham", "obligasi", "emas"]}
    us_saham = 100 * iv.geo((1 + m.tahunan["saham"]) / (1 + m.tahunan["inflasi"]) - 1)

    grafik_proyeksi(m.jalur("seimbang", modal, setoran), "seimbang", GRAFIK / "untung_proyeksi.png")
    grafik_tahunan(m.port["seimbang"], "seimbang", GRAFIK / "untung_tahunan.png")

    def thn_terburuk(n):
        p = m.port[n]
        return f"{pc(100 * nominal(p.min()), plus=True)} ({p.idxmin()})"

    nom = {n: {k: 100 * nominal(v) for k, v in sk[n].items()} for n in sk}
    ns = nom["seimbang"]
    L = []
    L += ["# Rencana Supaya Uang Bertambah", "",
          "Pertanyaan Anda: *\"intinya untung, keuangan saya bertambah; pakai compounding atau apa pun, tentukan "
          "sendiri sesuai riset terbaik, yang penting ada kalkulasi total untung per minggu/bulan.\"*", "",
          "Dokumen ini menjawabnya dengan data. Angka dihitung ulang oleh `scripts/rencana_untung.py`; "
          "Anda bisa memasukkan modal dan setoran sendiri (bagian 6).", "",
          "## Jawaban singkat", "",
          "1. **Jangan mengejar untung lewat trading aktif atau memperbesar lot (\"compounding\" di trading).** "
          "Semua setup mentor yang kita uji tidak untung setelah biaya di data yang belum pernah dipakai, dan riset "
          "besar menunjukkan mayoritas trader ritel rugi. Compounding hanya melipatgandakan hasil rata-rata: kalau "
          "rata-ratanya rugi, compounding justru mempercepat rugi.",
          "2. **Yang terbukti menambah uang dalam jangka panjang:** memiliki aset produktif (saham lewat reksa dana "
          "indeks/ETF), obligasi negara, dan sedikit emas, dengan biaya murah, **setor rutin tiap bulan, semua hasil "
          "diputar ulang** (inilah compounding yang benar), rebalance setahun sekali, dan ditahan minimal 10 tahun.",
          "3. **Pilihan saya untuk Anda: portofolio Seimbang 50/40/10** — 50% saham (separuh indeks Indonesia, "
          "separuh indeks global), 40% SBN ritel, 10% emas.",
          f"4. **Hasil yang wajar:** sekitar **{pc(ns['tengah'])} per tahun dalam rupiah** setelah biaya "
          f"(±{pc(100 * s['tengah'])} di atas inflasi). Dalam 10 tahun, 8 dari 10 simulasi berada di antara "
          f"{pc(ns['buruk'])} dan {pc(ns['bagus'])} per tahun. Bukan 20% per tahun, dan tidak untung setiap tahun.",
          f"5. **Contoh Rp 10 juta + Rp 1 juta/bulan:** setelah 10 tahun Anda sudah menyetor "
          f"{rp(tetap10['disetor'])}; skenario tengah saldonya **{rp(tetap10['saldo'])}** "
          f"(untung {rp(tetap10['untung'])}). Peluang saldo di bawah uang yang disetor: **{pc(r1['rugi'], 0)} "
          f"setelah 1 tahun, tetapi hanya {pc(t10s['rugi'])} setelah 10 tahun.**", "",
          "Ini bukan jaminan. Ini perkiraan terbaik dari data 98 tahun, dengan asumsi yang sengaja dibuat hati-hati.",
          ""]

    L += ["## 1. Kenapa bukan trading + compounding", "",
          "**Hasil uji kita sendiri.** Di [laporan backtest forex](LAPORAN_BACKTEST_FOREX.md) dan "
          "[laporan rencana cadangan](LAPORAN_RENCANA_CADANGAN.md), tidak ada setup mentor (Pola N, Ichimoku, "
          "Alvesting, Wyckoff, Ko Hengki) maupun versi perbaikannya yang lolos di data uji. Perkiraan terbaiknya "
          "sekitar impas sampai rugi setelah spread. Patokan riset (time-series momentum) hanya ±0% per tahun di "
          "forex dan +7% per tahun di kripto long saja, tetapi rugi -7,1% di periode uji akhir kripto.", "",
          "**Riset besar tentang trader ritel:**", "",
          "- Taiwan, seluruh day trader 1992–2006: kurang dari 1% yang bisa untung secara konsisten setelah biaya "
          "(Barber, Lee, Liu & Odean, 2014).",
          "- Brasil, semua orang yang day trading futures indeks ≥ 300 hari: 97% rugi, dan hanya 1,1% yang "
          "menghasilkan lebih dari upah minimum (Chague, De-Losso & Giovannetti, 2020).",
          "- Eropa: 74–89% akun ritel CFD/forex rugi (ESMA, 2018 — karena itu broker wajib menampilkan angka ini).", "",
          "**Hitungan sederhananya:**", "",
          "- Compounding = untung diputar lagi. Kalau rata-rata per transaksi negatif, memutar ulang membuat saldo "
          "turun lebih cepat, bukan naik.",
          "- Rumus Kelly (ukuran taruhan terbaik secara matematis) memberi jawaban **0** kalau tidak ada keunggulan.",
          "- Naik-turun besar menggerus hasil: +50% lalu -50% bukan impas, tetapi -25%. Leverage memperbesar efek ini.",
          "", "Jadi compounding tetap dipakai, tetapi pada sesuatu yang rata-ratanya memang naik.", ""]

    L += ["## 2. Apa yang terbukti menambah uang", "",
          "- **Pemilik usaha mendapat bagian keuntungan.** Saham dunia 1900–2024 memberi rata-rata **5,2% per tahun "
          "di atas inflasi**, obligasi 1,7%, dan simpanan jangka pendek 0,5% (Dimson, Marsh & Staunton, UBS Global "
          "Investment Returns Yearbook 2025). Tidak setiap tahun naik, tetapi dalam jangka panjang konsisten.",
          "- **Biaya murah menang.** Sekitar 9 dari 10 reksa dana aktif kalah dari indeksnya dalam 15 tahun "
          "(laporan SPIVA, S&P Dow Jones Indices). Alasannya sederhana: rata-rata semua pemain = pasar, dikurangi "
          "biaya (Sharpe, 1991). Pilih reksa dana indeks/ETF berbiaya rendah.",
          "- **Diversifikasi + rebalance.** Saham, obligasi, dan emas jarang jatuh bersamaan; mengembalikan bobot "
          "setahun sekali otomatis \"jual yang sudah mahal, beli yang sedang murah\".",
          "- **Perilaku lebih penting dari pilihan produk.** Investor rata-rata mendapat ±1% per tahun lebih sedikit "
          "dari reksa dananya sendiri karena masuk-keluar di waktu yang salah (Morningstar, *Mind the Gap*). "
          "Setoran otomatis dan tidak menjual saat turun menutup celah ini.",
          "- **Setor secepatnya.** Uang sekaligus yang langsung diinvestasikan mengalahkan dicicil di ±2 dari 3 "
          "periode sejarah (Vanguard, 2012). Untuk gaji bulanan, artinya: investasikan setiap kali gajian.",
          "- **Hasil diputar ulang.** Dividen dan kupon yang diinvestasikan kembali adalah sebagian besar dari hasil "
          "jangka panjang saham. Jangan ditarik tiap bulan.", ""]

    L += ["## 3. Rencana yang saya pilih", "",
          "Urutan ini penting; langkah 1–2 adalah \"untung pasti\" yang sering dilewatkan.", "",
          "1. **Dana darurat 3–6 bulan pengeluaran** di reksa dana pasar uang (RDPU) atau tabungan. Bukan untuk "
          "investasi, supaya Anda tidak terpaksa menjual saat pasar turun.",
          "2. **Lunasi utang berbunga tinggi dulu** (kartu kredit, paylater, pinjol: 20–100%+ per tahun). Melunasi "
          "utang 25% sama dengan untung pasti 25% per tahun — tidak ada investasi yang bisa menyamainya.",
          "3. **Setiap gajian, setor otomatis** ke portofolio **Seimbang 50/40/10**:",
          "   - 25% reksa dana indeks/ETF saham Indonesia (IHSG, LQ45, atau IDX30)",
          "   - 25% reksa dana indeks/ETF saham global (S&P 500 atau MSCI World)",
          "   - 40% SBN ritel (ORI/SR berkupon tetap, atau SBR/ST). SBN hanya dijual beberapa kali setahun: "
          "tampung dulu bagian ini di RDPU, lalu beli SBN di masa penawaran berikutnya (menurut jadwal sementara "
          "2026: ST017, 6 November – 2 Desember 2026).",
          "   - 10% emas (Antam/Pegadaian/bank), disimpan lama karena selisih jual-belinya 3–8%.",
          "4. **Semua kupon, dividen, dan bunga diputar ulang** ke portofolio yang sama.",
          "5. **Setahun sekali rebalance** ke 50/40/10. Cara paling murah: arahkan setoran baru ke bagian yang "
          "kurang, tanpa menjual.",
          "6. **Jangan lihat saldo tiap hari dan jangan menjual saat turun.** Dalam setahun, peluang saldo di bawah "
          f"uang yang disetor sekitar {pc(r1['rugi'], 0)}; itu normal, bukan tanda rencananya gagal.", "",
          "**Kapan memilih yang lain:**", "",
          "- Uangnya dibutuhkan dalam < 3 tahun (DP rumah, biaya nikah, sekolah): jangan masuk saham. Pakai "
          "deposito, RDPU, atau SBN yang jatuh temponya sebelum tanggal itu.",
          "- Jangka > 15 tahun dan Anda sanggup melihat saldo turun 30% tanpa menjual: Agresif 80/10/10 memberi "
          "hasil tengah lebih tinggi, tetapi peluang rugi setelah 10 tahun juga lebih besar (tabel di bagian 4).",
          "- **Bot/trading: 0% dari uang inti.** Kalau tetap ingin belajar, batasi maksimal 5% sebagai \"uang "
          "belajar\" yang siap hilang, pakai mode semi-otomatis `scripts/sinyal.py` dan catat jurnalnya.", "",
          "**Kenapa 50/40/10, bukan yang lain?** Bobot ini dipilih sebelum simulasi dijalankan (angka bulat standar, "
          f"bukan hasil optimasi). Hasilnya: dari tiga profil, Seimbang punya peluang rugi terkecil setelah 10 tahun "
          f"({pc(t10['seimbang']['rugi'])}, dibanding {pc(t10['hati_hati']['rugi'])} Hati-hati dan "
          f"{pc(t10['agresif']['rugi'])} Agresif) dengan hasil tengah yang tetap layak — cocok dengan prioritas Anda: "
          "*yang penting untung*.", ""]

    # ---- kalkulasi
    L += ["## 4. Kalkulasi untung", "",
          "### Asumsi (dikunci sebelum menghitung)", "",
          "| Asumsi | Nilai | Alasan |", "|---|---|---|",
          "| Data | Return tahunan AS 1928–2025 (98 tahun): saham termasuk dividen, obligasi pemerintah 10 tahun, emas, "
          "inflasi | Data publik terpanjang yang lengkap (Damodaran, NYU Stern) |",
          f"| Saham | Diturunkan {pc(-100 * m.geser, 2)} per tahun: dari {pc(us_saham, 2)} (AS) menjadi "
          f"{pc(geo['saham'], 2)} di atas inflasi | AS pasar paling beruntung; disamakan dengan rata-rata saham "
          "dunia 1900–2024 |",
          f"| Obligasi, emas | {pc(geo['obligasi'], 2)} dan {pc(geo['emas'], 2)} per tahun di atas inflasi "
          "(rata-rata sejarah) | Apa adanya. Kupon SBN sekarang (6,9–7%) lebih tinggi, jadi bagian obligasi "
          "sengaja konservatif |",
          "| Biaya dan pajak | 1% per tahun dari saldo | Biaya reksa dana, pajak kupon SBN 10%, selisih jual-beli emas |",
          "| Inflasi Indonesia | 3% per tahun | Sasaran BI 2,5 ± 1%; September 2026: 3,28% |",
          "| Rupiah | Hasil dihitung dalam daya beli, lalu ditambah inflasi Indonesia | Jangka panjang kurs kira-kira "
          f"mengikuti selisih inflasi: {kurs_teks(dep['2000'], '2000–2024')}, {kurs_teks(dep['2010'], '2010–2024')} |",
          "| Simulasi | 10.000 jalur, potongan 5 tahun berurutan dari sejarah (krisis beruntun tetap utuh), plus "
          "semua urutan tahun asli | Bootstrap blok, seed tetap |",
          "| Setoran | Tetap tiap akhir bulan; rebalance tiap awal tahun | Sederhana dan bisa diikuti |", "",
          "Varian yang dihitung: 3 profil portofolio + 2 pembanding berbunga tetap. Tidak ada yang disetel ulang "
          "setelah melihat hasil. Satu perubahan metode: pembanding deposito memakai bunga tetap, karena deposito "
          "tidak bisa rugi nominal (memakai T-bill AS + inflasi tetap membuatnya tampak rugi di tahun inflasi tinggi).",
          ""]

    L += ["### Contoh utama: Rp 10 juta sekarang + Rp 1 juta tiap bulan, Seimbang, skenario tengah", "",
          f"Hasil {pc(ns['tengah'])} per tahun dalam rupiah. \"Untung per bulan/minggu\" adalah rata-rata selama "
          "tahun itu; kenyataannya naik-turun (lihat bagian 5).", ""]
    L += md_table(["Tahun ke", "Total disetor", "Saldo akhir", "Total untung", "Untung per bulan (tahun itu)",
                   "Untung per minggu (tahun itu)", "Saldo dalam daya beli hari ini"],
                  [[str(x["tahun"]), rp(x["disetor"]), rp(x["saldo"]), rp(x["untung"]), rp(x["per_bulan"]),
                    rp(x["per_minggu"]), rp(x["daya_beli"])] for x in tetap])
    L += ["", f"**Yang perlu dipahami:** di tahun pertama untungnya hanya sekitar {rp(tetap1['per_minggu'])} per "
          f"minggu, jauh lebih kecil dari setoran {rp(setoran * 12 / MINGGU_PER_TAHUN)} per minggu. Di awal, "
          "**besarnya setoran jauh lebih menentukan daripada persentase untung.** Compounding baru terasa setelah "
          f"saldo besar: di tahun ke-10 untungnya sekitar {rp(tetap10['per_bulan'])} per bulan, dan di tahun ke-20 "
          f"sekitar {rp(tetap[-1]['per_bulan'])} per bulan. Cara tercepat menambah hasil adalah menaikkan setoran "
          "setiap kali penghasilan naik.", ""]

    L += ["### Rentang hasil (Seimbang, 10.000 simulasi)", ""]
    L += md_table(["Tahun ke", "Total disetor", "1 dari 10 terburuk", "Tengah", "1 dari 10 terbaik",
                   "Peluang saldo < uang disetor", "Terburuk dalam sejarah asli"],
                  [[str(x["tahun"]), rp(x["disetor"]), rp(x["buruk"]), rp(x["tengah"]), rp(x["bagus"]),
                    pc(x["rugi"]), rp(x["hist_min"])] for x in rent["seimbang"]])
    L += ["", "![Proyeksi saldo](grafik/untung_proyeksi.png)", "",
          "Kolom \"terburuk dalam sejarah asli\" adalah hasil kalau Anda mulai di tahun terburuk sejak 1928 "
          "(misalnya tepat sebelum Depresi Besar 1929 atau krisis 2008).", ""]

    L += ["### Kalau uangnya sekaligus: Rp 100 juta tanpa setoran tambahan (Seimbang)", ""]
    L += md_table(["Tahun ke", "1 dari 10 terburuk", "Tengah", "1 dari 10 terbaik", "Peluang < Rp 100 juta"],
                  [[str(x["tahun"]), rp(x["buruk"]), rp(x["tengah"]), rp(x["bagus"]), pc(x["rugi"])]
                   for x in sekali])
    L += [""]

    dep_nom, sbn_nom = cfg["deposito_bersih"], cfg["sbn_bersih"]
    dep_t = m.tabel_tetap(iv.riil_dari_nominal(dep_nom), modal, setoran, [10])[0]
    sbn_t = m.tabel_tetap(iv.riil_dari_nominal(sbn_nom), modal, setoran, [10])[0]
    L += ["### Perbandingan setelah 10 tahun (Rp 10 juta + Rp 1 juta/bulan, total disetor Rp 130 juta)", ""]
    rows = [[f"Deposito/RDPU saja (±{pc(100 * dep_nom, 0)} bersih, tetap)", pc(100 * dep_nom), rp(dep_t["saldo"]),
             rp(dep_t["saldo"]), "0%", "tidak pernah rugi nominal"],
            [f"SBN ritel saja (kupon ±6,9% − pajak = {pc(100 * sbn_nom)}, kalau kupon berikutnya sama)",
             pc(100 * sbn_nom), rp(sbn_t["saldo"]), rp(sbn_t["saldo"]), "0%*", "dijamin negara*"]]
    for n in ["hati_hati", "seimbang", "agresif"]:
        x = t10[n]
        rows.append([iv.NAMA[n] + (" **(rekomendasi)**" if n == "seimbang" else ""), pc(nom[n]["tengah"]),
                     rp(x["tengah"]), rp(x["buruk"]), pc(x["rugi"]), thn_terburuk(n)])
    rows.append(["Trading setup mentor / bot (hasil uji kita)", "sekitar impas sampai rugi", "–", "–", "–",
                 "drawdown 15–30%+"])
    L += md_table(["Pilihan", "Hasil per tahun (tengah)", "Saldo tengah", "Saldo 1 dari 10 terburuk",
                   "Peluang rugi", "Tahun terburuk"], rows)
    L += ["", "\\* SBN dijamin negara dan tidak rugi nominal kalau dipegang sampai jatuh tempo. Tetapi kupon "
          "6,9–7% adalah yang tertinggi sejak 2019; seri berikutnya bisa lebih rendah kalau suku bunga turun. "
          "Deposito dijamin LPS hanya sampai Rp 2 miliar per bank dan bila bunganya tidak melebihi bunga "
          "penjaminan LPS.", "",
          f"**Arti tabel ini:** saat ini SBN ritel memberi hasil yang hampir setara dengan skenario tengah Seimbang "
          "dengan risiko jauh lebih kecil — karena kupon SBN sedang tinggi dan model ini sengaja konservatif untuk "
          "bagian obligasi. Karena itu 40% Seimbang memang diisi SBN. Bagian saham tetap perlu untuk jangka panjang: "
          f"saham dunia memberi {pc(geo['saham'])} di atas inflasi per tahun, sedangkan kupon SBN di masa depan "
          "belum tentu setinggi sekarang.", ""]

    L += ["## 5. Seperti apa naik-turunnya per minggu (data nyata 2010–2026)", "",
          f"Portofolio dihitung minggu per minggu dari {mg['seimbang']['mulai']:%d %b %Y} sampai "
          f"{akhir_mg:%d %b %Y} memakai return harian nyata: saham AS termasuk dividen (Kenneth French), obligasi "
          "AS 10 tahun dari imbal hasil harian (FRED), dan emas (OANDA). Dalam dolar, sebelum biaya; periode ini "
          "termasuk masa bagus saham AS, jadi hasil per tahunnya lebih tinggi dari skenario tengah di atas.", ""]
    head = ["", *[iv.NAMA[n] for n in iv.PORTOFOLIO]]
    keys = [("Minggu yang naik", "pct_minggu_naik", lambda v: pc(v, 0)),
            ("Rata-rata per minggu", "rata_minggu", lambda v: pc(v, 2, True)),
            ("Minggu terburuk", "minggu_terburuk", lambda v: pc(v, 1, True)),
            ("Bulan yang naik", "pct_bulan_naik", lambda v: pc(v, 0)),
            ("Bulan terburuk", "bulan_terburuk", lambda v: pc(v, 1, True)),
            ("12 bulan terburuk", "setahun_terburuk", lambda v: pc(v, 1, True)),
            ("Turun terdalam dari puncak", "turun_terdalam", lambda v: pc(-v, 1, True)),
            ("Hasil per tahun", "cagr", lambda v: pc(v, 1, True))]
    L += md_table(head, [[label, *[f(mg[n][k]) for n in iv.PORTOFOLIO]] for label, k, f in keys])
    ms = mg["seimbang"]
    L += ["", f"**Contoh dengan saldo Rp 100 juta (Seimbang):** rata-rata naik "
          f"{rp(1e6 * ms['rata_minggu'])} per minggu, tetapi hanya {pc(ms['pct_minggu_naik'], 0)} minggu yang naik. "
          f"Minggu terburuk turun {rp(-1e6 * ms['minggu_terburuk'])}, bulan terburuk {rp(-1e6 * ms['bulan_terburuk'])}, "
          f"dan dari puncak sempat turun {rp(1e6 * ms['turun_terdalam'])} sebelum pulih. Karena itu untung dihitung "
          "per tahun, bukan per minggu.", "",
          "![Hasil per tahun](grafik/untung_tahunan.png)", ""]

    L += ["## 6. Hitung dengan angka Anda sendiri", "",
          "Ubah `modal`, `setoran_bulanan`, dan `portofolio` di `config/rencana.toml`, lalu:", "",
          "```bash", "python scripts/rencana_untung.py --layar", "```", "",
          "Atau langsung lewat perintah:", "",
          "```bash", "python scripts/rencana_untung.py --layar --modal 25000000 --setoran 2000000 --porto seimbang",
          "```", "",
          "Data riset diunduh sekali dengan `python -m bot.data.download riset`. Menjalankan skrip tanpa `--layar` "
          "menulis ulang laporan ini.", ""]

    L += ["## 7. Batasan (jujur)", "",
          "- Masa lalu bukan jaminan. Angka di atas adalah rentang yang masuk akal, bukan janji.",
          "- Data panjang hanya tersedia untuk AS. Return saham sudah diturunkan ke rata-rata dunia, tetapi "
          "pasar Indonesia bisa lebih baik atau lebih buruk.",
          "- Inflasi Indonesia dianggap tetap 3%. Kalau inflasi naik, angka rupiah naik tetapi daya belinya tidak.",
          "- Tahun dengan inflasi AS tinggi (misalnya 1946 dan 2022) tampak lebih buruk dalam angka rupiah karena "
          "lonjakan inflasi AS ikut terhitung. Ini membuat angka risiko sedikit dilebih-lebihkan (lebih aman).",
          "- Kurs rupiah tidak dimodelkan terpisah. Bagian saham global ikut naik-turun dengan kurs.",
          "- Biaya dan pajak memakai angka kasar 1% per tahun. Pilih produk berbiaya rendah dan terdaftar OJK.",
          "- Ini bahan pertimbangan, bukan nasihat keuangan pribadi. Cek kupon SBN dan produk terbaru sebelum membeli.",
          ""]

    L += ["## Sumber", "",
          "- Damodaran, A. *Historical Returns on Stocks, Bonds, Bills, Real Estate and Gold*, NYU Stern, pembaruan "
          "Januari 2026 — [histretSP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histret.html).",
          "- Dimson, E., Marsh, P. & Staunton, M. *UBS Global Investment Returns Yearbook 2025* — "
          "[ringkasan Cambridge Judge](https://www.jbs.cam.ac.uk/2025/report-stocks-have-far-outperformed-over-the-past-125-years/).",
          "- Kenneth R. French Data Library (return harian pasar saham AS) — "
          "[situs](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).",
          "- FRED: imbal hasil obligasi AS 10 tahun (DGS10), kurs USD/IDR dan IHK Indonesia (OECD).",
          "- Barber, B., Lee, Y., Liu, Y. & Odean, T. (2014). The cross-section of speculator skill: Evidence from "
          "day trading. *Journal of Financial Markets* 18.",
          "- Chague, F., De-Losso, R. & Giovannetti, B. (2020). Day Trading for a Living? Working paper, SSRN.",
          "- ESMA (2018). Product intervention measures on CFDs and binary options.",
          "- Kelly, J. L. (1956). A New Interpretation of Information Rate. *Bell System Technical Journal*.",
          "- Sharpe, W. F. (1991). The Arithmetic of Active Management. *Financial Analysts Journal*.",
          "- S&P Dow Jones Indices, *SPIVA Scorecards*; Morningstar, *Mind the Gap*; Vanguard (2012), "
          "*Dollar-cost averaging just means taking risk later*.",
          "- Bank Indonesia menahan BI rate 5,75% (RDG 20–21 Oktober 2026) — "
          "[Bisnis.com](https://finansial.bisnis.com/read/20261021/11/2014413/breaking-bank-indonesia-tahan-bi-rate-575-pada-rdg-oktober-2026).",
          "- BPS: inflasi September 2026 3,28% (yoy) — "
          "[Kontan](https://pusatdata.kontan.co.id/infografik/275/Inflasi-Tahunan-Naik-Menjadi-328-pada-September-2026).",
          "- Kupon ORI030: 6,9% (3 tahun) dan 7,0% (6 tahun) — "
          "[Bisnis.com](https://market.bisnis.com/read/20260718/92/1988984/di-balik-larisnya-ori030-kupon-jumbo-hingga-efek-reinvestasi).",
          "- Jadwal sementara SBN ritel 2026 — "
          "[OCBC](https://www.ocbc.id/id/article/2026/01/26/jadwal-sbn-ritel-2026-lengkap-ori-sr-st-dan-sbr-dari-januari-desember).",
          ""]
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"ditulis: {REPORT.relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layar", action="store_true", help="tampilkan hitungan di layar, tanpa menulis laporan")
    ap.add_argument("--modal", type=float)
    ap.add_argument("--setoran", type=float)
    ap.add_argument("--porto", choices=list(iv.PORTOFOLIO))
    a = ap.parse_args()
    cfg = tomllib.loads((ROOT / "config" / "rencana.toml").read_text(encoding="utf-8"))
    if a.modal is not None:
        cfg["modal"] = a.modal
    if a.setoran is not None:
        cfg["setoran_bulanan"] = a.setoran
    if a.porto:
        cfg["portofolio"] = a.porto
    m = Model()
    if a.layar:
        layar(m, cfg)
    else:
        laporan(m, cfg)


if __name__ == "__main__":
    main()
