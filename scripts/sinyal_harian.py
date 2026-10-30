"""Sinyal harian: kripto spot B6 trailing stop 10% di BTC dan ETH (reports/LAPORAN_MODUL_BARU.md) dan pengingat IPO
(reports/LAPORAN_IPO_BACKDOOR.md: kalau ikut e-IPO, jual di hari pertama listing).

    python scripts/sinyal_harian.py                  # cetak sinyal
    python scripts/sinyal_harian.py --telegram       # kirim ke Telegram kalau ada aksi/IPO, tiap Senin, atau gagal
    python scripts/sinyal_harian.py --telegram --selalu   # kirim apa pun isinya (untuk mencoba)

Dijalankan GitHub Actions tiap 07.15 WIB (.github/workflows/sinyal-harian.yml). Keputusan memakai close harian
07.00 WIB (00.00 UTC) dan dieksekusi segera (sama dengan open hari ini di uji). Porsi kripto dibagi dua: 50% untuk
BTC, 50% untuk ETH; tiap bagian dipegang di koinnya atau di stablecoin. Tidak ada order yang dikirim: Anda yang
mengeksekusi.
"""
from __future__ import annotations

import argparse
import html
import io
import json
import sys
import traceback
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot import telegram  # noqa: E402
from bot.data.download import DATA, KAGGLE_EIPO, _get, _klines  # noqa: E402
from bot.research import kripto_investasi as ki  # noqa: E402

JARAK = 0.10
KOIN = {"BTC": "Bitcoin", "ETH": "Ethereum"}
WIB = "Asia/Jakarta"
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
         "November", "Desember"]
KAGGLE_INFO = "https://www.kaggle.com/api/v1/datasets/view/fahmirk/e-ipo-realtime-data"
BERITA = "https://news.google.com/search?hl=id&amp;q="


def perbarui() -> None:
    (DATA / "kripto_harian").mkdir(parents=True, exist_ok=True)
    for coin in KOIN:
        df = _klines(f"{coin}USDT")
        df[["t", "o", "h", "l", "c", "v", "qv"]].to_parquet(DATA / "kripto_harian" / f"{coin}.parquet", index=False)
    ki.harga.cache_clear()


def status(c: pd.Series) -> dict:
    """Aksi untuk close terakhir `c` dan level yang memicu aksi berikutnya."""
    tinggi20 = c.rolling(20).max().shift(1)
    pos, puncak = ki.trailing(c.loc[ki.MULAI:], tinggi20, JARAK)
    sebelum, sekarang = pos.iloc[-2], pos.iloc[-1]
    if sekarang and not sebelum:
        aksi = "BELI"
    elif sebelum and not sekarang:
        aksi = "JUAL ke stablecoin"
    else:
        aksi = "TETAP PEGANG" if sekarang else "TETAP DI STABLECOIN"
    pemicu = puncak * (1 - JARAK) if sekarang else float(c.iloc[-20:].max())
    if sekarang:
        berikut = f"jual kalau close harian ≤ {pemicu:,.2f} (10% di bawah puncak {puncak:,.2f})"
    else:
        berikut = f"beli lagi kalau close harian > {pemicu:,.2f} (tertinggi 20 hari)"
    return {"tanggal_close": c.index[-1].date(), "close": float(c.iloc[-1]), "aksi": aksi, "pegang": bool(sekarang),
            "pemicu": pemicu, "puncak": float(puncak), "berikutnya": berikut}


def sinyal_kripto(kemarin: pd.Timestamp) -> dict[str, dict]:
    perbarui()
    out = {}
    for coin in KOIN:
        s = status(ki.harga(coin)["c"].loc[:kemarin])     # candle hari ini belum close: tidak dipakai
        if s["tanggal_close"] != kemarin.date():
            raise RuntimeError(f"data {coin} terakhir {s['tanggal_close']}, belum ada close {kemarin.date()}")
        out[coin] = s
    return out


def ipo_hari_ini(hari: pd.Timestamp) -> tuple[list[dict], list[dict], str]:
    """IPO yang book building / masa penawaran / listing-nya mulai hari ini, IPO yang sedang berjalan, dan tanggal
    data e-IPO terakhir diperbarui (dataset Kaggle yang disalin harian dari e-ipo.co.id)."""
    with zipfile.ZipFile(io.BytesIO(_get(KAGGLE_EIPO, retries=3))) as z:
        d = pd.read_csv(io.BytesIO(z.read("e-IPO Data.csv")))
    diperbarui = json.loads(_get(KAGGLE_INFO, retries=3)).get("lastUpdated", "")[:10]
    d = d[d["IPO Status"] != "Canceled"].rename(columns={
        "Ticker Code": "kode", "Company Name": "nama", "Listing Board": "papan", "Final Price (Rp)": "harga",
        "Lowest Book Building Price (Rp)": "bawah", "Highest Book Building Price (Rp)": "atas",
        "Book Building Opening": "bb", "Book Building Closing": "bb_akhir", "Opening of Offering Period": "tawar",
        "Closing of Offering Period": "tawar_akhir", "Listing Date": "listing"})
    for k in ("bb", "bb_akhir", "tawar", "tawar_akhir", "listing"):
        d[k] = pd.to_datetime(d[k], format="mixed", errors="coerce").dt.normalize()
    d["kode"] = d.kode.str.split("-").str[0]
    d["nama"] = d.nama.str.strip()
    acara, berjalan = [], []
    for info in d[["kode", "nama", "papan", "harga", "bawah", "atas", "bb", "bb_akhir", "tawar", "tawar_akhir",
                   "listing"]].to_dict("records"):
        acara += [{**info, "jenis": j} for j in ("listing", "tawar", "bb") if info[j] == hari]
        if pd.notna(info["bb"]) and info["bb"] <= hari and (pd.isna(info["listing"]) or info["listing"] >= hari):
            berjalan.append(info)
    return acara, berjalan, diperbarui


