"""Tulis reports/LAPORAN_MODUL_BARU.md dari hasil scripts/run_modul_baru.py --hitung."""
from __future__ import annotations

import math
import pickle
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import kripto_investasi as ki  # noqa: E402
from bot.research import multi_aset as ma  # noqa: E402
from bot.setups.pola import ALL_POLA  # noqa: E402
from scripts.make_report import BLUE, GRID, INK, INK2, SURF  # noqa: E402

ORANGE, AQUA = "#eb6834", "#1baf7a"
OUT = ROOT / "reports" / "hasil_modul_baru"
GRAFIK = ROOT / "reports" / "grafik"
REPORT = ROOT / "reports" / "LAPORAN_MODUL_BARU.md"
BH = "Beli-tahan BTC+ETH 50/50"


def pc(x, nd=1, plus=True):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    return (f"{x:+.{nd}f}%" if plus else f"{x:.{nd}f}%").replace(".", ",")


def num(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")


def rp(x):
    return f"Rp {x / 1e6:,.1f} juta".replace(",", "§").replace(".", ",").replace("§", ".")


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    return out + ["| " + " | ".join(r) + " |" for r in rows]


def _gaya(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_facecolor(SURF)


def grafik_kripto(h, out):
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=150)
    for nama, label, color, lw in [(BH, "Beli-tahan BTC+ETH", INK2, 1.2),
                                   ("A1 Filter tren SMA 200 (BTC+ETH)", "A1 filter tren SMA 200", BLUE, 1.6),
                                   ("B6 Trailing stop 10% (BTC+ETH)", "B6 trailing stop 10%", ORANGE, 1.6),
                                   ("B3 Cicil 5× masuk/keluar RSI mingguan (BTC+ETH)", "B3 cicil 5× RSI mingguan", AQUA,
                                    1.6)]:
        eq = h[nama]["eq"] * 10
        ax.plot(eq.index, eq.values, color=color, lw=lw, label=f"{label}: {rp(eq.iloc[-1] * 1e6)}")
    ax.set_yscale("log")
    ax.set_yticks([2, 5, 10, 20, 50, 100])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_ylabel("Nilai dari Rp 10 juta (juta rupiah, skala log)", color=INK2, fontsize=8.5)
    ax.set_title("Kripto spot tanpa leverage, Maret 2018 – Oktober 2026", color=INK, fontsize=10, loc="left")
    _gaya(ax)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def grafik_multi(m, out):
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
    for b, label, color in [("institusi", "Biaya institusi (futures)", BLUE), ("ritel", "Biaya CFD ritel", ORANGE)]:
        eq = m[b]["eq"]
        ax.plot(eq.index, 100 * (eq - 1), color=color, lw=1.5)
        ax.annotate(f"{label}: {pc(100 * (eq.iloc[-1] - 1), 0)}", (eq.index[-1], 100 * (eq.iloc[-1] - 1)),
                    xytext=(-4, 8), textcoords="offset points", ha="right", fontsize=8, color=INK)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_ylabel("Untung/rugi kumulatif (%)", color=INK2, fontsize=9)
    ax.set_title("A2 trend-following 34 pasar, 2006–2026 (volatilitas sasaran 10%)", color=INK, fontsize=10,
                 loc="left")
    _gaya(ax)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def laporan():
    h = pickle.loads((OUT / "kripto.pkl").read_bytes())
    m = pickle.loads((OUT / "multi_aset.pkl").read_bytes())
    pola = pickle.loads((OUT / "pola.pkl").read_bytes())
    GRAFIK.mkdir(parents=True, exist_ok=True)
    grafik_kripto(h, GRAFIK / "modul_kripto.png")
    grafik_multi(m, GRAFIK / "modul_multi_aset.png")
    tanpa_meme = ki.statistik(ki.b1_alokasi("I1a_tanpa_meme")[0])

    def baris(nama):
        v = h[nama]
        s = v["stat"]
        return [nama, pc(s["cagr"]), num(s["sharpe"]), pc(-s["dd"], 0), " / ".join(pc(x, 0) for x in s["sub"].values()),
                pc(s["uji_akhir"]), "**lolos**" if v.get("lolos") else ("patokan" if v.get("patokan") is None else "gagal")]

    head = ["Versi", "Per tahun", "Sharpe", "Turun terdalam", "2018–20 / 2021–23 / 2024–26", "Des 2024 – Okt 2026",
            "Hasil"]
    a1, bh = h["A1 Filter tren SMA 200 (BTC+ETH)"]["stat"], h[BH]["stat"]
    b6 = h["B6 Trailing stop 10% (BTC+ETH)"]["stat"]
    ins, rit = m["institusi"], m["ritel"]
    lay_ins, lay_rit = ma.layak(ins), ma.layak(rit)
    moon, tanpa = h["B2 Cicilan bulanan 70/15/15 dengan moon bag"], h["B2 Cicilan bulanan 70/15/15 tanpa moon bag"]

    L = ["# Laporan: rancangan saya sendiri + semua modul mentor yang belum diuji", "",
         "Permintaan Anda: *\"tanpa mentor, kamu yang buatkan cara supaya untung, hindari masalah yang sudah ketemu, dan "
         "sekalian uji semua modul yang belum diuji.\"* Aturan dikunci dulu di [pra-registrasi](RENCANA_MODUL_BARU.md) "
         "sebelum hasil dihitung.", "",
         "## Jawaban singkat", "",
         "- **Yang menolong di kripto ternyata bukan menebak pola, tetapi keluar saat tren turun.** Rancangan saya "
         f"(A1: pegang BTC/ETH hanya selama harga di atas rata-rata 200 hari) memberi {pc(a1['cagr'])} per tahun dengan "
         f"turun terdalam {pc(-a1['dd'], 0)}, dibanding beli-dan-tahan {pc(bh['cagr'])} per tahun dengan turun terdalam "
         f"{pc(-bh['dd'], 0)}. Di periode terakhir (Des 2024 – Okt 2026) A1 {pc(a1['uji_akhir'])}, beli-dan-tahan "
         f"{pc(bh['uji_akhir'])}.",
         f"- **Trailing stop Ko Andri (B6) dan cicil 5× Kalimasada (B3) juga lolos** dengan cara yang sama: keluar atau "
         f"tidak masuk saat pasar jatuh. B6 10%: {pc(b6['cagr'])} per tahun, turun terdalam {pc(-b6['dd'], 0)}.",
         "- **Tetap berisiko besar.** \"Lolos\" di sini artinya lebih baik dari beli-dan-tahan kripto — yang sendiri pernah "
         "turun 77–81%. Versi terbaik pun pernah turun 38–61%. Ini hanya untuk porsi kecil uang.",
         f"- **Trend-following 34 pasar lewat CFD ritel rugi** ({pc(rit['cagr'])} per tahun) karena biaya pembiayaan "
         f"broker. Dengan biaya institusi hasilnya {pc(ins['cagr'])} per tahun, tetapi turun terdalam "
         f"{pc(-ins['dd'], 0)} melewati batas 20%.",
         "- **Gagal:** Fear & Greed, moon bag (mengurangi hasil), pola harmonic (hampir tidak pernah muncul), dan pola "
         "klasik (forex gagal semua; di kripto untung 2017–2024 lalu rugi di uji akhir — pola yang sama dengan setup "
         "mentor sebelumnya).",
         "- **Rekomendasi:** uang inti tetap di [rencana Seimbang](RENCANA_UNTUNG.md). Kalau ingin porsi spekulatif, "
         "maksimal 10% di kripto spot dengan aturan A1 atau B6, tanpa leverage. Sinyal hariannya sekarang ada di "
         "`scripts/sinyal.py`.", ""]

    L += ["## Bagian A — rancangan saya sendiri", "",
          "Dibuat dari pelajaran uji sebelumnya: transaksi jarang (biaya kecil), aturan sederhana tanpa penyetelan, "
          "tanpa martingale dan tanpa leverage di kripto, disebar ke banyak pasar, dan ada aturan keluar saat tren turun.",
          "", "### A1 · Kripto spot dengan filter tren (SMA 200)", ""]
    L += md_table(head, [baris(BH), baris("Beli-tahan BTC"), baris("A1 Filter tren SMA 200 (BTC+ETH)"),
                         baris("A1 Filter tren SMA 200 (BTC saja)")])
    L += ["", "Syarat lolos: Sharpe lebih tinggi **dan** turun terdalam lebih kecil dari beli-dan-tahan, serta untung di "
          "≥ 2 dari 3 sub-periode. Periode dimulai Maret 2018 karena rata-rata 200 hari BTC baru tersedia saat itu. "
          "Biaya 0,11% per transaksi; uang di luar pasar tidak berbunga.", "",
          "![Kripto spot](grafik/modul_kripto.png)", "",
          f"A1 hanya berada di pasar ±52% dari waktu dan masuk-keluar ±30 kali per koin dalam 8,6 tahun. Ia tidak menghindari "
          "semua penurunan (masih pernah turun 61%), tetapi menghindari sebagian besar pasar bear 2018 dan 2022.", "",
          "### A2 · Trend-following 34 pasar (indeks, obligasi, komoditas, forex)", ""]
    rows = []
    for b, label, lay in [("institusi", "Biaya institusi (futures)", lay_ins), ("ritel", "Biaya CFD ritel", lay_rit)]:
        r = m[b]
        rows.append([label, pc(r["cagr"]), num(r["sharpe"]), num(r["t"]), pc(-r["dd"], 0),
                     " / ".join(pc(v, 1) for v in r["sub"].values()),
                     "**lolos**" if lay["lolos"] else "gagal (" + ", ".join(k for k, v in lay["syarat"].items()
                                                                       if not v) + ")"])
    L += md_table(["Biaya", "Per tahun", "Sharpe", "t-stat", "Turun terdalam", "2006–11 / 2012–18 / 2019–26", "Hasil"],
                  rows)
    kk = rit["kontrib_kelas"]
    L += ["", "![Multi-aset](grafik/modul_multi_aset.png)", "",
          f"Versi ritel membayar biaya pembiayaan 2,5% per tahun dari nilai posisi, padahal untuk mencapai volatilitas "
          f"10% nilai posisinya rata-rata ±{num(rit['gross'].median(), 1)}× modal (obligasi butuh posisi besar karena "
          f"geraknya kecil). Total biaya pembiayaan selama 20 tahun ±{pc(100 * rit['financing'], 0, False)} dari modal "
          f"awal; bagian obligasi saja menyumbang {pc(100 * kk['obligasi'], 0)}. Versi institusi (bunga dihitung wajar "
          "lewat futures) mirip dengan hasil dana trend-following profesional: positif tetapi naik-turun, dengan "
          "tahun-tahun rugi panjang (2009–2012, 2016–2020). Return harga dipakai sebagai perkiraan return berjangka, "
          "jadi ada ketidakpastian ±1–2% per tahun.", ""]

    L += ["## Bagian B — modul mentor yang belum diuji", "", "### B1–B6 · Modul investasi spot kripto", ""]
    nama_b = ["B1 Alokasi 70/15/15 (BTC/altcoin/meme)", "B1 Pasif BTC+ETH 50/50 (rebalance)",
              "B1 70% BTC + 30% stablecoin", "B3 Cicil 5× masuk/keluar RSI mingguan (BTC+ETH)", "B4 Fear & Greed (BTC)",
              "B5 Halving: 365 hari sebelum s.d. 365 hari sesudah (BTC)",
              "B5 Halving: 365 hari sebelum s.d. 500 hari sesudah (BTC)", "B6 Trailing stop 10% (BTC+ETH)",
              "B6 Trailing stop 5% (BTC+ETH)"]
    L += md_table(head, [baris(n) for n in nama_b])
    i1a = h["B1 Alokasi 70/15/15 (BTC/altcoin/meme)"]["stat"]
    L += ["", "Catatan per modul:", "",
          f"- **B1 70/15/15** terlihat paling tinggi ({pc(i1a['cagr'])} per tahun), tetapi kelebihannya hampir "
          f"seluruhnya dari lonjakan DOGE di 2021 (porsi meme 15% saat itu hanya berisi DOGE). Cek tambahan (bukan pra-registrasi): "
          f"kalau porsi meme diganti stablecoin, hasilnya {pc(tanpa_meme['cagr'])} per tahun dengan turun terdalam "
          f"{pc(-tanpa_meme['dd'], 0)}. Selain itu data meme bias: meme coin yang mati sebelum listing di Binance tidak "
          "ada di data. Turun terdalamnya juga paling dalam (±80%).",
          "- **B1 70% BTC + 30% stablecoin** lolos tipis: hasil hampir sama dengan beli-dan-tahan dengan turun terdalam "
          "lebih kecil.",
          "- **B3 cicil 5×** hanya membeli di dasar pasar bear (RSI mingguan di bawah 30) dan menjual bertahap saat RSI di "
          "atas 70, jadi sering memegang kas. Hasilnya lebih kecil, tetapi turun terdalamnya paling ringan di antara "
          "versi yang lolos.",
          "- **B4 Fear & Greed gagal**: \"extreme greed\" sering muncul di awal kenaikan besar, jadi aturan ini menjual "
          "terlalu cepat dan membeli lagi setelah harga jauh lebih mahal.",
          "- **B5 halving** lolos, tetapi hanya ada 2 siklus di data dan aturannya memang disusun dari sejarah siklus itu "
          "sendiri. Dua kejadian tidak bisa membuktikan apa-apa; jangan dijadikan dasar.",
          "- **B6 trailing stop** (Ko Andri) lolos di kedua versi. Aturan masuk lagi (tertinggi 20 hari) adalah pilihan saya "
          "karena tidak disebut mentor, jadi B6 sebenarnya juga aturan tren seperti A1.", "",
          "### B2 · Moon bag (cicilan bulanan USD 100 ke komposisi 70/15/15)", ""]
    L += md_table(["Versi", "Total setor", "Nilai akhir", "Kelipatan", "Turun terdalam (nilai ÷ setoran)", "Hasil"],
                  [["Dengan moon bag", f"USD {moon['cicilan']['setor']:,.0f}".replace(",", "."),
                    f"USD {moon['cicilan']['nilai']:,.0f}".replace(",", "."),
                    f"{num(moon['cicilan']['kelipatan'])}×", pc(-moon['cicilan']['dd'], 0),
                    "**lolos**" if moon.get("lolos") else "gagal"],
                   ["Tanpa moon bag", f"USD {tanpa['cicilan']['setor']:,.0f}".replace(",", "."),
                    f"USD {tanpa['cicilan']['nilai']:,.0f}".replace(",", "."),
                    f"{num(tanpa['cicilan']['kelipatan'])}×", pc(-tanpa['cicilan']['dd'], 0), "patokan"]])
    L += ["", "Menjual separuh saat harga 2× membuat modal \"aman\", tetapi di kripto 2018–2026 itu memotong kenaikan "
          "berikutnya yang jauh lebih besar, dan kas hasil penjualan tidak berbunga.", "",
          "### B7 · Pola grafik (pemilihan G-17 yang sama dengan 30 setup sebelumnya)", ""]
    rows = []
    for cls in ALL_POLA:
        for market, label in [("forex", "Forex (EURUSD, XAUUSD)"), ("crypto", "Kripto (BTC, ETH)")]:
            r = pola[market][cls.id]
            c = r.get("chosen", {})
            dev, sel = c.get("dev", {}), c.get("sel", {})
            fin = r.get("final", {}).get("final") if isinstance(r.get("final"), dict) else None
            rows.append([f"{cls.id} {cls.name}" if market == "forex" else "", label,
                         f"{dev.get('trades', 0)} trx · {pc(dev.get('net_pct', 0))}",
                         f"{sel.get('trades', 0)} trx · {pc(sel.get('net_pct', 0))}",
                         f"{fin['trades']} trx · {pc(fin['net_pct'])}" if fin else "–", r["status"]])
    L += md_table(["Setup", "Pasar", "Penyusunan", "Pemilihan", "Uji akhir", "Status"], rows)
    L += ["", "- **Harmonic hampir tidak pernah muncul** dengan rasio persis dari mentor dan titik swing yang objektif: "
          "0–5 transaksi per pasar dalam 9–16 tahun, jadi tidak bisa dinilai. Di grafik, pola ini sering \"terlihat\" "
          "karena mata kita memilih titik yang cocok.",
          "- **Pola klasik** banyak muncul, tetapi di forex semuanya rugi di data penyusunan atau pemilihan. Di kripto, "
          "head & shoulders dan broadening untung di 2017–2024 lalu rugi di uji akhir — persis pola setup mentor "
          "sebelumnya.", "",
          "### Modul yang tidak bisa diuji", ""]
    L += md_table(["Modul", "Alasan"], [
        ["Elliott Wave, Andrews Pitchfork", "Penghitungan gelombang / pemilihan titik pivot subjektif"],
        ["Akselerasi/deselerasi", "Mentor tidak memberi angka"],
        ["Wyckoff spring/UTAD", "Butuh penilaian tahap A–E; versi yang bisa dikodekan (AFS-06) sudah diuji dan gagal"],
        ["Order flow", "Mentor tidak menyebut entry, SL, dan TP"],
        ["Token baru (TGE)", "Butuh data valuasi investor tiap token"],
        ["Screening altcoin", "Filter untuk setup trading altcoin; butuh data dominasi BTC historis"],
        ["Valuasi Ko Andri, bandarmologi Ko Hengki, ARA/ARB",
         "Data saham BEI yang tersedia hanya 61 saham besar sejak 2023, tanpa riwayat fundamental dan broker summary. "
         "Kalau Anda punya ekspor data (misalnya dari Stockbit), modul ini bisa diuji"]])

    L += ["", "## Kesimpulan", "",
          "Ilmu baru dari uji ini:", "",
          "1. **Di kripto, keunggulan yang bisa dibuktikan adalah menghindari pasar bear, bukan menebak titik masuk.** "
          "Tiga aturan yang lolos (A1, B3, B6) semuanya bekerja dengan cara keluar atau tidak masuk saat tren turun.",
          "2. **Biaya menentukan segalanya.** Strategi yang terbukti di riset (trend-following multi-aset) berubah dari "
          "untung menjadi rugi hanya karena biaya pembiayaan CFD.",
          "3. **Pola grafik yang \"terlihat\" di chart sering tidak muncul kalau aturannya dibuat objektif**, atau muncul "
          "tetapi tidak bertahan di data baru.", "",
          "Batasan yang tetap berlaku: 12 versi kripto diuji, jadi sebagian yang lolos bisa karena kebetulan; periode "
          "2018–2026 termasuk kenaikan besar kripto yang belum tentu terulang; biaya exchange berizin OJK dan pajak "
          "transaksi kripto di Indonesia belum dihitung.", "",
          "**Cara memakai (semi-otomatis):**", "",
          "```bash", "python -m bot.data.download kripto_harian", "```", "",
          "```bash", "python scripts/sinyal.py", "```", "",
          "Bagian \"Kripto spot tanpa leverage\" di laporan sinyal memberi status hari ini untuk BTC dan ETH: PEGANG "
          "atau STABLECOIN, menurut A1 dan B6. Eksekusi di open berikutnya, tanpa leverage, dan hanya dengan uang yang "
          "siap turun separuhnya.", ""]
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"ditulis: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    laporan()
