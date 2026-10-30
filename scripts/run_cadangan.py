"""Rencana cadangan tahap 1 dan 3 (lihat reports/RENCANA_CADANGAN.md).

    python scripts/run_cadangan.py

Tahap 1: V1–V4 dijalankan sekali di data rancangan (EURUSD+XAUUSD) dan sekali di data uji
(GBPUSD+USDJPY), dengan pembagian periode yang sama dengan tahap 2.
Tahap 3: patokan time-series momentum di GBPUSD+USDJPY, EURUSD+XAUUSD, dan BTC+ETH.
Tahap 2 (kripto) dijalankan dengan: python scripts/run_backtest.py --market crypto, lalu
versi long saja dengan: python scripts/run_cadangan.py --crypto-long
"""
from __future__ import annotations

import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "reports" / "hasil_cadangan"


def stage1():
    from bot.research.selection import Evaluator, _daily_equity, _strip
    from bot.research.splits import market_splits
    from bot.setups.improved import IMPROVED
    splits = market_splits("forex")
    evs = {"rancangan": Evaluator("forex"), "uji": Evaluator("forex_uji", splits=splits)}
    res = {}
    for cls in IMPROVED:
        st = cls()
        p = st.params()
        res[st.id] = {"id": st.id, "name": st.name, "mentor": st.mentor, "params": p}
        for name, ev in evs.items():
            t0 = time.time()
            r = ev.evaluate(st, p, segs=("dev", "sel", "final", "full"))
            res[st.id][name] = _strip(r)
            res[st.id][name + "_equity"] = _daily_equity(r["full_res"])
            r["full_res"].frame().to_csv(OUT / f"transaksi_{st.id}_{name}.csv", index=False)
            f = r["full"]
            print(f"{st.id} {name}: {f['trades']} trx, net {f['net_pct']:+.1f}%, DD {f['max_dd_pct']:.1f}% "
                  f"({time.time() - t0:.0f} s)", flush=True)
    return res


def stage3():
    from bot.research.splits import market_splits
    from bot.research.tsmom import run_tsmom
    import pandas as pd
    fx = market_splits("forex")
    cr = market_splits("crypto")
    day = lambda t: str(pd.Timestamp(t, tz="UTC").date())
    runs = {
        "forex_uji": ("forex_uji", fx, False),
        "forex": ("forex", fx, False),
        "crypto": ("crypto", cr, False),
        "crypto_long": ("crypto", cr, True),
    }
    out = {}
    for key, (market, sp, long_only) in runs.items():
        out[key] = {}
        for seg in ("full", "dev", "sel", "final"):
            a, b = sp.seg(seg)
            r = run_tsmom(market, day(a), day(b), long_only=long_only)
            eq = r.pop("equity")
            out[key][seg] = r
            if seg == "full":
                out[key]["equity"] = [(str(i.date()), float(v)) for i, v in eq.items()]
        f = out[key]["full"]
        print(f"TSMOM {key}: CAGR {f['cagr_pct']:+.1f}%/th, DD {f['max_dd_pct']:.1f}%, Sharpe {f['sharpe']:.2f}",
              flush=True)
    return out


def stage2_long():
    """Versi long saja (akun kripto spot, G-16) untuk setup kripto yang sampai uji akhir.
    Parameter sama dengan pilihan terkunci; ini hanya laporan, bukan pemilihan ulang."""
    from bot.research.selection import Evaluator, _strip, key_of
    from bot.setups import REGISTRY
    src = ROOT / "reports" / "hasil_crypto"
    meta = pickle.loads((src / "_meta.pkl").read_bytes())
    ev = Evaluator("crypto")
    out = {}
    for sid in meta["order"]:
        r = pickle.loads((src / f"{sid}.pkl").read_bytes())
        if "final" not in r:
            continue
        st = REGISTRY[sid]()
        p = r["chosen"]["params"]
        ev._sig[st.id + key_of(p)] = [o for o in st.signals(ev.data, p) if o.direction > 0]
        out[sid] = _strip(ev.evaluate(st, p, segs=("dev", "sel", "final"), symbols=r["active"]))
        f = out[sid]["final"]
        print(f"{sid} long saja: uji akhir {f['trades']} trx, net {f['net_pct']:+.1f}%", flush=True)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if "--crypto-long" in sys.argv:
        (OUT / "crypto_long.pkl").write_bytes(pickle.dumps(stage2_long()))
        return
    res = {"stage1": stage1(), "stage3": stage3()}
    (OUT / "hasil.pkl").write_bytes(pickle.dumps(res))


if __name__ == "__main__":
    main()
