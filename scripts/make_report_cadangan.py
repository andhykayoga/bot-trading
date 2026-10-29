"""Laporan rencana cadangan (tahap 1–3) dalam bahasa sederhana.

    python scripts/make_report_cadangan.py

Membaca reports/hasil_cadangan/ dan reports/hasil_crypto/, menulis
reports/LAPORAN_RENCANA_CADANGAN.md dan grafik di reports/grafik/.
Aturan penilaian mengikuti pra-registrasi di reports/RENCANA_CADANGAN.md.
"""
from __future__ import annotations

import math
import pickle
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.make_report import (BLUE, GRID, INK, INK2, RED, SURF, decimal_comma, num, pct,  # noqa: E402
                                 ptext, reason_unrated, seg_cells)

HC = ROOT / "reports" / "hasil_cadangan"
HK = ROOT / "reports" / "hasil_crypto"
HF = ROOT / "reports" / "hasil"
GRAFIK = ROOT / "reports" / "grafik"
REPORT = ROOT / "reports" / "LAPORAN_RENCANA_CADANGAN.md"
YEARS_FX = 16.8   # 2010-01-04 – 2026-10-29


def cagr(net_pct: float, years: float) -> float:
    g = 1 + net_pct / 100
    return 100 * (g ** (1 / years) - 1) if g > 0 else -100.0


