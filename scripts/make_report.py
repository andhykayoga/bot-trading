"""Buat laporan backtest (bahasa sederhana) dari hasil scripts/run_backtest.py.

    python scripts/make_report.py

Menulis reports/LAPORAN_BACKTEST_FOREX.md, grafik di reports/grafik/, dan tabel CSV
di reports/hasil/.
"""
from __future__ import annotations

import math
import re
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
HASIL = ROOT / "reports" / "hasil"
GRAFIK = ROOT / "reports" / "grafik"
REPORT = ROOT / "reports" / "LAPORAN_BACKTEST_FOREX.md"

# warna (palet referensi dataviz): biru = untung, merah = rugi, teks netral
BLUE, RED, INK, INK2, GRID, SURF = "#2a78d6", "#e34948", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

PARAM_TEXT = {
    "tf": lambda v: f"timeframe {v}",
    "corr_max": lambda v: f"koreksi maks {v} candle",
    "corr_depth": lambda v: f"koreksi maks {v * 100:.0f}% impuls",
    "rr": lambda v: f"TP 1:{v:g}",
    "session": lambda v: "order 18.00–23.59 WIB" if v else "tanpa batas jam",
    "sl_atr": lambda v: f"jarak SL {v:g}×ATR",
    "sl_mode": lambda v: {"kijun": "SL di balik Kijun", "swing": "SL di balik swing",
                          "P": "SL di bawah P", "S1": "SL di bawah S1"}.get(v, v),
    "partial": lambda v: "50% di TP1 lalu titik impas" if v else "1 TP 1 SL",
    "points": lambda v: "4 dari 5 poin" if v == "4of5" else "5 dari 5 poin",
    "pattern": lambda v: "pola wajib" if v else "tanpa syarat pola",
    "hold_hours": lambda v: f"scalping maks {v} jam",
    "tol": lambda v: f"selisih puncak ≤ {v:g}×ATR",
    "mode": lambda v: "versi konfirmasi" if v == "confirm" else "versi antisipasi",
    "volume": lambda v: "pakai tick volume" if v == "tick" else "aturan volume dimatikan",
    "k_mult": lambda v: f"faktor k ×{v:g}",
    "sh_pen": lambda v: f"tembus ≥ {v:g}×ATR",
    "sh_bars": lambda v: f"kembali ≤ {v} candle",
    "entry": lambda v: "masuk saat candle BMS close" if v == "market" else "limit di FVG",
    "limit_bars": lambda v: f"limit batal setelah {v} candle",
    "retest_bars": lambda v: f"retest maks {v} candle",
    "retest": lambda v: f"retest maks {v} candle",
    "poc": lambda v: "POC minggu lalu (H1)" if v == "week" else "POC bulan lalu (H4)",
    "style": lambda v: "buy on weakness" if v == "weakness" else "buy on breakout",
    "rebound_pct": lambda v: f"pantulan {v:g}% (kripto)",
}


def ptext(p: dict) -> str:
    return "; ".join(PARAM_TEXT.get(k, lambda v, k=k: f"{k}={v}")(v) for k, v in p.items())


def pct(x, nd=1):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "–"
    return f"{x:+.{nd}f}%"


