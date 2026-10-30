"""Ukuran hasil backtest (G-14 butir 3, G-17 bagian 3)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from bot.engine.backtest import Result


def _streaks(wins: np.ndarray) -> tuple[int, int]:
    best_w = best_l = cur = 0
    last = None
    for w in wins:
        cur = cur + 1 if w == last else 1
        last = w
        if w:
            best_w = max(best_w, cur)
        else:
            best_l = max(best_l, cur)
    return best_w, best_l


def summarize(res: Result, symbols: list[str] | None = None) -> dict:
    """Ringkasan satu periode. `symbols` membatasi ke instrumen tertentu (equity
    dihitung ulang hanya dari transaksi instrumen itu)."""
    trades = [t for t in res.trades if symbols is None or t.symbol in symbols]
    sub = res if symbols is None else Result(res.sim, trades, res.i_start, res.i_end, res.stats)
    init = res.sim.rules.initial_balance
    n = len(trades)
    out = {"trades": n}
    if n == 0:
        out.update(net=0.0, net_pct=0.0, max_dd_pct=0.0, recovery=np.nan, win_rate=np.nan,
                   profit_factor=np.nan, avg_r=np.nan, max_win_streak=0, max_loss_streak=0,
                   pct_per_month=0.0, swap=0.0, dd_alarm=None)
        return out
    pnl = np.array([t.pnl for t in trades])
    eq = sub.equity()
    peak = np.maximum.accumulate(eq)
    dd = (peak - eq) / peak
    max_dd_abs = float((peak - eq).max())
    net = float(pnl.sum())
    months = (res.sim.g.t[res.i_end - 1] - res.sim.g.t[res.i_start]) / (30.44 * 86400e9)
    wins = pnl > 0
    gw, gl = pnl[wins].sum(), -pnl[~wins].sum()
    alarm_i = np.flatnonzero(dd >= res.sim.rules.dd_alarm)
    out.update(
        net=net,
        net_pct=100 * net / init,
        max_dd_pct=100 * float(dd.max()),
        recovery=net / max_dd_abs if max_dd_abs > 0 else np.inf,
        win_rate=100 * wins.mean(),
        profit_factor=float(gw / gl) if gl > 0 else np.inf,
        avg_r=float(np.mean([t.r for t in trades])),
        max_win_streak=_streaks(wins)[0],
        max_loss_streak=_streaks(wins)[1],
        pct_per_month=100 * net / init / months if months > 0 else 0.0,
        swap=float(sum(t.swap for t in trades)),
        dd_alarm=str(pd.Timestamp(res.sim.g.t[res.i_start + alarm_i[0]], tz="UTC").date()) if len(alarm_i) else None,
    )
    return out


def by_symbol(res: Result) -> dict[str, dict]:
    return {s: summarize(res, [s]) for s in res.sim.syms}
