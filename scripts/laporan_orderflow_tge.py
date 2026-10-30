"""Tulis reports/LAPORAN_ORDERFLOW_TGE.md dari hasil scripts/run_orderflow_tge.py --orderflow --tge."""
from __future__ import annotations

import pickle
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research.tge import VALUASI  # noqa: E402
from scripts.laporan_modul_baru import md_table, num, pc  # noqa: E402

OUT = ROOT / "reports" / "hasil_orderflow_tge"
REPORT = ROOT / "reports" / "LAPORAN_ORDERFLOW_TGE.md"
DICARI_TANPA_VALUASI = ["ZK", "MOVE", "ETHFI", "DYM", "ALT", "TNSR", "AEVO", "JTO", "CYBER", "ARKM", "ID", "USUAL",
                        "VANA", "BABY", "SOPH", "SAHARA", "PARTI", "HYPER", "BB", "PORTAL", "PIXEL", "HUMA", "RESOLV",
                        "MAV", "LISTA", "KERNEL", "GPS", "SIGN", "KAITO", "RED", "WCT", "NTRN", "NFP"]
NAMA = {"AFS-16T":"AFS-16T (Supertrend tren)", "AFS-18": "AFS-18 (breakout)", "AFS-20B": "AFS-20B (breakout)",
        "HKI-01-H4": "HKI-01-H4 (tren Ko Hengki)"}


def usd(x):
    if x >= 1e9:
        return f"${num(x / 1e9, 1)} M".replace(",0 M", " M")
    return f"${x / 1e6:.0f} jt"


def harga(x):
    return num(x, 4 if x < 0.1 else 3 if x < 1 else 2)


def bagian_orderflow(of) -> list[str]:
    a = of["afs22d"]
    rows = []
    for t in a["tried"]:
        p = t["params"]
        rows.append([p["tf"], num(p["sl_atr"], 1), f"{t['dev']['trades']}", pc(t["dev"]["net_pct"]),
                     f"{t['sel']['trades']}", pc(t["sel"]["net_pct"])])
    frows = []
    for sid, f in of["filter"].items():
        a0, a1 = f["tanpa"], f["dengan"]
        frows.append([NAMA[sid],
                      f"{pc(a0['dev']['net_pct'])} → {pc(a1['dev']['net_pct'])}",
                      f"{pc(a0['sel']['net_pct'])} → {pc(a1['sel']['net_pct'])}",
                      f"{pc(a0['final']['net_pct'])} ({a0['final']['trades']}) → "
                      f"{pc(a1['final']['net_pct'])} ({a1['final']['trades']})",
                      "lolos (tipis)" if a1["final"]["net_pct"] > 0 and a1["final"]["trades"] >= 30
                      and a1["final"]["net_pct"] > a0["final"]["net_pct"] else "tidak lolos"])
    return [
        "## A. Order flow (AFS-22, Alvesting)",
        "",
        "### Yang saya lengkapi dari riset",
        "",
        "Mentor hanya menjelaskan cara membaca delta, tanpa entry, SL, dan TP. Dua penelitian yang saya pakai:",
        "",
        "- [Cont, Kukanov & Stoikov (2014)](https://arxiv.org/abs/1011.6402): ketidakseimbangan beli-jual agresif "
        "menjelaskan gerak harga **pada saat yang sama**, bukan ke depan.",
        "- [Kim & Hansen (2026)](https://arxiv.org/abs/2607.09426), data perpetual Binance 2021–2024: "
        "ketidakseimbangan di awal tiap 15 menit memang meramal arah 4–12 jam ke depan, tetapi besarnya ±0,5 bp, "
        "kira-kira sepersepuluh biaya transaksi. Penulisnya sendiri menyebut ini bukan strategi yang berdiri sendiri.",
        "",
        "Karena itu delta saya pakai sebagai **konfirmasi** di titik yang sudah punya alasan (zona support/resistance, "
        "atau sinyal setup tren/breakout yang sudah ada), di timeframe H1/H4. Data: candle 1 jam spot Binance BTC & ETH "
        "2017–2026 beserta volume beli taker. Data footprint per level harga tidak dipakai karena ukurannya puluhan GB "
        "per bulan, jadi imbalance 300%, stacked imbalance, dan HVN tidak diuji.",
        "",
        "### AFS-22D · candle merah + delta positif di support (dan kebalikannya di resistance)",
        "",
        "Masuk di open candle berikutnya, SL di luar ujung candle sinyal ± sl_atr × ATR, TP 2R. Pemilihan memakai "
        "aturan G-17 yang sama dengan setup lain.",
        "",
        *md_table(["Timeframe", "sl_atr", "Transaksi penyusunan", "Hasil penyusunan", "Transaksi pemilihan",
                   "Hasil pemilihan"], rows),
        "",
        f"Status: **{a['status']}**, karena tidak ada varian yang untung di data penyusunan. Semua varian rugi 83–99% "
        "di 2017–2023. Satu varian (H4, sl_atr 1,5) untung +5% di data pemilihan, tetapi setelah rugi 83% di data "
        "sebelumnya; itu kebetulan, bukan pola. Uji akhir tidak dijalankan.",
        "",
        "### AFS-22F · delta sebagai filter setup yang sudah ada",
        "",
        "Long hanya kalau delta candle sinyal positif, short hanya kalau negatif. Parameter setup tidak diubah.",
        "",
        *md_table(["Setup", "Penyusunan (tanpa → dengan)", "Pemilihan (tanpa → dengan)",
                   "Uji akhir (transaksi)", "Syarat lolos"], frows),
        "",
        "Satu dari empat lolos secara teknis: HKI-01-H4 berubah dari −1,4% menjadi +0,3% di uji akhir. Tetapi:",
        "",
        "- +0,3% dalam hampir dua tahun itu praktis impas, jauh di bawah bunga deposito.",
        "- Di data penyusunan dan pemilihan, filter delta justru **menurunkan** hasil di hampir semua setup (termasuk "
        "HKI-01-H4: 46,1% → 44,1% dan 15,1% → 10,6%). Kalau delta benar-benar membantu, hasilnya harus naik di semua "
        "periode, bukan hanya di satu periode.",
        "- Dengan empat percobaan, satu yang lolos tipis sangat mungkin kebetulan.",
        "",
        "**Kesimpulan order flow:** delta candle (versi yang bisa diuji dari data publik) tidak memberi keunggulan yang "
        "bisa dipakai, sejalan dengan riset di atas: informasinya sudah langsung tercermin di harga.",
        "",
    ]