def num(x, nd=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    if isinstance(x, float) and math.isinf(x):
        return "∞"
    return f"{x:.{nd}f}"


def seg_cells(m: dict) -> list[str]:
    if not m or m.get("trades", 0) == 0:
        return ["0", "–", "–", "–"]
    return [str(m["trades"]), pct(m["net_pct"]), f"{m['max_dd_pct']:.1f}%", num(m["recovery"])]


def decimal_comma(text: str) -> str:
    """Angka desimal ditulis dengan koma (gaya Indonesia), kecuali di dalam `kode`."""
    text = re.sub(r"(\d{1,2})\.(\d{2})(?=–|\s?WIB|\s?New York)", r"\1§\2", text)  # jam tetap pakai titik
    parts = re.split(r"(`[^`]*`|\]\([^)]*\))", text)
    out = "".join(p if p.startswith("`") or p.startswith("](") else re.sub(r"(\d)\.(\d)", r"\1,\2", p)
                  for p in parts)
    return out.replace("§", ".")


def load():
    meta = pickle.loads((HASIL / "_meta.pkl").read_bytes())
    res = {}
    for sid in meta["order"]:
        f = HASIL / f"{sid}.pkl"
        if f.exists():
            res[sid] = pickle.loads(f.read_bytes())
    return meta, res


def reason_unrated(r: dict) -> str:
    tried = r["tried"]
    enough = [t for t in tried if t["sel"]["trades"] >= 30]
    profit = [t for t in tried if t["dev"]["net"] > 0 and t["sel"]["net"] > 0]
    if not enough:
        return "transaksi terlalu sedikit: < 30 di data pemilihan di semua varian"
    if profit:
        return "varian yang untung di kedua bagian transaksinya < 30; varian yang transaksinya cukup rugi di salah satu bagian"
    return "semua varian rugi di data penyusunan atau pemilihan"


def one_line(sid: str, r: dict, defaults: dict) -> str:
    """Satu kalimat: hasil versi mentor (nilai awal) + rentang semua varian + alasan status."""
    tried = r["tried"]
    base = next((t for t in tried if t["params"] == defaults), tried[0])
    d, s_ = base["dev"], base["sel"]
    lo = min(t["sel"]["net_pct"] for t in tried)
    hi = max(t["sel"]["net_pct"] for t in tried)
    why = reason_unrated(r) if r.get("status") == "belum bisa dinilai" else ""
    txt = (f"- **{sid}** ({r['name']}): **{r.get('status')}**. Versi mentor (nilai awal): data penyusunan "
           f"{pct(d['net_pct'])} dari {d['trades']} transaksi (drawdown terburuk {d['max_dd_pct']:.1f}%), data pemilihan "
           f"{pct(s_['net_pct'])} dari {s_['trades']} transaksi (drawdown {s_['max_dd_pct']:.1f}%). "
           f"Semua {r['trials']} varian di data pemilihan: {pct(lo)} s.d. {pct(hi)}.")
    if why:
        txt += f" Alasan: {why}."
    if "final" in r:
        f = r["final"]["final"]
        txt += (f" **Uji akhir:** {pct(f['net_pct'])} dari {f['trades']} transaksi, drawdown terburuk {f['max_dd_pct']:.1f}%.")
    return txt


def chart_final(res: dict, order: list[str]) -> str | None:
    rows = [(sid, r["final"]["final"]["net_pct"]) for sid in order if (r := res.get(sid)) and "final" in r]
    if not rows:
        return None
    rows.sort(key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(7.5, 0.42 * len(rows) + 1.2), dpi=150)
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    names = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    ax.barh(names, vals, color=[BLUE if v > 0 else RED for v in vals], height=0.6)
    ax.axvline(0, color=INK2, lw=1)
    span = max(abs(v) for v in vals) or 1
    for i, v in enumerate(vals):
        ax.text(v + (0.02 * span if v >= 0 else -0.02 * span), i, f"{v:+.1f}%".replace(".", ","), va="center",
                ha="left" if v >= 0 else "right", fontsize=8, color=INK)
    ax.set_xlim(-span * 1.25, span * 1.25)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
    ax.set_xlabel("Untung/rugi bersih di uji akhir (% saldo awal)", color=INK2, fontsize=9)
    ax.set_title("Hasil uji akhir per setup (Jun 2023 – Okt 2026)", color=INK, fontsize=11, loc="left")
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    fig.tight_layout()
    GRAFIK.mkdir(parents=True, exist_ok=True)
    out = GRAFIK / "hasil_uji_akhir.png"
    fig.savefig(out, facecolor=SURF); plt.close(fig)
    return out.relative_to(ROOT / "reports").as_posix()


def chart_equity(res: dict, ids: list[str], name: str, title: str) -> str | None:
    ids = [i for i in ids if i in res and "equity" in res[i]]
    if not ids:
        return None
    n = len(ids)
    cols = 2 if n > 1 else 1
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(7.5, 2.3 * rows + 0.6), dpi=150, squeeze=False)
    fig.patch.set_facecolor(SURF)
    for k, sid in enumerate(ids):
        ax = axes[k // cols][k % cols]
        ax.set_facecolor(SURF)
        eq = res[sid]["equity"]["final"]
        s = pd.Series([v for _, v in eq], index=pd.to_datetime([d for d, _ in eq]))
        s = (s / s.iloc[0] - 1) * 100
        ax.plot(s.index, s.values, color=BLUE if s.iloc[-1] >= 0 else RED, lw=1.6)
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(f"{sid}: {s.iloc[-1]:+.1f}%".replace(".", ","), fontsize=9, color=INK, loc="left")
        ax.tick_params(colors=INK2, labelsize=7)
        ax.grid(axis="y", color=GRID, lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(GRID)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
        ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    for k in range(n, rows * cols):
        axes[k // cols][k % cols].axis("off")
    fig.suptitle(title, x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout()
    out = GRAFIK / f"{name}.png"
    fig.savefig(out, facecolor=SURF); plt.close(fig)
    return out.relative_to(ROOT / "reports").as_posix()


def main():
    meta, res = load()
    order = meta["order"]
    from bot.setups import REGISTRY
    sp = meta["splits"]
    p1 = [s for s in order if REGISTRY[s].priority == 1]
    p2 = [s for s in order if REGISTRY[s].priority == 2]

    def status(sid):
        return res[sid].get("status", "belum dijalankan") if sid in res else "belum dijalankan"

    passed1 = [s for s in p1 if status(s) == "lolos"]
    passed2 = sorted([s for s in p2 if status(s) == "lolos"],
                     key=lambda s: -res[s]["final"]["final"]["recovery"])

    # CSV ringkasan
    rows = []
    for sid in order:
        r = res.get(sid)
        if not r:
            continue
        ch = r["chosen"]
        fin = r.get("final", {}).get("final", {})
        ast = r.get("astro", {}).get("final", {})
        rows.append({
            "setup": sid, "nama": r["name"], "prioritas": r["priority"], "status": r.get("status"),
            "varian_dicoba": r["trials"], "pilihan": ptext(ch["params"]),
            "instrumen_aktif": ",".join(r.get("active", [])), "instrumen_dimatikan": ",".join(r.get("disabled", [])),
            **{f"{seg}_{k}": (r.get("final", ch)[seg] if seg != "final" else fin).get(k) for seg in ("dev", "sel", "final")
               for k in ("trades", "net_pct", "max_dd_pct", "recovery", "win_rate")},
            "final_astro_trades": ast.get("trades"), "final_astro_net_pct": ast.get("net_pct"),
            "final_astro_max_dd_pct": ast.get("max_dd_pct"),
        })
        if "trades_final" in r and len(r["trades_final"]):
            r["trades_final"].to_csv(HASIL / f"transaksi_uji_akhir_{sid}.csv", index=False)
    pd.DataFrame(rows).to_csv(HASIL / "ringkasan.csv", index=False)

    g_final = chart_final(res, order)
    show = passed1 + passed2[:6] if (passed1 or passed2) else \
        [s for s in order if "final" in res.get(s, {})][:6]
    g_eq = chart_equity(res, show, "equity_uji_akhir", "Pergerakan saldo di uji akhir (setup yang dilaporkan)")

    L = []
    w = L.append
    w("# Laporan backtest bot forex (EURUSD & XAUUSD)\n")
    w("Laporan ini dibuat otomatis oleh `scripts/make_report.py` dari hasil `scripts/run_backtest.py`. "
      "Semua aturan mengikuti [rulebook](../rulebook/README.md): aturan global G-01 – G-17, definisi D-01 – D-12, "
      "dan filter waktu di [07](../rulebook/07-filter-waktu.md).\n")

    # ---------------------------------------------------------------- jawaban singkat
    def base_of(sid):
        r = res[sid]
        return next((t for t in r["tried"] if t["params"] == REGISTRY[sid]().params()), r["tried"][0])
    bases = {sid: base_of(sid) for sid in order if sid in res}
    prof_dev = [s for s, b_ in bases.items() if b_["dev"]["net"] > 0]
    prof_both = [s for s, b_ in bases.items() if b_["dev"]["net"] > 0 and b_["sel"]["net"] > 0]
    worst = max(bases.items(), key=lambda kv: kv[1]["dev"]["max_dd_pct"])
    fins = {s: res[s]["final"]["final"] for s in order if "final" in res.get(s, {})}
    w("## Jawaban singkat\n")
    w(f"1. **Untung atau rugi?** Hampir semua **rugi setelah biaya**. Dengan angka asli mentor (nilai awal), hanya "
      f"{len(prof_dev)} dari {len(bases)} setup yang untung di data 2010–2020, dan hanya {len(prof_both)} yang untung di "
      f"data 2010–2020 **dan** 2020–2023 ({', '.join(prof_both) if prof_both else 'tidak ada'}).")
    w(f"2. **Drawdown terburuk?** Bervariasi per setup (tabel di bawah). Yang paling dalam: {worst[0]} "
      f"{worst[1]['dev']['max_dd_pct']:.1f}% di data 2010–2020 (versi mentor). Setup prioritas 1: "
      + "; ".join(f"{s} {bases[s]['dev']['max_dd_pct']:.1f}%" for s in p1 if s in bases) + ".")
    if fins:
        w(f"3. **Hasil di data yang tidak dipakai saat menyusun strategi (uji akhir, Jun 2023 – Okt 2026)?** Hanya {len(fins)} setup "
          f"yang lolos syarat sampai ke sana, dan **semuanya {'rugi' if all(f['net'] <= 0 for f in fins.values()) else 'bervariasi'}**: "
          + "; ".join(f"{s} {pct(f['net_pct'])} (drawdown {f['max_dd_pct']:.1f}%, {f['trades']} transaksi)" for s, f in fins.items())
          + ". Setup lain tidak diuji akhir karena sudah gagal di data penyusunan/pemilihan (aturan G-17).")
    else:
        w("3. **Hasil di data uji akhir?** Tidak ada setup yang lolos syarat sampai ke uji akhir.")
    if passed1:
        w(f"4. **Layak lanjut?** Ya, dari prioritas 1: {', '.join(passed1)} — lanjut ke akun demo.")
    elif passed2:
        w(f"4. **Layak lanjut?** Prioritas 1 tidak ada yang lolos, jadi dipakai prioritas 2: {', '.join(passed2)} — lanjut ke akun demo.")
    else:
        w("4. **Layak lanjut?** **Belum ada.** Pola N dan Ichimoku Rafał (prioritas 1) tidak lolos, dan setup mentor saham–kripto "
          "di forex (prioritas 2) juga tidak lolos. Bot sebaiknya **tidak** dijalankan dengan uang sungguhan.")
    w("5. **Filter Astronacci?** Lihat bagian Filter Astronacci: tanggal kandidat memang sedikit lebih sering jadi titik balik, "
      "tetapi menyalakan filter tidak membuat satu setup pun lolos.\n")

    # ---------------------------------------------------------------- ringkasan
    w("## Ringkasan dalam bahasa sederhana\n")
    w(f"- **Data:** candle 5 menit EURUSD dan XAUUSD sejak 2010, dibagi menurut tanggal: "
      f"**penyusunan** {sp['penyusunan'][0][:10]} – {sp['penyusunan'][1][:10]}, "
      f"**pemilihan** {sp['pemilihan'][0][:10]} – {sp['pemilihan'][1][:10]}, "
      f"**uji akhir** {sp['uji akhir'][0][:10]} – {sp['uji akhir'][1][:10]}. "
      "Uji akhir adalah \"data yang tidak dipakai saat menyusun strategi\": dijalankan sekali setelah semua pilihan dikunci.")
    w("- **Biaya ikut dihitung:** spread EURUSD 1,4 pip, emas minimal 0,30 USD (melebar 0,015% dari harga), "
      "dan swap menginap. Saldo awal tiap bagian data USD 100 ribu, risiko 1% per transaksi (scalping 0,5%).")
    n_eval = sum(1 for s in order if "final" in res.get(s, {}))
    n_pass = sum(1 for s in order if status(s) == "lolos")
    w(f"- **{len(res)} setup diuji.** {n_eval} sampai ke uji akhir; **{n_pass} lolos** "
      "(untung bersih setelah biaya dengan minimal 30 transaksi di uji akhir). Sisanya \"belum bisa dinilai\" "
      "(gagal syarat di data penyusunan/pemilihan) atau \"tidak lolos\".\n")
    w("### Setup mana yang layak lanjut (sesuai urutan prioritas Anda)\n")
    if passed1:
        w("**Prioritas 1 — setup forex (Pola N, Ichimoku Rafał): ada yang lolos.** Yang layak lanjut ke akun demo:\n")
        for s in passed1:
            f = res[s]["final"]["final"]
            w(f"- **{s}** ({res[s]['name']}): uji akhir {pct(f['net_pct'])}, drawdown terburuk {f['max_dd_pct']:.1f}%, "
              f"{f['trades']} transaksi.")
        w("\nSesuai urutan prioritas, setup mentor saham–kripto tidak perlu dipakai dulu; hasilnya tetap dicatat di bawah.\n")
    else:
        w("**Prioritas 1 — setup forex (Pola N, Ichimoku Rafał): tidak ada yang lolos.**\n")
        for s in p1:
            if s in res:
                w(one_line(s, res[s], REGISTRY[s]().params()))
        w("")
        if passed2:
            w("**Karena itu dipakai prioritas 2 — setup mentor saham–kripto di forex.** Yang lolos uji akhir "
              "(urut dari Recovery Factor uji akhir terbaik), layak lanjut ke akun demo:\n")
            for s in passed2:
                f = res[s]["final"]["final"]
                ins = ", ".join(res[s]["active"])
                w(f"- **{s}** ({res[s]['name']}; {ins}): uji akhir {pct(f['net_pct'])}, "
                  f"drawdown terburuk {f['max_dd_pct']:.1f}%, {f['trades']} transaksi, Recovery Factor {num(f['recovery'])}.")
            w("")
        else:
            w("**Prioritas 2 — setup mentor saham–kripto di forex: juga tidak ada yang lolos.** "
              "Belum ada setup yang layak dipakai dengan uang sungguhan. Lihat bagian \"Langkah berikutnya\".\n")
            reached = [x for x in p2 if "final" in res.get(x, {})]
            if reached:
                w("Setup prioritas 2 yang sampai ke uji akhir (lolos syarat di data penyusunan & pemilihan), tetapi rugi di uji akhir:\n")
                for x in reached:
                    w(one_line(x, res[x], REGISTRY[x]().params()))
                w("")
    w("Lolos backtest belum berarti siap dipakai dengan uang sungguhan: rulebook (G-14, Q-03) mewajibkan uji di **akun demo** dulu.\n")
    bench = meta.get("benchmark")
    if bench:
        w("### Kenapa hampir semua setup rugi?\n")
        w("Sebagai pembanding, mesin backtest yang sama dijalankan dengan **arah acak** (SL = TP = 1 × ATR). Tanpa keunggulan apa pun, "
          "hasilnya hanya minus biaya. Rata-rata per transaksi (R = kelipatan risiko):\n")
        w("| Timeframe | Transaksi | % menang | Rata-rata per transaksi |")
        w("|---|---|---|---|")
        for tf, x in bench.items():
            w(f"| {tf} | {x['trades']} | {x['win_rate']:.1f}% | {x['avg_r']:+.3f} R |")
        w("\nArtinya, di timeframe kecil biaya spread saja sudah memakan sekitar 0,1–0,2 R per transaksi. Setup harus punya keunggulan "
          "lebih besar dari itu untuk bisa untung; kebanyakan setup di sini tidak punya.\n")
    if g_final:
        w(f"![Hasil uji akhir]({g_final})\n")
    if g_eq:
        w(f"![Pergerakan saldo di uji akhir]({g_eq})\n")

    # ---------------------------------------------------------------- tabel
    w("## Cara membaca tabel\n")
    w("- **Trx** = jumlah transaksi. **Untung/rugi** = untung bersih setelah biaya, dalam % saldo awal bagian data itu. "
      "**DD** = drawdown terburuk dari equity (saldo + untung/rugi posisi terbuka). "
      "**RF** = Recovery Factor = untung bersih ÷ drawdown terburuk (ukuran \"lebih baik\" di G-17; makin besar makin baik, negatif = rugi).")
    w("- **Status:** *lolos* = untung bersih di uji akhir dengan ≥ 30 transaksi. *tidak lolos* = sampai uji akhir tetapi rugi atau "
      "transaksinya < 30. *belum bisa dinilai* = tidak ada varian yang punya ≥ 30 transaksi di data pemilihan **dan** untung di "
      "data penyusunan maupun pemilihan (G-17 butir 4.4); setup ini tidak diuji akhir supaya data uji akhir tetap bersih.")
    w("- **Varian** = jumlah kombinasi parameter yang dicoba (G-14 butir 3). Makin banyak varian, makin besar peluang hasil bagus "
      "hanya karena kebetulan (Bailey dkk.).\n")

    def table(ids, title):
        w(f"## {title}\n")
        w("| Setup | Status | Varian | Pilihan terkunci | Penyusunan: Trx · Untung/rugi · DD · RF | "
          "Pemilihan: Trx · Untung/rugi · DD · RF | **Uji akhir**: Trx · Untung/rugi · DD · RF |")
        w("|---|---|---|---|---|---|---|")
        for sid in ids:
            r = res.get(sid)
            if not r:
                w(f"| {sid} | belum dijalankan | | | | | |")
                continue
            src = r.get("final", r["chosen"])
            dev, sel = seg_cells(src["dev"]), seg_cells(src["sel"])
            fin = seg_cells(r["final"]["final"]) if "final" in r else ["–"] * 4
            st = r.get("status")
            if st == "belum bisa dinilai":
                st += f" ({reason_unrated(r)})"
            extra = ""
            if r.get("disabled"):
                extra = f" Dimatikan di {', '.join(r['disabled'])} (rugi di penyusunan & pemilihan)."
            pre = "(gambaran) " if r.get("status") == "belum bisa dinilai" else ""
            w(f"| **{sid}** {r['name']} | {st} | {r['trials']} | {pre}{ptext(r['chosen']['params'])}.{extra} | "
              f"{' · '.join(dev)} | {' · '.join(sel)} | {' · '.join(fin)} |")
        w("")
        w("Angka penyusunan/pemilihan untuk setup *belum bisa dinilai* adalah varian dengan RF terbaik di data pemilihan, "
          "hanya sebagai gambaran.\n")

    table(p1, "Prioritas 1 — setup forex (Pola N dan Ichimoku Rafał)")
    table(p2, "Prioritas 2 — setup mentor saham–kripto yang diterapkan di forex")

    # per instrumen uji akhir
    ev = [s for s in order if "final" in res.get(s, {})]
    if ev:
        w("## Uji akhir per instrumen\n")
        w("| Setup | EURUSD: Trx · Untung/rugi · DD | XAUUSD: Trx · Untung/rugi · DD | Rugi beruntun terpanjang | % menang |")
        w("|---|---|---|---|---|")
        for sid in ev:
            fs = res[sid]["final"].get("final_sym", {})
            cell = lambda s: " · ".join(seg_cells(fs.get(s, {}))[:3]) if s in res[sid]["active"] else "dimatikan"
            f = res[sid]["final"]["final"]
            w(f"| {sid} | {cell('EURUSD')} | {cell('XAUUSD')} | {f.get('max_loss_streak', '–')} | "
              f"{num(f.get('win_rate'), 0)}% |")
        w("")
        alarms = [(s, res[s]["final"]["final"].get("dd_alarm")) for s in ev if res[s]["final"]["final"].get("dd_alarm")]
        if alarms:
            w("Rem darurat drawdown 15% (G-15) **akan menyala** di uji akhir pada: " +
              "; ".join(f"{s} ({d})" for s, d in alarms) + ". Backtest tetap diteruskan supaya hasil lengkap terlihat.\n")

    # ---------------------------------------------------------------- Astronacci
    tp = meta["astro_tp"]
    ch = tp["chosen"]
    w("## Filter Astronacci\n")
    w("Rulebook 07: filter waktu default **mati** dan baru boleh mengubah keputusan bot setelah lolos uji. "
      "Kalau dinyalakan, efeknya (Q-38, Q-41): pada tanggal kandidat titik balik hanya setup **pembalikan** yang boleh masuk "
      "(hanya entry H4 ke atas), dan setup **breakout** tidak masuk saat Merkurius retrograde.\n")
    w("### Uji 1 — apakah tanggal Astronacci lebih sering jadi titik balik?\n")
    w("Titik balik = swing D1 fractal 2–2. Pilihan uji (jendela bulan ±1/±2 hari, cara Fibonacci a/b, ambang ≥3/≥4) "
      f"dipilih di data penyusunan & pemilihan ({len(tp['rows'])} definisi dicoba), lalu dikunci.\n")
    w("| Definisi | Penyusunan: hari kandidat · peluang titik balik (kandidat vs hari lain) | Pemilihan: hari kandidat · peluang |")
    w("|---|---|---|")
    for r in tp["rows"]:
        d, s = r["dev"], r["sel"]
        mark = " **(terpilih)**" if r is ch or r["label"] == ch["label"] else ""
        w(f"| {r['label']}{mark} | {d['n_cand']} · {d['rate_cand'] * 100:.1f}% vs {d['rate_other'] * 100:.1f}% | "
          f"{s['n_cand']} · {s['rate_cand'] * 100:.1f}% vs {s['rate_other'] * 100:.1f}% |")
    f = ch["final"]
    fp = ch["final_paper"]
    w("")
    w(f"**Uji akhir (sekali, definisi terpilih):** di {f['n_cand']} hari kandidat, peluang titik balik "
      f"{f['rate_cand'] * 100:.1f}% vs {f['rate_other'] * 100:.1f}% di hari lain (p = {f['p']:.3f}). "
      f"Kesimpulan: **{tp['verdict']}**. Dengan titik balik versi makalah Gema yang lebih ketat: "
      f"{fp['rate_cand'] * 100:.1f}% vs {fp['rate_other'] * 100:.1f}% (p = {fp['p']:.3f}).")
    if not tp["chosen_ok_in_dev_sel"]:
        w("Catatan: tidak ada definisi yang lebih baik dari hari biasa di data penyusunan **dan** pemilihan; "
          "definisi terpilih hanya yang terbaik di data pemilihan.")
    w(f"Catatan kehati-hatian: {len(tp['rows'])} definisi dicoba sebelum satu dipilih, jadi p-value tunggal ini "
      "terlalu optimis (Bailey dkk.).\n")
    rt = meta["retro"]
    w("### Uji 2 — apakah setup breakout lebih sering gagal saat Merkurius retrograde (WKT-04)?\n")
    for seg, nm in (("sel", "Pemilihan"), ("final", "Uji akhir")):
        x = rt.get(seg)
        if x:
            w(f"- {nm}: kena SL {x['sl_rate_retro'] * 100:.0f}% saat retrograde ({x['n_retro']} transaksi) vs "
              f"{x['sl_rate_other'] * 100:.0f}% di luar retrograde ({x['n_other']} transaksi), p = {x['p']:.3f}.")
    w(f"- Kesimpulan di data pemilihan: **{rt['verdict_sel']}**; di uji akhir: **{rt['verdict_final']}**.\n")
    w("### Dampak filter pada tiap setup (dengan vs tanpa filter)\n")
    w("| Setup | Tanpa filter: uji akhir Trx · Untung/rugi · DD · RF | Dengan filter Astronacci: uji akhir Trx · Untung/rugi · DD · RF | "
      "Pemilihan RF: tanpa → dengan | Status dengan filter |")
    w("|---|---|---|---|---|")
    for sid in ev:
        r = res[sid]
        a = r.get("astro")
        if not a:
            continue
        same = a["final"]["trades"] == r["final"]["final"]["trades"] and \
            abs(a["final"]["net_pct"] - r["final"]["final"]["net_pct"]) < 1e-9
        note = " (filter tidak berpengaruh)" if same else ""
        w(f"| {sid}{note} | {' · '.join(seg_cells(r['final']['final']))} | {' · '.join(seg_cells(a['final']))} | "
          f"{num(r['final']['sel']['recovery'])} → {num(a['sel']['recovery'])} | {r.get('astro_status', '–')} |")
    w("")
    w("Filter tidak mengubah apa pun pada (a) setup dengan entry di bawah H4, kecuali setup breakout yang terkena aturan "
      "retrograde, dan (b) setup pembalikan, karena setup pembalikan justru boleh masuk di tanggal kandidat (07, Q-39).\n")
    any_astro_pass = [s_ for s_ in ev if res[s_].get("astro_status") == "lolos"]
    w("**Kesimpulan filter Astronacci:** " + (
        f"dengan filter, setup yang lolos uji akhir: {', '.join(any_astro_pass)}." if any_astro_pass else
        "dengan maupun tanpa filter, **tidak ada setup yang lolos**. Karena itu filter tetap **mati** di bot "
        "(config `forex.astronacci.enabled = false`), dan hanya dicatat seperti aturan 07.") + "\n")

    # ---------------------------------------------------------------- metodologi
    w("## Cara pengujian (ringkas)\n")
    w("1. **Data:** candle 5 menit OANDA (harga tengah + tick volume) dari dataset publik Hugging Face `bunqi/OANDA_*`. "
      "Candle M15/H1/H4/D1/W1 dibentuk sendiri dengan batas hari 17.00 New York (D-12); kutipan akhir pekan dibuang. "
      "Dukascopy tidak bisa diakses (dibatasi).")
    w("2. **Eksekusi (D-10):** sinyal dari candle yang sudah close; order pasar diisi di open candle 5 menit berikutnya; "
      "SL/TP dicek di candle 5 menit; kalau SL dan TP tersentuh di candle yang sama dianggap SL dulu.")
    w("3. **Aturan global:** risiko 1% (scalping 0,5%), maks 3 transaksi baru per hari, 1 posisi per instrumen, "
      "risiko terbuka maks 3%, total nilai posisi maks 10× saldo, rem harian 3% dan mingguan 6% dari equity, "
      "tidak ada posisi baru ±30 menit dari berita high impact, scalping ditutup setelah 3 jam dan sebelum berita.")
    w("4. **Biaya:** spread di setiap entry/exit; swap tiap pergantian hari (akhir pekan 3 malam) dari selisih suku bunga Fed–ECB "
      "(emas: bunga USD) ditambah biaya admin broker 1%/tahun EURUSD dan 2,5%/tahun emas.")
    w("5. **Pemilihan varian (G-17):** timeframe & pilihan setara lebih dulu, lalu nilai awal vs varian (satu parameter diubah sekali, "
      "0,5× · 1× · 1,5× nilai awal). Nilai awal dipertahankan kecuali ada varian dengan Recovery Factor lebih baik di penyusunan **dan** "
      "pemilihan. Pilihan dibuat per pasar (EURUSD + XAUUSD digabung), lalu instrumen yang rugi di kedua bagian dimatikan.")
    w("6. **Uji akhir:** sekali, dengan pilihan terkunci. Lolos = untung bersih setelah biaya dengan ≥ 30 transaksi.\n")

    w("## Asumsi dan keterbatasan\n")
    w("- **Spread tetap**, bukan spread historis per detik; saat berita spread sungguhan bisa jauh lebih lebar. Tidak ada slippage "
      "tambahan pada order stop/SL.")
    w("- **Suku bunga swap** memakai perkiraan bulanan suku bunga kebijakan; swap broker sungguhan bisa berbeda.")
    w("- **Kalender berita:** Forex Factory sampai 7 April 2025 (sekitar 40% baris hanya punya tanggal; jamnya diisi jam yang biasa "
      "dipakai berita itu). Sesudahnya hanya FOMC, NFP, CPI, rapat ECB, dan sebagian berita AS (PPI, Retail Sales, JOLTS, PCE, GDP). "
      "Jadi sebagian akhir periode uji akhir memakai daftar berita yang lebih pendek.")
    w("- **Tafsiran teknis** yang tidak ditulis mentor (mis. definisi \"Tenkan mulai naik\", cara memasang limit di garis yang "
      "bergerak, POC dari tick volume 24 baris) dijelaskan di komentar kode setiap setup di `bot/setups/`.")
    w("- **AFS-12** (pivot) diuji di H1, M15, dan M5 sebagai pilihan timeframe setara; **AFS-15** dan **AFS-18** juga diuji di dua "
      "timeframe yang disebut mentor. **AFS-04** dan **AFS-10** menjalankan dua timeframe mentor bersamaan.")
    w("- Rem darurat drawdown (berhenti total sampai diperiksa) tidak menghentikan backtest; tanggal saat ia akan menyala dicatat.")
    w("- WKT-05 (angka waktu Hosoda untuk Ichimoku) bukan bagian Astronacci dan belum diuji di putaran ini.\n")

    w("## Langkah berikutnya\n")
    if passed1 or passed2:
        w("1. Jalankan setup yang lolos di **akun demo** (G-14, Q-03) dengan aturan yang sama, lalu bandingkan hasilnya dengan uji akhir.")
    else:
        w("1. Tidak ada setup yang layak dipakai dengan uang sungguhan. Jangan menyalakan bot di akun live.")
        w("   Beberapa setup untung di data 2020–2023 tetapi rugi besar di 2010–2020 (mis. ICH-02, AFS-13A, AFS-20R, AFS-20B). "
          "Itu tanda hasilnya bergantung pada kondisi pasar tertentu, bukan keunggulan yang stabil.")
    w("2. Setup *belum bisa dinilai* tidak boleh diubah lalu diuji ulang di data uji akhir yang sama (G-17 bagian 6). "
      "Kalau aturannya mau diperbaiki, keputusan dan alasannya dicatat dulu di rulebook, lalu diuji di data baru (mis. hasil demo).")
    w("3. Setup timeframe besar (D1/W1) hampir selalu *belum bisa dinilai* karena data pemilihan (±3,4 tahun, 2 instrumen) "
      "tidak memberi 30 transaksi. Kalau ingin menilainya, perlu keputusan baru di rulebook (mis. menambah instrumen di Q-02 "
      "atau mengubah syarat 30 transaksi), dicatat dulu sebelum diuji.")
    w("4. Kripto: kerangka sudah siap (`bot/markets.py` pasar `crypto`, akun & batas hari terpisah). Tinggal menambah data BTC/ETH "
      "dan biayanya, lalu menjalankan `scripts/run_backtest.py` untuk pasar kripto.\n")

    w("## File hasil\n")
    w("- `reports/hasil/ringkasan.csv` — semua angka di tabel ini.")
    w("- `reports/hasil/transaksi_uji_akhir_<setup>.csv` — daftar transaksi uji akhir per setup.")
    w("- `reports/grafik/` — grafik di laporan ini.")
    REPORT.write_text(decimal_comma("\n".join(L)) + "\n")
    print("laporan:", REPORT)


if __name__ == "__main__":
    main()
