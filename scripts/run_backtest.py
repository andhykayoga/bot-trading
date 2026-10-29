"""Jalankan backtest lengkap sesuai rulebook G-14/G-17 untuk setup yang dinyalakan.

    python scripts/run_backtest.py                          # forex: semua setup di config/setups.toml
    python scripts/run_backtest.py --setups PLN-01,ICH-01 --jobs 4
    python scripts/run_backtest.py --market crypto          # setup mentor saham–kripto di BTC & ETH

Hasil forex disimpan di reports/hasil/, kripto di reports/hasil_crypto/. Laporan forex dibuat
oleh scripts/make_report.py, laporan rencana cadangan oleh scripts/make_report_cadangan.py.
Filter Astronacci hanya diuji untuk forex (tahap 2 asli).
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import pickle
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_EV = None


def out_dir(market: str) -> Path:
    return ROOT / "reports" / ("hasil" if market == "forex" else f"hasil_{market}")


def _init(market):
    global _EV
    from bot.research.selection import Evaluator
    _EV = Evaluator(market)


def _run_one(args):
    sid, adef = args
    from bot.research.selection import AstroFilter, final_test, select
    from bot.setups import REGISTRY
    setup = REGISTRY[sid]()
    t0 = time.time()
    logs = []
    afilter = AstroFilter.build(adef, _EV.sim.syms) if adef is not None else None
    sel = select(_EV, setup, log=logs.append)
    res = final_test(_EV, setup, sel, afilter)
    res["log"] = logs
    res["seconds"] = time.time() - t0
    return sid, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", default="forex")
    ap.add_argument("--setups", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--meta-only", action="store_true", help="hanya hitung ulang uji filter & ringkasan")
    args = ap.parse_args()
    market = args.market
    cfg = tomllib.loads((ROOT / "config" / "setups.toml").read_text())
    all_ids = cfg[market]["enabled"]
    ids = [s for s in args.setups.split(",") if s] or all_ids
    OUT = out_dir(market)
    OUT.mkdir(parents=True, exist_ok=True)

    from bot.research.astro_test import retro_test, turning_point_test
    from bot.research.splits import market_splits
    from bot.markets import MARKETS
    splits = market_splits(market)
    print("pembagian data:", splits.describe(), flush=True)
    tpt, adef = None, None
    if market == "forex":
        tpt = turning_point_test(splits, list(MARKETS[market].instruments))
        adef = tpt["chosen"]["def"]
        print("filter Astronacci terpilih:", adef.label, "→ uji akhir:", tpt["verdict"], flush=True)

    results = {}
    if not args.meta_only:
        with mp.get_context("fork").Pool(args.jobs, initializer=_init, initargs=(market,)) as pool:
            for sid, res in pool.imap_unordered(_run_one, [(s, adef) for s in ids]):
                results[sid] = res
                print(f"[{len(results)}/{len(ids)}] {sid}: {res.get('status')} ({res['seconds']:.0f} s)", flush=True)
                (OUT / f"{sid}.pkl").write_bytes(pickle.dumps(res))

    # gabungkan dengan hasil setup lain yang sudah ada (kalau hanya sebagian setup dijalankan ulang)
    for sid in all_ids:
        f = OUT / f"{sid}.pkl"
        if sid not in results and f.exists():
            results[sid] = pickle.loads(f.read_bytes())
    ids = [s for s in all_ids if s in results]
    from bot.engine.backtest import Simulator
    from bot.research.benchmark import random_entries
    bench = random_entries(Simulator(market), splits.start, splits.end)
    meta = {"splits": splits.describe(), "order": ids, "benchmark": bench, "market": market}
    if market == "forex":
        from bot.setups import REGISTRY
        brk = {"sel": [], "final": []}
        for sid, r in results.items():
            cat = REGISTRY[sid]().category_of(r["chosen"]["params"]) if "chosen" in r else ""
            if cat in ("breakout", "both") and "sl_flags" in r:
                for seg in brk:
                    brk[seg] += r["sl_flags"][seg]
        meta["retro"] = retro_test(brk)
        meta["astro_tp"] = tpt
        print("WKT-04 retrograde:", meta["retro"]["verdict_sel"], "| uji akhir:", meta["retro"]["verdict_final"])
    (OUT / "_meta.pkl").write_bytes(pickle.dumps(meta))


if __name__ == "__main__":
    main()
