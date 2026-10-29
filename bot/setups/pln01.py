"""PLN-01 · Pola N: impuls → koreksi sempit → tembus (rulebook 06 bagian A)."""
from __future__ import annotations

from bot import indicators as ind
from bot.engine.orders import Order
from bot.setups.base import Setup, TestPlan

NS_H = 3600 * 10**9


class PolaN(Setup):
    id = "PLN-01"
    name = "Pola N (impuls → koreksi sempit → tembus)"
    mentor = "Mentor forex_2 (Pola N)"
    priority = 1
    category = "breakout"
    entry_tf = "H1"
    defaults = {
        "corr_max": 3,        # jumlah candle koreksi maksimal (Q-34)
        "corr_depth": 0.5,    # kedalaman koreksi maksimal, pecahan panjang impuls (Q-34)
        "rr": 1.5,            # TP 1:1,5 atau 1:2, keduanya dari mentor (setara)
        "session": True,      # order hanya dipasang 18.00–23.59 WIB (pembanding: tanpa batas jam)
    }

    def plan(self) -> TestPlan:
        return TestPlan(setara={"rr": [1.5, 2.0]},
                        tested={"corr_max": [2, 3, 4], "corr_depth": [0.25, 0.5, 0.75]},
                        comparisons={"session": [True, False]})

    def signals_for(self, sym, d, p):
        b = d["H1"]
        o, h, l, c = b.o, b.h, b.l, b.c
        strong = ind.strong_candle(o, h, l, c, 0.7)
        bull_imp = strong & (c > o)
        bear_imp = strong & (c < o)
        # jam WIB (UTC+7) saat order dipasang = waktu close candle sinyal
        wib_hour = ((b.t_close // NS_H) + 7) % 24
        in_session = (wib_hour >= 18) & (wib_hour <= 23)
        n = len(c)
        kmax = int(p["corr_max"])
        depth = float(p["corr_depth"])
        out: list[Order] = []
        for j in range(2, n - 1):
            if p["session"] and not in_session[j]:
                continue
            for m in range(1, kmax + 1):           # m = jumlah candle koreksi, impuls di j−m
                i = j - m
                if i < 0:
                    break
                found = []
                for dirn, imp in ((1, bull_imp), (-1, bear_imp)):
                    if not imp[i]:
                        continue
                    seg_h = h[i + 1: j + 1]
                    seg_l = l[i + 1: j + 1]
                    rng = h[i] - l[i]
                    if dirn > 0:
                        # koreksi tidak membuat high baru di atas impuls dan tidak lebih dalam dari batas
                        if seg_h.max() > h[i] or h[i] - seg_l.min() > depth * rng:
                            continue
                        entry, sl = seg_h.max(), seg_l.min()   # buy stop di atas wick tertinggi koreksi
                    else:
                        if seg_l.min() < l[i] or seg_h.max() - l[i] > depth * rng:
                            continue
                        entry, sl = seg_l.min(), seg_h.max()
                    if (entry - sl) * dirn > 0:
                        found.append((dirn, entry, sl))
                if len(found) == 1:                  # impuls terbaru yang memenuhi syarat dipakai
                    dirn, entry, sl = found[0]
                    out.append(Order(
                        self.id, sym, dirn, int(b.t_close[j]), "stop", sl=float(sl), price=float(entry),
                        tp_rr=float(p["rr"]), min_rr=1.5, expiry=int(b.t_close[j + 1]),
                        entry_tf="H1", tags={"koreksi": m}))
                if found:
                    break
        return out