def bagian_tge(tg) -> list[str]:
    t = tg["token"].merge(pd.read_csv(VALUASI)[["coin", "proyek", "valuasi_usd", "sumber"]], on="coin")
    t = t.sort_values("listing")
    rows = []
    for _, r in t.iterrows():
        rows.append([f"[{r['coin']}]({r['sumber']})" + ("" if r["status"] == "ketat" else "*"),
                     str(r["listing"]), usd(r["valuasi_usd"]), harga(r["lantai"]), harga(r["harga_listing"]),
                     num(r["listing_per_lantai"], 1) + "×",
                     str(r["tgl_base"]) if r["tgl_base"] else "–", f"{r['alasan']} ({r['tgl_keluar']})",
                     pc(100 * r["hasil"], 0), pc(100 * r["tahan_365"], 0), pc(100 * r["btc_365"], 0)])
    s, k = tg["semua"], tg["ketat"]

    def baris(nama, x):
        return [nama, str(x["n"]), pc(100 * x["rata"], 1), pc(100 * x["median"], 1), f"{x['positif']}/{x['n']}",
                pc(100 * x["rata_tahan_365"], 1), pc(100 * x["median_tahan_365"], 1), pc(100 * x["rata_btc_365"], 1),
                "**lolos**" if x["lolos"] else "tidak lolos"]
    alasan = t["alasan"].value_counts()
    return [
        "## B. Token baru / TGE (LIVE-02)",
        "",
        "### Aturan yang diuji",
        "",
        "Dari mentor: tunggu listing spot; **lantai** = valuasi investor terakhir ÷ jumlah token; masuk 30% di harga "
        "listing, 70% di base dekat lantai; cut loss di bawah lantai; target dari FDV. Yang saya lengkapi (dikunci di "
        "`reports/RENCANA_ORDERFLOW_TGE.md` sebelum hasil dihitung): harga listing = close hari pertama di Binance; base "
        "= harga ≤ 50% harga listing, ≤ 1,3 × lantai, dan tidak mencetak low baru selama 14 hari; cut loss di close "
        "< 0,833 × lantai; target di close ≥ 3,33 × lantai; maksimal 730 hari; biaya 0,2% per transaksi.",
        "",
        "### Data valuasi (dikumpulkan dari pemberitaan, tiap angka ada sumbernya)",
        "",
        f"Dari {tg['jumlah_listing_jendela']} pasangan USDT yang mulai diperdagangkan di Binance antara Januari 2023 dan "
        f"Juni 2025, hanya **{s['n']} token** yang valuasi putaran investornya bisa diverifikasi dari berita "
        "(The Block, TechCrunch, Fortune, Decrypt, laporan Arrakis); daftar dan sumbernya di "
        f"`bot/research/tge_valuasi.csv`. {len(DICARI_TANPA_VALUASI)} proyek lain sudah saya cari tetapi valuasinya "
        f"tidak diumumkan atau hanya dari satu sumber yang lemah: {', '.join(DICARI_TANPA_VALUASI)}. Sisanya kebanyakan "
        "bukan TGE (token lama yang baru masuk Binance, stablecoin, ganti nama) atau koin meme/komunitas tanpa investor. "
        "Beberapa token TGE lain tidak sempat dicari (mis. EDU, XAI, AI, ACE, BANANA, GUN, HOME, NEWT, HAEDAL).",
        "",
        "Untuk token yang jumlahnya terus bertambah (inflasi, tanpa batas maksimum), saya pakai jumlah token saat TGE, "
        "karena itu dasar harga yang dibayar investor. Tanda * = putaran sesudahnya tidak mengumumkan valuasi, jadi "
        "yang dipakai valuasi terakhir yang diketahui.",
        "",
        "### Hasil per token",
        "",
        *md_table(["Token", "Listing", "Valuasi", "Lantai ($)", "Harga listing ($)", "Listing ÷ lantai",
                   "Beli base", "Keluar", "Hasil aturan", "Beli-tahan 365 hari", "BTC 365 hari"], rows),
        "",
        "### Ringkasan",
        "",
        *md_table(["Sampel", "Token", "Rata-rata", "Median", "Untung", "Rata-rata beli-tahan 365 hari",
                   "Median beli-tahan 365 hari", "Rata-rata BTC 365 hari", "Syarat lolos"],
                  [baris("Semua", s), baris("Hanya valuasi putaran terakhir (tambahan)", k)]),
        "",
        "Cara keluar: " + ", ".join(f"{v} token {i}" for i, v in alasan.items()) + ".",
        "",
    ]