# ---------------------------------------------------------------- tampilan untuk Telegram (HTML, ramah awam)

def tgl(t: pd.Timestamp, hari: bool = True) -> str:
    s = f"{t.day} {BULAN[t.month - 1]} {t.year}"
    return f"{HARI[t.weekday()]}, {s}" if hari else s


def usd(x: float) -> str:
    return "$" + f"{x:,.0f}".replace(",", ".")


def rp(x) -> str:
    return "Rp" + f"{float(x):,.0f}".replace(",", ".") if pd.notna(x) else "–"


def persen(x: float) -> str:
    x = 100 * abs(x)
    return (f"{x:.2f}%" if x < 1 else f"{x:.1f}%").replace(".", ",")


def baris_koin(coin: str, s: dict) -> list[str]:
    nama = f"{KOIN[coin]} ({coin})"
    jarak = s["pemicu"] / s["close"] - 1
    if s["aksi"] == "BELI":
        return [f"🟢 <b>BELI {coin}</b>",
                f"Pakai USDT bagian {coin} (setengah uang kripto Anda) untuk membeli {nama}.",
                f"Harga penutupan: <b>{usd(s['close'])}</b>, tembus harga tertinggi 20 hari."]
    if s["aksi"].startswith("JUAL"):
        return [f"🔴 <b>JUAL {coin}</b>",
                f"Jual semua {nama} Anda ke USDT.",
                f"Harga penutupan: <b>{usd(s['close'])}</b>, sudah turun 10% dari puncak {usd(s['puncak'])}."]
    if s["pegang"]:
        return [f"🟢 <b>{coin}</b>: tetap pegang, tidak perlu apa-apa.",
                f"Harga {usd(s['close'])}. Dijual kalau penutupan turun ke {usd(s['pemicu'])} atau lebih rendah "
                f"(turun {persen(jarak)} lagi)."]
    return [f"⚪ <b>{coin}</b>: tetap di USDT, tidak perlu apa-apa.",
            f"Harga {usd(s['close'])}. Dibeli lagi kalau penutupan di atas {usd(s['pemicu'])} "
            f"(naik {persen(jarak)} lagi)."]


def baris_ipo(a: dict) -> list[str]:
    judul = f"<b>{html.escape(a['kode'])}</b> ({html.escape(str(a['nama']))})"
    if a["jenis"] == "listing":
        return [f"🔔 {judul} mulai diperdagangkan hari ini.",
                "Kalau Anda dapat jatah: <b>jual hari ini</b> sebelum bursa tutup. Jangan ditahan."]
    if a["jenis"] == "tawar":
        akhir = tgl(a["tawar_akhir"], False) if pd.notna(a["tawar_akhir"]) else "–"
        listing = tgl(a["listing"], False) if pd.notna(a["listing"]) else "–"
        return [f"🛒 IPO {judul} bisa dipesan mulai hari ini sampai {akhir}.",
                f"Harga {rp(a['harga'])} per lembar · papan {html.escape(str(a['papan']))} · "
                f"mulai diperdagangkan {listing}.",
                "Kalau ikut: pesan lewat menu e-IPO di aplikasi saham Anda, lalu jual di hari pertama."]
    akhir = tgl(a["bb_akhir"], False) if pd.notna(a["bb_akhir"]) else "–"
    return [f"📝 Calon IPO {judul}: masa book building (minat awal) sampai {akhir}, kisaran harga "
            f"{rp(a['bawah'])}–{rp(a['atas'])}.", "Ini baru info awal; pesanan sungguhan dibuka saat masa penawaran."]


PENGINGAT_KRIPTO = ("⚠️ Spot saja, tanpa pinjaman (leverage). Di uji 2018–2026 aturan ini rata-rata +29,5% per "
                    "tahun, tetapi pernah turun 42%. Bukan jaminan untung.")
PENGINGAT_IPO = ("ℹ️ Di uji 202 IPO, jual di hari pertama rata-rata untung (79% naik), tetapi IPO yang ramai "
                 "biasanya hanya memberi jatah beberapa lot. Membeli setelah listing lalu ditahan setahun: "
                 "median −32%.")


