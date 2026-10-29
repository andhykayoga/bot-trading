"""Uji forex "cepat" sesuai pra-registrasi reports/RENCANA_FOREX_CEPAT.md.

- Bagian A: hitungan impas jual-beli cepat (gerak harga per rentang waktu vs biaya).
- Bagian B: tiga strategi dari jurnal, satu varian masing-masing — S1 pola jam sesi (Ranaldo 2009; Breedon &
  Ranaldo 2013), S2 dolar di hari FOMC (Mueller, Tahbaz-Salehi & Vedolin 2017), S3 fixing London 16.00
  (Krohn, Mueller & Whelan 2024).
- Bagian C: demonstrasi mengotak-atik SMA cepat/lambat di EURUSD H1.

Return candle k = close k / close k−1 − 1; posisi candle k ditentukan dari waktu buka candle k. Setiap perubahan
posisi 1 unit dikenai setengah biaya pulang-pergi.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from bot.data.candles import load_instrument
from bot.markets import INSTRUMENTS

PAIRS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"]
PAIRS_BARU = ["AUDUSD", "USDCAD", "USDCHF", "NZDUSD"]
# Biaya pulang-pergi dalam pip: ECN (spread mentah rata-rata + komisi USD 7/lot) dan standar.
BIAYA_ECN = {"EURUSD": 0.9, "GBPUSD": 1.2, "USDJPY": 1.0, "AUDUSD": 1.0, "USDCAD": 1.2, "USDCHF": 1.2, "NZDUSD": 1.3}
BIAYA_STD = {"EURUSD": 1.4, "GBPUSD": 1.8, "USDJPY": 1.4, "AUDUSD": 1.6, "USDCAD": 2.0, "USDCHF": 1.8, "NZDUSD": 2.0}
MULAI = "2014-01-01"
SUB = [("2014–2017", "2014-01-01", "2017-12-31"), ("2018–2021", "2018-01-01", "2021-12-31"),
       ("2022–2026", "2022-01-01", "2100-01-01")]
PUSAT = {"USD": "America/New_York", "EUR": "Europe/Berlin", "GBP": "Europe/London", "JPY": "Asia/Tokyo",
         "AUD": "Australia/Sydney", "CAD": "America/Toronto", "CHF": "Europe/Zurich", "NZD": "Pacific/Auckland"}
# Rapat FOMC terjadwal (hari pengumuman), dari jadwal resmi Fed; dicek silang dengan kalender ekonomi.
FOMC = """2014-01-29 2014-03-19 2014-04-30 2014-06-18 2014-07-30 2014-09-17 2014-10-29 2014-12-17
2015-01-28 2015-03-18 2015-04-29 2015-06-17 2015-07-29 2015-09-17 2015-10-28 2015-12-16
2016-01-27 2016-03-16 2016-04-27 2016-06-15 2016-07-27 2016-09-21 2016-11-02 2016-12-14
2017-02-01 2017-03-15 2017-05-03 2017-06-14 2017-07-26 2017-09-20 2017-11-01 2017-12-13
2018-01-31 2018-03-21 2018-05-02 2018-06-13 2018-08-01 2018-09-26 2018-11-08 2018-12-19
2019-01-30 2019-03-20 2019-05-01 2019-06-19 2019-07-31 2019-09-18 2019-10-30 2019-12-11
2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split()
HARI_TAHUN = 261


def pip(symbol: str) -> float:
    return 0.01 if symbol.endswith("JPY") else 0.0001


def _menit_lokal(t_ns: np.ndarray, tz: str) -> tuple[np.ndarray, np.ndarray]:
    """(hari dalam minggu, menit sejak tengah malam) waktu setempat untuk tiap waktu UTC."""
    idx = pd.DatetimeIndex(t_ns.astype("datetime64[ns]")).tz_localize("UTC").tz_convert(tz)
    return idx.weekday.to_numpy(), (idx.hour * 60 + idx.minute).to_numpy()


def _buka(t_ns: np.ndarray, ccy: str) -> np.ndarray:
    wd, mnt = _menit_lokal(t_ns, PUSAT[ccy])
    return (wd < 5) & (mnt >= 8 * 60) & (mnt < 17 * 60)


def _rollover(t_ns: np.ndarray) -> np.ndarray:
    _, mnt = _menit_lokal(t_ns, "America/New_York")
    return (mnt >= 16 * 60 + 55) & (mnt < 17 * 60 + 5)