def pembuka(of, tg) -> list[str]:
    t, s = tg["token"], tg["semua"]
    hki = of["filter"]["HKI-01-H4"]["dengan"]["final"]["net_pct"]
    turun = int((t["tahan_365"] < 0).sum())
    return [
        "# Laporan: order flow dan token baru (TGE)",
        "",
        "Ditulis 29 Oktober 2026. Aturan diuji persis seperti yang dikunci lebih dulu di "
        "`reports/RENCANA_ORDERFLOW_TGE.md` (di-commit sebelum hasil dihitung). Bagian yang tidak dijelaskan mentor "
        "saya lengkapi dari riset dan pemberitaan, dengan sumber yang dicantumkan.",
        "",
        "## Ringkasan",
        "",
        *md_table(["Modul", "Hasil", "Artinya"], [
            ["Order flow AFS-22D: candle berlawanan dengan delta di zona",
             "belum bisa dinilai: semua varian rugi 83–99% di data penyusunan", "jangan dipakai"],
            ["Order flow AFS-22F: delta sebagai filter 4 setup",
             f"1 dari 4 lolos tipis ({pc(hki)} dalam ±2 tahun); di periode lain filter justru menurunkan hasil",
             "tidak ada keunggulan nyata"],
            [f"Token baru LIVE-02 ({s['n']} token)",
             f"tidak lolos: rata-rata {pc(100 * s['rata'])}, median {pc(100 * s['median'])} per token",
             "aturan mentor tidak menghasilkan untung"],
        ]),
        "",
        f"Temuan terpenting justru dari pembandingnya. Token baru di Binance 2023–2025 dibuka rata-rata di "
        f"{num(t['listing_per_lantai'].median(), 1)}× harga yang dibayar investor terakhir (median). Kalau dibeli saat "
        f"listing dan ditahan setahun, {turun} dari {s['n']} token turun, dengan median "
        f"{pc(100 * s['median_tahan_365'], 0)}. \"Lantai\" valuasi investor juga tidak menahan harga: "
        f"{int((t['terendah_per_lantai'] < 1).sum())} dari {s['n']} token pernah jatuh di bawah lantai dalam dua tahun.",
        "",
    ]


