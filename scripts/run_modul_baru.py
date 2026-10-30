"""Uji rancangan sendiri + semua modul mentor yang belum diuji (reports/RENCANA_MODUL_BARU.md).

    python -m bot.data.download harian kripto_harian
    python scripts/run_modul_baru.py --hitung       # hitung semuanya (±30–60 menit, pola grafik paling lama)
    python scripts/run_modul_baru.py                # tulis laporan dari hasil tersimpan

Menulis reports/LAPORAN_MODUL_BARU.md, grafik di reports/grafik/, hasil di reports/hasil_modul_baru/.
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "reports" / "hasil_modul_baru"

_EV = None


def _init(market):
    global _EV
    from bot.research.selection import Evaluator
    _EV = Evaluator(market)


def _run_pola(sid):
    from bot.research.selection import final_test, select
    from bot.setups import REGISTRY
    setup = REGISTRY[sid]()
    t0 = time.time()
    logs = []
    sel = select(_EV, setup, log=logs.append)
    res = final_test(_EV, setup, sel, None)
    res["log"] = logs
    res["seconds"] = time.time() - t0
    return sid, res


def hitung_pola(jobs: int) -> dict:
    from bot.setups.pola import ALL_POLA
    ids = [c.id for c in ALL_POLA]
    hasil = {}
    for market in ("forex", "crypto"):
        hasil[market] = {}
        with mp.get_context("fork").Pool(jobs, initializer=_init, initargs=(market,)) as pool:
            for sid, res in pool.imap_unordered(_run_pola, ids):
                hasil[market][sid] = res
                print(f"[{market}] {sid}: {res.get('status')} ({res['seconds']:.0f} s)", flush=True)
    return hasil


def hitung(jobs: int) -> None:
    from bot.research import kripto_investasi as ki
    from bot.research import multi_aset as ma
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "kripto.pkl").write_bytes(pickle.dumps(ki.semua()))
    print("kripto selesai", flush=True)
    (OUT / "multi_aset.pkl").write_bytes(pickle.dumps({b: ma.jalankan(b) for b in ("institusi", "ritel")}))
    print("multi-aset selesai", flush=True)
    (OUT / "pola.pkl").write_bytes(pickle.dumps(hitung_pola(jobs)))
    print("pola selesai", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hitung", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    if a.hitung:
        hitung(a.jobs)
    from scripts.laporan_modul_baru import laporan
    laporan()