def _arah_usd(symbol: str) -> int:
    """+1 kalau 'beli USD' = beli pair (USD mata uang dasar), −1 kalau USD mata uang kuotasi."""
    inst = INSTRUMENTS[symbol]
    return 1 if inst.base_ccy == "USD" else -1


def posisi(strategi: str, symbol: str, t_ns: np.ndarray) -> np.ndarray:
    inst = INSTRUMENTS[symbol]
    pos = np.zeros(len(t_ns))
    if strategi == "S1":
        b, q = _buka(t_ns, inst.base_ccy), _buka(t_ns, inst.quote_ccy)
        pos[b & ~q] = -1.0
        pos[q & ~b] = 1.0
    elif strategi == "S2":
        for d in FOMC:
            hari = pd.Timestamp(d)
            a = (hari - pd.Timedelta(days=1) + pd.Timedelta(hours=17, minutes=5)).tz_localize("America/New_York")
            z = (hari + pd.Timedelta(hours=16, minutes=55)).tz_localize("America/New_York")
            m = (t_ns >= a.value) & (t_ns < z.value)
            pos[m] = -_arah_usd(symbol)
    elif strategi == "S3":
        wd, mnt = _menit_lokal(t_ns, "Europe/London")
        kerja = wd < 5
        pos[kerja & (mnt >= 15 * 60) & (mnt < 16 * 60)] = _arah_usd(symbol)
        pos[kerja & (mnt >= 16 * 60) & (mnt < 17 * 60)] = -_arah_usd(symbol)
    else:
        raise ValueError(strategi)
    pos[_rollover(t_ns)] = 0.0
    return pos


def _m5(symbol: str):
    b = load_instrument(symbol)["M5"]
    start = pd.Timestamp(MULAI, tz="UTC").value
    k = np.searchsorted(b.t_open, start)
    return b.t_open[k - 1:], b.c[k - 1:], b.day[k - 1:]


def harian(strategi: str, symbol: str) -> pd.DataFrame:
    """Return harian (pecahan nilai posisi) per pair: kotor, bersih ECN, bersih standar, jumlah transaksi."""
    t, c, day = _m5(symbol)
    r = c[1:] / c[:-1] - 1
    t, day, harga = t[1:], day[1:], c[:-1]
    pos = posisi(strategi, symbol, t)
    ubah = np.abs(np.diff(np.concatenate([[0.0], pos])))
    kotor = pos * r
    out = {"kotor": kotor, "transaksi": (ubah > 0) & (pos != 0)}
    for nama, tabel in [("ecn", BIAYA_ECN), ("std", BIAYA_STD)]:
        biaya = ubah * tabel[symbol] * pip(symbol) / 2 / harga
        out[nama] = kotor - biaya
    df = pd.DataFrame(out)
    df["day"] = pd.to_datetime(day.astype("int64") * 86400 * 10**9)
    return df.groupby("day").sum()


def portofolio(strategi: str) -> dict:
    per = {s: harian(strategi, s) for s in PAIRS}
    idx = sorted(set().union(*[d.index for d in per.values()]))
    cols = {k: pd.DataFrame({s: per[s][k].reindex(idx).fillna(0.0) for s in PAIRS}) for k in ["kotor", "ecn", "std"]}
    trans = pd.DataFrame({s: per[s]["transaksi"].reindex(idx).fillna(0) for s in PAIRS})
    return {"pair": cols, "transaksi": trans, "port": {k: v.mean(axis=1) for k, v in cols.items()}}


def statistik(d: pd.Series, target_vol: float = 0.10) -> dict:
    sd = d.std()
    tahun = len(d) / HARI_TAHUN
    k = target_vol / (sd * np.sqrt(HARI_TAHUN)) if sd > 0 else 0.0
    eq = (1 + k * d).cumprod()
    return {"t": d.mean() / sd * np.sqrt(len(d)) if sd > 0 else 0.0,
            "sharpe": d.mean() / sd * np.sqrt(HARI_TAHUN) if sd > 0 else 0.0,
            "per_tahun_10vol": 100 * (eq.iloc[-1] ** (1 / tahun) - 1), "dd_10vol": -100 * (eq / eq.cummax() - 1).min(),
            "skala": k, "per_tahun_1x": 100 * d.mean() * HARI_TAHUN,
            "sub": {nama: float(d.loc[a:z].mean() * HARI_TAHUN * 100) for nama, a, z in SUB}}


