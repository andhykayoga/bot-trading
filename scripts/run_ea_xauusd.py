"""Uji tipe EA XAUUSD yang viral (reports/RENCANA_EA_XAUUSD.md) dan tulis laporannya.

    python scripts/run_ea_xauusd.py            # pakai hasil tersimpan kalau ada
    python scripts/run_ea_xauusd.py --ulang    # hitung ulang semuanya (±5 menit)

Menulis reports/LAPORAN_EA_XAUUSD.md, grafik di reports/grafik/, ringkasan CSV di reports/hasil_ea_xauusd/.
"""
from __future__ import annotations

import argparse
import math
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bot.research import ea_xauusd as ea  # noqa: E402
from scripts.make_report import BLUE, GRID, INK, INK2, RED, SURF  # noqa: E402

ORANGE, AQUA = "#eb6834", "#1baf7a"
OUT = ROOT / "reports" / "hasil_ea_xauusd"
GRAFIK = ROOT / "reports" / "grafik"
REPORT = ROOT / "reports" / "LAPORAN_EA_XAUUSD.md"
NAMA = {"E1": "E1 Grid martingale beli saja", "E2": "E2 Grid martingale dua arah", "E3": "E3 Breakout sesi London",
        "BH": "Beli-dan-tahan emas (CFD, bayar swap)", "BH_harga": "Harga emas saja"}
SENS = [(s, m) for s in (0.005, 0.01, 0.02) for m in (1.2, 1.5, 2.0)]
VIRAL = "Periode viral 2024–2026"
FULL = "Seluruh 2010–2026"


def usd(x: float) -> str:
    return ("-" if x < 0 else "") + f"USD {abs(x):,.0f}".replace(",", ".")


def ribuan(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def pc(x: float, nd: int = 1, plus: bool = False) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    return (f"{x:+.{nd}f}%" if plus else f"{x:.{nd}f}%").replace(".", ",")


def md_table(head: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    return out + ["| " + " | ".join(r) + " |" for r in rows]


def _sens(args):
    step, mult = args
    d = ea.load(*ea.PERIODE[FULL])
    return step, mult, ea.grid(d, (1,), step=step, mult=mult).ringkas()


def hitung() -> tuple[dict, list]:
    res = {(n, p): ea.jalankan(n, a, z) for n in NAMA for p, (a, z) in ea.PERIODE.items()}
    with ProcessPoolExecutor(4) as ex:
        sens = list(ex.map(_sens, SENS))
    return res, sens


def _sumbu_usd(ax) -> None:
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", "."))
    ax.yaxis.set_major_formatter(fmt)
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def _gaya(ax) -> None:
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_facecolor(SURF)


def grafik_viral(h: ea.Hasil, r: dict, out: Path) -> None:
    eq = pd.Series(h.ekuitas, index=pd.to_datetime(h.t)).resample("4h").last().dropna()
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=150)
    ax.plot(eq.index, eq.values, color=BLUE, lw=1.2)
    hb = pd.DatetimeIndex(h.habis)
    y = eq.reindex(hb, method="ffill")
    ax.scatter(hb, [max(v, 1) for v in y.values], s=14, color=RED, zorder=3, edgecolor=SURF, lw=0.8,
               label="Akun habis (stop-out), diisi lagi USD 1.000")
    ax.set_yscale("log")
    _sumbu_usd(ax)
    ax.set_ylabel("Ekuitas (USD, skala log)", color=INK2, fontsize=9)
    ax.set_title(f"E1 grid martingale beli saja, 2024–2026: {pc(r['menang'])} transaksi menang, "
                 f"akun habis {r['habis']} kali", color=INK, fontsize=10, loc="left")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    _gaya(ax)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def grafik_tanpa_martingale(res: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=150)
    pendek = {"E3": "EA breakout", "BH": "Beli-tahan CFD", "BH_harga": "Harga emas"}
    for n, color in [("E3", BLUE), ("BH", ORANGE), ("BH_harga", AQUA)]:
        h = res[(n, FULL)]
        eq = pd.Series(h.ekuitas, index=pd.to_datetime(h.t)).resample("D").last().dropna()
        ax.plot(eq.index, eq.values, color=color, lw=1.5)
        ax.annotate(f"{pendek[n]}\n{usd(eq.iloc[-1])}", (eq.index[-1], eq.iloc[-1]), xytext=(6, 0),
                    textcoords="offset points", ha="left", va="center", fontsize=8, color=INK)
    ax.axhline(ea.MODAL, color=INK2, lw=0.8, ls="--")
    ax.set_yscale("log")
    ax.set_yticks([500, 1000, 2000, 4000])
    _sumbu_usd(ax)
    ax.set_xlim(right=pd.Timestamp("2029-06-01"))
    ax.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2010, 2027, 2)])
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    ax.set_ylabel("Ekuitas dari USD 1.000 (skala log)", color=INK2, fontsize=9)
    ax.set_title("Tanpa martingale: EA breakout vs emas dibeli dan disimpan, 2010–2026", color=INK, fontsize=10,
                 loc="left")
    _gaya(ax)
    fig.patch.set_facecolor(SURF)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURF); plt.close(fig)