def small_multiples(series: dict[str, pd.Series], name: str, title: str, cols: int = 2) -> str:
    n = len(series)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(7.5, 2.3 * rows + 0.6), dpi=150, squeeze=False)
    fig.patch.set_facecolor(SURF)
    for k, (label, s) in enumerate(series.items()):
        ax = axes[k // cols][k % cols]
        ax.set_facecolor(SURF)
        s = (s / s.iloc[0] - 1) * 100
        ax.plot(s.index, s.values, color=BLUE if s.iloc[-1] >= 0 else RED, lw=1.6)
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(f"{label}: {s.iloc[-1]:+.1f}%".replace(".", ","), fontsize=9, color=INK, loc="left")
        ax.tick_params(colors=INK2, labelsize=7)
        ax.grid(axis="y", color=GRID, lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(GRID)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
        ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(base=2 if (s.index[-1] - s.index[0]).days > 3000 else 1))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    for k in range(n, rows * cols):
        axes[k // cols][k % cols].axis("off")
    fig.suptitle(title, x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout()
    GRAFIK.mkdir(parents=True, exist_ok=True)
    out = GRAFIK / f"{name}.png"
    fig.savefig(out, facecolor=SURF)
    plt.close(fig)
    return out.relative_to(ROOT / "reports").as_posix()


def eq_series(pairs) -> pd.Series:
    return pd.Series([v for _, v in pairs], index=pd.to_datetime([d for d, _ in pairs]))


def main():
    hc = pickle.loads((HC / "hasil.pkl").read_bytes())
    s1, s3 = hc["stage1"], hc["stage3"]
    clong = pickle.loads((HC / "crypto_long.pkl").read_bytes()) if (HC / "crypto_long.pkl").exists() else {}
    kmeta = pickle.loads((HK / "_meta.pkl").read_bytes())
    kres = {sid: pickle.loads((HK / f"{sid}.pkl").read_bytes()) for sid in kmeta["order"]}
    fx_trials = sum(pickle.loads(f.read_bytes())["trials"] for f in HF.glob("*.pkl") if not f.name.startswith("_"))
    k_trials = sum(r["trials"] for r in kres.values())
    ksp = kmeta["splits"]

    # ------------------------------------------------ tahap 1: penilaian sesuai pra-registrasi
    verdict1 = {}
    for vid, v in s1.items():
        u, d = v["uji"], v["rancangan"]
        f = u["full"]
        lolos = f["trades"] >= 30 and f["net"] > 0
        segs_pos = sum(u[s]["net"] > 0 for s in ("dev", "sel", "final"))
        c = cagr(f["net_pct"], YEARS_FX)
        layak = lolos and d["full"]["net"] > 0 and segs_pos >= 2 and c >= 2 and f["max_dd_pct"] <= 20
        verdict1[vid] = {"lolos": lolos, "layak": layak, "segs_pos": segs_pos, "cagr": c}
    k_final = [sid for sid, r in kres.items() if "final" in r]
    for sid in k_final:
        kres[sid]["trades_final"].to_csv(HK / f"transaksi_uji_akhir_{sid}.csv", index=False)
    k_pass = [sid for sid in k_final if kres[sid]["status"] == "lolos"]
    t3 = {k: s3[k]["full"] for k in s3}

    L = []
    w = L.append
    w("# Laporan rencana cadangan: perbaikan terbatas, kripto, dan patokan riset\n")
    w("Dibuat otomatis oleh `scripts/make_report_cadangan.py`. Rencana, data, dan aturan penilaiannya sudah ditulis dan "
      "di-commit **sebelum** pengujian, di [`RENCANA_CADANGAN.md`](RENCANA_CADANGAN.md). Tidak ada aturan yang diubah "
      "setelah hasil terlihat.\n")

    # ------------------------------------------------ jawaban singkat
    w("## Jawaban singkat\n")
    v_txt = "; ".join(f"{vid} {pct(s1[vid]['uji']['full']['net_pct'])} ({s1[vid]['uji']['full']['trades']} transaksi)"
                      for vid in s1)
    w(f"1. **Perbaikan terbatas (tahap 1), dinilai di GBPUSD + USDJPY yang belum pernah disentuh:** {v_txt}. "
      f"**{sum(x['lolos'] for x in verdict1.values())} dari {len(s1)} versi lolos.** V4 sama sekali tidak menghasilkan "
      "transaksi: di H1, aturan TP mentor (likuiditas terdekat dengan RR ≥ 1:2) tidak pernah terpenuhi.")
    kf = "; ".join(f"{sid} {pct(kres[sid]['final']['final']['net_pct'])}" for sid in k_final)
    w(f"2. **Setup mentor saham–kripto di BTC & ETH (tahap 2):** {len(k_final)} dari {len(kres)} setup lolos syarat "
      f"di data penyusunan & pemilihan (2017–2024), sebagian dengan untung besar. Tetapi di uji akhir "
      f"({ksp['uji akhir'][0][:10]} – {ksp['uji akhir'][1][:10]}) **semuanya rugi**: {kf}. "
      f"**{len(k_pass)} lolos.** Versi long saja (akun spot) juga rugi.")
    w(f"3. **Patokan riset, time-series momentum (tahap 3):** di GBPUSD + USDJPY hasilnya {pct(t3['forex_uji']['cagr_pct'])} "
      f"per tahun (drawdown terburuk {t3['forex_uji']['max_dd_pct']:.0f}%); di BTC + ETH versi long saja "
      f"{pct(t3['crypto_long']['cagr_pct'])} per tahun (drawdown {t3['crypto_long']['max_dd_pct']:.0f}%), tetapi rugi "
      f"{pct(s3['crypto_long']['final']['total_pct'])} di periode uji akhir kripto.")
    w("4. **Bot full otomatis realistis?** **Belum.** Dengan aturan yang ditetapkan sebelum pengujian, tidak ada pilihan "
      "yang layak: semua versi setup mentor rugi di data yang belum pernah disentuh, dan patokan riset pun hanya untung "
      "di kripto dengan hasil yang naik-turun.")
    w("5. **Hasil wajar per tahun:** untuk setup mentor yang diotomatisasi, perkiraan terbaik dari data ini adalah **sekitar "
      "impas sampai rugi** setelah biaya. Untuk pendekatan sistematis terbaik yang diuji (momentum, risiko sasaran ±10% "
      "volatilitas per tahun), sekitar **0% per tahun di forex** dan **±5–7% per tahun di kripto long saja**, dengan drawdown "
      "15–30% dan tahun-tahun rugi. Target 20% per tahun (patokan Ko Andri, AND-03) tidak realistis tanpa risiko yang jauh lebih besar.")
    w("6. **Usulan:** versi **semi-otomatis** — bot memindai sinyal, menghitung lot dan mengingatkan aturan risiko; Anda yang "
      "memutuskan dan mengeksekusi di akun demo dulu, dan setiap sinyal dicatat di jurnal untuk dinilai. Rinciannya di bagian akhir.\n")

    # ------------------------------------------------ varian
    w("## Jumlah varian yang dicoba\n")
    w("| Tahap | Yang diuji | Varian | Data penilaian |")
    w("|---|---|---|---|")
    w(f"| (sebelumnya) backtest forex tahap 2 | 30 setup di EURUSD + XAUUSD | {fx_trials} | uji akhir EURUSD/XAUUSD Jun 2023 – Okt 2026 (sudah terpakai) |")
    w(f"| 1 — perbaikan terbatas | V1–V4, satu konfigurasi terkunci per versi | **4** (tidak ada jalan ulang) | GBPUSD + USDJPY 2010–2026 |")
    w(f"| 2 — kripto | 26 setup mentor saham–kripto, pemilihan G-17 | **{k_trials}** | BTC + ETH {ksp['uji akhir'][0][:10]} – {ksp['uji akhir'][1][:10]} |")
    w("| 3 — patokan riset | time-series momentum, parameter dari makalah | **1** (dijalankan di 4 kumpulan data, tanpa penyetelan) | sama dengan tahap 1 dan 2 |")
    w("")
    w("Makin banyak varian yang dicoba, makin besar kemungkinan ada yang terlihat bagus hanya karena kebetulan (Bailey dkk. 2014). "
      "Karena itu tahap 1 dan 3 sengaja memakai sesedikit mungkin varian.\n")

    # ------------------------------------------------ tahap 1
    w("## Tahap 1 — perbaikan terbatas setup mentor (forex)\n")
    w("Dirancang dengan EURUSD + XAUUSD (data yang sudah terlihat), lalu **dinilai sekali** di GBPUSD + USDJPY. "
      "Periode: 2010–2020 / 2020–2023 / 2023–2026, sama dengan tahap 2.\n")
    w("| Versi | Data rancangan EURUSD+XAUUSD: Trx · Untung/rugi · DD · RF | **Data uji GBPUSD+USDJPY**: Trx · Untung/rugi · DD · RF | "
      "Uji per periode (2010–20 / 20–23 / 23–26) | Per instrumen uji | Lolos? | Layak otomatis? |")
    w("|---|---|---|---|---|---|---|")
    for vid, v in s1.items():
        u, d, vd = v["uji"], v["rancangan"], verdict1[vid]
        per = " / ".join(pct(u[s]["net_pct"]) for s in ("dev", "sel", "final"))
        sym = "; ".join(f"{s} {u['full_sym'][s]['trades']} trx {pct(u['full_sym'][s]['net_pct'])}" for s in u["full_sym"])
        w(f"| **{vid}** {v['name']} | {' · '.join(seg_cells(d['full']))} | {' · '.join(seg_cells(u['full']))} | {per} | "
          f"{sym} | {'ya' if vd['lolos'] else 'tidak'} | {'ya' if vd['layak'] else 'tidak'} |")
    w("")
    w("Aturan \"layak otomatis\" (ditetapkan sebelumnya): lolos, untung juga di data rancangan, untung di ≥ 2 dari 3 periode uji, "
      "hasil ≥ 2% per tahun, dan drawdown ≤ 20%.\n")
    eqs = {f"{vid} (uji)": eq_series(s1[vid]["uji_equity"]) for vid in s1 if s1[vid]["uji"]["full"]["trades"] > 0}
    if eqs:
        w(f"![Tahap 1 di data uji]({small_multiples(eqs, 'cadangan_tahap1_uji', 'Tahap 1: saldo versi perbaikan di GBPUSD + USDJPY')})\n")
    w("**Kenapa gagal, dengan bahasa sederhana:** memindah setup ke timeframe besar memang memperkecil biaya per transaksi, "
      "tetapi jumlah transaksinya juga turun drastis (±40 dalam 16 tahun untuk dua pair), dan sinyalnya sendiri tidak punya "
      "keunggulan yang cukup. Filter kondisi pasar (searah struktur D1) tidak mengubah hasil itu.\n")

    # ------------------------------------------------ tahap 2
    w("## Tahap 2 — setup mentor saham–kripto di pasar asalnya (BTC & ETH)\n")
    w(f"Data spot Binance 5 menit, dibagi menurut tanggal: penyusunan {ksp['penyusunan'][0][:10]} – {ksp['penyusunan'][1][:10]}, "
      f"pemilihan {ksp['pemilihan'][0][:10]} – {ksp['pemilihan'][1][:10]}, uji akhir {ksp['uji akhir'][0][:10]} – "
      f"{ksp['uji akhir'][1][:10]}. Biaya pulang-pergi 0,22% (komisi + spread), leverage 1×, berita FOMC/CPI/NFP.\n")
    w("| Setup | Status | Varian | Pilihan terkunci | Penyusunan: Trx · Untung/rugi · DD · RF | Pemilihan: Trx · Untung/rugi · DD · RF | "
      "**Uji akhir**: Trx · Untung/rugi · DD · RF | Uji akhir long saja |")
    w("|---|---|---|---|---|---|---|---|")
    for sid, r in kres.items():
        src = r.get("final", r["chosen"])
        fin = seg_cells(r["final"]["final"]) if "final" in r else ["–"] * 4
        st = r.get("status")
        if st == "belum bisa dinilai":
            st += f" ({reason_unrated(r)})"
        pre = "(gambaran) " if r.get("status") == "belum bisa dinilai" else ""
        lo = " · ".join(seg_cells(clong[sid]["final"])) if sid in clong else "–"
        w(f"| **{sid}** {r['name']} | {st} | {r['trials']} | {pre}{ptext(r['chosen']['params'])} | "
          f"{' · '.join(seg_cells(src['dev']))} | {' · '.join(seg_cells(src['sel']))} | {' · '.join(fin)} | {lo} |")
    w("")
    if k_final:
        eqk = {sid: eq_series(kres[sid]["equity"]["final"]) for sid in k_final}
        w(f"![Tahap 2 uji akhir]({small_multiples(eqk, 'cadangan_kripto_uji_akhir', 'Tahap 2: saldo di uji akhir kripto')})\n")
    w("**Pola yang terlihat:** setup tren/breakout (Donchian mode tren, CMF breakout, LRC breakout, Ko Hengki breakout H4) sangat "
      "untung di 2017–2024 — periode dengan tren kripto yang kuat — lalu rugi di 2025–2026. Setup pembalikan dan scalping rugi besar "
      "sejak awal karena biaya 0,22% per transaksi terlalu berat untuk timeframe kecil (entry acak di M15 rata-rata "
      f"{kmeta['benchmark']['M15']['avg_r']:+.2f} R per transaksi, di D1 {kmeta['benchmark']['D1']['avg_r']:+.2f} R). "
      "Hasil bagus di data penyusunan dan pemilihan ternyata tidak bertahan di data baru.\n")

    # ------------------------------------------------ tahap 3
    w("## Tahap 3 — patokan dari riset: time-series momentum\n")
    w("Aturan dari Moskowitz, Ooi & Pedersen (2012) dan Hurst, Ooi & Pedersen (2017): tiap akhir bulan, pegang long kalau "
      "harga lebih tinggi dari 12 bulan lalu dan short kalau lebih rendah; ukuran posisi diatur supaya volatilitas portofolio "
      "±10% per tahun. Di riset aslinya, aturan ini diuji di puluhan pasar berjangka sekaligus (58 di makalah 2012, 67 sejak "
      "1880 di makalah 2017) dan hasilnya positif dalam jangka panjang. Di sini hanya ada 2 instrumen per pasar, jadi manfaat "
      "diversifikasinya jauh lebih kecil.\n")
    w("| Data | Seluruh periode: hasil/tahun · drawdown · Sharpe | Periode 1 | Periode 2 | Periode 3 (uji akhir) | Biaya spread + swap |")
    w("|---|---|---|---|---|---|")
    names = {"forex_uji": "GBPUSD + USDJPY (data uji tahap 1)", "forex": "EURUSD + XAUUSD (instrumen bot)",
             "crypto": "BTC + ETH, long & short", "crypto_long": "BTC + ETH, long saja (spot)"}
    for k, nm in names.items():
        x = s3[k]
        cell = lambda d: f"{pct(d['cagr_pct'])}/th · {d['max_dd_pct']:.1f}% · {num(d['sharpe'])}"
        w(f"| {nm} | {cell(x['full'])} | {pct(x['dev']['total_pct'])} | {pct(x['sel']['total_pct'])} | "
          f"{pct(x['final']['total_pct'])} | {-100 * x['full']['costs']:.1f}% + {100 * x['full']['swap']:.1f}% |")
    w("")
    w("Periode forex: 2010–2020 / 2020–2023 / 2023–2026. Periode kripto: sama dengan tahap 2. Kripto baru punya sinyal setelah "
      "data 12 bulan pertama (mulai Agustus 2018). Sharpe = hasil rata-rata ÷ naik-turunnya; di bawah 0,5 tergolong lemah.\n")
    eqt = {nm.split(" (")[0]: eq_series(s3[k]["equity"]) for k, nm in names.items()}
    w(f"![Patokan TSMOM]({small_multiples(eqt, 'cadangan_tsmom', 'Tahap 3: time-series momentum (volatilitas sasaran ±10%/tahun)')})\n")
    w("**Arti hasil ini:** bahkan pendekatan yang terbukti di riset hampir tidak menghasilkan apa-apa di 2 pair forex selama "
      "2010–2026 (swap CFD menggerus ±1–2% per tahun karena posisi dipegang terus), dan di kripto hasilnya bergantung pada beberapa tahun tren kuat (2020, 2021, 2024). "
      "Jadi kegagalan setup mentor bukan karena kode bot, tetapi karena keunggulan yang bisa diotomatisasi di pasar ini memang kecil.\n")

    # ------------------------------------------------ perbandingan
    w("## Perbandingan di data yang belum pernah disentuh\n")
    best_v = max((x for x in s1 if s1[x]["uji"]["full"]["trades"] > 0), key=lambda x: s1[x]["uji"]["full"]["net_pct"])
    w("| Pendekatan | Data penilaian | Hasil |")
    w("|---|---|---|")
    w(f"| Setup mentor diperbaiki (terbaik: {best_v}) | GBPUSD + USDJPY 2010–2026 | {pct(s1[best_v]['uji']['full']['net_pct'])} total, "
      f"drawdown {s1[best_v]['uji']['full']['max_dd_pct']:.1f}% |")
    w(f"| Time-series momentum | GBPUSD + USDJPY 2010–2026 | {pct(s3['forex_uji']['full']['total_pct'])} total "
      f"({pct(t3['forex_uji']['cagr_pct'])}/th), drawdown {t3['forex_uji']['max_dd_pct']:.1f}% |")
    if k_final:
        best_k = max(k_final, key=lambda x: kres[x]["final"]["final"]["net_pct"])
        w(f"| Setup mentor di kripto (terbaik: {best_k}) | BTC + ETH uji akhir | {pct(kres[best_k]['final']['final']['net_pct'])}, "
          f"drawdown {kres[best_k]['final']['final']['max_dd_pct']:.1f}% |")
    w(f"| Time-series momentum, long saja | BTC + ETH uji akhir | {pct(s3['crypto_long']['final']['total_pct'])}, "
      f"drawdown {s3['crypto_long']['final']['max_dd_pct']:.1f}% |")
    w("")

    # ------------------------------------------------ kesimpulan
    w("## Kesimpulan jujur\n")
    w("**Bot full otomatis belum realistis.** Tiga jalur cadangan sudah dicoba berurutan dengan aturan yang ditetapkan di depan:")
    w("1. Perbaikan terbatas setup mentor: tidak ada yang untung di pair yang belum pernah disentuh.")
    w("2. Setup mentor saham–kripto di pasar asalnya: untung besar di 2017–2024, tetapi semuanya rugi di 22 bulan terakhir yang "
      "belum pernah dilihat. Pola ini — bagus di data lama, gagal di data baru — adalah tanda klasik hasil yang tidak bisa diandalkan.")
    w("3. Patokan riset: sekitar impas di forex; di kripto long saja positif dalam jangka panjang tetapi juga rugi di periode terakhir.\n")
    w("Catatan adil: periode uji akhir kripto hanya ±22 bulan dan sebagian besar berupa pasar turun/menyamping. Strategi tren "
      "memang biasa mengalami periode rugi panjang, jadi kegagalan ini belum membuktikan bahwa setup tren kripto *tidak punya* "
      "keunggulan sama sekali. Tetapi data ini juga tidak bisa membuktikan sebaliknya, dan menurut aturan yang ditetapkan di depan, "
      "hasilnya tidak lolos. Satu-satunya cara jujur untuk tahu adalah mengamati ke depan (demo), bukan menguji ulang data yang sama.\n")
    w("**Hasil per tahun yang wajar diharapkan** dari bot yang benar-benar otomatis di pasar ini, berdasarkan data uji: "
      "**sekitar 0% (forex) sampai ±5–7% per tahun (kripto, momentum long saja)**, dengan drawdown 15–30% dan beberapa tahun rugi. "
      "Angka ini pada risiko sasaran ±10% volatilitas per tahun; menggandakan ukuran posisi kira-kira menggandakan hasil **dan** "
      "drawdown-nya. "
      "Riset momentum yang lebih luas (puluhan pasar) melaporkan hasil positif jangka panjang, tetapi itu butuh diversifikasi yang "
      "tidak tersedia dengan 2–4 instrumen. Angka 20% per tahun ke atas secara konsisten tidak didukung data ini.\n")
    w("**Yang paling mendekati** untuk diamati lebih lanjut (bukan untuk uang sungguhan): momentum bulanan long saja di BTC/ETH, "
      "dan keluarga setup tren/breakout di kripto H4 (AFS-16T, AFS-18, AFS-20B, HKI-01-H4). Keduanya hanya untung saat pasar sedang "
      "tren kuat.\n")

    # ------------------------------------------------ semi otomatis
    w("## Usulan versi semi-otomatis (bot memberi sinyal, Anda yang mengeksekusi)\n")
    w("Sudah dibuat di `scripts/sinyal.py`, tanpa koneksi broker:\n")
    w("1. Perbarui data: `python -m bot.data.download forex crypto`.")
    w("2. Jalankan `python scripts/sinyal.py`. Hasilnya `reports/sinyal/<tanggal>.md`: order baru dari setup yang Anda pilih di "
      "`config/sinyal.toml` (entry, SL, TP, RR, ukuran posisi untuk saldo Anda), posisi momentum bulan ini, peringatan berita 1 jam "
      "ke depan, dan daftar aturan risiko yang harus Anda jaga (maks 3 transaksi/hari, rem 3%/6%/15%).")
    w("3. Anda memutuskan mengambil atau tidak, lalu mengeksekusi sendiri di broker/exchange dengan SL dan TP dipasang bersamaan.")
    w("4. Setiap sinyal otomatis ditambahkan ke `reports/sinyal/jurnal.csv`. Isi kolom `diambil` dan `hasil_R`.\n")
    w("**Kenapa semi-otomatis dan bukan otomatis:** sebagian ajaran mentor memang butuh \"mata\" trader (Elliott Wave, Wyckoff spring, "
      "konteks berita, kondisi pasar sideways), yang tidak bisa dikodekan dengan adil. Mode ini memberi bot pekerjaan yang ia kuasai "
      "(memindai, menghitung lot, menjaga aturan risiko) dan menyerahkan penilaian ke Anda.\n")
    w("**Tetapi harus jujur:** belum ada bukti bahwa penilaian manual mengubah setup yang rugi menjadi untung. Karena itu:")
    w("- Mulai di **akun demo** (G-14, Q-03).")
    w("- Setelah **minimal 30 sinyal yang diambil** atau 6 bulan, bandingkan di jurnal: apakah transaksi yang Anda ambil untung "
      "setelah biaya, dan apakah lebih baik daripada semua sinyal (termasuk yang dilewati)? Kalau tidak, penilaian manual tidak "
      "menambah keunggulan.")
    w("- Risiko per transaksi tetap maksimal 1% dan rem darurat tetap berlaku.\n")

    w("## Keterbatasan\n")
    w("- GBPUSD/USDJPY menguji \"pasar lain di waktu yang sama\", bukan masa depan; GBPUSD cukup mirip EURUSD.")
    w("- Biaya memakai angka tetap (spread ritel, komisi Binance 0,1%); exchange berizin OJK bisa lebih mahal. Short kripto di "
      "backtest tanpa biaya funding.")
    w("- Suku bunga swap dan jadwal rapat BoE/BoJ setelah April 2025 adalah perkiraan.")
    w("- Jumlah transaksi versi D1 kecil (±40 per 16 tahun untuk dua pair), jadi hasil per versi masih banyak dipengaruhi kebetulan.\n")
    w("## File\n")
    w("- `reports/RENCANA_CADANGAN.md` — pra-registrasi (ditulis sebelum pengujian).")
    w("- `reports/hasil_cadangan/transaksi_V*_uji.csv` — transaksi versi perbaikan di data uji.")
    w("- `reports/hasil_crypto/transaksi_uji_akhir_<setup>.csv` — transaksi uji akhir kripto.")
    REPORT.write_text(decimal_comma("\n".join(L)) + "\n")
    print("laporan:", REPORT)


if __name__ == "__main__":
    main()
