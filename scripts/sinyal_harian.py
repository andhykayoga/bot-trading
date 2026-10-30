"""Sinyal harian kripto spot: B6 trailing stop 10% di BTC dan ETH (reports/LAPORAN_MODUL_BARU.md).

    python scripts/sinyal_harian.py          # ambil candle harian terbaru, lalu cetak sinyal

Dipakai tugas terjadwal 07.15 WIB. Keputusan memakai close harian 07.00 WIB (00.00 UTC) dan dieksekusi segera
(sama dengan open hari ini di uji). Porsi kripto dibagi dua: 50% untuk BTC, 50% untuk ETH; tiap bagian dipegang
di koinnya atau di stablecoin. Tidak ada order yang dikirim: Anda yang mengeksekusi.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot.data.download import DATA, _klines  # noqa: E402
from bot.research import kripto_investasi as ki  # noqa: E402

JARAK = 0.10
KOIN = ("BTC", "ETH")


def perbarui() -> None:
    (DATA / "kripto_harian").mkdir(parents=True, exist_ok=True)
    for coin in KOIN:
        df = _klines(f"{coin}USDT")
        df[["t", "o", "h", "l", "c", "v", "qv"]].to_parquet(DATA / "kripto_harian" / f"{coin}.parquet", index=False)
    ki.harga.cache_clear()


def status(c: pd.Series) -> dict:
    """Aksi untuk close terakhir `c` dan level yang memicu aksi berikutnya."""
    tinggi20 = c.rolling(20).max().shift(1)
    pos, puncak = ki.trailing(c.loc[ki.MULAI:], tinggi20, JARAK)
    sebelum, sekarang = pos.iloc[-2], pos.iloc[-1]
    if sekarang and not sebelum:
        aksi = "BELI"
    elif sebelum and not sekarang:
        aksi = "JUAL ke stablecoin"
    else:
        aksi = "TETAP PEGANG" if sekarang else "TETAP DI STABLECOIN"
    if sekarang:
        berikut = f"jual kalau close harian ≤ {puncak * (1 - JARAK):,.2f} (10% di bawah puncak {puncak:,.2f})"
    else:
        berikut = f"beli lagi kalau close harian > {c.iloc[-20:].max():,.2f} (tertinggi 20 hari)"
    return {"tanggal_close": c.index[-1].date(), "close": float(c.iloc[-1]), "aksi": aksi, "berikutnya": berikut}


def main() -> None:
    perbarui()
    kemarin = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=1)).tz_localize(None)
    print(f"# Sinyal kripto spot (trailing stop 10%) — close {kemarin.date()} 07.00 WIB\n")
    for coin in KOIN:
        c = ki.harga(coin)["c"].loc[:kemarin]            # candle hari ini belum close: tidak dipakai
        s = status(c)
        if s["tanggal_close"] != kemarin.date():
            print(f"- {coin}: PERINGATAN data terakhir {s['tanggal_close']}, belum ada close {kemarin.date()}")
            continue
        print(f"- {coin} (50% porsi kripto): **{s['aksi']}** · close ${s['close']:,.2f} · {s['berikutnya']}")
    print("\nEksekusi sendiri di exchange (spot, tanpa leverage). Di uji 2018–2026 aturan ini +29,5% per tahun "
          "tetapi pernah turun 42%; tidak menjamin untung.")


if __name__ == "__main__":
    main()
