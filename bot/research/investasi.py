"""Rencana investasi jangka panjang: data riset, portofolio, dan proyeksi saldo.

Semua pilihan di sini ditetapkan sebelum melihat hasil (tidak disetel supaya angkanya bagus):

- Data: return tahunan AS 1928–2025 dari Damodaran (NYU Stern) — saham S&P 500 termasuk dividen,
  obligasi pemerintah 10 tahun, T-bill 3 bulan, emas, inflasi. Semua dihitung riil (setelah inflasi),
  karena daya beli itulah yang bisa dipindahkan ke rupiah.
- Saham AS adalah pasar paling beruntung abad ke-20, jadi return riilnya digeser turun supaya rata-rata
  majemuknya sama dengan saham dunia 1900–2024: 5,2% per tahun (Dimson, Marsh & Staunton, UBS Global
  Investment Returns Yearbook 2025).
- Biaya dan pajak: 1% per tahun dari saldo (biaya reksa dana/ETF, pajak kupon SBN 10%, selisih jual-beli
  emas).
- Inflasi Indonesia: 3% per tahun (sasaran BI 2,5 ± 1%; September 2026: 3,28%). Rupiah = riil + inflasi.
- Rebalance setahun sekali ke bobot awal; setoran bulanan tetap dalam rupiah.
- Simulasi: urutan tahun asli (jendela bergulir) dan bootstrap blok 5 tahun, 10.000 jalur, seed 0.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RISET = ROOT / "data" / "riset"

WORLD_EQUITY_REAL = 0.052
BIAYA = 0.01
INFLASI_ID = 0.03
BLOK = 5
N_JALUR = 10_000

# Bobot bulat standar, bukan hasil optimasi. "seimbang" adalah rekomendasi.
PORTOFOLIO = {
    "hati_hati": {"saham": 0.2, "obligasi": 0.7, "emas": 0.1},
    "seimbang": {"saham": 0.5, "obligasi": 0.4, "emas": 0.1},
    "agresif": {"saham": 0.8, "obligasi": 0.1, "emas": 0.1},
}
NAMA = {"hati_hati": "Hati-hati 20/70/10", "seimbang": "Seimbang 50/40/10", "agresif": "Agresif 80/10/10"}


# ---------------------------------------------------------------- data tahunan 1928–2025

def _first_block(df: pd.DataFrame) -> pd.DataFrame:
    yrs = pd.to_numeric(df[0], errors="coerce")
    start = int(np.flatnonzero(yrs == 1928)[0])
    end = start
    while end < len(df) and not np.isnan(yrs.iloc[end]):
        end += 1
    out = df.iloc[start:end].copy()
    out.index = yrs.iloc[start:end].astype(int)
    return out


def load_tahunan() -> pd.DataFrame:
    """Return nominal tahunan AS + inflasi, indeks tahun."""
    x = pd.ExcelFile(RISET / "histretSP.xls")
    r = _first_block(pd.read_excel(x, "Returns by year", header=None))
    infl = _first_block(pd.read_excel(x, "Nominal vs Real Data", header=None))[4]
    df = pd.DataFrame({"saham": r[1], "kas": r[3], "obligasi": r[4], "emas": r[7]}).astype(float)
    df["inflasi"] = infl.reindex(df.index).astype(float)
    return df


def geo(r) -> float:
    r = np.asarray(r, dtype=float)
    return float(np.exp(np.log1p(r).mean()) - 1)


def riil(df: pd.DataFrame, saham_dunia: bool = True) -> tuple[pd.DataFrame, float]:
    """Return riil per kelas aset. Saham digeser supaya rata-rata majemuknya = saham dunia."""
    out = pd.DataFrame({c: (1 + df[c]) / (1 + df["inflasi"]) - 1 for c in ["saham", "obligasi", "emas", "kas"]})
    geser = 0.0
    if saham_dunia:
        lo, hi = -0.2, 0.2
        for _ in range(100):
            geser = (lo + hi) / 2
            if geo(out["saham"] + geser) > WORLD_EQUITY_REAL:
                hi = geser
            else:
                lo = geser
        out["saham"] = out["saham"] + geser
    return out, geser


def return_portofolio(r: pd.DataFrame, nama: str) -> pd.Series:
    """Return riil tahunan portofolio, rebalance tiap awal tahun, setelah biaya."""
    w = PORTOFOLIO[nama]
    gross = sum(wt * r[k] for k, wt in w.items())
    return (1 + gross) * (1 - BIAYA) - 1


def riil_dari_nominal(nominal: float, inflasi: float = INFLASI_ID) -> float:
    """Untuk pembanding berbunga tetap (deposito, SBN): bunga nominal → return riil."""
    return (1 + nominal) / (1 + inflasi) - 1


# ---------------------------------------------------------------- simulasi

def bootstrap(r: np.ndarray, tahun: int, n: int = N_JALUR, blok: int = BLOK, seed: int = 0) -> np.ndarray:
    """Bootstrap blok melingkar: potongan 5 tahun berurutan supaya krisis beruntun tetap utuh."""
    rng = np.random.default_rng(seed)
    r = np.asarray(r, dtype=float)
    nb = -(-tahun // blok)
    starts = rng.integers(0, len(r), size=(n, nb))
    idx = (starts[:, :, None] + np.arange(blok)) % len(r)
    return r[idx.reshape(n, -1)[:, :tahun]]


def jendela(r: np.ndarray, tahun: int) -> np.ndarray:
    """Semua urutan tahun asli sepanjang `tahun` (mulai 1928, 1929, ...)."""
    r = np.asarray(r, dtype=float)
    return np.array([r[s:s + tahun] for s in range(len(r) - tahun + 1)])


def proyeksi(r_tahunan, modal: float, setoran: float, inflasi: float = INFLASI_ID) -> np.ndarray:
    """Saldo rupiah nominal di akhir tiap bulan, bentuk (jalur, 12×tahun + 1).

    r_tahunan: return riil per tahun (jalur × tahun). Return bulanan dibagi rata secara majemuk dalam
    setahun; setoran masuk di akhir tiap bulan.
    """
    r = np.atleast_2d(np.asarray(r_tahunan, dtype=float))
    rm = np.repeat(((1 + r) * (1 + inflasi)) ** (1 / 12) - 1, 12, axis=1)
    out = np.empty((rm.shape[0], rm.shape[1] + 1))
    bal = np.full(rm.shape[0], float(modal))
    out[:, 0] = bal
    for k in range(rm.shape[1]):
        bal = bal * (1 + rm[:, k]) + setoran
        out[:, k + 1] = bal
    return out


def total_setoran(modal: float, setoran: float, bulan: int) -> float:
    return modal + setoran * bulan


def cagr_jalur(r: np.ndarray) -> np.ndarray:
    return np.exp(np.log1p(r).mean(axis=1)) - 1


# ---------------------------------------------------------------- cek mingguan 2010–2026 (USD)

def _french_daily() -> pd.Series:
    with zipfile.ZipFile(RISET / "ff_daily.zip") as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    rows = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 5 and parts[0].isdigit() and len(parts[0]) == 8:
            rows.append((parts[0], float(parts[1]) + float(parts[4])))
    s = pd.Series([v / 100 for _, v in rows], index=pd.to_datetime([d for d, _ in rows]))
    return s[~s.index.duplicated()]   # file berisi satu tabel harian; jaga-jaga duplikat


def obligasi_harian() -> pd.Series:
    """Return harian obligasi 10 tahun dari imbal hasil (cara 'par bond'): kupon = imbal hasil kemarin,
    dihargai ulang di imbal hasil hari ini, plus bunga berjalan."""
    y = pd.read_csv(RISET / "dgs10.csv", index_col=0, parse_dates=True).iloc[:, 0]
    y = pd.to_numeric(y, errors="coerce").dropna() / 100
    y0, y1 = y.shift(1), y
    dt = y.index.to_series().diff().dt.days / 365.0
    v = (1 + y1 / 2) ** -20
    harga = y0 / y1 * (1 - v) + v
    return (harga - 1 + y0 * dt).dropna()


def emas_harian() -> pd.Series:
    from bot.data.candles import load_instrument
    d1 = load_instrument("XAUUSD")["D1"]
    return pd.Series(d1.c, index=pd.to_datetime(d1.day * 86400 * 10**9)).pct_change().dropna()


def mingguan(nama: str, mulai: str = "2010-01-01") -> pd.Series:
    """Nilai portofolio akhir tiap minggu (USD, sebelum biaya), rebalance tiap awal tahun."""
    harian = pd.DataFrame({"saham": _french_daily(), "obligasi": obligasi_harian(), "emas": emas_harian()})
    akhir = min(harian[c].last_valid_index() for c in harian)
    harian = harian.loc[mulai:akhir].fillna(0.0)
    level = (1 + harian).cumprod()
    wk = level.resample("W-FRI").last().pct_change().dropna()
    w = PORTOFOLIO[nama]
    hold = pd.Series({k: w.get(k, 0.0) for k in wk.columns})
    nilai, tahun, out = 1.0, None, []
    for t, r in wk.iterrows():
        if tahun is not None and t.year != tahun:
            hold = pd.Series({k: w.get(k, 0.0) for k in wk.columns}) * nilai
        tahun = t.year
        hold = hold * (1 + r)
        nilai = float(hold.sum())
        out.append(nilai)
    return pd.Series(out, index=wk.index)


def statistik_mingguan(v: pd.Series) -> dict:
    r = v.pct_change().fillna(v.iloc[0] - 1)
    bulanan = v.resample("ME").last().pct_change().dropna()
    tahun = (v.index[-1] - v.index[0]).days / 365.25 + 7 / 365.25
    return {
        "minggu": len(r), "pct_minggu_naik": 100 * (r > 0).mean(), "rata_minggu": 100 * r.mean(),
        "minggu_terburuk": 100 * r.min(), "minggu_terbaik": 100 * r.max(),
        "pct_bulan_naik": 100 * (bulanan > 0).mean(), "bulan_terburuk": 100 * bulanan.min(),
        "setahun_terburuk": 100 * (v / v.shift(52) - 1).min(),
        "turun_terdalam": -100 * (v / v.cummax() - 1).min(),
        "cagr": 100 * (v.iloc[-1] ** (1 / tahun) - 1), "mulai": v.index[0], "akhir": v.index[-1],
    }


def pelemahan_rupiah_riil(a: int, b: int) -> dict:
    """Pelemahan rupiah per tahun dibanding selisih inflasi Indonesia–AS (akhir Desember a → b).

    Kalau mendekati 0, kurs mengikuti daya beli dan return riil aset dolar ≈ return riilnya dalam rupiah.
    """
    kurs = pd.read_csv(RISET / "usdidr.csv", index_col=0, parse_dates=True).iloc[:, 0].dropna()
    ihk = pd.read_csv(RISET / "idcpi.csv", index_col=0, parse_dates=True).iloc[:, 0].dropna()
    n = b - a
    dep = (kurs[f"{b}-12"].iloc[0] / kurs[f"{a}-12"].iloc[0]) ** (1 / n) - 1
    inf_id = (ihk[f"{b}-12"].iloc[0] / ihk[f"{a}-12"].iloc[0]) ** (1 / n) - 1
    inf_us = float(np.prod(1 + load_tahunan()["inflasi"].loc[a + 1:b]) ** (1 / n) - 1)
    return {"pelemahan": dep, "inflasi_id": inf_id, "inflasi_us": inf_us,
            "riil": (1 + dep) * (1 + inf_us) / (1 + inf_id) - 1}
