"""Cek cepat satu atau beberapa saham BEI: harga dan tren, valuasi dan utang, dividen, umur sejak IPO, dan tanda
bahaya dari pengumuman resmi BEI 12 bulan terakhir. Hanya informasi untuk menghindari saham bermasalah, bukan sinyal
beli: belum ada aturan memilih saham BEI yang lolos uji (lihat reports/LAPORAN_SAHAM_KO_ANDRI.md dan
reports/LAPORAN_IPO_BACKDOOR.md).

    python scripts/cek_saham.py BBRI PANI
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request

import numpy as np
import pandas as pd

UA = {"User-Agent": "Mozilla/5.0"}
CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{k}.JK?range=2y&interval=1d&events=div%2Csplit"
FUND = ("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{k}.JK?type="
        "trailingNetIncomeCommonStockholders,quarterlyCommonStockEquity,quarterlyTotalLiabilitiesNetMinorityInterest,"
        "quarterlyOrdinarySharesNumber,annualTotalRevenue,annualNetIncomeCommonStockholders,annualOperatingCashFlow"
        "&period1=1609459200&period2={t}")
IDX = ("https://www.idx.id/primary/ListedCompany/GetAnnouncement?kodeEmiten={k}&emitenType=*&indexFrom=0"
       "&pageSize=300&dateFrom={a}&dateTo={b}&lang=id&keyword=")

# (kata di judul pengumuman, arti untuk pengguna)
BAHAYA = [
    (("pemantauan khusus",), "masuk Papan Pemantauan Khusus (saham bermasalah: rugi/ekuitas negatif/likuiditas rendah)"),
    (("penghentian sementara", "suspensi"), "pernah disuspensi bursa"),
    (("unusual market activity", "uma"), "kena UMA (pergerakan harga/transaksi tidak wajar)"),
    (("pkpu", "pailit", "kepailitan"), "ada perkara PKPU/pailit"),
    (("gagal bayar", "default", "penundaan pembayaran"), "ada gagal/tunda bayar utang"),
    (("going concern", "kelangsungan usaha"), "ada keraguan kelangsungan usaha"),
    (("penghapusan pencatatan", "delisting", "potensi delisting"), "ada pembahasan delisting"),
    (("opini tidak wajar", "tidak menyatakan pendapat", "disclaimer"), "opini auditor buruk"),
]
INFO = [
    (("pengendali", "pengambilalihan", "tender wajib"), "ada perubahan/rencana ganti pengendali (backdoor?)"),
    (("tanpa hmetd",), "menerbitkan saham baru tanpa HMETD (private placement, kepemilikan Anda terdilusi)"),
    (("dengan hmetd", "hak memesan efek terlebih dahulu", "rights issue"), "ada rights issue"),
    (("pembelian kembali", "buyback", "buy back"), "ada buyback saham"),
]


def _json(url: str) -> dict:
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception:  # noqa: BLE001 - jaringan: coba lagi dengan jeda
            if i == 3:
                raise
            time.sleep(2 ** (i + 1))
    raise RuntimeError("unreachable")


def harga(kode: str) -> dict:
    r = _json(CHART.format(k=kode))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    p = pd.DataFrame({"c": q["close"], "v": q["volume"]},
                     index=pd.to_datetime(r["timestamp"], unit="s").normalize()).dropna(subset=["c"])
    c = p.c
    div = [(pd.to_datetime(e["date"], unit="s"), e["amount"]) for e in r.get("events", {}).get("dividends", {}).values()]
    setahun = c.index[-1] - pd.Timedelta(days=365)
    ubah = {lbl: c.iloc[-1] / c[c.index <= c.index[-1] - pd.Timedelta(days=d)].iloc[-1] - 1
            for lbl, d in [("1 bln", 30), ("3 bln", 91), ("1 thn", 365)] if c.index[0] <= c.index[-1] - pd.Timedelta(days=d)}
    return {"tanggal": c.index[-1].date(), "tutup": c.iloc[-1], "ubah": ubah,
            "tinggi_1thn": c[c.index > setahun].max(), "rendah_1thn": c[c.index > setahun].min(),
            "sma200": c.rolling(200).mean().iloc[-1] if len(c) >= 200 else np.nan,
            "nilai_transaksi_20h": float((p.c * p.v).tail(20).mean()),
            "hari_tanpa_transaksi_20h": int((p.v.tail(20) == 0).sum()),
            "dividen_12bln": sum(a for t, a in div if t > setahun),
            "listing": pd.to_datetime(r["meta"].get("firstTradeDate"), unit="s") if r["meta"].get("firstTradeDate")
            else None}


def fundamental(kode: str, tutup: float) -> dict:
    res = _json(FUND.format(k=kode, t=int(time.time())))["timeseries"]["result"]
    seri, uang = {}, "IDR"
    for r in res:
        t = r["meta"]["type"][0]
        v = [x for x in r.get(t) or [] if x]
        if v:
            seri[t] = [(x["asOfDate"], x["reportedValue"]["raw"]) for x in v]
            uang = v[-1].get("currencyCode") or uang
    kurs = 1.0
    if uang != "IDR":                      # sebagian emiten (mis. tambang, CDIA) melapor dalam dolar AS
        kurs = _json(f"https://query1.finance.yahoo.com/v8/finance/chart/{uang}IDR=X?range=5d&interval=1d"
                     )["chart"]["result"][0]["meta"]["regularMarketPrice"]
    akhir = {k: v[-1][1] * (1 if "Shares" in k else kurs) for k, v in seri.items()}
    laba, ekuitas = akhir.get("trailingNetIncomeCommonStockholders"), akhir.get("quarterlyCommonStockEquity")
    saham, utang = akhir.get("quarterlyOrdinarySharesNumber"), akhir.get("quarterlyTotalLiabilitiesNetMinorityInterest")
    out = {"per_tanggal": seri.get("quarterlyCommonStockEquity", [("?", 0)])[-1][0]}
    if saham and ekuitas:
        out["pbv"] = tutup / (ekuitas / saham)
        out["nilai_pasar"] = tutup * saham
    if saham and laba:
        out["per"] = tutup / (laba / saham) if laba > 0 else None
    if laba is not None and ekuitas:
        out["roe"] = laba / ekuitas
        out["rugi"] = laba < 0
    if utang is not None and ekuitas:
        out["der"] = utang / ekuitas
    out["ekuitas_negatif"] = ekuitas is not None and ekuitas < 0
    rev = seri.get("annualTotalRevenue", [])
    if len(rev) >= 2 and rev[-2][1]:
        out["tumbuh_pendapatan"] = rev[-1][1] / rev[-2][1] - 1
    ocf = seri.get("annualOperatingCashFlow", [])
    if ocf:
        out["arus_kas_operasi_negatif"] = ocf[-1][1] < 0
    return out


def pengumuman(kode: str) -> list[tuple[str, str]]:
    b = pd.Timestamp.today()
    d = _json(IDX.format(k=kode, a=(b - pd.Timedelta(days=365)).strftime("%Y%m%d"), b=b.strftime("%Y%m%d")))
    return [(r["pengumuman"]["TglPengumuman"][:10], r["pengumuman"]["JudulPengumuman"].strip()) for r in d["Replies"]]


def cocok(judul: list[tuple[str, str]], daftar) -> list[str]:
    out = []
    for kata, arti in daftar:
        kena = [t for t, j in judul if any(re.search(rf"\b{k}\b", j.lower()) for k in kata)]
        if kena:
            out.append(f"{arti} (terakhir {max(kena)}, {len(kena)} pengumuman)")
    return out


def rp(x: float) -> str:
    for batas, sat in [(1e12, "T"), (1e9, "M"), (1e6, "jt")]:
        if abs(x) >= batas:
            return f"Rp{x / batas:,.1f} {sat}".replace(",", "§").replace(".", ",").replace("§", ".")
    return f"Rp{x:,.0f}".replace(",", ".")


def pc(x: float, tanda: bool = True) -> str:
    return (f"{100 * x:+.1f}%" if tanda else f"{100 * x:.1f}%").replace(".", ",")


def cek(kode: str) -> str:
    kode = kode.upper()
    try:
        h = harga(kode)
    except Exception:  # noqa: BLE001 - saham yang sudah lama disuspensi/dihapus tidak ada di Yahoo
        judul = pengumuman(kode)
        return "\n".join([f"== {kode}: tidak ada data harga di Yahoo (biasanya sudah lama disuspensi atau dihapus "
                          "dari bursa). Jangan dibeli sebelum jelas statusnya.",
                          "Tanda bahaya: " + ("; ".join(cocok(judul, BAHAYA)) or "–"),
                          "Pengumuman BEI terbaru: " + " | ".join(f"{t} {j[:70]}" for t, j in judul[:5])])
    try:
        f = fundamental(kode, h["tutup"])
    except Exception as e:  # noqa: BLE001 - fundamental Yahoo kadang kosong untuk saham kecil
        f = {"galat": str(e)}
    try:
        judul = pengumuman(kode)
    except Exception as e:  # noqa: BLE001
        judul, f["galat_idx"] = [], str(e)
    bahaya, info = cocok(judul, BAHAYA), cocok(judul, INFO)
    if f.get("rugi"):
        bahaya.append("rugi dalam 12 bulan terakhir")
    if f.get("ekuitas_negatif"):
        bahaya.append("ekuitas negatif (utang lebih besar dari aset)")
    if h["hari_tanpa_transaksi_20h"] >= 5:
        bahaya.append(f"tidak ada transaksi di {h['hari_tanpa_transaksi_20h']} dari 20 hari terakhir")
    if h["nilai_transaksi_20h"] < 1e9:
        bahaya.append(f"sepi: rata-rata transaksi hanya {rp(h['nilai_transaksi_20h'])}/hari (susah jual)")
    umur = (pd.Timestamp(h["tanggal"]) - h["listing"]).days if h["listing"] is not None else None
    if umur is not None and umur < 365:
        bahaya.append(f"baru IPO {umur} hari lalu: di uji, beli setelah listing lalu tahan setahun median -32%")

    s = [f"== {kode} (tutup {h['tanggal']}: Rp{h['tutup']:,.0f})".replace(",", "."),
         "Harga: " + ", ".join(f"{k} {pc(v)}" for k, v in h["ubah"].items())
         + f"; 1 tahun terakhir Rp{h['rendah_1thn']:,.0f}–Rp{h['tinggi_1thn']:,.0f}".replace(",", ".")]
    if not np.isnan(h["sma200"]):
        s.append(f"Tren: {'di atas' if h['tutup'] > h['sma200'] else 'di bawah'} rata-rata 200 hari "
                 f"(Rp{h['sma200']:,.0f})".replace(",", "."))
    s.append(f"Likuiditas: rata-rata transaksi 20 hari {rp(h['nilai_transaksi_20h'])}/hari")
    if "pbv" in f:
        bagian = [f"PBV {f['pbv']:.2f}".replace(".", ",")]
        bagian.append(f"PER {f['per']:.1f}".replace(".", ",") if f.get("per") else "PER – (rugi)")
        if "roe" in f:
            bagian.append(f"ROE {pc(f['roe'])}")
        if "der" in f:
            bagian.append(f"DER {f['der']:.2f}".replace(".", ","))
        s.append(f"Valuasi (laporan s.d. {f['per_tanggal']}): " + ", ".join(bagian)
                 + f"; nilai pasar {rp(f.get('nilai_pasar', 0))}")
        ko = {"PBV<1": f["pbv"] < 1, "laba positif": bool(f.get("per")), "ROE>5%": f.get("roe", 0) > 0.05,
              "ada dividen": h["dividen_12bln"] > 0}
        s.append("Checklist Ko Andri (tanpa pembanding sektor): "
                 + ", ".join(f"{k} {'✓' if v else '✗'}" for k, v in ko.items())
                 + ". Di uji, checklist ini bukan sinyal beli.")
    if "tumbuh_pendapatan" in f:
        s.append(f"Pendapatan tahun terakhir {pc(f['tumbuh_pendapatan'])}"
                 + ("; arus kas operasi negatif" if f.get("arus_kas_operasi_negatif") else ""))
    s.append(f"Dividen 12 bulan: Rp{h['dividen_12bln']:,.1f}".replace(",", "§").replace(".", ",").replace("§", ".")
             + (f" (imbal hasil {pc(h['dividen_12bln'] / h['tutup'], False)})" if h["dividen_12bln"] else ""))
    s.append("Tanda bahaya: " + ("; ".join(bahaya) if bahaya else "tidak ada yang terdeteksi"))
    if info:
        s.append("Perlu diketahui: " + "; ".join(info))
    s.append("Pengumuman BEI terbaru: " + " | ".join(f"{t} {j[:70]}" for t, j in judul[:5]))
    for k in ("galat", "galat_idx"):
        if k in f:
            s.append(f"(Catatan: data {'fundamental' if k == 'galat' else 'pengumuman BEI'} tidak terbaca: {f[k]})")
    return "\n".join(s)


if __name__ == "__main__":
    for k in sys.argv[1:] or ["BBRI"]:
        print(cek(k), "\n")