def pesan(hari: pd.Timestamp, kripto: dict | None, acara: list[dict], berjalan: list[dict], diperbarui: str,
          galat: list[str]) -> tuple[str, bool]:
    """Teks pesan dan apakah ada yang perlu dilakukan (aksi kripto atau acara IPO)."""
    aksi = [c for c, s in (kripto or {}).items() if s["aksi"] in ("BELI", "JUAL ke stablecoin")]
    penting = bool(aksi or acara)
    if aksi:
        kepala = ["🚨 <b>ADA SINYAL KRIPTO HARI INI</b>"]
    elif acara:
        kepala = ["🆕 <b>INFO IPO HARI INI</b>"]
    else:
        kepala = ["📊 <b>Laporan mingguan</b>" if hari.weekday() == 0 else "📊 <b>Status sinyal</b>",
                  "Tidak ada yang perlu dilakukan. Bot tetap memantau tiap pagi."]
    s = [*kepala, f"<i>{tgl(hari)} · harga penutupan 07.00 WIB</i>", ""]
    if kripto:
        urut = aksi + [c for c in kripto if c not in aksi]
        for c in urut:
            s += [*baris_koin(c, kripto[c]), ""]
        if aksi:
            s += ["📲 <b>Cara eksekusi</b>",
                  "1. Buka aplikasi exchange kripto Anda.",
                  "2. " + "; ".join(f"Jual {c} → USDT" if kripto[c]["aksi"].startswith("JUAL")
                                    else f"Beli {c} pakai USDT" for c in aksi) + " (pilih <i>market order</i>).",
                  "3. Selesai. Tidak perlu memasang order lain; bot memeriksa lagi besok pagi.",
                  "", PENGINGAT_KRIPTO,
                  "🔎 Cek berita dulu (opsional): " + " · ".join(
                      f'<a href="{BERITA}{KOIN[c].lower()}">{KOIN[c]}</a>' for c in aksi),
                  ""]
    if acara:
        s += ["🏢 <b>IPO saham</b>"]
        for a in acara:
            s += [*baris_ipo(a), ""]
        s += [PENGINGAT_IPO, ""]
    elif not penting:
        lain = [b for b in berjalan if pd.notna(b["bb"])]
        s += ["🏢 IPO: " + (", ".join(f"<b>{b['kode']}</b>" for b in lain) + " sedang berjalan; info dikirim saat "
                           "pemesanan dibuka." if lain else "belum ada IPO yang dibuka."),
              f"<i>Data e-IPO terakhir diperbarui {diperbarui or '–'}.</i>", ""]
    for g in galat:
        s += [f"⚠️ <b>Ada yang gagal:</b> {html.escape(g)}. Jangan lakukan apa-apa berdasarkan bagian yang gagal; "
              "bot mencoba lagi besok.", ""]
    return "\n".join(s).strip(), penting


def teks_biasa(kemarin: pd.Timestamp, kripto: dict) -> str:
    out = [f"# Sinyal kripto spot (trailing stop 10%) — close {kemarin.date()} 07.00 WIB", ""]
    for coin, s in kripto.items():
        out.append(f"- {coin} (50% porsi kripto): **{s['aksi']}** · close ${s['close']:,.2f} · {s['berikutnya']}")
    out += ["", "Eksekusi sendiri di exchange (spot, tanpa leverage). Di uji 2018–2026 aturan ini +29,5% per tahun "
            "tetapi pernah turun 42%; tidak menjamin untung."]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--telegram", action="store_true", help="kirim ke Telegram (aksi/IPO, tiap Senin, atau gagal)")
    ap.add_argument("--selalu", action="store_true", help="kirim apa pun isinya")
    a = ap.parse_args()
    hari = pd.Timestamp.now(tz=WIB).normalize().tz_localize(None)
    kemarin = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=1)).tz_localize(None)
    galat, kripto, acara, berjalan, diperbarui = [], None, [], [], ""
    try:
        kripto = sinyal_kripto(kemarin)
        print(teks_biasa(kemarin, kripto), "\n")
    except Exception as e:  # noqa: BLE001 - laporkan ke pengguna, jangan diam
        traceback.print_exc()
        galat.append(f"data harga kripto tidak bisa diambil ({e})")
    try:
        acara, berjalan, diperbarui = ipo_hari_ini(hari)
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        galat.append(f"data IPO tidak bisa diambil ({e})")
    teks, penting = pesan(hari, kripto, acara, berjalan, diperbarui, galat)
    print(teks)
    kirim = a.selalu or penting or bool(galat) or hari.weekday() == 0
    if a.telegram and kirim:
        if telegram.siap():
            telegram.kirim(teks)
            print("\n[terkirim ke Telegram]")
        else:
            print("\n[TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID belum diisi: pesan tidak dikirim]")
    elif a.telegram:
        print("\n[tidak ada aksi hari ini: tidak dikirim]")


if __name__ == "__main__":
    main()
