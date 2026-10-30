"""Rancangan A1 dan modul investasi spot kripto B1–B6 (reports/RENCANA_MODUL_BARU.md).

Candle harian spot Binance. Sinyal dari close hari t, eksekusi di open hari t+1. Uang tunai tidak berbunga.
Data koin berhenti di jeda > 7 hari pertama (delisting/penghentian perdagangan, mis. LUNA Mei 2022, FTT Nov 2022);
posisi yang masih ada dijual di close terakhir.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from bot.data.download import ALTCOIN, MEME

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "kripto_harian"
MULAI = "2018-03-05"          # hari pertama SMA 200 BTC tersedia (pemanasan indikator)
AKHIR = "2026-10-28"
SUB = [("2018–2020", "2018-03-05", "2020-12-31"), ("2021–2023", "2021-01-01", "2023-12-31"),
       ("2024–2026", "2024-01-01", AKHIR)]
UJI_AKHIR = ("2024-12-29", AKHIR)
HALVING = [pd.Timestamp("2020-05-11"), pd.Timestamp("2024-04-20")]


def biaya(coin: str) -> float:
    return 0.0011 if coin in ("BTC", "ETH") else 0.002


@lru_cache(maxsize=None)
def harga(coin: str) -> pd.DataFrame:
    d = pd.read_parquet(DATA / f"{coin}.parquet")
    gap = d["t"].diff().dt.days
    putus = np.flatnonzero(gap.to_numpy() > 7)
    if len(putus):
        d = d.iloc[:putus[0]]
    return d.set_index(d["t"].dt.normalize())[["o", "h", "l", "c", "qv"]]


def hari() -> pd.DatetimeIndex:
    return harga("BTC").loc[MULAI:AKHIR].index


# ---------------------------------------------------------------- satu aset: masuk/keluar

def sleeve(coin: str, posisi: pd.Series, modal: float = 1.0) -> pd.Series:
    """Ekuitas harian satu aset. `posisi` = porsi modal yang diinginkan di aset (0..1), diputuskan di close hari
    itu dan dieksekusi di open hari berikutnya."""
    p = harga(coin)
    idx = hari()
    o, c = p["o"].reindex(idx), p["c"].reindex(idx)
    # posisi hari i = keputusan di close hari i−1 (hari pertama: keadaan awal aturan)
    kemarin = posisi.reindex(p.index.union(posisi.index)).ffill().shift(1).reindex(idx).bfill()
    target = kemarin.fillna(0.0).to_numpy()
    fee = biaya(coin)
    units, cash, out = 0.0, modal, []
    for i in range(len(idx)):
        if np.isnan(c.iloc[i]):                      # aset sudah delisting: jual di close terakhir
            if units:
                cash += units * p["c"].iloc[-1] * (1 - fee)
                units = 0.0
            out.append(cash)
            continue
        if i == 0 or target[i] != target[i - 1]:      # transaksi hanya saat keputusan berubah
            px = o.iloc[i]
            nilai = units * px + cash
            mau = target[i] * nilai / (px * (1 + fee)) if target[i] > 0 else 0.0
            beda = mau - units
            if beda:
                cash -= beda * px + abs(beda) * px * fee
                units = mau
        out.append(units * c.iloc[i] + cash)
    return pd.Series(out, index=idx)


def a1_filter_tren(coin: str) -> pd.Series:
    c = harga(coin)["c"]
    return (c > c.rolling(200).mean()).astype(float)


def b4_fear_greed() -> pd.Series:
    f = pd.read_csv(ROOT / "data" / "riset" / "fng.csv")
    f["t"] = pd.to_datetime(f["timestamp"].astype(int), unit="s").dt.normalize()
    f = f.set_index("t").sort_index()["value_classification"]
    sinyal = pd.Series(np.nan, index=f.index)
    sinyal[f == "Extreme Fear"] = 1.0
    sinyal[f == "Extreme Greed"] = 0.0
    return sinyal.ffill().fillna(0.0)


def b5_halving(setelah: int) -> pd.Series:
    idx = harga("BTC").index
    s = pd.Series(0.0, index=idx)
    for h in HALVING:
        s[(idx > h - pd.Timedelta(days=365)) & (idx <= h + pd.Timedelta(days=setelah))] = 1.0
    return s


def trailing(c: pd.Series, tinggi20: pd.Series, jarak: float) -> tuple[pd.Series, float]:
    """Posisi trailing stop per close (1 = pegang, 0 = stablecoin) dan puncak terakhir sejak masuk."""
    pos, puncak, out = 1.0, c.iloc[0], []
    for dt, px in c.items():
        if pos:
            puncak = max(puncak, px)
            if px <= puncak * (1 - jarak):
                pos = 0.0
        elif px > tinggi20.loc[dt]:
            pos, puncak = 1.0, px
        out.append(pos)
    return pd.Series(out, index=c.index), puncak


def b6_trailing(coin: str, jarak: float, akhir: str | None = AKHIR) -> pd.Series:
    c = harga(coin)["c"].loc[MULAI:akhir]
    tinggi20 = harga(coin)["c"].rolling(20).max().shift(1).reindex(c.index)
    return trailing(c, tinggi20, jarak)[0]


def b3_cicil_5x(coin: str, modal: float = 1.0) -> pd.Series:
    """KMS-I3: candle mingguan (Senin 00.00 UTC), RSI(14) cara TradingView; tiap minggu RSI < 30 beli 1/5 modal
    siklus, tiap minggu RSI > 70 jual 1/5 posisi saat fase jual dimulai. Eksekusi di open Senin berikutnya."""
    p = harga(coin)
    w = p.resample("W-SUN").agg({"o": "first", "c": "last"}).dropna()
    delta = w["c"].diff()
    naik, turun = delta.clip(lower=0), -delta.clip(upper=0)
    rs = naik.ewm(alpha=1 / 14, adjust=False).mean() / turun.ewm(alpha=1 / 14, adjust=False).mean()
    rsi = 100 - 100 / (1 + rs)
    fee = biaya(coin)
    idx = hari()
    c = p["c"].reindex(idx)
    units, cash, k_siklus, jatah_jual = 0.0, modal, modal, 0.0
    aksi = {}                                         # tanggal eksekusi (Senin) → "beli"/"jual"
    for i in range(14, len(w) - 1):
        senin = w.index[i] + pd.Timedelta(days=1)
        if rsi.iloc[i] < 30:
            aksi[senin] = "beli"
        elif rsi.iloc[i] > 70:
            aksi[senin] = "jual"
    out = []
    for dt in idx:
        a = aksi.get(dt)
        px = p["o"].get(dt, np.nan)
        if a == "beli" and cash >= k_siklus / 5 * 0.999 and not np.isnan(px):
            uang = min(k_siklus / 5, cash)
            units += uang / (px * (1 + fee))
            cash -= uang
            jatah_jual = 0.0
        elif a == "jual" and units > 0 and not np.isnan(px):
            if jatah_jual == 0.0:
                jatah_jual = units / 5
            jual = min(jatah_jual, units)
            cash += jual * px * (1 - fee)
            units -= jual
            if units <= 1e-12:
                units, k_siklus, jatah_jual = 0.0, cash, 0.0
        out.append(units * c.loc[dt] + cash)
    return pd.Series(out, index=idx)


# ---------------------------------------------------------------- portofolio dengan rebalance (B1, B2)

def keranjang_alt(tanggal: pd.Timestamp, n: int = 5) -> list[str]:
    skor = {}
    for coin in ALTCOIN:
        p = harga(coin)
        sebelum = p.loc[:tanggal - pd.Timedelta(days=1)]
        if len(sebelum) < 30 or sebelum.index[-1] < tanggal - pd.Timedelta(days=2):
            continue
        skor[coin] = sebelum["qv"].iloc[-90:].sum()
    return [c for c, _ in sorted(skor.items(), key=lambda x: -x[1])[:n]]


def keranjang_meme(tanggal: pd.Timestamp) -> list[str]:
    out = []
    for coin in MEME:
        p = harga(coin)
        sebelum = p.loc[:tanggal - pd.Timedelta(days=1)]
        if len(sebelum) and sebelum.index[-1] >= tanggal - pd.Timedelta(days=2):
            out.append(coin)
    return out


def bobot_i1(tanggal: pd.Timestamp, versi: str) -> dict[str, float]:
    if versi == "I1b":
        return {"BTC": 0.5, "ETH": 0.5}
    if versi == "I1c":
        return {"BTC": 0.7}
    alt = keranjang_alt(tanggal)
    meme = [] if versi == "I1a_tanpa_meme" else keranjang_meme(tanggal)   # cek tambahan: porsi meme → stablecoin
    w = {"BTC": 0.7}
    for c in alt:
        w[c] = w.get(c, 0.0) + 0.15 / len(alt)
    for c in meme:
        w[c] = w.get(c, 0.0) + 0.15 / len(meme)
    return w


def awal_kuartal(idx: pd.DatetimeIndex) -> set:
    q = pd.Series(idx, index=idx).groupby(idx.to_period("Q")).first()
    return set(q.to_list())


def b1_alokasi(versi: str, modal: float = 1.0) -> tuple[pd.Series, list]:
    idx = hari()
    reb = awal_kuartal(idx) | {idx[0]}
    units: dict[str, float] = {}
    cash, out, riwayat = modal, [], []
    for dt in idx:
        # koin yang sudah delisting: jual di close terakhir
        for coin in list(units):
            p = harga(coin)
            if dt > p.index[-1]:
                cash += units.pop(coin) * p["c"].iloc[-1] * (1 - biaya(coin))
        if dt in reb:
            w = bobot_i1(dt, versi)
            riwayat.append((dt, w))
            px = {c: harga(c)["o"].get(dt, np.nan) for c in set(units) | set(w)}
            nilai = cash + sum(u * px[c] for c, u in units.items())
            for coin in set(units) | set(w):
                if np.isnan(px[coin]):
                    continue
                mau = w.get(coin, 0.0) * nilai / px[coin]
                beda = mau - units.get(coin, 0.0)
                cash -= beda * px[coin] + abs(beda) * px[coin] * biaya(coin)
                units[coin] = mau
                if mau == 0:
                    units.pop(coin)
        nilai = cash + sum(u * harga(c)["c"].get(dt, harga(c)["c"].iloc[-1]) for c, u in units.items())
        out.append(nilai)
    return pd.Series(out, index=idx), riwayat


def b2_moon_bag(pakai_moon: bool, setoran: float = 100.0) -> tuple[pd.Series, pd.Series]:
    """Cicilan bulanan ke komposisi I1a. Kalau nilai lot aktif satu koin ≥ 2× modalnya, jual 50% (ke kas),
    sisanya menjadi moon bag yang tidak dijual. Hasil: (nilai, total setoran)."""
    idx = hari()
    bulan_awal = set(pd.Series(idx, index=idx).groupby(idx.to_period("M")).first().to_list())
    aktif: dict[str, list] = {}       # coin → [units, modal]
    moon: dict[str, float] = {}
    cash, setor, nilai_out, setor_out = 0.0, 0.0, [], []
    jual_besok: list[str] = []
    for dt in idx:
        for coin in list(set(aktif) | set(moon)):
            p = harga(coin)
            if dt > p.index[-1]:
                u = aktif.pop(coin, [0.0, 0.0])[0] + moon.pop(coin, 0.0)
                cash += u * p["c"].iloc[-1] * (1 - biaya(coin))
        for coin in jual_besok:
            if coin in aktif and dt in harga(coin).index:
                u, _ = aktif.pop(coin)
                px = harga(coin)["o"].loc[dt]
                cash += u / 2 * px * (1 - biaya(coin))
                moon[coin] = moon.get(coin, 0.0) + u / 2
        jual_besok = []
        if dt in bulan_awal:
            setor += setoran
            q = dt.to_period("Q").start_time
            for coin, w in bobot_i1(max(q, idx[0]), "I1a").items():
                px = harga(coin)["o"].get(dt, np.nan)
                if np.isnan(px):
                    cash += setoran * w
                    continue
                u = setoran * w / (px * (1 + biaya(coin)))
                a = aktif.setdefault(coin, [0.0, 0.0])
                a[0] += u
                a[1] += setoran * w
            sisa = setoran - sum(bobot_i1(max(q, idx[0]), "I1a").values()) * setoran
            cash += sisa                               # porsi meme sebelum ada meme coin
        nilai = cash
        for coin in set(aktif) | set(moon):
            px = harga(coin)["c"].get(dt, np.nan)
            if np.isnan(px):
                continue
            u_aktif = aktif.get(coin, [0.0, 0.0])
            nilai += (u_aktif[0] + moon.get(coin, 0.0)) * px
            if pakai_moon and u_aktif[0] > 0 and u_aktif[0] * px >= 2 * u_aktif[1]:
                jual_besok.append(coin)
        nilai_out.append(nilai)
        setor_out.append(setor)
    return pd.Series(nilai_out, index=idx), pd.Series(setor_out, index=idx)


# ---------------------------------------------------------------- statistik

def statistik(eq: pd.Series) -> dict:
    r = eq.pct_change().dropna()
    tahun = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / tahun) - 1 if eq.iloc[-1] > 0 else -1.0
    sub = {nama: 100 * (eq.loc[a:z].iloc[-1] / eq.loc[a:z].iloc[0] - 1) for nama, a, z in SUB}
    a, z = UJI_AKHIR
    return {"cagr": 100 * cagr, "total": 100 * (eq.iloc[-1] / eq.iloc[0] - 1),
            "sharpe": r.mean() / r.std() * np.sqrt(365) if r.std() > 0 else 0.0,
            "dd": -100 * (eq / eq.cummax() - 1).min(), "sub": sub,
            "uji_akhir": 100 * (eq.loc[a:z].iloc[-1] / eq.loc[a:z].iloc[0] - 1),
            "waktu_di_pasar": None}


def statistik_cicilan(nilai: pd.Series, setor: pd.Series) -> dict:
    rasio = nilai / setor.replace(0, np.nan)
    rasio = rasio.dropna()
    return {"setor": float(setor.iloc[-1]), "nilai": float(nilai.iloc[-1]), "kelipatan": float(rasio.iloc[-1]),
            "dd": -100 * (rasio / rasio.cummax() - 1).min()}


def layak(st: dict, patokan: dict) -> dict:
    s = {"Sharpe lebih tinggi": st["sharpe"] > patokan["sharpe"],
         "penurunan lebih kecil": st["dd"] < patokan["dd"],
         "untung ≥ 2 dari 3 sub-periode": sum(v > 0 for v in st["sub"].values()) >= 2}
    return {"syarat": s, "lolos": all(s.values())}


def semua() -> dict:
    """Jalankan semua versi; hasil: nama → dict(eq, stat, patokan, layak)."""
    hasil = {}
    bh_btc = sleeve("BTC", pd.Series(1.0, index=hari()))
    bh_eth = sleeve("ETH", pd.Series(1.0, index=hari()), 0.5)
    bh_campur = sleeve("BTC", pd.Series(1.0, index=hari()), 0.5) + bh_eth
    pat = {"BTC": statistik(bh_btc), "BTC+ETH": statistik(bh_campur)}
    hasil["Beli-tahan BTC"] = {"eq": bh_btc, "stat": pat["BTC"], "patokan": None}
    hasil["Beli-tahan BTC+ETH 50/50"] = {"eq": bh_campur, "stat": pat["BTC+ETH"], "patokan": None}

    def tambah(nama, eq, patokan):
        st = statistik(eq)
        hasil[nama] = {"eq": eq, "stat": st, "patokan": patokan, **layak(st, pat[patokan])}

    a1 = sleeve("BTC", a1_filter_tren("BTC"), 0.5) + sleeve("ETH", a1_filter_tren("ETH"), 0.5)
    tambah("A1 Filter tren SMA 200 (BTC+ETH)", a1, "BTC+ETH")
    tambah("A1 Filter tren SMA 200 (BTC saja)", sleeve("BTC", a1_filter_tren("BTC")), "BTC")
    for v, nama in [("I1a", "B1 Alokasi 70/15/15 (BTC/altcoin/meme)"), ("I1b", "B1 Pasif BTC+ETH 50/50 (rebalance)"),
                    ("I1c", "B1 70% BTC + 30% stablecoin")]:
        eq, riwayat = b1_alokasi(v)
        tambah(nama, eq, "BTC+ETH")
        hasil[nama]["riwayat"] = riwayat
    tambah("B3 Cicil 5× masuk/keluar RSI mingguan (BTC+ETH)", b3_cicil_5x("BTC", 0.5) + b3_cicil_5x("ETH", 0.5),
           "BTC+ETH")
    tambah("B4 Fear & Greed (BTC)", sleeve("BTC", b4_fear_greed()), "BTC")
    tambah("B5 Halving: 365 hari sebelum s.d. 365 hari sesudah (BTC)", sleeve("BTC", b5_halving(365)), "BTC")
    tambah("B5 Halving: 365 hari sebelum s.d. 500 hari sesudah (BTC)", sleeve("BTC", b5_halving(500)), "BTC")
    for j in (0.10, 0.05):
        eq = sleeve("BTC", b6_trailing("BTC", j), 0.5) + sleeve("ETH", b6_trailing("ETH", j), 0.5)
        tambah(f"B6 Trailing stop {int(j * 100)}% (BTC+ETH)", eq, "BTC+ETH")
    moon = b2_moon_bag(True)
    tanpa = b2_moon_bag(False)
    hasil["B2 Cicilan bulanan 70/15/15 dengan moon bag"] = {"cicilan": statistik_cicilan(*moon), "eq": moon[0],
                                                             "setor": moon[1]}
    hasil["B2 Cicilan bulanan 70/15/15 tanpa moon bag"] = {"cicilan": statistik_cicilan(*tanpa), "eq": tanpa[0],
                                                            "setor": tanpa[1]}
    m, t = hasil["B2 Cicilan bulanan 70/15/15 dengan moon bag"], hasil["B2 Cicilan bulanan 70/15/15 tanpa moon bag"]
    m["lolos"] = m["cicilan"]["kelipatan"] > t["cicilan"]["kelipatan"] and m["cicilan"]["dd"] < t["cicilan"]["dd"]
    return hasil
