"""Sinyal harian bertanda skor (reports/SKOR_STRATEGI.md): empat aturan kripto spot di BTC dan ETH, pengingat IPO,
dan info ganti pengendali. Anda memilih sendiri aturan mana yang diikuti; tiap sinyal dicatat di jurnal/sinyal.csv.

    python scripts/sinyal_harian.py                  # cetak sinyal
    python scripts/sinyal_harian.py --telegram --jurnal   # kirim ke Telegram (aksi/IPO, tiap Senin, atau gagal) dan
                                                          # catat di jurnal
    python scripts/sinyal_harian.py --telegram --selalu   # kirim apa pun isinya (untuk mencoba)
    python scripts/sinyal_harian.py --catat-jawaban  # hanya mencatat jawaban tombol Telegram ke jurnal

Dijalankan GitHub Actions tiap 07.15 WIB (.github/workflows/sinyal-harian.yml). Keputusan memakai close harian
07.00 WIB (00.00 UTC) dan dieksekusi segera (sama dengan open hari ini di uji). Tidak ada order yang dikirim: Anda
yang mengeksekusi.
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import traceback
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot import jurnal, telegram  # noqa: E402
from bot.data.download import DATA, KAGGLE_EIPO, _get, _klines  # noqa: E402
from bot.research import kripto_investasi as ki  # noqa: E402

KOIN = {"BTC": "Bitcoin", "ETH": "Ethereum"}
# Skor dari reports/SKOR_STRATEGI.md. TS10 adalah aturan yang dipilih sejak awal; urutan = urutan di pesan.
ATURAN = {"TS10": ("Trailing stop 10%", 100), "TS5": ("Trailing stop 5%", 100),
          "MA200": ("Rata-rata 200 hari", 100), "RSI5": ("Cicil 5× RSI mingguan", 87)}
SKOR_IPO, SKOR_BACKDOOR = 100, 49
JUDUL_BACKDOOR = (r"perubahan dalam pengendalian|tentang pengambilalihan|rencana pengambilalihan|pengendali baru"
                  r"|tender wajib|nego[si]{2}asi")
BUKAN_BACKDOOR = r"tidak (?:menyebabkan|mengubah|mengakibatkan)|pasar negosiasi|perkara hukum|oleh perseroan"
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


def _aksi(sebelum: bool, sekarang: bool) -> str:
    if sekarang and not sebelum:
        return "BELI"
    if sebelum and not sekarang:
        return "JUAL"
    return "PEGANG" if sekarang else "USDT"


def status_trailing(c: pd.Series, jarak: float) -> dict:
    """Trailing stop B6: pegang sampai close turun `jarak` dari puncak; masuk lagi saat tembus tertinggi 20 hari."""
    tinggi20 = c.rolling(20).max().shift(1)
    pos, puncak = ki.trailing(c.loc[ki.MULAI:], tinggi20, jarak)
    sekarang = bool(pos.iloc[-1])
    pemicu = puncak * (1 - jarak) if sekarang else float(c.iloc[-20:].max())
    return {"aksi": _aksi(bool(pos.iloc[-2]), sekarang), "pegang": sekarang, "pemicu": float(pemicu),
            "puncak": float(puncak)}


def status_ma200(c: pd.Series) -> dict:
    """A1: pegang hanya selama close di atas rata-rata 200 hari."""
    rata = c.rolling(200).mean()
    pos = c > rata
    return {"aksi": _aksi(bool(pos.iloc[-2]), bool(pos.iloc[-1])), "pegang": bool(pos.iloc[-1]),
            "pemicu": float(rata.iloc[-1])}


def status_rsi(c: pd.Series) -> dict:
    """B3 Kalimasada: RSI(14) candle mingguan (Senin–Minggu). Sinyal hanya tiap Senin pagi, setelah minggu ditutup:
    RSI < 30 beli 1/5 uang cicilan, RSI > 70 jual 1/5 posisi."""
    w = c.resample("W-SUN").last()
    if c.index[-1].weekday() != 6:                    # minggu berjalan belum ditutup
        w = w.iloc[:-1]
    delta = w.diff()
    naik, turun = delta.clip(lower=0), -delta.clip(upper=0)
    rsi = float((100 - 100 / (1 + naik.ewm(alpha=1 / 14, adjust=False).mean()
                                  / turun.ewm(alpha=1 / 14, adjust=False).mean())).iloc[-1])
    aksi = "TUNGGU"
    if c.index[-1].weekday() == 6:
        aksi = "BELI 1/5" if rsi < 30 else "JUAL 1/5" if rsi > 70 else "TUNGGU"
    return {"aksi": aksi, "rsi": rsi}


def sinyal_kripto(kemarin: pd.Timestamp) -> dict[str, dict]:
    """Per koin: harga penutupan kemarin dan status tiap aturan."""
    perbarui()
    out = {}
    for coin in KOIN:
        c = ki.harga(coin)["c"].loc[:kemarin]            # candle hari ini belum close: tidak dipakai
        if c.index[-1] != kemarin:
            raise RuntimeError(f"data {coin} terakhir {c.index[-1].date()}, belum ada close {kemarin.date()}")
        out[coin] = {"close": float(c.iloc[-1]), "TS10": status_trailing(c, 0.10), "TS5": status_trailing(c, 0.05),
                     "MA200": status_ma200(c), "RSI5": status_rsi(c)}
    return out


def aksi_kripto(kripto: dict | None, hari: pd.Timestamp) -> list[dict]:
    """Daftar sinyal yang perlu dikerjakan hari ini (untuk pesan, tombol, dan jurnal)."""
    out = []
    for coin, k in (kripto or {}).items():
        for kode, (nama, skor) in ATURAN.items():
            a = k[kode]["aksi"]
            if a in ("BELI", "JUAL", "BELI 1/5", "JUAL 1/5"):
                out.append({"id": f"{hari:%Y%m%d}-{coin}-{kode}", "tanggal": f"{hari:%Y-%m-%d}", "strategi": nama,
                            "singkat": kode, "skor": skor, "aset": coin, "aksi": a, "harga": round(k["close"], 2)})
    return out


def backdoor_hari_ini(hari: pd.Timestamp) -> list[dict]:
    """Pengumuman BEI kemarin dan hari ini yang judulnya menyinggung ganti pengendali (perlu dicek manual: kadang
    emiten yang membeli perusahaan lain, atau perpindahan di dalam grup)."""
    a, b = (hari - pd.Timedelta(days=1)).strftime("%Y%m%d"), hari.strftime("%Y%m%d")
    url = (f"https://www.idx.id/primary/ListedCompany/GetAnnouncement?kodeEmiten=&emitenType=*&indexFrom=0"
           f"&pageSize=1000&dateFrom={a}&dateTo={b}&lang=id&keyword=")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})   # tanpa ini situs BEI menolak (403)
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    out, ada = [], set()
    for r in d["Replies"]:
        p = r["pengumuman"]
        judul, kode = re.sub(r"\s+", " ", p["JudulPengumuman"]).strip(), (p["Kode_Emiten"] or "").strip()
        if len(kode) != 4 or kode in ada or not re.search(JUDUL_BACKDOOR, judul, re.I) \
                or re.search(BUKAN_BACKDOOR, judul, re.I):
            continue
        ada.add(kode)
        lamp = [x["FullSavePath"].replace("www.idx.co.id", "www.idx.id") for x in r.get("attachments") or []]
        out.append({"kode": kode, "judul": judul, "tautan": lamp[0] if lamp else "",
                    "id": f"{hari:%Y%m%d}-{kode}-GANTI", "tanggal": f"{hari:%Y-%m-%d}", "strategi": "Ganti pengendali",
                    "singkat": "GANTI", "skor": SKOR_BACKDOOR, "aset": kode, "aksi": "INFO", "harga": ""})
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


def baris_aksi(x: dict, kripto: dict) -> list[str]:
    """Dua baris untuk satu sinyal kripto: apa yang dikerjakan dan kenapa."""
    k, a, coin = kripto[x["aset"]], x["aksi"], x["aset"]
    tanda = "🔴" if a.startswith("JUAL") else "🟢"
    kepala = f"{tanda} <b>{a} {coin}</b> · {x['strategi']} · skor {x['skor']}/100"
    if x["singkat"] == "RSI5":
        isi = (f"Beli {coin} seharga 1/5 uang cicilan Anda." if a == "BELI 1/5" else
               f"Jual 1/5 dari {coin} yang Anda kumpulkan lewat cicilan.") + \
              f" RSI mingguan {k['RSI5']['rsi']:.0f}."
    elif a == "BELI":
        isi = f"Beli {coin} pakai USDT yang Anda siapkan untuk aturan ini. Harga penutupan <b>{usd(k['close'])}</b>."
    else:
        isi = f"Jual {coin} untuk aturan ini ke USDT. Harga penutupan <b>{usd(k['close'])}</b>."
    return [kepala, isi]


def papan(coin: str, k: dict) -> list[str]:
    """Posisi tiap aturan untuk satu koin dan seberapa jauh dari sinyal berikutnya."""
    out = [f"<b>{KOIN[coin]} ({coin}) {usd(k['close'])}</b>"]
    for kode, (nama, skor) in ATURAN.items():
        st = k[kode]
        if kode == "RSI5":
            ket = f"RSI mingguan {st['rsi']:.0f} · beli kalau di bawah 30, jual kalau di atas 70 (dicek tiap Senin)"
        else:
            jarak = st["pemicu"] / k["close"] - 1
            if st["pegang"]:
                ket = f"pegang · jual kalau penutupan ≤ {usd(st['pemicu'])} (turun {persen(jarak)} lagi)"
            else:
                ket = f"di USDT · beli kalau penutupan di atas {usd(st['pemicu'])} (naik {persen(jarak)} lagi)"
        out.append(f"• {nama} ({skor}): {ket}")
    return out


def baris_ipo(a: dict) -> list[str]:
    judul = f"<b>{html.escape(a['kode'])}</b> ({html.escape(str(a['nama']))})"
    if a["jenis"] == "listing":
        return [f"🔔 {judul} mulai diperdagangkan hari ini · skor {SKOR_IPO}/100",
                "Kalau Anda dapat jatah: <b>jual hari ini</b> sebelum bursa tutup. Jangan ditahan."]
    if a["jenis"] == "tawar":
        akhir = tgl(a["tawar_akhir"], False) if pd.notna(a["tawar_akhir"]) else "–"
        listing = tgl(a["listing"], False) if pd.notna(a["listing"]) else "–"
        return [f"🛒 IPO {judul} bisa dipesan mulai hari ini sampai {akhir} · skor {SKOR_IPO}/100",
                f"Harga {rp(a['harga'])} per lembar · papan {html.escape(str(a['papan']))} · "
                f"mulai diperdagangkan {listing}.",
                "Kalau ikut: pesan lewat menu e-IPO di aplikasi saham Anda, lalu jual di hari pertama."]
    akhir = tgl(a["bb_akhir"], False) if pd.notna(a["bb_akhir"]) else "–"
    return [f"📝 Calon IPO {judul}: masa book building (minat awal) sampai {akhir}, kisaran harga "
            f"{rp(a['bawah'])}–{rp(a['atas'])}.", "Ini baru info awal; pesanan sungguhan dibuka saat masa penawaran."]


def sinyal_ipo(acara: list[dict], hari: pd.Timestamp) -> list[dict]:
    """IPO yang bisa dikerjakan hari ini (pesan, atau jual di hari listing) untuk tombol dan jurnal."""
    out = []
    for a in acara:
        if a["jenis"] in ("tawar", "listing"):
            out.append({"id": f"{hari:%Y%m%d}-{a['kode']}-IPO", "tanggal": f"{hari:%Y-%m-%d}",
                        "strategi": "IPO jual hari pertama", "singkat": "IPO", "skor": SKOR_IPO, "aset": a["kode"],
                        "aksi": "PESAN" if a["jenis"] == "tawar" else "JUAL", "harga": a["harga"]})
    return out


PENGINGAT_KRIPTO = ("⚠️ Spot saja, tanpa pinjaman (leverage). Di uji 2018–2026 aturan-aturan ini rata-rata +18% "
                    "sampai +34% per tahun, tetapi pernah turun 38–61%. Bukan jaminan untung.")
PENGINGAT_IPO = ("ℹ️ Di uji 202 IPO, jual di hari pertama rata-rata untung (79% naik), tetapi IPO yang ramai "
                 "biasanya hanya memberi jatah beberapa lot. Membeli setelah listing lalu ditahan setahun: "
                 "median −32%.")
PENGINGAT_BACKDOOR = (f"ℹ️ Skor {SKOR_BACKDOOR}/100: di uji 48 kasus 2023–2025, membeli sehari setelah berita "
                      "ganti pengendali lalu menahan setahun median −4%; separuh menang, separuh kalah. Cek dulu "
                      "isinya: kadang emiten itu yang membeli perusahaan lain.")
CARA_PILIH = ("🧭 Pilih <b>satu</b> aturan kripto dan ikuti terus. Mengganti-ganti aturan setelah rugi biasanya "
              "memperburuk hasil. Jurnal menilai tiap aturan terpisah.")


def pesan(hari: pd.Timestamp, kripto: dict | None, acara: list[dict], berjalan: list[dict], diperbarui: str,
          galat: list[str], backdoor: list[dict] | None = None, info_jurnal: str = "") -> tuple[str, bool]:
    """Teks pesan dan apakah ada yang perlu dilakukan (aksi kripto, acara IPO, atau info ganti pengendali)."""
    aksi = aksi_kripto(kripto, hari)
    backdoor = backdoor or []
    penting = bool(aksi or acara or backdoor)
    if aksi:
        kepala = ["🚨 <b>ADA SINYAL KRIPTO HARI INI</b>"]
    elif acara or backdoor:
        kepala = ["🆕 <b>INFO SAHAM HARI INI</b>"]
    else:
        kepala = ["📊 <b>Laporan mingguan</b>" if hari.weekday() == 0 else "📊 <b>Status sinyal</b>",
                  "Tidak ada yang perlu dilakukan. Bot tetap memantau tiap pagi."]
    s = [*kepala, f"<i>{tgl(hari)} · harga penutupan 07.00 WIB</i>", ""]
    for x in aksi:
        s += [*baris_aksi(x, kripto), ""]
    if aksi:
        s += ["📲 Cara eksekusi: buka aplikasi exchange, pilih <i>market order</i>, selesai. Tidak perlu memasang "
              "order lain; bot memeriksa lagi besok pagi.",
              "🔎 Cek berita dulu (opsional): " + " · ".join(
                  f'<a href="{BERITA}{KOIN[c].lower()}">{KOIN[c]}</a>'
                  for c in dict.fromkeys(x["aset"] for x in aksi)),
              ""]
    if kripto:
        s += ["📋 <b>Papan skor kripto</b> (skor 0–100, makin tinggi makin meyakinkan di uji)"]
        for coin, k in kripto.items():
            s += [*papan(coin, k), ""]
        s += [CARA_PILIH, PENGINGAT_KRIPTO, ""]
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
    if backdoor:
        s += ["📰 <b>Info ganti pengendali</b>"]
        for b in backdoor:
            judul = html.escape(b["judul"][:140])
            s += [f"<b>{b['kode']}</b>: " + (f'<a href="{html.escape(b["tautan"])}">{judul}</a>' if b["tautan"]
                                            else judul)]
        s += ["", PENGINGAT_BACKDOOR, ""]
    if penting:
        s += ["👇 Tekan ✅ kalau Anda menjalankan sinyal itu, ❌ kalau tidak. Jawaban masuk jurnal untuk dinilai "
              "nanti.", ""]
    if info_jurnal:
        s += [f"<i>{html.escape(info_jurnal)}</i>", ""]
    for g in galat:
        s += [f"⚠️ <b>Ada yang gagal:</b> {html.escape(g)}. Jangan lakukan apa-apa berdasarkan bagian yang gagal; "
              "bot mencoba lagi besok.", ""]
    return "\n".join(s).strip(), penting


def teks_biasa(kemarin: pd.Timestamp, kripto: dict) -> str:
    out = [f"# Sinyal kripto spot — close {kemarin.date()} 07.00 WIB", ""]
    for coin, k in kripto.items():
        out.append(f"- {coin} close ${k['close']:,.2f}: " + "; ".join(
            f"{nama} (skor {skor}) {k[kode]['aksi']}" for kode, (nama, skor) in ATURAN.items()))
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--telegram", action="store_true", help="kirim ke Telegram (aksi/IPO, tiap Senin, atau gagal)")
    ap.add_argument("--selalu", action="store_true", help="kirim apa pun isinya")
    ap.add_argument("--jurnal", action="store_true", help="catat sinyal dan jawaban tombol di jurnal/sinyal.csv")
    ap.add_argument("--catat-jawaban", action="store_true", help="hanya mencatat jawaban tombol, tanpa sinyal")
    a = ap.parse_args()
    if a.jurnal or a.catat_jawaban:
        print(f"jawaban tombol dicatat: {jurnal.tarik_jawaban()}")
    if a.catat_jawaban:
        return
    hari = pd.Timestamp.now(tz=WIB).normalize().tz_localize(None)
    kemarin = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=1)).tz_localize(None)
    galat, kripto, acara, berjalan, diperbarui, backdoor = [], None, [], [], "", []
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
    try:
        backdoor = backdoor_hari_ini(hari)
    except Exception:  # noqa: BLE001 - info tambahan: kalau situs BEI tidak bisa dibuka, lewati saja
        traceback.print_exc()
    semua = aksi_kripto(kripto, hari) + sinyal_ipo(acara, hari) + backdoor
    if a.jurnal:
        jurnal.catat(semua)
    info = jurnal.ringkas() if hari.weekday() == 0 or a.selalu else ""
    teks, penting = pesan(hari, kripto, acara, berjalan, diperbarui, galat, backdoor, info)
    print(teks)
    kirim = a.selalu or penting or bool(galat) or hari.weekday() == 0
    if a.telegram and kirim:
        if telegram.siap():
            telegram.kirim(teks, jurnal.tombol(semua))
            print("\n[terkirim ke Telegram]")
        else:
            print("\n[TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID belum diisi: pesan tidak dikirim]")
    elif a.telegram:
        print("\n[tidak ada aksi hari ini: tidak dikirim]")


if __name__ == "__main__":
    main()
