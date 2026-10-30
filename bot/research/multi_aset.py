"""Rancangan A2: trend-following multi-aset terdiversifikasi (reports/RENCANA_MODUL_BARU.md).

34 CFD OANDA harian. Akhir bulan: arah = tanda return 252 hari bursa; bobot = arah × (10% ÷ √N) ÷ volatilitas
(EWMA, pusat massa 60), lalu portofolio diskalakan ke perkiraan volatilitas 10% per tahun (kovarians 252 hari),
total nilai posisi maksimal 6× modal. Return harga dipakai sebagai perkiraan return berjangka.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "harian"
KELAS = {
    "indeks": ["SPX500USD", "NAS100USD", "US2000USD", "DE30EUR", "UK100GBP", "FR40EUR", "EU50EUR", "JP225USD",
               "AU200AUD", "HK33HKD"],
    "obligasi": ["USB02YUSD", "USB05YUSD", "USB10YUSD", "USB30YUSD", "DE10YBEUR", "UK10YBGBP"],
    "logam": ["XAUUSD", "XAGUSD", "XPTUSD", "XCUUSD"],
    "minyak": ["WTICOUSD", "BCOUSD"],
    "gas_pertanian": ["NATGASUSD", "CORNUSD", "SOYBNUSD", "WHEATUSD", "SUGARUSD"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"],
}
SPREAD_BP = {"indeks": 1.5, "obligasi": 2.0, "logam": 2.0, "minyak": 4.0, "gas_pertanian": 10.0, "forex": 1.0}
FINANCING = {"indeks": 0.025, "obligasi": 0.025, "logam": 0.025, "minyak": 0.025, "gas_pertanian": 0.025,
             "forex": 0.01}
MULAI, TARGET, LEV_MAX, HARI = "2006-01-01", 0.10, 6.0, 261
SUB = [("2006–2011", "2006-01-01", "2011-12-31"), ("2012–2018", "2012-01-01", "2018-12-31"),
       ("2019–2026", "2019-01-01", "2026-12-31")]


def kelas_of(sym: str) -> str:
    return next(k for k, v in KELAS.items() if sym in v)


def harga() -> pd.DataFrame:
    cols = {}
    for syms in KELAS.values():
        for s in syms:
            d = pd.read_parquet(DATA / f"{s}.parquet")
            # candle harian OANDA dibuka 17.00 New York; diberi tanggal hari close-nya
            t = (pd.to_datetime(d["time"], unit="s") + pd.Timedelta(hours=7)).dt.normalize()
            cols[s] = pd.Series(d["close"].to_numpy(), index=t)
    px = pd.DataFrame(cols).sort_index()
    px = px[px.index.dayofweek < 5]
    return px.ffill(limit=5)


def jalankan(biaya: str = "ritel") -> dict:
    px = harga()
    syms = list(px.columns)
    ret = px.pct_change(fill_method=None)
    ada = px.notna().cumsum() >= 300
    vol = np.sqrt((ret ** 2).ewm(com=60, min_periods=60).mean() * HARI)
    arah = np.sign(px / px.shift(252) - 1)
    bulan_akhir = px.index.to_series().groupby(px.index.to_period("M")).transform("max") == px.index.to_series()
    idx = px.loc[MULAI:].index
    kelas = pd.Series({s: kelas_of(s) for s in syms})
    half = kelas.map(SPREAD_BP) / 1e4 * (2.0 if biaya == "ritel" else 1.0)
    fin = kelas.map(FINANCING) if biaya == "ritel" else kelas.map(lambda _: 0.0)
    eq, notional = 1.0, pd.Series(0.0, index=syms)
    out, gross_out, biaya_tot, fin_tot, kontrib = [], [], 0.0, 0.0, pd.Series(0.0, index=syms)
    prev = None
    for day in idx:
        if prev is not None:
            r = ret.loc[day].fillna(0.0)
            pnl = notional * r
            hari = (day - prev).days
            f = float((notional.abs() * fin).sum() * hari / 365)
            eq += float(pnl.sum()) - f
            kontrib += pnl - notional.abs() * fin * hari / 365
            fin_tot += f
            notional = notional * (1 + r)
        if bulan_akhir.loc[day] or prev is None:
            ok = ada.loc[day] & vol.loc[day].notna() & arah.loc[day].notna() & (vol.loc[day] > 0)
            n = int(ok.sum())
            w = pd.Series(0.0, index=syms)
            if n:
                w[ok] = arah.loc[day][ok] * (TARGET / np.sqrt(n)) / vol.loc[day][ok]
                jendela = ret.loc[:day].iloc[-252:][w.index[ok]].fillna(0.0)
                cov = jendela.cov().to_numpy() * HARI
                wv = w[ok].to_numpy()
                sig = float(np.sqrt(wv @ cov @ wv))
                if sig > 0:
                    w *= TARGET / sig
                g = w.abs().sum()
                if g > LEV_MAX:
                    w *= LEV_MAX / g
            target = w * eq
            c = float(((target - notional).abs() * half).sum())
            eq -= c
            biaya_tot += c
            kontrib -= (target - notional).abs() * half
            notional = target
        out.append(eq)
        gross_out.append(float(notional.abs().sum() / eq) if eq > 0 else 0.0)
        prev = day
    s = pd.Series(out, index=idx)
    return {"eq": s, "gross": pd.Series(gross_out, index=idx), "biaya": biaya_tot, "financing": fin_tot,
            "kontrib_kelas": kontrib.groupby(kelas).sum(), **statistik(s)}


def statistik(eq: pd.Series) -> dict:
    r = eq.pct_change().dropna()
    tahun = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / tahun) - 1 if eq.iloc[-1] > 0 else -1.0
    tahunan = eq.resample("YE").last().pct_change()
    tahunan.iloc[0] = eq.resample("YE").last().iloc[0] / eq.iloc[0] - 1
    return {"cagr": 100 * cagr, "vol": 100 * r.std() * np.sqrt(HARI),
            "sharpe": r.mean() / r.std() * np.sqrt(HARI) if r.std() > 0 else 0.0,
            "t": r.mean() / r.std() * np.sqrt(len(r)) if r.std() > 0 else 0.0,
            "dd": -100 * (eq / eq.cummax() - 1).min(),
            "sub": {nama: 100 * ((eq.loc[a:z].iloc[-1] / eq.loc[a:z].iloc[0]) **
                                 (365.25 / max((eq.loc[a:z].index[-1] - eq.loc[a:z].index[0]).days, 1)) - 1)
                    for nama, a, z in SUB},
            "tahunan": {int(k.year): 100 * v for k, v in tahunan.items()}}


def layak(st: dict) -> dict:
    s = {"t-stat ≥ 2,0": st["t"] >= 2.0, "untung ≥ 2 dari 3 sub-periode": sum(v > 0 for v in st["sub"].values()) >= 2,
         "hasil ≥ 2% per tahun": st["cagr"] >= 2.0, "penurunan ≤ 20%": st["dd"] <= 20.0}
    return {"syarat": s, "lolos": all(s.values())}
