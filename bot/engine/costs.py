"""Biaya transaksi (D-10 butir 6): spread dan swap.

- Spread: harga data = harga tengah. Beli diisi di ask = tengah + spread/2, jual di
  bid = tengah − spread/2. SL/TP posisi long dipicu oleh bid, posisi short oleh ask.
  Besar spread per instrumen ada di `bot/markets.py`.
- Swap (biaya menginap): dihitung tiap pergantian hari trading (17.00 New York),
  akhir pekan dihitung 3 malam. Tarif per tahun dari nilai posisi:
      long  = (bunga mata uang dasar − bunga mata uang kuotasi) − biaya admin broker
      short = (bunga mata uang kuotasi − bunga mata uang dasar) − biaya admin broker
  Bunga = suku bunga kebijakan bulanan (perkiraan, dibulatkan) Fed, ECB, BoE, BoJ;
  emas dianggap berbunga 0. Kripto spot tidak kena swap. Biaya admin dari `Instrument.swap_markup`.
"""
from __future__ import annotations

import bisect

# (mulai berlaku YYYY-MM, persen per tahun). Perkiraan suku bunga efektif kebijakan.
USD = [("2008-12", 0.15), ("2015-12", 0.35), ("2016-12", 0.65), ("2017-03", 0.9), ("2017-06", 1.15),
       ("2017-12", 1.4), ("2018-03", 1.65), ("2018-06", 1.9), ("2018-09", 2.15), ("2018-12", 2.4),
       ("2019-08", 2.15), ("2019-09", 1.9), ("2019-11", 1.6), ("2020-03", 0.1), ("2022-03", 0.35),
       ("2022-05", 0.85), ("2022-06", 1.6), ("2022-08", 2.35), ("2022-10", 3.1), ("2022-11", 3.85),
       ("2022-12", 4.35), ("2023-02", 4.6), ("2023-03", 4.85), ("2023-05", 5.1), ("2023-08", 5.35),
       ("2024-09", 4.85), ("2024-11", 4.6), ("2024-12", 4.35), ("2025-09", 4.1), ("2025-10", 3.85),
       ("2025-12", 3.6)]
EUR = [("2009-05", 0.25), ("2011-04", 0.5), ("2011-07", 0.75), ("2011-11", 0.5), ("2011-12", 0.25),
       ("2012-07", 0.0), ("2014-06", -0.1), ("2014-09", -0.2), ("2015-12", -0.3), ("2016-03", -0.4),
       ("2019-09", -0.5), ("2022-07", 0.0), ("2022-09", 0.75), ("2022-11", 1.5), ("2022-12", 2.0),
       ("2023-02", 2.5), ("2023-03", 3.0), ("2023-05", 3.25), ("2023-06", 3.5), ("2023-08", 3.75),
       ("2023-09", 4.0), ("2024-06", 3.75), ("2024-09", 3.5), ("2024-10", 3.25), ("2024-12", 3.0),
       ("2025-02", 2.75), ("2025-03", 2.5), ("2025-04", 2.25), ("2025-06", 2.0)]
GBP = [("2009-03", 0.5), ("2016-08", 0.25), ("2017-11", 0.5), ("2018-08", 0.75), ("2020-03", 0.1),
       ("2021-12", 0.25), ("2022-02", 0.5), ("2022-03", 0.75), ("2022-05", 1.0), ("2022-06", 1.25),
       ("2022-08", 1.75), ("2022-09", 2.25), ("2022-11", 3.0), ("2022-12", 3.5), ("2023-02", 4.0),
       ("2023-03", 4.25), ("2023-05", 4.5), ("2023-06", 5.0), ("2023-08", 5.25), ("2024-08", 5.0),
       ("2024-11", 4.75), ("2025-02", 4.5), ("2025-05", 4.25), ("2025-08", 4.0), ("2025-12", 3.75)]
JPY = [("2008-12", 0.1), ("2016-02", -0.1), ("2024-03", 0.1), ("2024-08", 0.25), ("2025-01", 0.5),
       ("2025-12", 0.75)]
RATES = {"USD": USD, "EUR": EUR, "GBP": GBP, "JPY": JPY}


def policy_rate(ccy: str, yyyymm: str) -> float:
    table = RATES.get(ccy)
    if table is None:
        return 0.0
    keys = [k for k, _ in table]
    i = bisect.bisect_right(keys, yyyymm) - 1
    return table[max(i, 0)][1] / 100.0


def swap_rate(base: str, quote: str, direction: int, yyyymm: str, markup: float) -> float:
    """Tarif swap per tahun (pecahan nilai posisi); negatif = biaya."""
    diff = policy_rate(base, yyyymm) - policy_rate(quote, yyyymm)
    return (diff if direction > 0 else -diff) - markup
