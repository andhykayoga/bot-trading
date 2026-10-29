"""Jalankan uji forex cepat sesuai reports/RENCANA_FOREX_CEPAT.md dan tulis laporannya.

    python -m bot.data.download forex forex_uji forex_riset
    python scripts/run_forex_cepat.py

Menulis reports/LAPORAN_FOREX_CEPAT.md, grafik di reports/grafik/, dan CSV di reports/hasil_forex_cepat/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import forex_cepat as fc  # noqa: E402
from scripts.make_report import BLUE, GRID, INK, INK2, RED, SURF  # noqa: E402

ORANGE = "#eb6834"
OUT = ROOT / "reports" / "hasil_forex_cepat"
GRAFIK = ROOT / "reports" / "grafik"
REPORT = ROOT / "reports" / "LAPORAN_FOREX_CEPAT.md"
NAMA = {"S1": "S1 Pola jam sesi", "S2": "S2 Dolar di hari FOMC", "S3": "S3 Fixing London 16.00"}


def pc(x: float, nd: int = 1, plus: bool = True) -> str:
    return (f"{x:+.{nd}f}%" if plus else f"{x:.{nd}f}%").replace(".", ",")


def num(x: float, nd: int = 2) -> str:
    return f"{x:.{nd}f}".replace(".", ",")


def ribuan(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def md_table(head: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    return out + ["| " + " | ".join(r) + " |" for r in rows]


def _gaya(ax) -> None:
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_facecolor(SURF)


def grafik_strategi(hasil: dict, out: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.9), dpi=150, sharey=True)
    for ax, sid in zip(axes, hasil):
        port = hasil[sid]["port"]
        for k, label, color, ls in [("kotor", "Sebelum biaya", INK2, "--"), ("ecn", "Biaya ECN", BLUE, "-"),
                                    ("std", "Biaya standar", ORANGE, "-")]:
            skala = hasil[sid]["stat"]["ecn"]["skala"]
            eq = 100 * ((1 + skala * port[k]).cumprod() - 1)
            ax.plot(eq.index, eq.values, color=color, lw=1.4, ls=ls, label=label)
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(NAMA[sid], fontsize=9, color=INK, loc="left")
        ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(4))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
        _gaya(ax)
    axes[0].set_ylabel("Untung/rugi kumulatif (%)", color=INK2, fontsize=8)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.suptitle("Tiga strategi riset, 7 pair, 2014–2026 (skala volatilitas 10% per tahun)",
                 x=0.02, ha="left", fontsize=10, color=INK)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def grafik_otak_atik(d: dict, out: Path) -> None:
    df = d["tabel"]
    b = d["terbaik"]
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=150)
    ax.scatter(df["is"], df["oos"], s=8, color=BLUE, alpha=0.35, lw=0)
    ax.scatter([b["is"]], [b["oos"]], s=50, color=RED, zorder=3, edgecolor=SURF, lw=1.5)
    ax.annotate(f"Terbaik di data penyusunan (SMA {int(b['cepat'])}/{int(b['lambat'])})", (b["is"], b["oos"]),
                xytext=(-8, 12), textcoords="offset points", ha="right", fontsize=8, color=INK,
                bbox={"facecolor": SURF, "edgecolor": "none", "alpha": 0.9, "pad": 1.5})
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlabel("Data penyusunan 2014–2019 (% per tahun)", color=INK2, fontsize=9)
    ax.set_ylabel("Data baru 2020–2026 (% per tahun)", color=INK2, fontsize=9)
    ax.set_title(f"{ribuan(d['n'])} kombinasi SMA di EURUSD H1: bagus di masa lalu ≠ bagus di masa depan",
                 color=INK, fontsize=10, loc="left")
    _gaya(ax); ax.grid(axis="x", color=GRID, lw=0.8)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def hitung() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    impas = {s: fc.impas(s) for s in fc.PAIRS}
    pd.DataFrame([dict(pair=s, **x) for s in impas for x in impas[s]]).to_csv(OUT / "impas.csv", index=False)
    hasil = {sid: fc.nilai(sid) for sid in ["S1", "S2", "S3"]}
    rows = []
    for sid, h in hasil.items():
        for s in fc.PAIRS:
            rows.append(dict(strategi=sid, pair=s, **h["per_pair"][s]))
    pd.DataFrame(rows).to_csv(OUT / "per_pair.csv", index=False)
    demo = fc.demo_otak_atik()
    demo["tabel"].to_csv(OUT / "otak_atik_sma.csv", index=False)
    return {"impas": impas, "hasil": hasil, "demo": demo}


def laporan(r: dict) -> None:
    GRAFIK.mkdir(parents=True, exist_ok=True)
    hasil, demo, impas = r["hasil"], r["demo"], r["impas"]
    grafik_strategi(hasil, GRAFIK / "forex_cepat_strategi.png")
    grafik_otak_atik(demo, GRAFIK / "forex_cepat_otak_atik.png")
    eu = {x["rentang"]: x for x in impas["EURUSD"]}
    lolos = [sid for sid in hasil if hasil[sid]["lolos"]]
    s1, s2 = hasil["S1"], hasil["S2"]
    b = demo["terbaik"]

    L = ["# Laporan Uji Forex Cepat", "",
         "Permintaan Anda: *\"buatkan supaya profit di forex, entah diotak-atik teknikalnya atau main cepat jual "
         "beli cepat, bebas, yang penting untung.\"* Aturan uji dikunci lebih dulu di "
         "[pra-registrasi](RENCANA_FOREX_CEPAT.md) (di-commit sebelum hasil dihitung), lalu dijalankan sekali.", "",
         "## Jawaban singkat", ""]
    if lolos:
        L += [f"- Strategi yang lolos: {', '.join(NAMA[s] for s in lolos)}. Lihat bagian B sebelum memakai uang."]
    else:
        L += ["- **Tidak ada cara yang lolos.** Saya sudah mencoba yang Anda minta: jual-beli cepat, tiga pola forex "
              "jangka pendek yang diterbitkan di jurnal top, dan mengotak-atik teknikal. Hasilnya rugi atau terlalu "
              "kecil untuk dibedakan dari kebetulan."]
    L += [f"- **Jual-beli cepat kalah oleh biaya.** Di EURUSD, harga rata-rata hanya bergerak "
          f"{num(eu['5 menit']['rata'], 1)} pip per 5 menit, sedangkan biaya termurah {num(fc.BIAYA_ECN['EURUSD'], 1)} pip "
          f"per transaksi. Supaya impas, bot harus **benar {pc(eu['5 menit']['impas_ecn'], 0, False)} dari seluruh "
          "transaksi** — tidak ada metode yang diketahui bisa begitu. Per detik, gerak harga "
          f"(±{num(eu['1 detik (perkiraan)']['rata'], 2)} pip) lebih kecil dari biayanya, jadi mustahil.",
          f"- **Mengotak-atik teknikal hanya menghasilkan ilusi.** Dari {ribuan(demo['n'])} kombinasi SMA, yang "
          f"terbaik di masa lalu ({pc(b['is'])} per tahun) hanya {pc(b['oos'])} per tahun di data baru; 10 terbaik "
          f"rata-rata {pc(demo['top10_oos'])}. Peringkat masa lalu hampir tidak berhubungan dengan masa depan "
          f"(korelasi {num(demo['spearman'])}).",
          "- **Berita bot \"mahasiswa China\" bukan bukti bahwa forex bisa diakali dengan bot cepat** — mekanismenya "
          "berbeda (bagian D).",
          "- Untuk menambah uang, tetap pakai [rencana investasi](RENCANA_UNTUNG.md). Kalau ingin tetap bermain "
          "forex, anggap uang belajar (maksimal 5%), bukan sumber untung.", ""]

    # ---- A
    L += ["## A. Jual-beli cepat: berapa persen harus benar supaya impas?", "",
          "Rata-rata besar gerak harga EURUSD per rentang waktu (2014–2026) dibanding biaya satu transaksi "
          "pulang-pergi. Kolom \"harus benar\" = persentase transaksi yang harus benar arahnya hanya untuk impas, "
          "kalau untung saat benar sama dengan rugi saat salah.", ""]
    rows = []
    for x in impas["EURUSD"]:
        imp_e = "mustahil (> 100%)" if x["impas_ecn"] > 100 else pc(x["impas_ecn"], 1, False)
        imp_s = "mustahil (> 100%)" if x["impas_std"] > 100 else pc(x["impas_std"], 1, False)
        rows.append([x["rentang"], num(x["rata"], 2) + " pip", pc(x["biaya_ecn_pct"], 0, False), imp_e, imp_s])
    L += md_table(["Pegang posisi selama", "Rata-rata gerak", "Biaya ECN ÷ gerak", "Harus benar (ECN 0,9 pip)",
                   "Harus benar (standar 1,4 pip)"], rows)
    rows = []
    for s in fc.PAIRS:
        d = {x["rentang"]: x for x in impas[s]}
        rows.append([s, pc(d["5 menit"]["impas_ecn"], 1, False), pc(d["1 jam"]["impas_ecn"], 1, False),
                     pc(d["1 hari"]["impas_ecn"], 1, False)])
    L += ["", "Semua pair, biaya ECN:", ""]
    L += md_table(["Pair", "Harus benar: 5 menit", "1 jam", "1 hari"], rows)
    L += ["", "**Artinya:** makin cepat jual-beli, makin besar porsi biaya dibanding gerak harga. Tebakan arah yang "
          "sangat bagus (benar 55% dari waktu) sudah luar biasa langka, tetapi itu pun masih rugi di bawah 1 jam. "
          "Yang untung dari jual-beli per detik di forex adalah pihak yang **menerima** spread (broker, bank, "
          "market maker), bukan yang membayarnya. Baris \"1 detik\" adalah perkiraan dari data 5 menit (aturan akar "
          "waktu), karena data per detik tidak tersedia.", ""]

    # ---- B
    L += ["## B. Tiga pola forex dari jurnal, diuji apa adanya", "",
          "Masing-masing satu aturan tetap dari makalahnya (detail di pra-registrasi), di 7 pair mayor 2014–2026. "
          "Empat pair (AUDUSD, USDCAD, USDCHF, NZDUSD) belum pernah dipakai di uji mana pun.", "",
          "- **S1 Pola jam sesi** (Ranaldo 2009; Breedon & Ranaldo 2013): mata uang cenderung melemah di jam kerja "
          "negaranya. Jual mata uang yang pusatnya sedang buka sendirian, beli yang sebaliknya. ±2 transaksi per hari.",
          "- **S2 Dolar di hari FOMC** (Mueller, Tahbaz-Salehi & Vedolin 2017): jual USD dari sore sebelum "
          "pengumuman suku bunga Fed sampai sore hari pengumuman. 8 transaksi per tahun.",
          "- **S3 Fixing London** (Krohn, Mueller & Whelan 2024): beli USD sejam sebelum fixing 16.00 London, jual "
          "USD sejam sesudahnya. 2 transaksi per hari.", ""]
    rows = []
    for sid, h in hasil.items():
        k, e, s = h["stat"]["kotor"], h["stat"]["ecn"], h["stat"]["std"]
        rows.append([NAMA[sid], pc(k["per_tahun_1x"], 2), pc(e["per_tahun_1x"], 2), pc(s["per_tahun_1x"], 2),
                     num(e["t"]), pc(e["per_tahun_10vol"]), f"{num(e['dd_10vol'], 0)}%",
                     " / ".join(pc(v, 1) for v in e["sub"].values()),
                     "**lolos**" if h["lolos"] else "gagal"])
    L += md_table(["Strategi", "Per tahun sebelum biaya", "Setelah biaya ECN", "Setelah biaya standar",
                   "t-stat (ECN)", "Per tahun di skala 10% vol (ECN)", "Drawdown terburuk (10% vol)",
                   "Per sub-periode 2014–17 / 18–21 / 22–26 (ECN)", "Hasil"], rows)
    L += ["", "\"Per tahun\" dihitung untuk posisi 1× nilai di tiap pair (rata-rata 7 pair). \"Skala 10% vol\" "
          "memperbesar posisi sampai naik-turunnya 10% per tahun, supaya bisa dibandingkan. Syarat lolos: t-stat ≥ 2,4, "
          "untung di ≥ 2 dari 3 sub-periode, drawdown ≤ 20%, untung di ≥ 2/3 pair.", "",
          "![Tiga strategi riset](grafik/forex_cepat_strategi.png)", ""]
    rows = []
    for s in fc.PAIRS:
        rows.append([s, *[("tidak berlaku" if hasil[sid]["per_pair"][s]["transaksi_per_tahun"] == 0
                           else pc(hasil[sid]["per_pair"][s]["ecn"], 2)) for sid in hasil]])
    L += ["Per pair, per tahun setelah biaya ECN (posisi 1×):", ""]
    L += md_table(["Pair", *[NAMA[s] for s in hasil]], rows)
    s1_eu = s1["per_pair"]["EURUSD"]["ecn"]
    L += ["", "**Arti hasil ini:**", "",
          f"- **S1** sebenarnya sedikit untung sebelum biaya ({pc(s1['stat']['kotor']['per_tahun_1x'], 1)} per "
          f"tahun), tetapi ±520 transaksi per tahun per pair membuatnya rugi {pc(s1['stat']['ecn']['per_tahun_1x'], 1)} "
          f"per tahun setelah biaya ECN. Hanya EURUSD yang untung ({pc(s1_eu, 1)}); memilih EURUSD saja setelah "
          "melihat hasil ini adalah persis \"otak-atik\" di bagian C (1 dari 7 pair bisa untung karena kebetulan).",
          f"- **S2** satu-satunya yang untung setelah biaya, dan konsisten di 7 pair dan 3 sub-periode. Tetapi "
          f"hasilnya kecil: {pc(s2['stat']['ecn']['per_tahun_1x'], 2)} per tahun untuk posisi 1×, t-stat "
          f"{num(s2['stat']['ecn']['t'])} (belum bisa dibedakan dari kebetulan), dan karena hanya 8 hari per tahun, "
          f"untuk mencapai {pc(s2['stat']['ecn']['per_tahun_10vol'], 1)} per tahun perlu leverage ±"
          f"{num(s2['stat']['ecn']['skala'], 0)}× dengan drawdown {num(s2['stat']['ecn']['dd_10vol'], 0)}%. "
          "Ketujuh pair bergerak bersama (semuanya jual USD di hari yang sama), jadi konsistensinya sebenarnya satu "
          "taruhan, bukan tujuh.",
          "- **S3** nol sebelum biaya dan rugi besar setelah biaya. Pola yang ditemukan riset sudah tidak cukup "
          "besar untuk membayar biaya ritel.", ""]

    # ---- C
    L += ["## C. Kalau teknikal diotak-atik sampai bagus", "",
          f"Saya coba {ribuan(demo['n'])} kombinasi SMA cepat/lambat di EURUSD candle 1 jam. Kombinasi dipilih dari "
          "data 2014–2019, lalu dicek di data 2020–2026 yang tidak ikut dipakai memilih. Biaya standar; swap tidak "
          "dihitung dan posisi tidak ditutup harian (keduanya menguntungkan demo ini).", ""]
    L += md_table(["", "Data penyusunan 2014–2019", "Data baru 2020–2026"],
                  [[f"Kombinasi terbaik (SMA {int(b['cepat'])}/{int(b['lambat'])})", pc(b["is"]), pc(b["oos"])],
                   ["Rata-rata 10 terbaik", pc(demo["top10_is"]), pc(demo["top10_oos"])],
                   ["Porsi kombinasi yang untung", pc(demo["pct_is_untung"], 0, False),
                    pc(demo["pct_oos_untung"], 0, False)]])
    to = demo["terbaik_oos"]
    L += ["", "![Otak-atik SMA](grafik/forex_cepat_otak_atik.png)", "",
          f"Kombinasi yang ternyata terbaik di 2020–2026 (SMA {int(to['cepat'])}/{int(to['lambat'])}, "
          f"{pc(to['oos'])} per tahun) justru rugi {pc(to['is'])} per tahun di 2014–2019 — tidak mungkin dipilih "
          "sebelumnya. Inilah sebabnya backtest yang diotak-atik selalu bisa dibuat terlihat bagus, dan selalu "
          "mengecewakan saat dipakai: yang ditemukan adalah kebetulan di data lama, bukan pola yang berulang "
          f"(Bailey, Borwein, López de Prado & Zhu, 2014). Dengan leverage 10×, kombinasi terbaik tadi bisa "
          f"dipamerkan sebagai backtest {pc(10 * b['is'], 0)} per tahun, padahal di data baru hanya "
          f"{pc(10 * b['oos'], 0)} per tahun sebelum swap. Justru cara seperti itu yang tidak boleh dipakai.", ""]

    # ---- D
    L += ["## D. Soal berita bot \"mahasiswa China\" yang untung besar", "",
          "Saya tidak menemukan berita terverifikasi tentang mahasiswa China yang untung besar dengan bot DEX per "
          "detik. Yang paling dekat: akun Polymarket \"Gravia\" milik mahasiswa China di Jepang dengan klaim "
          "keuntungan luar biasa, yang diragukan oleh media yang memberitakannya. Apa pun cerita persisnya, bot "
          "kripto per detik yang benar-benar untung biasanya bukan menebak arah harga, melainkan:", "",
          "- **Arbitrase**: membeli di satu bursa/pool dan menjual di tempat lain dalam hitungan detik. Studi "
          "terhadap 19 bot arbitrase CEX–DEX terbesar: untung kotor USD 233,8 juta, tetapi hanya USD 90,1 juta yang "
          "tersisa setelah membayar pembuat blok, dan peluangnya hilang dalam 0,5–1,5 detik. Ini perlombaan "
          "infrastruktur antar tim profesional.",
          "- **MEV / sandwich**: menyalip transaksi orang lain di blockchain. Ini merugikan pengguna lain dan tidak "
          "akan saya buatkan.",
          "- **Bias berita**: yang diberitakan adalah satu orang yang menang, bukan ribuan bot yang rugi.", "",
          "Di forex ritel, semua itu tidak tersedia: tidak ada antrean transaksi publik untuk dilihat, harga datang "
          "dari broker, dan bot yang memanfaatkan harga broker yang terlambat (latency arbitrage) dilarang di "
          "perjanjian hampir semua broker — transaksinya dibatalkan dan akunnya ditutup.", ""]

    L += ["## Kesimpulan", "",
          "Dengan semua yang sudah diuji di repo ini — 30-an setup mentor, versi perbaikannya, momentum, tiga pola "
          "dari jurnal, scalping, dan otak-atik teknikal — **tidak ada bot forex yang terbukti untung setelah biaya "
          "di data yang belum dipakai menyusunnya.** Ini konsisten dengan riset: mayoritas trader ritel forex rugi. "
          "Saya tidak bisa membuatkan bot forex yang untung, dan siapa pun yang menjanjikannya sedang menjual "
          "sesuatu.", "",
          "Yang bisa dilakukan:", "",
          "1. Tambah uang lewat [rencana investasi](RENCANA_UNTUNG.md) (Seimbang 50/40/10, ±6% per tahun, peluang "
          "rugi setelah 10 tahun ±2%).",
          "2. Kalau tetap ingin di forex sebagai hobi: maksimal 5% uang, akun demo dulu, pakai "
          "`scripts/sinyal.py` (semi-otomatis) dan jurnal. Ukur hasilnya minimal 100 transaksi sebelum menambah.",
          "3. Strategi baru apa pun (dari mentor, grup, atau video) bisa diuji dengan kerangka yang sama: aturan "
          "dikunci dulu, lalu diuji sekali di data yang belum dipakai.", ""]

    L += ["## Sumber", "",
          "- Ranaldo, A. (2009). Segmentation and time-of-day patterns in foreign exchange markets. *Journal of "
          "Banking & Finance* 33(12).",
          "- Breedon, F. & Ranaldo, A. (2013). Intraday patterns in FX returns and order flow. *Journal of Money, "
          "Credit and Banking* 45(5).",
          "- Mueller, P., Tahbaz-Salehi, A. & Vedolin, A. (2017). Exchange rates and monetary policy uncertainty. "
          "*Journal of Finance* 72(3).",
          "- Krohn, I., Mueller, P. & Whelan, P. (2024). Foreign exchange fixings and returns around the clock. "
          "*Journal of Finance* 79(1).",
          "- Bailey, D., Borwein, J., López de Prado, M. & Zhu, Q. (2014). Pseudo-mathematics and financial "
          "charlatanism. *Notices of the AMS* 61(5).",
          "- Berita akun Polymarket \"Gravia\" — "
          "[money.it](https://www.money.it/da-090-a-408292-in-48-ore-con-l-ai-trading-genio-della-finanza-o-clamorosa-fake-news).",
          "- Ringkasan studi bot arbitrase CEX–DEX — [ChainCatcher](https://www.chaincatcher.com/article/2193465).",
          "- Data: candle 5 menit OANDA (Hugging Face `bunqi/OANDA_*`); jadwal FOMC dari Federal Reserve.", ""]
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"ditulis: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    import pickle
    r = hitung()
    (OUT / "hasil.pkl").write_bytes(pickle.dumps(r))
    laporan(r)
