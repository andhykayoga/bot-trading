"""Mode semi-otomatis: bot memberi sinyal, Anda yang memutuskan dan mengeksekusi.

    python -m bot.data.download forex crypto      # perbarui data dulu
    python scripts/sinyal.py                      # tulis reports/sinyal/<tanggal>.md

Isi laporan sinyal:
- order baru dari setup yang dipilih di config/sinyal.toml (dari candle terakhir yang sudah
  close), lengkap dengan entry, SL, TP, dan ukuran posisi untuk saldo Anda (G-01);
- posisi bulan ini untuk patokan time-series momentum (kalau dinyalakan);
- pengingat aturan global yang harus Anda jaga sendiri (G-08, G-13, G-15).
Setiap sinyal juga ditambahkan ke reports/sinyal/jurnal.csv. Isi kolom `diambil` dan
`hasil_R` setelah transaksi selesai, supaya hasil eksekusi manual bisa dinilai nanti.
Tidak ada koneksi broker: tidak ada order yang dikirim otomatis.
"""
from __future__ import annotations

import csv
import sys
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot.data import news  # noqa: E402
from bot.data.candles import TF_MINUTES, load_instrument  # noqa: E402
from bot.markets import INSTRUMENTS, MARKETS  # noqa: E402
from bot.setups import REGISTRY  # noqa: E402
from bot.setups.improved import IMPROVED  # noqa: E402

OUT = ROOT / "reports" / "sinyal"
ALL = {**REGISTRY, **{c.id: c for c in IMPROVED}}


def md_table(rows: list[dict]) -> str:
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out)


def fmt_t(ns: int) -> str:
    return pd.Timestamp(ns, tz="UTC").tz_convert("Asia/Jakarta").strftime("%Y-%m-%d %H:%M WIB")


def setup_signals(market: str, ids: list[str], params: dict, balance: float, risk_pct: float) -> list[dict]:
    syms = MARKETS[market].instruments
    data = {s: load_instrument(s) for s in syms}
    now = max(int(d["M5"].t_close[-1]) for d in data.values())
    rows = []
    for sid in ids:
        st = ALL[sid]()
        p = st.params(**params.get(sid, {}))
        tf = st.entry_tf_of(p)
        window = TF_MINUTES.get(tf, 60) * 60 * 10**9
        for o in st.signals(data, p):
            fresh = o.created >= now - window
            pending_ok = o.kind != "market" and o.expiry > now
            if not (fresh or pending_ok):
                continue
            inst = INSTRUMENTS[o.symbol]
            entry = o.price if o.kind != "market" else float(data[o.symbol][tf].c[-1])
            dist = abs(entry - o.sl)
            tp = o.tp if not np.isnan(o.tp) else entry + o.direction * o.tp_rr * dist
            risk = balance * (risk_pct / 2 if o.label == "scalping" else risk_pct)
            units = risk / (dist * inst.usd_per_quote(entry)) if dist > 0 else 0.0
            rows.append({
                "dibuat": fmt_t(o.created), "setup": sid, "instrumen": o.symbol,
                "arah": "BUY" if o.direction > 0 else "SELL",
                "jenis": {"market": "pasar", "limit": "limit", "stop": "stop"}[o.kind],
                "entry": round(entry, 5), "sl": round(o.sl, 5), "tp": round(tp, 5),
                "rr": round(abs(tp - entry) / dist, 2) if dist else None,
                "unit": round(units, 4), "lot_standar": round(units / 100_000, 2) if inst.market != "crypto" and o.symbol != "XAUUSD"
                else (round(units / 100, 2) if o.symbol == "XAUUSD" else None),
                "berlaku_sampai": fmt_t(o.expiry) if o.kind != "market" and o.expiry < 2**62 else "-",
                "berita_1_jam": bool(news.in_blackout(o.symbol, now) or news.next_window_start(o.symbol, now) - now
                                     < 3600 * 10**9),
            })
    return rows


def tsmom_positions(market: str, long_only: bool) -> list[dict]:
    from bot.research.tsmom import _daily_closes
    syms = MARKETS[market].instruments
    px = _daily_closes(syms)
    ret = px.pct_change()
    periods = 365 if market == "crypto" else 261
    vol = np.sqrt((ret ** 2).ewm(com=60, min_periods=60).mean() * periods).iloc[-1]
    past = px.asof(px.index[-1] - pd.Timedelta(days=365))
    out = []
    for s in syms:
        sig = np.sign(px[s].iloc[-1] / past[s] - 1)
        if long_only:
            sig = max(sig, 0)
        w = sig * (0.10 / np.sqrt(len(syms))) / vol[s]
        out.append({"instrumen": s, "return_12_bulan_%": round(100 * (px[s].iloc[-1] / past[s] - 1), 1),
                    "posisi": "LONG" if sig > 0 else ("SHORT" if sig < 0 else "tidak pegang"),
                    "nilai_posisi_%_saldo": round(100 * abs(w), 1)})
    return out


