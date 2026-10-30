"""Uji valuasi Ko Andri di 45 saham LQ45 2018 — reports/RENCANA_SAHAM_KO_ANDRI.md.

Laporan keuangan: ekspor Stockbit pengguna (data/saham/financials_45.xlsx, tidak disimpan di git), dengan baris EPS dan
BVPS dari Key Ratio (laba dan ekuitas milik induk). Harga, dividen, split: Yahoo (data/idx/). SRIL dan WSKT tidak ada di
Yahoo: harga akhir April dari Stockbit (data/saham/harga_manual.csv), dividen dan suspensi dari berita
(bot/research/saham_manual.csv).
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from bot.data.download import LQ45_2018

ROOT = Path(__file__).resolve().parents[2]
IDX = ROOT / "data" / "idx"
SAHAM = ROOT / "data" / "saham"
MANUAL = Path(__file__).with_name("saham_manual.csv")
AKHIR = pd.Timestamp("2026-10-28")
BELI, JUAL = 0.0015, 0.0025
DEPOSITO = 0.04
NOL_SETELAH_SUSPENSI = 183          # suspensi > 6 bulan (atau pailit) → nilai 0 sejak tanggal suspensi

SEKTOR = {
    "Bank": ["BBCA", "BBRI", "BMRI", "BBNI", "BBTN", "BJBR"],
    "Konstruksi & properti": ["ADHI", "PTPP", "WIKA", "WSKT", "WSBP", "BSDE", "LPKR", "BKSL"],
    "Infrastruktur": ["TLKM", "EXCL", "JSMR"],
    "Energi": ["ADRO", "INDY", "ITMG", "PTBA", "MEDC", "PGAS", "ELSA", "AKRA"],
    "Barang baku": ["ANTM", "INCO", "INTP", "SMGR", "INKP", "BRPT", "TPIA"],
    "Konsumen primer & kesehatan": ["ICBP", "INDF", "UNVR", "GGRM", "HMSP", "KLBF", "SSMS"],
    "Konsumen non-primer & industri": ["ASII", "UNTR", "LPPF", "MNCN", "SCMA", "SRIL"],
}
SEKTOR_DARI = {k: s for s, ks in SEKTOR.items() for k in ks}

# baris laporan: (kunci, awalan label, bagian) — bagian "is" = income statement, "bs" = balance sheet, "kr" = key ratio
BARIS = [("ni_total", "Laba Bersih Tahun Berjalan", "is"), ("liabilitas", "Total Liabilitas", "bs"),
         ("ekuitas", "Total Ekuitas", "bs"), ("nci", "Kepentingan Non Pengenda", "bs"), ("aset", "Total Aset", "bs"),
         ("eps", "EPS", "kr"), ("bvps", "BVPS", "kr")]
TEPAT = {"Total Liabilitas", "Total Ekuitas", "Total Aset"}       # label yang harus sama persis (bukan awalan)


def _angka(v) -> float:
    """Angka dari sel Excel; teks seperti '12.238,94', '12,238.94', '(1.234)' atau '-' juga dibaca."""
    if v is None:
        return np.nan
    if not isinstance(v, str):
        return float(v)
    s = v.strip().replace(" ", "").replace("B", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    if "," in s and "." in s:                                  # pemisah desimal = yang muncul terakhir
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) != 3 else s.replace(",", "")
    try:
        x = float(s)
    except ValueError:
        return np.nan
    return -x if neg else x


def baca_keuangan(path: Path | None = None) -> pd.DataFrame:
    """Satu baris per (kode, tahun). Nilai dalam miliar rupiah; eps & bvps dalam rupiah per saham (seperti dilaporkan)."""
    import openpyxl
    wb = openpyxl.load_workbook(path or SAHAM / "financials_45.xlsx", read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        if ws.title not in LQ45_2018:
            continue
        rows = [r for r in ws.iter_rows(values_only=True)]
        lab = [str(r[0]).strip() if r and r[0] is not None else "" for r in rows]
        i_bs = next(i for i, s in enumerate(lab) if "BALANCE SHEET" in s)
        hdr = next(rows[i] for i, s in enumerate(lab) if s == "Pos Laporan")
        tahun = [int(str(h)[-4:]) for h in hdr[1:] if h]
        rec = {t: {"kode": ws.title, "tahun": t} for t in tahun}
        for kunci, awal, bagian in BARIS:
            rng = range(0, i_bs) if bagian == "is" else range(i_bs, len(rows))
            cocok = [i for i in rng if (lab[i] == awal if awal in TEPAT else lab[i].startswith(awal))]
            if kunci in ("eps", "bvps"):
                cocok = [i for i in range(len(rows)) if lab[i].upper().startswith(awal)
                         or (kunci == "bvps" and lab[i].startswith("Book Value Per Share"))]
            for j, t in enumerate(tahun):
                rec[t][kunci] = _angka(rows[cocok[0]][j + 1]) if cocok and j + 1 < len(rows[cocok[0]]) else np.nan
        out += list(rec.values())
    df = pd.DataFrame(out)
    df["nci"] = df["nci"].fillna(0.0)
    return df.sort_values(["kode", "tahun"]).reset_index(drop=True)


# ---------------------------------------------------------------- harga, dividen, split

@lru_cache(maxsize=None)
def kalender() -> pd.DatetimeIndex:
    d = pd.read_parquet(IDX / "IHSG.parquet")
    cal = pd.DatetimeIndex(d["t"]).normalize().unique().sort_values()
    return cal[cal <= AKHIR]


def manual() -> pd.DataFrame:
    return pd.read_csv(MANUAL, parse_dates=["tanggal"])


def suspensi() -> dict[str, pd.Timestamp]:
    m = manual()
    return dict(zip(m.loc[m.jenis == "suspensi", "kode"], m.loc[m.jenis == "suspensi", "tanggal"]))


@lru_cache(maxsize=None)
def harga() -> pd.DataFrame:
    """Close harian (disesuaikan split, belum dividen) di kalender IHSG; NaN = tidak diperdagangkan.
    Saham yang disuspensi lebih dari 6 bulan bernilai 0 sejak tanggal suspensi."""
    cal = kalender()
    cols = {}
    for k in ["IHSG", *LQ45_2018]:
        f = IDX / f"{k}.parquet"
        if f.exists():
            d = pd.read_parquet(f)
            cols[k] = d.set_index(d["t"].dt.normalize())["c"].groupby(level=0).last().reindex(cal)
    f = SAHAM / "harga_manual.csv"
    if f.exists():                                             # SRIL, WSKT: harga akhir April dari Stockbit
        m = pd.read_csv(f, parse_dates=["tanggal"])
        for k, g in m.groupby("kode"):
            cols[k] = g.set_index("tanggal")["close"].reindex(cal).ffill()
    p = pd.DataFrame(cols).ffill()                             # hari tanpa transaksi: harga terakhir
    for k, t in suspensi().items():
        if k in p:
            p.loc[p.index >= t, k] = 0.0                       # SRIL pailit, WSKT disuspensi > 24 bulan
    return p


@lru_cache(maxsize=None)
def aksi() -> pd.DataFrame:
    a = pd.read_csv(IDX / "aksi_korporasi.csv", parse_dates=["tanggal"])
    m = manual()
    m = m[m.jenis == "dividends"][["kode", "tanggal", "jenis", "nilai"]]
    return pd.concat([a, m], ignore_index=True)


def faktor_split(kode: str, setelah: pd.Timestamp) -> float:
    a = aksi()
    s = a[(a.kode == kode) & (a.jenis == "splits") & (a.tanggal > setelah)]
    return float(np.prod(s.nilai)) if len(s) else 1.0


def dividen_12bln(kode: str, tanggal: pd.Timestamp) -> float:
    a = aksi()
    d = a[(a.kode == kode) & (a.jenis == "dividends") & (a.tanggal <= tanggal)
          & (a.tanggal > tanggal - pd.DateOffset(years=1))]
    return float(d.nilai.sum())


def tanggal_pilih(tahun: int) -> pd.Timestamp:
    cal = kalender()
    return cal[(cal.year == tahun) & (cal.month == 4)][-1]


# ---------------------------------------------------------------- metrik dan pemilihan

@lru_cache(maxsize=None)
def _saham_yahoo() -> pd.DataFrame:
    y = pd.read_csv(IDX / "yahoo_fundamental.csv")
    return y[y.jenis == "annualOrdinarySharesNumber"].pivot(index="kode", columns="tahun", values="nilai")


def per_saham_kini(kode: str, tahun: int, eq_induk: float, bvps: float) -> float:
    """Faktor pembagi supaya EPS/BVPS (Stockbit) setara satuan harga Yahoo (disesuaikan split sampai sekarang).
    Dideteksi dari jumlah saham tersirat (ekuitas induk ÷ BVPS): kalau mendekati jumlah saham sebelum split, angka
    Stockbit belum disesuaikan dan dibagi faktor split; kalau mendekati jumlah sekarang, sudah disesuaikan."""
    f = faktor_split(kode, pd.Timestamp(f"{tahun}-12-31"))
    if f == 1.0 or not np.isfinite(bvps) or bvps <= 0:
        return 1.0
    ys = _saham_yahoo()
    if kode not in ys.index:
        return f
    acuan = ys.loc[kode].dropna()
    acuan = acuan[acuan.index >= tahun].iloc[0] if (acuan.index >= tahun).any() else acuan.iloc[-1]
    tersirat = eq_induk * 1e9 / bvps
    return f if abs(np.log(tersirat * f / acuan)) < abs(np.log(tersirat / acuan)) else 1.0


def metrik(fin: pd.DataFrame, tahun_buku: int) -> pd.DataFrame:
    """Rasio Ko Andri di hari pemilihan (akhir April tahun berikutnya) dari laporan tahun buku `tahun_buku`."""
    tgl = tanggal_pilih(tahun_buku + 1)
    p = harga().loc[tgl]
    rows = []
    for _, r in fin[fin.tahun == tahun_buku].iterrows():
        k = r.kode
        px = p.get(k, np.nan)
        if not np.isfinite(px) or px <= 0 or not (np.isfinite(r.eps) and np.isfinite(r.bvps)):
            continue
        eq_induk = r.ekuitas - r.nci
        f = per_saham_kini(k, tahun_buku, eq_induk, r.bvps)
        eps, bvps = r.eps / f, r.bvps / f
        rows.append({"kode": k, "sektor": SEKTOR_DARI[k], "harga": px, "eps": eps, "bvps": bvps,
                     "pbv": px / bvps if bvps > 0 else np.inf, "per": px / eps if eps > 0 else np.nan,
                     "roe": r.eps / r.bvps if r.bvps > 0 else np.nan, "der": r.liabilitas / r.ekuitas if r.ekuitas > 0 else np.inf,
                     "dividen": dividen_12bln(k, tgl), "tanggal": tgl})
    return syarat(pd.DataFrame(rows))


def syarat(m: pd.DataFrame) -> pd.DataFrame:
    """Lima syarat Ko Andri. Median PER sektor hanya dari saham yang labanya positif."""
    m = m.copy()
    m["med_per"] = m.groupby("sektor")["per"].transform("median")
    m["med_der"] = m.groupby("sektor")["der"].transform("median")
    m["s_pbv"] = m.pbv < 1
    m["s_per"] = m.per.notna() & (m.per < m.med_per)
    m["s_roe"] = m.roe > 0.05
    m["s_der"] = m.der < m.med_der
    m["s_div"] = m.dividen > 0
    m["skor"] = m[["s_pbv", "s_per", "s_roe", "s_der", "s_div"]].sum(axis=1)
    return m


# ---------------------------------------------------------------- simulasi portofolio

def simulasi(target: dict[pd.Timestamp, list[str]], mulai: pd.Timestamp, akhir: pd.Timestamp = AKHIR) -> pd.Series:
    """Ekuitas harian (modal 1). `target` = {tanggal pemilihan: daftar saham bobot sama}. Transaksi di close hari
    pemilihan, biaya hanya untuk bagian yang berubah. Dividen masuk kas di tanggal ex. Daftar kosong → deposito 4%."""
    p = harga()
    cal = kalender()
    cal = cal[(cal >= mulai) & (cal <= akhir)]
    a = aksi()
    div = a[a.jenis == "dividends"].groupby(["tanggal", "kode"]).nilai.sum()
    units: dict[str, float] = {}
    kas, deposito, eq = 1.0, False, []
    prev = None
    for d in cal:
        if deposito and prev is not None:
            kas *= (1 + DEPOSITO) ** ((d - prev).days / 365)
        if d in div.index.get_level_values(0):
            for k, v in div.loc[d].items():
                kas += units.get(k, 0.0) * v
        if d in target:
            px = p.loc[d]
            nilai = {k: u * px.get(k, 0.0) for k, u in units.items()}
            v = kas + sum(nilai.values())
            pilih = [k for k in target[d] if np.isfinite(px.get(k, np.nan)) and px.get(k, 0) > 0]
            if pilih:
                w, v_net = 1 / len(pilih), v
                for _ in range(20):                            # biaya beli/jual mengecilkan nilai bersih
                    jual = sum(max(0.0, nilai.get(k, 0.0) - (w * v_net if k in pilih else 0.0)) for k in nilai)
                    beli = sum(max(0.0, w * v_net - nilai.get(k, 0.0)) for k in pilih)
                    v_net = v - JUAL * jual - BELI * beli
                units = {k: w * v_net / px[k] for k in pilih}
                kas, deposito = 0.0, False
            else:
                jual = sum(nilai.values())
                units, kas, deposito = {}, v - JUAL * jual, True
        px = p.loc[d]
        eq.append(kas + sum(u * (px.get(k, 0.0) if np.isfinite(px.get(k, np.nan)) else 0.0) for k, u in units.items()))
        prev = d
    return pd.Series(eq, index=cal)


def max_dd(eq: pd.Series) -> float:
    return float((eq / eq.cummax() - 1).min())


def cagr(eq: pd.Series) -> float:
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    return float((eq.iloc[-1] / eq.iloc[0]) ** (1 / yrs) - 1)


def per_periode(eq: pd.Series, tanggal: list[pd.Timestamp]) -> list[float]:
    batas = [t for t in tanggal if t <= eq.index[-1]] + [eq.index[-1]]
    return [float(eq.loc[b] / eq.loc[a] - 1) for a, b in zip(batas[:-1], batas[1:]) if b > a]


def jalankan_semua(fin: pd.DataFrame | None = None) -> dict:
    fin = baca_keuangan() if fin is None else fin
    hasil = {}
    for nama, th0, th1 in [("utama", 2019, 2026), ("tambahan_2015_2019", 2015, 2019)]:
        tgl = [tanggal_pilih(y) for y in range(th0, th1 + 1)]
        akhir = AKHIR if nama == "utama" else tgl[-1]
        tgl_pilih = tgl if nama == "utama" else tgl[:-1]
        mets = {t: metrik(fin, t.year - 1) for t in tgl_pilih}
        p = harga()
        semua = {t: [k for k in LQ45_2018 if k in p and np.isfinite(p.at[t, k]) and p.at[t, k] > 0] for t in tgl_pilih}
        ko5 = {t: m.loc[m.skor == 5, "kode"].tolist() for t, m in mets.items()}
        ko4 = {t: m.loc[m.skor >= 4, "kode"].tolist() for t, m in mets.items()}
        kurva = {"Ko Andri (5 syarat)": simulasi(ko5, tgl[0], akhir), "Ko Andri (≥ 4 syarat)": simulasi(ko4, tgl[0], akhir),
                 "45 saham bobot sama": simulasi(semua, tgl[0], akhir)}
        ih = p["IHSG"].loc[tgl[0]:akhir].dropna()
        kurva["IHSG (tanpa dividen)"] = ih / ih.iloc[0]
        dep = pd.Series((1 + DEPOSITO) ** ((ih.index - ih.index[0]).days / 365), index=ih.index)
        kurva["Deposito 4%"] = dep
        ring = {n: {"cagr": cagr(e), "dd": max_dd(e), "periode": per_periode(e, tgl)} for n, e in kurva.items()}
        ka, ew = ring["Ko Andri (5 syarat)"], ring["45 saham bobot sama"]
        menang = sum(a > b for a, b in zip(ka["periode"], ew["periode"]))
        lolos = {"cagr": ka["cagr"] > ew["cagr"], "menang": menang >= 5, "dd": ka["dd"] >= ew["dd"] - 0.10,
                 "jumlah_menang": menang, "jumlah_periode": len(ka["periode"])}
        lolos["lolos"] = nama == "utama" and lolos["cagr"] and lolos["menang"] and lolos["dd"]
        hasil[nama] = {"tanggal": tgl, "metrik": mets, "pilihan": ko5, "pilihan4": ko4, "kurva": kurva,
                       "ringkas": ring, "lolos": lolos}
    return hasil
