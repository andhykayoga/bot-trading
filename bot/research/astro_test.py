"""Uji filter waktu Astronacci sebelum dipakai (rulebook 07, "Cara menguji sebelum dipakai").

WKT-01/02/03: apakah tanggal kandidat lebih sering menjadi titik balik (swing D1
fractal 2–2) dibanding hari biasa? Pilihan uji (jendela ±1/±2, cara a/b, ambang ≥3/≥4)
dipilih di data penyusunan & pemilihan, lalu dicek sekali di uji akhir.
WKT-04: apakah setup breakout lebih sering kena SL saat Merkurius retrograde?
"""
from __future__ import annotations

import numpy as np
from scipy.stats import fisher_exact

from bot.data.candles import load_instrument
from bot.filters import astro
from bot.research.splits import Splits

MIN_CAND = 30


def paper_turning_points(d1) -> np.ndarray:
    """Versi makalah Gema: high naik 2× berturut-turut sebelum puncak dan turun 2× sesudahnya."""
    h, l = d1.h, d1.l
    n = len(h)
    tp = np.zeros(n, bool)
    for i in range(2, n - 2):
        peak = h[i - 2] < h[i - 1] < h[i] > h[i + 1] > h[i + 2]
        trough = l[i - 2] > l[i - 1] > l[i] < l[i + 1] < l[i + 2]
        tp[i] = peak or trough
    return tp


def _stats(cand: np.ndarray, tp: np.ndarray) -> dict:
    a, b = int((cand & tp).sum()), int((cand & ~tp).sum())
    c, d = int((~cand & tp).sum()), int((~cand & ~tp).sum())
    rc = a / (a + b) if a + b else np.nan
    rn = c / (c + d) if c + d else np.nan
    p = fisher_exact([[a, b], [c, d]], alternative="greater")[1] if a + b and c + d else np.nan
    return {"n_cand": a + b, "n_other": c + d, "rate_cand": rc, "rate_other": rn,
            "lift": rc / rn if rn else np.nan, "p": float(p)}


def turning_point_test(splits: Splits, symbols: list[str]) -> dict:
    rows = []
    per = {}
    for s in symbols:
        d1 = load_instrument(s)["D1"]
        per[s] = (d1, astro.turning_points(d1), paper_turning_points(d1))
    for adef in astro.all_defs():
        row = {"def": adef, "label": adef.label}
        for seg in ("dev", "sel", "final"):
            a, b = splits.seg(seg)
            cands, tps, tpp = [], [], []
            for s, (d1, tp, tp_paper) in per.items():
                m = (d1.t_open >= a) & (d1.t_open < b)
                c = astro.candidate_days(d1, adef)
                cands.append(c[m]); tps.append(tp[m]); tpp.append(tp_paper[m])
            cand, tp, tp_paper = np.concatenate(cands), np.concatenate(tps), np.concatenate(tpp)
            row[seg] = _stats(cand, tp)
            row[seg + "_paper"] = _stats(cand, tp_paper)
        rows.append(row)
    ok = [r for r in rows if r["dev"]["lift"] > 1 and r["sel"]["n_cand"] >= MIN_CAND and r["sel"]["lift"] > 1]
    pool = ok if ok else rows
    chosen = max(pool, key=lambda r: r["sel"]["lift"])
    fin = chosen["final"]
    verdict = "lolos" if fin["lift"] > 1 and fin["p"] < 0.05 else "buang (tidak lebih baik dari acak)"
    return {"rows": rows, "chosen": chosen, "chosen_ok_in_dev_sel": bool(ok), "verdict": verdict}


def retro_test(trades_by_seg: dict[str, list[dict]]) -> dict:
    """trades_by_seg: {"sel": [...], "final": [...]} transaksi setup breakout (entry_day, kena_sl)."""
    retro = astro.retro_day_set()
    out = {}
    for seg, trades in trades_by_seg.items():
        if not trades:
            out[seg] = None
            continue
        r = np.array([t["day"] in retro for t in trades])
        sl = np.array([t["sl"] for t in trades])
        a, b = int((r & sl).sum()), int((r & ~sl).sum())
        c, d = int((~r & sl).sum()), int((~r & ~sl).sum())
        p = fisher_exact([[a, b], [c, d]], alternative="greater")[1] if a + b and c + d else np.nan
        out[seg] = {"n_retro": a + b, "n_other": c + d,
                    "sl_rate_retro": a / (a + b) if a + b else np.nan,
                    "sl_rate_other": c / (c + d) if c + d else np.nan, "p": float(p)}
    s = out.get("sel")
    out["verdict_sel"] = "lebih sering gagal saat retrograde" if s and s["sl_rate_retro"] > s["sl_rate_other"] \
        and s["p"] < 0.05 else "tidak terbukti"
    f = out.get("final")
    out["verdict_final"] = "lebih sering gagal saat retrograde" if f and f["sl_rate_retro"] > f["sl_rate_other"] \
        and f["p"] < 0.05 else "tidak terbukti"
    return out
