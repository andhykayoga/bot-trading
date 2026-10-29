"""Pemeriksaan mesin: entry acak dengan SL = TP = 1 × ATR(14).

Kalau mesin benar, hasil rata-rata per transaksi ≈ minus biaya (spread + swap) saja,
karena arah acak tidak punya keunggulan. Angka ini juga menunjukkan berapa besar
"pajak biaya" yang harus dikalahkan sebuah setup di tiap timeframe.
"""
from __future__ import annotations

import numpy as np

from bot.data.candles import load_instrument
from bot.engine.backtest import Simulator
from bot.engine.orders import Order
from bot.setups.base import Ctx


def random_entries(sim: Simulator, start: int, end: int, tfs=("M15", "H1", "H4", "D1"), seed: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    out = {}
    for tf in tfs:
        orders = []
        step = {"M15": 29, "H1": 7, "H4": 3, "D1": 1}[tf]
        for s in sim.syms:
            ctx = Ctx.get(load_instrument(s), tf)
            b, a = ctx.b, ctx.atr
            for t in range(50, len(b), step):
                if np.isnan(a[t]):
                    continue
                d = int(rng.choice([1, -1]))
                orders.append(Order("ACAK", s, d, int(b.t_close[t]), "market", sl=float(b.c[t] - d * a[t]),
                                    tp_rr=1.0, min_rr=0.99, entry_tf=tf))
        res = sim.run(orders, start, end)
        r = np.array([t.r for t in res.trades])
        out[tf] = {"trades": len(r), "avg_r": float(r.mean()) if len(r) else np.nan,
                   "win_rate": float((r > 0).mean() * 100) if len(r) else np.nan}
    return out