def kripto_spot_tren() -> list[dict]:
    """Status hari ini untuk aturan spot tanpa leverage dari reports/LAPORAN_MODUL_BARU.md:
    A1 (pegang selama close di atas SMA 200) dan B6 (trailing stop 10%, masuk lagi di tertinggi 20 hari)."""
    from bot.research import kripto_investasi as ki
    ki.harga.cache_clear()
    kemarin = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=1)).tz_localize(None)
    out = []
    for coin in ("BTC", "ETH"):
        c = ki.harga(coin)["c"].loc[:kemarin]            # candle hari ini belum close: tidak dipakai
        sma = c.rolling(200).mean()
        b6 = ki.b6_trailing(coin, 0.10, akhir=str(kemarin.date()))
        out.append({"koin": coin, "tanggal_close": c.index[-1].date(), "close": round(float(c.iloc[-1]), 2),
                    "SMA_200": round(float(sma.iloc[-1]), 2),
                    "A1_filter_tren": "PEGANG" if c.iloc[-1] > sma.iloc[-1] else "STABLECOIN",
                    "B6_trailing_10%": "PEGANG" if b6.iloc[-1] else "STABLECOIN"})
    return out


def main():
    cfg = tomllib.loads((ROOT / "config" / "sinyal.toml").read_text())
    bal, risk = float(cfg["saldo_usd"]), float(cfg["risiko_per_transaksi"])
    OUT.mkdir(parents=True, exist_ok=True)
    today = pd.Timestamp.now(tz="Asia/Jakarta").strftime("%Y-%m-%d")
    lines = [f"# Sinyal {today}\n", f"Saldo {bal:,.0f} USD, risiko {risk:.1%} per transaksi (scalping setengahnya).\n",
             "**Bot tidak mengirim order.** Anda yang memutuskan dan mengeksekusi, lalu mengisi jurnal.\n"]
    journal = []
    for market, mcfg in cfg.get("pasar", {}).items():
        rows = setup_signals(market, mcfg.get("setup", []), mcfg.get("parameter", {}), bal, risk)
        lines.append(f"## Sinyal setup — {market}\n")
        if rows:
            lines.append(md_table(rows) + "\n")
            journal += [dict(r, diambil="", hasil_R="") for r in rows]
        else:
            lines.append("Tidak ada sinyal baru.\n")
        if mcfg.get("tsmom"):
            lines.append(f"## Posisi patokan time-series momentum — {market} (ubah hanya di akhir bulan)\n")
            lines.append(md_table(tsmom_positions(market, bool(mcfg.get("tsmom_long_only")))) + "\n")
    if cfg.get("kripto_spot", {}).get("aktif"):
        lines.append("## Kripto spot tanpa leverage — aturan tren (eksekusi di open besok, 07.00 WIB)\n")
        lines.append(md_table(kripto_spot_tren()) + "\n")
        lines.append("Perbarui data dulu: `python -m bot.data.download kripto_harian`. Hanya untuk porsi kecil uang yang "
                     "siap turun 40–60%; lihat reports/LAPORAN_MODUL_BARU.md.\n")
    lines += ["## Aturan yang Anda jaga sendiri\n",
              "- Maks 3 transaksi baru per hari, 1 posisi per instrumen, total risiko terbuka maks 3% (G-08). Kalau ada "
              "beberapa sinyal di instrumen yang sama, ambil paling banyak satu; sinyal yang berlawanan arah di candle "
              "yang sama = pasar ragu, sebaiknya dilewati.",
              "- Untuk order pasar, kolom `entry` = harga terakhir; harga isi sebenarnya bisa sedikit berbeda, jadi hitung "
              "ulang lot dari jarak SL sebenarnya.",
              "- Jangan buka posisi 30 menit sebelum sampai 30 menit sesudah berita high impact (G-13); kolom "
              "`berita_1_jam` = True berarti ada berita dalam 1 jam.",
              "- Berhenti hari ini kalau rugi 3%, minggu ini kalau rugi 6%, berhenti total kalau drawdown 15% (G-15).",
              "- SL dan TP dipasang bersamaan dengan entry, tidak digeser (G-07, G-12)."]
    (OUT / f"{today}.md").write_text("\n".join(lines) + "\n")
    if journal:
        jf = OUT / "jurnal.csv"
        new = not jf.exists()
        with jf.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(journal[0].keys()))
            if new:
                w.writeheader()
            w.writerows(journal)
    print((OUT / f"{today}.md").read_text())


if __name__ == "__main__":
    main()
