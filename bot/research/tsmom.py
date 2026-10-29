"""Patokan sistematis dari riset: time-series momentum (TSMOM).

Sumber: Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum", Journal of Financial
Economics 104(2); juga Hurst, Ooi & Pedersen (2017), "A Century of Evidence on
Trend-Following Investing". Aturannya sederhana dan dipakai apa adanya (satu varian,
tanpa penyetelan):

- Akhir tiap bulan: arah = tanda return 12 bulan terakhir (naik → long, turun → short).
- Ukuran posisi diatur supaya tiap instrumen punya volatilitas sasaran yang sama:
  bobot = arah × (10% ÷ √N) ÷ volatilitas tahunan perkiraan (EWMA return harian,
  pusat massa 60 hari, seperti di makalah). Target volatilitas portofolio ±10% per tahun.
- Posisi dipegang sebulan; total nilai posisi dibatasi leverage pasar (forex 10×,
  kripto 1×). Versi kripto "spot" = hanya long (arah turun → tidak pegang posisi).
- Biaya: setengah spread (kripto: komisi + setengah spread) dari setiap perubahan posisi,
  dan swap harian di forex (selisih suku bunga + biaya admin, sama dengan mesin utama).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from bot.data.candles import load_instrument
from bot.engine.costs import swap_rate
from bot.markets import INSTRUMENTS, MARKETS


def _daily_closes(symbols) -> pd.DataFrame:
    cols = {}
    for s in symbols:
        d1 = load_instrument(s)["D1"]
        cols[s] = pd.Series(d1.c, index=pd.to_datetime(d1.day * 86400 * 10**9))
    return pd.DataFrame(cols).sort_index().ffill()


def run_tsmom(market: str, start: str, end: str, target_vol: float = 0.10, long_only: bool = False,
              lookback_days: int = 365) -> dict:
    m = MARKETS[market]
    syms = list(m.instruments)
    px = _daily_closes(syms)
    ret = px.pct_change().fillna(0.0)
    periods = 365 if market == "crypto" else 261
    vol = np.sqrt((ret ** 2).ewm(com=60, min_periods=60).mean() * periods)
    # return 12 bulan: harga hari ini dibanding harga ±365 hari kalender sebelumnya
    past = px.reindex(px.index - pd.Timedelta(days=lookback_days), method="ffill")
    past.index = px.index
    signal = np.sign(px / past - 1).fillna(0.0)
    if long_only:
        signal = signal.clip(lower=0)
    per_inst = target_vol / np.sqrt(len(syms))
    month_end = px.index.to_series().groupby(px.index.to_period("M")).transform("max") == px.index.to_series()
    idx = px.loc[start:end].index
    eq = 1.0
    notional = pd.Series(0.0, index=syms)
    out_eq, cost_tot, swap_tot = [], 0.0, 0.0
    prev_day = None
    for day in idx:
        if prev_day is not None:
            r = ret.loc[day]
            pnl = float((notional * r).sum())
            # swap harian untuk forex (akhir pekan = 3 malam karena selisih hari kalender)
            days = (day - prev_day).days
            sw = 0.0
            for s in syms:
                inst = INSTRUMENTS[s]
                if inst.swap and notional[s] != 0:
                    rate = swap_rate(inst.base_ccy, inst.quote_ccy, int(np.sign(notional[s])),
                                     day.strftime("%Y-%m"), inst.swap_markup)
                    sw += abs(notional[s]) * rate * days / 365.0
            notional = notional * (1 + r)
            eq += pnl + sw
            swap_tot += sw
        if month_end.loc[day] or prev_day is None:
            w = signal.loc[day] * (per_inst / vol.loc[day]).replace([np.inf], 0).fillna(0.0)
            gross = w.abs().sum()
            if gross > m.leverage_cap:
                w = w * m.leverage_cap / gross
            target = w * eq
            cost = 0.0
            for s in syms:
                half = float(INSTRUMENTS[s].spread(px.loc[day, s])) / 2 / px.loc[day, s]
                cost += abs(target[s] - notional[s]) * half
            eq -= cost
            cost_tot += cost
            notional = target
        out_eq.append(eq)
        prev_day = day
    s = pd.Series(out_eq, index=idx)
    return {"equity": s, "costs": cost_tot, "swap": swap_tot, **stats(s, periods)}


def stats(eq: pd.Series, periods: int) -> dict:
    if len(eq) < 2:
        return {}
    r = eq.pct_change().dropna()
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1 if years > 0 and eq.iloc[-1] > 0 else np.nan
    vol = r.std() * np.sqrt(periods)
    dd = (eq / eq.cummax() - 1).min()
    yearly = eq.resample("YE").last().pct_change()
    yearly.iloc[0] = eq.resample("YE").last().iloc[0] / eq.iloc[0] - 1
    return {"total_pct": 100 * (eq.iloc[-1] / eq.iloc[0] - 1), "cagr_pct": 100 * cagr, "vol_pct": 100 * vol,
            "sharpe": r.mean() / r.std() * np.sqrt(periods) if r.std() > 0 else np.nan,
            "max_dd_pct": -100 * dd, "yearly": {int(i.year): 100 * v for i, v in yearly.items()},
            "years": years}