def nilai(strategi: str) -> dict:
    p = portofolio(strategi)
    st = {k: statistik(p["port"][k]) for k in ["kotor", "ecn", "std"]}
    aktif = [s for s in PAIRS if p["transaksi"][s].sum() > 0]
    per_pair = {s: {k: 100 * p["pair"][k][s].sum() / (len(p["pair"][k]) / HARI_TAHUN) for k in ["kotor", "ecn", "std"]}
                | {"transaksi_per_tahun": p["transaksi"][s].sum() / (len(p["transaksi"]) / HARI_TAHUN)}
                for s in PAIRS}
    e = st["ecn"]
    untung_pair = sum(per_pair[s]["ecn"] > 0 for s in aktif)
    syarat = {"t ≥ 2,4": e["t"] >= 2.4, "untung ≥ 2 dari 3 sub-periode": sum(v > 0 for v in e["sub"].values()) >= 2,
              "drawdown ≤ 20%": e["dd_10vol"] <= 20,
              "untung di ≥ 2/3 pair aktif": len(aktif) > 0 and untung_pair >= 2 / 3 * len(aktif)}
    return {"stat": st, "per_pair": per_pair, "aktif": aktif, "syarat": syarat, "lolos": all(syarat.values()),
            "untung_std": st["std"]["per_tahun_1x"] > 0, "port": p["port"]}


# ---------------------------------------------------------------- Bagian A

RENTANG = [("5 menit", "M5"), ("15 menit", "M15"), ("1 jam", "H1"), ("4 jam", "H4"), ("1 hari", "D1")]


def impas(symbol: str) -> list[dict]:
    d = load_instrument(symbol)
    start = pd.Timestamp(MULAI, tz="UTC").value
    out = []
    for nama, tf in RENTANG:
        b = d[tf]
        k = np.searchsorted(b.t_open, start)
        gerak = np.abs(np.diff(b.c[k - 1:])) / pip(symbol)
        out.append({"rentang": nama, "rata": gerak.mean(), "median": float(np.median(gerak))})
    m5 = out[0]["rata"]
    out.insert(0, {"rentang": "1 detik (perkiraan)", "rata": m5 / np.sqrt(300), "median": out[0]["median"] / np.sqrt(300)})
    for x in out:
        for nama, tabel in [("ecn", BIAYA_ECN), ("std", BIAYA_STD)]:
            x[f"impas_{nama}"] = 100 * (0.5 + tabel[symbol] / (2 * x["rata"]))
            x[f"biaya_{nama}_pct"] = 100 * tabel[symbol] / x["rata"]
    return out


# ---------------------------------------------------------------- Bagian C

def demo_otak_atik(symbol: str = "EURUSD") -> dict:
    b = load_instrument(symbol)["H1"]
    c = pd.Series(b.c, index=pd.to_datetime(b.t_open))
    r = c.pct_change().to_numpy()
    biaya = BIAYA_STD[symbol] * pip(symbol) / 2 / c.shift(1).to_numpy()
    t = c.index
    is_m = (t >= "2014-01-01") & (t < "2020-01-01")
    oos_m = t >= "2020-01-01"
    th_is, th_oos = is_m.sum() / (HARI_TAHUN * 24), oos_m.sum() / (HARI_TAHUN * 24)
    sma = {n: c.rolling(n).mean().to_numpy() for n in set(range(2, 51)) | set(range(10, 301, 5))}
    rows = []
    for f in range(2, 51):
        for s in range(10, 301, 5):
            if f >= s:
                continue
            sig = np.sign(sma[f] - sma[s])
            pos = np.concatenate([[0.0], sig[:-1]])           # sinyal close k−1 untuk return candle k
            pos = np.nan_to_num(pos)
            ubah = np.abs(np.diff(np.concatenate([[0.0], pos])))
            net = np.nan_to_num(pos * r - ubah * biaya)
            rows.append((f, s, 100 * net[is_m].sum() / th_is, 100 * net[oos_m].sum() / th_oos))
    df = pd.DataFrame(rows, columns=["cepat", "lambat", "is", "oos"])
    best = df.sort_values("is", ascending=False)
    return {"n": len(df), "terbaik": best.iloc[0].to_dict(), "top10_is": best["is"].head(10).mean(),
            "top10_oos": best["oos"].head(10).mean(), "pct_is_untung": 100 * (df["is"] > 0).mean(),
            "pct_oos_untung": 100 * (df["oos"] > 0).mean(), "spearman": df["is"].corr(df["oos"], method="spearman"),
            "terbaik_oos": df.sort_values("oos", ascending=False).iloc[0].to_dict(), "tabel": df}