def tge_baca(tg) -> list[str]:
    t, s = tg["token"], tg["semua"]
    langsung = t[t["listing_per_lantai"] >= 3.33]
    nanti = t[(t["listing_per_lantai"] < 3.33) & (t["alasan"] == "target")]
    base = t[t["tgl_base"].notna()]
    lewati = t["hasil"].where(t["listing_per_lantai"] < 3.33, 0.0)
    naik = ", ".join(t.loc[t["tahan_365"] > 0, "coin"])
    return [
        "### Cara membaca hasilnya",
        "",
        f"- **{len(langsung)} dari {s['n']} token** sudah listing di atas target (3,33 × lantai). Aturan langsung "
        "menjual porsi 30% di hari kedua, jadi hasilnya kecil, antara "
        f"{pc(100 * langsung['hasil'].min(), 0)} dan {pc(100 * langsung['hasil'].max(), 0)}. "
        f"{len(nanti)} token lain ({', '.join(nanti['coin'])}) naik ke target sesudahnya ("
        + ", ".join(pc(100 * x, 0) for x in nanti["hasil"]) + ").",
        f"- Hanya **{len(base)} token** yang turun cukup dalam sehingga porsi 70% dibeli di \"base dekat lantai\" "
        f"({', '.join(base['coin'])}). Semuanya lalu kena cut loss ("
        + ", ".join(pc(100 * x, 0) for x in base["hasil"]) + ") karena harga terus turun menembus lantai.",
        f"- *(Tambahan, bukan syarat lolos)* Kalau token yang listing di atas target dilewati saja (tidak dibeli sama "
        f"sekali), rata-rata per token tetap negatif: {pc(100 * lewati.mean())}.",
        f"- **Lantai bukan support.** {int((t['terendah_per_lantai'] < 1).sum())} dari {s['n']} token pernah di bawah "
        f"lantai, dan {int((t['akhir_per_lantai'] < 1).sum())} berada di bawah lantai pada hari ke-730 (atau di data "
        "terakhir kalau belum genap dua tahun). Valuasi investor bukan harga yang dijaga siapa pun; investor awal justru "
        "sering menjual setelah token mereka terbuka.",
        f"- **Pembanding beli saat listing, tahan 365 hari:** rata-rata {pc(100 * s['rata_tahan_365'], 0)}, median "
        f"{pc(100 * s['median_tahan_365'], 0)}; hanya {naik} yang naik. BTC di tanggal yang sama rata-rata "
        f"{pc(100 * s['rata_btc_365'], 0)}. Jadi aturan mentor jauh lebih baik daripada membeli saat listing, terutama "
        "karena aturan itu membuat Anda hampir selalu cepat keluar atau tidak masuk sama sekali.",
        "",
        "### Catatan kejujuran",
        "",
        f"- Sampel {s['n']} token hanya sedikit di atas syarat minimum 20. Valuasi yang diberitakan kebanyakan milik "
        "proyek besar dan terkenal; token kecil bisa berperilaku lain.",
        "- Sebagian valuasi berasal dari sumber anonim atau agregator (SCR, TIA, ENA, SOLV, OMNI). Valuasi perusahaan "
        "juga tidak selalu sama dengan valuasi token. Hasil hanya-valuasi-putaran-terakhir ditampilkan terpisah di atas "
        "dan kesimpulannya sama.",
        "- Harga listing = close hari pertama. Candle pertama Binance kadang dimulai dari harga yang tidak bisa didapat "
        "(misalnya OMNI dibuka $1 lalu ditutup $27), jadi open hari pertama tidak dipakai.",
        "- Token yang sudah dihapus dari Binance ikut dicari. OMNI masuk sampel; NTRN dan NFP tidak punya valuasi yang "
        "bisa diverifikasi.",
        "",
    ]


def penutup() -> list[str]:
    return [
        "## Apa artinya untuk Anda",
        "",
        "- **Order flow:** untuk BTC/ETH di H1/H4, informasi delta candle sudah tercermin di harga. Tidak perlu "
        "membeli alat footprint/order flow untuk tujuan ini.",
        "- **Token baru:** bagian aturan mentor yang berguna adalah bagian **menahan diri**: jangan beli di pre-market "
        "atau saat listing kalau harga sudah berkali-kali lipat valuasi investor. Bagian \"beli di base dekat lantai\" "
        "tidak terbukti, karena lantai tidak menahan harga.",
        "- Ini sejalan dengan laporan sebelumnya: yang terbukti tetap aturan sederhana di BTC/ETH (filter tren SMA 200, "
        "trailing stop) dan rencana investasi di `reports/RENCANA_UNTUNG.md`.",
        "- **Valuasi Ko Andri dan bandarmologi Ko Hengki** menunggu data saham. Panduannya ada di "
        "`reports/PANDUAN_DATA_STOCKBIT.md`.",
        "",
        "## Cara mengulang",
        "",
        "```bash",
        "python -m bot.data.download orderflow tge",
        "python scripts/run_orderflow_tge.py --orderflow --tge",
        "python scripts/run_orderflow_tge.py",
        "```",
    ]


def laporan() -> None:
    of = pickle.loads((OUT / "orderflow.pkl").read_bytes())
    tg = pickle.loads((OUT / "tge.pkl").read_bytes())
    lines = [*pembuka(of, tg), *bagian_orderflow(of), *bagian_tge(tg), *tge_baca(tg), *penutup()]
    REPORT.write_text("\n".join(lines) + "\n")
    print("tulis", REPORT.relative_to(ROOT))
