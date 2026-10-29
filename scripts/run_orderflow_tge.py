"""Uji order flow (AFS-22) dan token baru (LIVE-02) sesuai reports/RENCANA_ORDERFLOW_TGE.md.

    python scripts/run_orderflow_tge.py --orderflow     # ±1 menit
    python scripts/run_orderflow_tge.py --tge           # butuh bot/research/tge_valuasi.csv + data/tge
    python scripts/run_orderflow_tge.py                 # tulis laporan dari hasil tersimpan
"""
from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "reports" / "hasil_orderflow_tge"
BASE_IDS = ["AFS-16T", "AFS-18", "AFS-20B", "HKI-01-H4"]


def hitung_orderflow() -> dict:
    from bot.research.selection import Evaluator, final_test, select
    from bot.setups import REGISTRY
    from bot.setups.orderflow import AFS22D, DeltaFilter
    ev = Evaluator("crypto")
    logs = []
    st = AFS22D()
    sel = select(ev, st, log=logs.append)
    d = final_test(ev, st, sel, None)
    d["log"] = logs
    filt = {}
    for sid in BASE_IDS:
        prev = pickle.loads((ROOT / "reports" / "hasil_crypto" / f"{sid}.pkl").read_bytes())
        base = REGISTRY[sid]()
        p, act = base.params(**prev["chosen"]["params"]), prev["active"]
        tanpa = ev.evaluate(base, p, segs=("dev", "sel", "final"), symbols=act)
        dengan = ev.evaluate(DeltaFilter(base), p, segs=("dev", "sel", "final"), symbols=act)
        strip = lambda r: {k: v for k, v in r.items() if not k.endswith("_res")}  # noqa: E731
        filt[sid] = {"params": p, "tanpa": strip(tanpa), "dengan": strip(dengan)}
        print(sid, "final tanpa", round(tanpa["final"]["net_pct"], 1), tanpa["final"]["trades"],
              "dengan", round(dengan["final"]["net_pct"], 1), dengan["final"]["trades"], flush=True)
    print("AFS-22D:", d["status"], flush=True)
    return {"afs22d": d, "filter": filt}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--orderflow", action="store_true")
    ap.add_argument("--tge", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.orderflow:
        (OUT / "orderflow.pkl").write_bytes(pickle.dumps(hitung_orderflow()))
    if a.tge:
        from bot.research.tge import jalankan_semua
        hasil = jalankan_semua()
        (OUT / "tge.pkl").write_bytes(pickle.dumps(hasil))
        hasil["token"].round(6).to_csv(OUT / "tge_per_token.csv", index=False)
    if not (a.orderflow or a.tge):
        from scripts.laporan_orderflow_tge import laporan
        laporan()