def laporan(res: dict, sens: list) -> None:
    GRAFIK.mkdir(parents=True, exist_ok=True)
    R = {k: h.ringkas() for k, h in res.items()}
    rows = [dict(ea=n, periode=p, **{k: v for k, v in R[(n, p)].items() if k != "habis_pertama"})
            for n, p in R]
    pd.DataFrame(rows).to_csv(OUT / "ringkasan.csv", index=False)
    pd.DataFrame([dict(jarak_grid=s, pengali=m, **{k: v for k, v in r.items() if k != "habis_pertama"})
                  for s, m, r in sens]).to_csv(OUT / "sensitivitas_grid.csv", index=False)
    grafik_viral(res[("E1", VIRAL)], R[("E1", VIRAL)], GRAFIK / "ea_xauusd_viral.png")
    grafik_tanpa_martingale(res, GRAFIK / "ea_xauusd_tanpa_martingale.png")

    e1, e1v, e2, e3 = R[("E1", FULL)], R[("E1", VIRAL)], R[("E2", FULL)], R[("E3", FULL)]
    bh, bhh, bhv, bhhv = R[("BH", FULL)], R[("BH_harga", FULL)], R[("BH", VIRAL)], R[("BH_harga", VIRAL)]
    e3v = R[("E3", VIRAL)]
    s_habis = [r["habis"] for _, _, r in sens]
    s_umur = max(r["umur_max"] for _, _, r in sens)
    layak = {n: (R[(n, FULL)]["habis"] == 0 and sum(R[(n, p)]["bersih"] > 0 for p in ea.SUB) >= 2
                 and (R[(n, FULL)]["cagr"] or 0) >= 2 and R[(n, FULL)]["dd"] <= 20) for n in NAMA}

    L = ["# Laporan Uji EA XAUUSD \"Viral\"", "",
         "Anda bilang EA (robot MetaTrader) XAUUSD yang viral itu bagus. Isi EA berbayar tidak bisa dilihat, jadi "
         "saya membuat ulang tipe-tipe yang paling sering dijual, dengan pengaturan khas iklannya, lalu "
         "menjalankannya di seluruh data emas 2010–2026 — bukan hanya di periode yang dipilih penjualnya. Aturan "
         "dikunci dulu di [pra-registrasi](RENCANA_EA_XAUUSD.md) sebelum hasil dihitung.", "",
         "## Jawaban singkat", "",
         f"- **EA emas yang viral hampir selalu grid/martingale.** Kelihatannya hebat: **{pc(e1['menang'])} "
         "transaksi menang** dan kurva saldo naik mulus — itulah yang di-screenshot. Tetapi di data 2010–2026, "
         f"versi yang saya buat ulang **habis {e1['habis']} kali** (umur akun median {e1['umur_median']:.0f} hari). "
         f"Dari total setoran {usd(e1['setor'])}, yang tersisa {usd(e1['akhir'])}.",
         f"- **Di periode viral 2024–2026 pun habis {e1v['habis']} kali**, walaupun harga emas naik "
         f"{pc(bhhv['cagr'], 0, True)} per tahun. "
         f"Versi dua arah (\"hedging grid\") lebih parah: habis {e2['habis']} kali.",
         f"- **Mengganti pengaturan tidak menyelamatkan.** Cek tambahan dengan 9 kombinasi jarak grid dan pengali "
         f"lot: semuanya habis {min(s_habis)}–{max(s_habis)} kali; akun yang paling lama bertahan pun hanya "
         f"{ribuan(s_umur)} hari (±{str(round(s_umur / 365, 1)).replace('.', ',')} tahun).",
         f"- **EA tanpa martingale (breakout London) tidak pernah habis, tetapi rugi {pc(e3['cagr'], 1, True)} per "
         f"tahun** dengan drawdown {pc(e3['dd'], 0)}.",
         f"- **Yang membuat EA emas 2024–2026 terlihat hebat adalah kenaikan harga emas itu sendiri** "
         f"({pc(bhhv['cagr'], 0, True)} per tahun). Emas yang dibeli dan disimpan tanpa robot sudah mendapat itu — "
         f"tetapi 2011–2015 harganya turun {pc(R[('BH_harga', '2010–2015')]['dd'], 0)} dan baru pulih bertahun-tahun "
         "kemudian.",
         f"- Hasil: {'tidak ada tipe EA yang layak' if not any(layak[n] for n in ['E1', 'E2', 'E3']) else 'lihat tabel'} "
         "menurut syarat yang dikunci sebelumnya.", ""]

    L += ["## 1. Kenapa EA grid/martingale terlihat bagus", "",
          "Cara kerjanya: beli; kalau harga turun, beli lagi dengan lot lebih besar; tutup semua begitu harga naik "
          "sedikit di atas harga rata-rata. Hampir selalu ada pantulan kecil, jadi hampir semua \"keranjang\" ditutup "
          "untung. Masalahnya ada di sisanya: saat emas turun lurus tanpa pantulan, posisi menumpuk dengan lot "
          "terbesar dan tanpa stop loss, sampai broker menutup paksa (stop-out).", "",
          f"Di uji ini, untung rata-rata per keranjang E1 {usd(e1['rata_untung'])}, sedangkan rugi terbesar satu "
          f"kejadian {usd(e1['rugi_terbesar'])} — karena lot otomatis ikut membesar saat saldo tumbuh, satu kejadian "
          "menghapus semua untung berbulan-bulan sekaligus. Akun yang tumbuh paling besar baru habis setelah "
          "tumbuh ratusan kali lipat (di dunia nyata batas lot broker akan menahan pertumbuhan ini, tetapi tidak "
          "mencegah habisnya). Inilah sebabnya screenshot EA viral menampilkan kurva mulus dan \"win rate 98%\".", ""]

    L += ["## 2. Hasil per tipe EA", "",
          "Akun USD 1.000, leverage 1:500, biaya spread + swap. Tiap periode dimulai dengan akun baru; akun yang "
          "habis diisi lagi USD 1.000.", ""]
    rows = []
    for n in NAMA:
        for p in ea.PERIODE:
            r = R[(n, p)]
            hasil = (f"{usd(r['setor'])} disetor → {usd(r['akhir'])}" if r["habis"]
                     else f"{usd(r['akhir'])} ({pc(r['cagr'], 1, True)}/th)")
            rows.append([NAMA[n] if p == FULL else "", p, str(r["habis"]),
                         f"{r['umur_median']:.0f} hari" if r["habis"] else "–",
                         pc(r["menang"], 0) if r["n_transaksi"] else "–", pc(r["bulan_hijau"], 0), hasil,
                         "habis" if r["habis"] else pc(r["dd"], 0)])
    L += md_table(["Tipe", "Periode", "Akun habis", "Umur akun (median)", "Transaksi menang", "Bulan hijau",
                   "Hasil", "Drawdown terburuk"], rows)
    L += ["", f"Syarat \"layak\" (tidak pernah habis, untung di ≥ 2 dari 3 sub-periode, ≥ 2% per tahun, drawdown "
          f"≤ 20%): E1 {'lolos' if layak['E1'] else 'gagal'}, E2 {'lolos' if layak['E2'] else 'gagal'}, "
          f"E3 {'lolos' if layak['E3'] else 'gagal'}.", "",
          f"E3 melewati {ribuan(e3['hari_lewat'])} hari karena lot minimum 0,01 sudah melebihi risiko 1% untuk akun USD 1.000 "
          f"(di 2024–2026: {e3v['hari_lewat']} hari, karena harga emas ±USD 4.000 membuat rentang Asia lebar). EA yang "
          "tetap memaksa lot minimum di kondisi itu sebenarnya mempertaruhkan lebih dari 1% per transaksi.", ""]

    L += ["## 3. Cek tambahan: pengaturan grid lain", "",
          "Bukan bagian pra-registrasi; ditambahkan setelah hasil terlihat untuk menjawab \"EA viral pakai "
          "pengaturan lain\". Grid beli saja, maksimal 10 posisi, take profit 0,3% di atas rata-rata, 2010–2026.", ""]
    rows = [[pc(100 * s, 1), str(m).replace(".", ","), str(r["habis"]), f"{r['umur_median']:.0f} hari",
             f"{ribuan(r['umur_max'])} hari", pc(r["menang"], 1), pc(r["bulan_hijau"], 0),
             f"{usd(r['setor'])} → {usd(r['akhir'])}"] for s, m, r in sens]
    L += md_table(["Jarak grid", "Pengali lot", "Akun habis", "Umur median", "Umur terlama", "Transaksi menang",
                   "Bulan hijau", "Setoran → sisa"], rows)
    L += ["", "Grid yang lebih lebar membuat akun bertahan lebih lama dan bulan hijau lebih banyak — persis yang "
          "membuatnya lebih meyakinkan untuk dijual — tetapi tetap habis. Kedalaman grid selalu terbatas, sedangkan "
          "emas sesekali bergerak lurus 5–15% (April 2013, Agustus 2020, dan beberapa kali di 2024–2026).", ""]

    L += ["## 4. Yang ditampilkan iklan vs kenyataan", "",
          "![E1 di periode viral](grafik/ea_xauusd_viral.png)", "",
          f"Setiap titik merah adalah akun yang habis. Penjual cukup memotong grafik di antara dua titik merah: "
          f"akun yang paling lama bertahan di periode ini hidup {e1v['umur_max']} hari dengan kurva naik mulus. "
          "Akun-akun yang habis tidak pernah dipamerkan.", ""]

    L += ["## 5. Emas tanpa robot", "",
          "![EA breakout vs beli-dan-tahan](grafik/ea_xauusd_tanpa_martingale.png)", ""]
    rows = []
    for n in ["E3", "BH", "BH_harga"]:
        rows.append([NAMA[n], *[pc(R[(n, p)]["cagr"], 1, True) for p in ea.PERIODE], pc(R[(n, FULL)]["dd"], 0)])
    L += md_table(["", *[f"{p} (per tahun)" for p in ea.PERIODE], "Drawdown terburuk 2010–2026"], rows)
    L += ["", f"Harga emas naik {pc(bhh['cagr'], 1, True)} per tahun sejak 2010, tetapi lewat CFD/akun forex swap "
          f"beli emas memotongnya menjadi {pc(bh['cagr'], 1, True)} per tahun. Kalau ingin memiliki emas, emas fisik "
          "atau tabungan emas (tanpa swap) lebih masuk akal daripada robot. Rencana di "
          "[RENCANA_UNTUNG.md](RENCANA_UNTUNG.md) sudah memasukkan 10% emas.", ""]

    L += ["## 6. Cara memeriksa EA viral sebelum membeli", "",
          "1. **Minta rekam jejak akun real yang terverifikasi** (Myfxbook atau FXBlue dengan status verified) "
          "minimal 2 tahun. Backtest, akun demo, dan screenshot tidak berarti apa-apa.",
          "2. **Lihat riwayat lot.** Lot membesar setelah rugi, atau banyak posisi searah terbuka bersamaan = "
          "martingale/grid.",
          "3. **Win rate di atas 90% tanpa stop loss** adalah tanda bahaya, bukan tanda bagus.",
          "4. **Drawdown \"4%\" biasanya dihitung dari saldo tertutup.** Lihat drawdown ekuitas (termasuk posisi "
          "mengambang) — di grid, itulah yang membuat akun habis.",
          "5. **Janji profit tetap per bulan, sistem member/referral, atau dana disetor ke pihak lain** adalah ciri "
          "skema Ponzi. Contoh di Indonesia: robot trading emas ATG (Auto Trade Gold) — diblokir Bappebti sejak "
          "April 2022, pendirinya ditangkap Maret 2023, polisi menyebut ±25.000 korban.",
          "6. Kirim nama EA, link Myfxbook, atau aturannya ke saya — saya uji dengan cara yang sama di data "
          "2010–2026.", ""]

    L += ["## Kesimpulan", "",
          "EA XAUUSD yang viral tampak bagus karena dua hal: martingale membuat hampir semua transaksi menang sampai "
          "akunnya habis, dan harga emas sedang naik kencang sejak 2024. Di data 16 tahun, tidak ada tipe EA emas "
          "yang diuji di sini yang layak dipakai dengan uang sungguhan. Untuk menambah uang, tetap pakai "
          "[rencana investasi](RENCANA_UNTUNG.md).", "",
          "## Sumber", "",
          "- Data: candle 5 menit XAUUSD OANDA (Hugging Face `bunqi/OANDA_XAUUSD_Gold`), 2010–2026.",
          "- Kasus ATG — [Bisnis.com: perjalanan kasus](https://kabar24.bisnis.com/read/20230308/15/1635461/perjalanan-kasus-crazy-rich-surabaya-wahyu-kenzo-bos-robot-trading-atg), "
          "[Bisnis.com: 25 ribu korban](https://kabar24.bisnis.com/read/20230316/16/1637981/cara-crazy-rich-surabaya-wahyu-kenzo-jerat-25-ribu-orang-korbannya-di-8-negara), "
          "[Selular.ID: diblokir Bappebti](https://selular.id/2023/03/bappebti-telah-blokir-robot-trading-atg-yang-buat-crazy-rich-surabaya-jadi-tersangka/).",
          "- Contoh iklan EA emas dengan klaim Myfxbook dan peringatan risiko grid dari penjualnya sendiri — "
          "[MQL5: Gold Hedge Martingale Pro](https://www.mql5.com/it/market/product/185970), "
          "[MQL5: SmartBalance Gold EA](https://www.mql5.com/tr/market/product/187408).", ""]
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"ditulis: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ulang", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    simpan = OUT / "hasil_lengkap.pkl"
    if a.ulang or not simpan.exists():
        res, sens = hitung()
        simpan.write_bytes(pickle.dumps((res, sens)))
    else:
        res, sens = pickle.loads(simpan.read_bytes())
    laporan(res, sens)
