"""Filter waktu Astronacci (rulebook 07, WKT-01 – WKT-04).

- WKT-01 fase bulan: hari dalam ±1 atau ±2 hari dari New Moon / Full Moon.
- WKT-02 tumpukan proyeksi Fibonacci waktu dari titik balik D1 (fractal 2–2):
    cara (a) hitung maju 13, 21, 34, 55, 89, 144, 233 candle dari tiap titik balik;
    cara (b) kelipatan 0,382 / 0,618 / 1 / 1,618 / 2,618 × jarak dua titik balik sejenis berurutan.
  Toleransi ±1 candle; kandidat kalau ≥3 (atau ≥4) proyeksi bertumpuk.
- WKT-03 tanggal Astronacci = WKT-01 ∩ WKT-02.
- WKT-04 Merkurius retrograde (bujur ekliptika geosentris mengecil).

Semua dihitung per hari trading (D-12) dan hanya memakai informasi yang sudah ada
sebelum hari itu dimulai (titik balik baru diakui 2 candle sesudahnya).
Posisi Bulan dan planet dihitung dengan pustaka `ephem` (tanpa situs pihak ketiga).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import ephem
import numpy as np
import pandas as pd

from bot import indicators as ind
from bot.data.candles import Bars

FIB_COUNTS = (13, 21, 34, 55, 89, 144, 233)
FIB_RATIOS = (0.382, 0.618, 1.0, 1.618, 2.618)
DAY_NS = 86400 * 10**9


@lru_cache(maxsize=None)
def moon_phase_days(start_year: int = 2008, end_year: int = 2028) -> np.ndarray:
    """Tanggal (hari sejak epoch, UTC) setiap New Moon dan Full Moon."""
    out = []
    d = ephem.Date(f"{start_year}/1/1")
    end = ephem.Date(f"{end_year}/1/1")
    for fn in (ephem.next_new_moon, ephem.next_full_moon):
        x = d
        while True:
            x = fn(x)
            if x > end:
                break
            out.append(int(pd.Timestamp(x.datetime()).value // DAY_NS))
            x = ephem.Date(x + 1)
    return np.array(sorted(out))


@lru_cache(maxsize=None)
def mercury_retro_days(start_year: int = 2008, end_year: int = 2028) -> np.ndarray:
    """Hari-hari (sejak epoch) saat Merkurius retrograde, dari bujur ekliptika harian."""
    days = np.arange(pd.Timestamp(f"{start_year}-01-01").value // DAY_NS,
                     pd.Timestamp(f"{end_year}-01-01").value // DAY_NS)
    lon = []
    m = ephem.Mercury()
    for dd in days:
        m.compute(ephem.Date(pd.Timestamp(int(dd) * DAY_NS).to_pydatetime()) + 0.5)
        lon.append(float(ephem.Ecliptic(m).lon))
    lon = np.unwrap(np.array(lon))
    retro = np.r_[False, np.diff(lon) < 0]
    return days[retro]


def moon_window(days: np.ndarray, n: int) -> np.ndarray:
    """True kalau hari trading berada ±n hari kalender dari New/Full Moon (WKT-01)."""
    ph = moon_phase_days()
    k = np.searchsorted(ph, days)
    dist = np.minimum(np.abs(days - ph[np.clip(k - 1, 0, len(ph) - 1)]),
                      np.abs(ph[np.clip(k, 0, len(ph) - 1)] - days))
    return dist <= n


def fib_counts(d1: Bars, method: str) -> np.ndarray:
    """Jumlah proyeksi Fibonacci waktu yang jatuh di tiap candle D1 (toleransi ±1)."""
    n = len(d1)
    sh, sl = ind.swings(d1.h, d1.l, 2)
    cnt = np.zeros(n + 300, int)
    turns = np.flatnonzero(sh | sl)
    if method == "a":
        for i in turns:
            for k in FIB_COUNTS:
                j = i + k
                if j - 1 >= i + 3:
                    cnt[j - 1: j + 2] += 1
    else:
        for kind in (np.flatnonzero(sh), np.flatnonzero(sl)):
            for prev, cur in zip(kind[:-1], kind[1:]):
                dist = cur - prev
                if dist > 233:
                    continue
                for r in FIB_RATIOS:
                    j = cur + int(round(r * dist))
                    lo = max(j - 1, cur + 3)  # proyeksi baru diketahui setelah titik balik diakui
                    if lo <= j + 1:
                        cnt[lo: j + 2] += 1
    return cnt[:n]


def turning_points(d1: Bars) -> np.ndarray:
    sh, sl = ind.swings(d1.h, d1.l, 2)
    return sh | sl


@dataclass(frozen=True)
class AstroDef:
    """Definisi tanggal kandidat yang diuji (pilihan WKT-01/02/03)."""
    kind: str            # "moon" | "fib" | "astronacci"
    moon_n: int = 1      # ±1 / ±2 hari
    method: str = "a"    # cara a / b
    min_stack: int = 3   # ≥3 / ≥4

    @property
    def label(self) -> str:
        if self.kind == "moon":
            return f"WKT-01 fase bulan ±{self.moon_n}"
        if self.kind == "fib":
            return f"WKT-02 Fibonacci waktu cara {self.method} ≥{self.min_stack}"
        return f"WKT-03 Astronacci (bulan ±{self.moon_n} ∩ Fibonacci cara {self.method} ≥{self.min_stack})"


def all_defs() -> list[AstroDef]:
    out = [AstroDef("moon", n) for n in (1, 2)]
    out += [AstroDef("fib", 1, m, k) for m in ("a", "b") for k in (3, 4)]
    out += [AstroDef("astronacci", n, m, k) for n in (1, 2) for m in ("a", "b") for k in (3, 4)]
    return out


def candidate_days(d1: Bars, adef: AstroDef) -> np.ndarray:
    """Boolean per candle D1: apakah hari itu tanggal kandidat titik balik."""
    if adef.kind == "moon":
        return moon_window(d1.day, adef.moon_n)
    fib = fib_counts(d1, adef.method) >= adef.min_stack
    if adef.kind == "fib":
        return fib
    return fib & moon_window(d1.day, adef.moon_n)


def candidate_day_set(d1: Bars, adef: AstroDef) -> set[int]:
    return set(d1.day[candidate_days(d1, adef)].tolist())


def retro_day_set() -> set[int]:
    return set(mercury_retro_days().tolist())
