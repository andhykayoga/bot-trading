"""Jadwal berita "high impact" untuk jendela larangan G-13 (±30 menit).

Sumber dan cara mengisinya:
1. Forex Factory 2007-01 s.d. 2025-04-07: semua berita "High Impact Expected"
   untuk USD dan EUR. Sekitar 40% baris hanya punya tanggal (jam tersimpan sebagai
   00.00 waktu Teheran). Jamnya diisi dengan jam yang paling sering dipakai berita
   yang sama (zona waktu negaranya), misalnya NFP 08.30 New York.
2. Setelah 2025-04-07 (data Forex Factory berhenti):
   - FOMC dari jadwal Fed (dataset XOOMAR) + konferensi pers 30 menit sesudahnya;
   - NFP, CPI, PPI, Retail Sales, JOLTS, PCE, GDP awal dari dataset XOOMAR (mulai Des 2025);
   - NFP & CPI April–November 2025 dan rapat ECB 2025–2026 diisi manual di bawah.
   Jadi periode akhir 2025–2026 hanya memuat berita minimal G-13 ditambah beberapa
   berita AS lain; laporan mencatat keterbatasan ini.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from bot.markets import INSTRUMENTS

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "data" / "calendar"
WINDOW_NS = 30 * 60 * 10**9
HOME_TZ = {"USD": "America/New_York", "EUR": "Europe/Berlin", "GBP": "Europe/London", "JPY": "Asia/Tokyo"}
DEFAULT_TIME = {"USD": "08:30", "EUR": "14:15", "GBP": "12:00", "JPY": "12:00"}

# Diisi manual (waktu lokal negara asal). Sumber: jadwal resmi BLS 2025 (termasuk
# penundaan karena government shutdown Okt–Nov 2025) dan kalender rapat ECB.
MANUAL = [
    *[("USD", d, "08:30", "Non-Farm Employment Change") for d in
      ["2025-04-04", "2025-05-02", "2025-06-06", "2025-07-03", "2025-08-01", "2025-09-05", "2025-11-20"]],
    *[("USD", d, "08:30", "CPI m/m") for d in
      ["2025-04-10", "2025-05-13", "2025-06-11", "2025-07-15", "2025-08-12", "2025-09-11", "2025-10-24"]],
    *[(ccy_t[0], d, ccy_t[1], ccy_t[2]) for d in
      ["2025-04-17", "2025-06-05", "2025-07-24", "2025-09-11", "2025-10-30", "2025-12-18",
       "2026-02-05", "2026-03-19", "2026-04-30", "2026-06-11", "2026-07-23", "2026-09-10", "2026-10-29"]
      for ccy_t in [("EUR", "14:15", "Main Refinancing Rate"), ("EUR", "14:45", "ECB Press Conference")]],
    # Untuk pair uji GBPUSD/USDJPY: rapat BoE dan BoJ setelah data Forex Factory berhenti (perkiraan jadwal).
    *[("GBP", d, "12:00", "Official Bank Rate") for d in
      ["2025-05-08", "2025-06-19", "2025-08-07", "2025-09-18", "2025-11-06", "2025-12-18",
       "2026-02-05", "2026-03-19", "2026-04-30", "2026-06-18", "2026-07-30", "2026-09-17"]],
    *[("JPY", d, "12:00", "BOJ Policy Rate") for d in
      ["2025-05-01", "2025-06-17", "2025-07-31", "2025-09-19", "2025-10-30", "2025-12-19",
       "2026-01-23", "2026-03-19", "2026-04-28", "2026-06-16", "2026-07-31", "2026-09-18"]],
]
XOOMAR_KEYS = ("FOMC Rate Decision", "Nonfarm Payrolls", "CPI (Consumer Price Index)", "PPI (Producer",
               "Retail Sales", "JOLTS", "Personal Income and Outlays", "GDP (Advance")


def _local_to_utc(ccy: str, date: str, hhmm: str) -> pd.Timestamp:
    return pd.Timestamp(f"{date} {hhmm}").tz_localize(HOME_TZ[ccy]).tz_convert("UTC")


@lru_cache(maxsize=None)
def events() -> pd.DataFrame:
    """Semua berita: kolom t (UTC), ccy, event, source."""
    rows = []
    ff = pd.read_csv(CAL / "forex_factory.csv")
    ff = ff[(ff.Impact == "High Impact Expected") & ff.Currency.isin(list(HOME_TZ))].copy()
    ff["dateonly"] = ff.DateTime.str[11:19] == "00:00:00"
    ff["t"] = pd.to_datetime(ff.DateTime, utc=True)
    # jam lokal yang paling sering per berita (dari baris yang punya jam)
    known = ff[~ff.dateonly].copy()
    known["hhmm"] = [t.tz_convert(HOME_TZ[c]).strftime("%H:%M") for t, c in zip(known.t, known.Currency)]
    mode = known.groupby(["Currency", "Event"]).hhmm.agg(lambda s: s.value_counts().index[0]).to_dict()
    for r in ff.itertuples():
        if r.dateonly:
            hhmm = mode.get((r.Currency, r.Event), DEFAULT_TIME[r.Currency])
            t = _local_to_utc(r.Currency, r.DateTime[:10], hhmm)
        else:
            t = r.t
        rows.append((t, r.Currency, r.Event, "forexfactory"))
    ff_end = ff.t.max()
    us = pd.read_csv(CAL / "us_releases.csv")
    us["t"] = pd.to_datetime(us.scheduled_at, utc=True)
    us = us[(us.t > ff_end) & us.event_name.str.startswith(XOOMAR_KEYS)]
    for r in us.itertuples():
        rows.append((r.t, "USD", r.event_name, "xoomar"))
        if r.event_name.startswith("FOMC"):
            rows.append((r.t + pd.Timedelta(minutes=30), "USD", "FOMC Press Conference", "xoomar"))
    for ccy, d, hhmm, name in MANUAL:
        rows.append((_local_to_utc(ccy, d, hhmm), ccy, name, "manual"))
    df = pd.DataFrame(rows, columns=["t", "ccy", "event", "source"]).drop_duplicates(["t", "ccy"])
    return df.sort_values("t").reset_index(drop=True)


@lru_cache(maxsize=None)
def windows(symbol: str) -> tuple[np.ndarray, np.ndarray]:
    """Jendela larangan G-13 yang sudah digabung: (awal, akhir) dalam ns UTC."""
    ev = events()
    inst = INSTRUMENTS[symbol]
    ev = ev[ev.ccy.isin(inst.news_ccys)]
    if inst.news_events:   # kripto: hanya FOMC, CPI AS, NFP (G-13)
        ev = ev[ev.event.str.contains("|".join(inst.news_events), regex=True)]
    t = np.sort(ev.t.dt.as_unit("ns").astype("int64").to_numpy())
    start, end = t - WINDOW_NS, t + WINDOW_NS
    # gabungkan jendela yang tumpang tindih
    ms, me = [start[0]], [end[0]]
    for s, e in zip(start[1:], end[1:]):
        if s <= me[-1]:
            me[-1] = max(me[-1], e)
        else:
            ms.append(s); me.append(e)
    return np.array(ms), np.array(me)


def in_blackout(symbol: str, t_ns) -> np.ndarray:
    s, e = windows(symbol)
    i = np.searchsorted(s, t_ns, side="right") - 1
    t_ns = np.asarray(t_ns)
    return (i >= 0) & (t_ns < e[np.clip(i, 0, None)])


def next_window_start(symbol: str, t_ns: int) -> int:
    """Awal jendela larangan berikutnya setelah t (untuk menutup posisi scalping)."""
    s, _ = windows(symbol)
    i = np.searchsorted(s, t_ns, side="right")
    return int(s[i]) if i < len(s) else np.iinfo(np.int64).max
