"""Uji tipe EA XAUUSD yang viral, sesuai pra-registrasi reports/RENCANA_EA_XAUUSD.md.

E1 grid martingale beli saja, E2 grid martingale dua arah, E3 breakout sesi London, plus patokan beli-dan-tahan.
Akun USD 1.000, leverage 1:500, stop-out margin level 50%; akun yang habis dicatat lalu diisi lagi USD 1.000.
Dalam satu candle kejadian yang merugikan diproses dulu.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from bot.data.candles import load_instrument
from bot.engine.costs import swap_rate
from bot.markets import INSTRUMENTS

MODAL = 1000.0
LEVERAGE = 500.0
STOP_OUT = 0.5
OZ = 100.0
STEP, MULT, MAX_POS, TP = 0.005, 1.5, 10, 0.003
MARKUP = INSTRUMENTS["XAUUSD"].swap_markup
PERIODE = {"Seluruh 2010–2026": ("2010-01-04", "2026-12-31"), "2010–2015": ("2010-01-04", "2015-12-31"),
           "2016–2020": ("2016-01-01", "2020-12-31"), "2021–2026": ("2021-01-01", "2026-12-31"),
           "Periode viral 2024–2026": ("2024-01-01", "2026-12-31")}
SUB = ["2010–2015", "2016–2020", "2021–2026"]


def lot_round(x: float) -> float:
    return max(0.01, math.floor(x * 100 + 0.5) / 100)


@dataclass
class Data:
    t: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    day: np.ndarray
    sp: np.ndarray
    swap_long: np.ndarray    # tarif swap per tahun untuk posisi beli, per candle (bulan berjalan)
    swap_short: np.ndarray


def load(mulai: str, akhir: str) -> Data:
    b = load_instrument("XAUUSD")["M5"]
    a = np.searchsorted(b.t_open, pd.Timestamp(mulai, tz="UTC").value)
    z = np.searchsorted(b.t_open, pd.Timestamp(akhir, tz="UTC").value + 86400 * 10**9)
    sl = slice(a, z)
    t = b.t_open[sl]
    ym = pd.DatetimeIndex(t.astype("datetime64[ns]")).strftime("%Y-%m")
    rates = {m: (swap_rate("XAU", "USD", 1, m, MARKUP), swap_rate("XAU", "USD", -1, m, MARKUP)) for m in set(ym)}
    c = b.c[sl]
    return Data(t, b.o[sl], b.h[sl], b.l[sl], c, b.day[sl], INSTRUMENTS["XAUUSD"].spread(c),
                np.array([rates[m][0] for m in ym]), np.array([rates[m][1] for m in ym]))


@dataclass
class Keranjang:
    arah: int
    base: float = 0.0
    lots: list = field(default_factory=list)
    harga: list = field(default_factory=list)

    def total(self) -> float:
        return sum(self.lots)

    def rata(self) -> float:
        return sum(lt * p for lt, p in zip(self.lots, self.harga)) / self.total()

    def nilai(self, mid: float, sp: float) -> float:
        """Untung/rugi mengambang kalau ditutup di harga tengah `mid`."""
        if not self.lots:
            return 0.0
        keluar = mid - sp / 2 if self.arah > 0 else mid + sp / 2
        return self.arah * OZ * sum(lt * (keluar - p) for lt, p in zip(self.lots, self.harga))

    def reset(self) -> None:
        self.lots, self.harga, self.base = [], [], 0.0


@dataclass
class Hasil:
    t: np.ndarray
    ekuitas: np.ndarray
    setoran: np.ndarray
    habis: list
    transaksi: list            # untung/rugi tiap keranjang atau transaksi (USD)
    hari_lewat: int = 0        # E3: hari yang dilewati karena lot minimum melebihi risiko 1%

    def ringkas(self) -> dict:
        eq = pd.Series(self.ekuitas, index=pd.to_datetime(self.t))
        dep = pd.Series(self.setoran, index=eq.index)
        harian = eq.resample("D").last().dropna()
        # bulan "hijau": ekuitas akhir bulan − awal bulan − setoran baru di bulan itu > 0
        e_bln, d_bln = eq.resample("ME").last().dropna(), dep.resample("ME").last().dropna()
        e_awal = pd.concat([pd.Series([MODAL]), pd.Series(e_bln.to_numpy()[:-1])]).to_numpy()
        d_awal = pd.concat([pd.Series([MODAL]), pd.Series(d_bln.to_numpy()[:-1])]).to_numpy()
        hijau = (e_bln.to_numpy() - e_awal - (d_bln.to_numpy() - d_awal)) > 0
        # umur akun: dari mulai/isi ulang sampai habis
        mulai = [eq.index[0]] + list(self.habis[:-1])
        umur = [(b - a).days for a, b in zip(mulai, self.habis)]
        # puncak ekuitas yang pernah dicapai satu akun sebelum habis
        puncak = float(eq.max())
        tahun = max((eq.index[-1] - eq.index[0]).days / 365.25, 1e-9)
        total_setor = float(self.setoran[-1])
        akhir = float(self.ekuitas[-1])
        # drawdown sampai akun pertama kali habis (sesudahnya ekuitas memuat setoran baru)
        sampai = harian if not self.habis else harian.loc[:self.habis[0]]
        dd = float(-100 * (sampai / sampai.cummax() - 1).min()) if len(sampai) else 0.0
        if self.habis:
            dd = 100.0
        tr = np.array(self.transaksi)
        cagr = 100 * ((akhir / total_setor) ** (1 / tahun) - 1) if not self.habis and akhir > 0 else float("nan")
        return {"akhir": akhir, "setor": total_setor, "bersih": akhir - total_setor, "habis": len(self.habis),
                "habis_pertama": self.habis[0] if self.habis else None, "cagr": cagr, "dd": dd,
                "menang": 100 * (tr > 0).mean() if len(tr) else float("nan"), "n_transaksi": len(tr),
                "bulan_hijau": 100 * hijau.mean() if len(hijau) else float("nan"),
                "umur_median": float(np.median(umur)) if umur else float("nan"),
                "umur_max": max(umur) if umur else None, "puncak": puncak, "hari_lewat": self.hari_lewat,
                "rugi_terbesar": float(tr.min()) if len(tr) else 0.0, "rata_untung": float(tr[tr > 0].mean())
                if (tr > 0).any() else 0.0}


def grid(d: Data, sisi: tuple[int, ...], step: float = STEP, mult: float = MULT, max_pos: int = MAX_POS,
         tp: float = TP) -> Hasil:
    n = len(d.c)
    bal, setor = MODAL, MODAL
    kr = {s: Keranjang(s) for s in sisi}
    eq_out, dep_out, habis, transaksi = np.empty(n), np.empty(n), [], []
    for k in range(n):
        o, h, lo, c, sp = d.o[k], d.h[k], d.l[k], d.c[k], d.sp[k]
        if k and d.day[k] != d.day[k - 1]:
            hari = int(d.day[k] - d.day[k - 1])
            for s, K in kr.items():
                if K.lots:
                    rate = d.swap_long[k] if s > 0 else d.swap_short[k]
                    bal += K.total() * OZ * o * rate * hari / 365
        ekuitas = bal + sum(K.nilai(o, sp) for K in kr.values())
        for s, K in kr.items():
            if not K.lots:
                K.base = lot_round(0.01 * max(ekuitas, 0.0) / 1000)
                K.lots.append(K.base)
                K.harga.append(o + sp / 2 if s > 0 else o - sp / 2)
        # 1) kejadian merugikan: tambah posisi grid
        for s, K in kr.items():
            if s > 0:
                ask_open, ask_low = o + sp / 2, lo + sp / 2
                while len(K.lots) < max_pos and ask_low <= K.harga[-1] * (1 - step):
                    K.harga.append(min(K.harga[-1] * (1 - step), ask_open))
                    K.lots.append(lot_round(K.base * mult ** len(K.lots)))
            else:
                bid_open, bid_high = o - sp / 2, h - sp / 2
                while len(K.lots) < max_pos and bid_high >= K.harga[-1] * (1 + step):
                    K.harga.append(max(K.harga[-1] * (1 + step), bid_open))
                    K.lots.append(lot_round(K.base * mult ** len(K.lots)))
        # 2) stop-out di harga terburuk candle
        terburuk = None
        for px in (lo, h):
            eq_px = bal + sum(K.nilai(px, sp) for K in kr.values())
            margin = sum(K.total() for K in kr.values()) * OZ * px / LEVERAGE
            if eq_px <= STOP_OUT * margin and (terburuk is None or eq_px < terburuk):
                terburuk = eq_px
        if terburuk is not None:
            transaksi.append(terburuk - bal)
            bal = max(terburuk, 0.0) + MODAL
            setor += MODAL
            habis.append(pd.Timestamp(int(d.t[k])))
            for K in kr.values():
                K.reset()
        else:
            # 3) kejadian menguntungkan: take profit keranjang
            for s, K in kr.items():
                if not K.lots:
                    continue
                target = K.rata() * (1 + tp) if s > 0 else K.rata() * (1 - tp)
                if s > 0 and h - sp / 2 >= target:
                    keluar = max(target, o - sp / 2)
                elif s < 0 and lo + sp / 2 <= target:
                    keluar = min(target, o + sp / 2)
                else:
                    continue
                untung = s * OZ * sum(lt * (keluar - p) for lt, p in zip(K.lots, K.harga))
                bal += untung
                transaksi.append(untung)
                K.reset()
        eq_out[k] = bal + sum(K.nilai(c, sp) for K in kr.values())
        dep_out[k] = setor
    return Hasil(d.t, eq_out, dep_out, habis, transaksi)


def breakout_london(d: Data) -> Hasil:
    idx = pd.DatetimeIndex(d.t.astype("datetime64[ns]")).tz_localize("UTC").tz_convert("Europe/London")
    tanggal = idx.date
    menit = (idx.hour * 60 + idx.minute).to_numpy()
    wd = idx.weekday.to_numpy()
    bal, lewat = MODAL, 0
    eq_out, dep_out, transaksi = np.full(len(d.c), np.nan), np.full(len(d.c), MODAL), []
    batas = np.flatnonzero(np.r_[True, tanggal[1:] != tanggal[:-1], True])
    for a, z in zip(batas[:-1], batas[1:]):
        eq_out[a:z] = bal
        if wd[a] >= 5:
            continue
        m = menit[a:z]
        asia = np.flatnonzero(m < 7 * 60) + a
        dagang = np.flatnonzero((m >= 7 * 60) & (m < 20 * 60)) + a
        if len(asia) < 12 or not len(dagang):
            continue                                   # hari libur/data bolong
        H, L = d.h[asia].max(), d.l[asia].min()
        R = H - L
        if R <= 0:
            continue
        posisi, entry, lots = 0, 0.0, 0.0
        for k in dagang:
            o, h, lo, sp = d.o[k], d.h[k], d.l[k], d.sp[k]
            if posisi == 0:
                naik, turun = h >= H, lo <= L
                if not (naik or turun):
                    continue
                if naik and turun:                     # dua-duanya tersentuh di satu candle: anggap rugi
                    naik = abs(o - H) <= abs(o - L)
                    turun = not naik
                posisi = 1 if naik else -1
                rugi_per_oz = R + sp / 2
                lots = math.floor(0.01 * bal / (rugi_per_oz * OZ) * 100) / 100
                if lots < 0.01:                        # lot minimum sudah > 1% risiko: hari ini dilewati
                    posisi = 0
                    lewat += 1
                    break
                entry = max(H, o) + sp / 2 if posisi > 0 else min(L, o) - sp / 2
                if (posisi > 0 and lo - sp / 2 <= L) or (posisi < 0 and h + sp / 2 >= H):
                    keluar = L if posisi > 0 else H        # stop loss di candle yang sama
                    untung = posisi * lots * OZ * (keluar - entry)
                    bal += untung; transaksi.append(untung); posisi = 0
                    break
                continue
            sl, tp = (L, H + R) if posisi > 0 else (H, L - R)
            if posisi > 0:
                kena_sl, kena_tp = lo - sp / 2 <= sl, h - sp / 2 >= tp
            else:
                kena_sl, kena_tp = h + sp / 2 >= sl, lo + sp / 2 <= tp
            if kena_sl or kena_tp:
                keluar = sl if kena_sl else tp           # dua-duanya: stop loss dulu
                untung = posisi * lots * OZ * (keluar - entry)
                bal += untung; transaksi.append(untung); posisi = 0
                break
        if posisi != 0:                                # tutup paksa 20.00 London
            k = dagang[-1]
            keluar = d.c[k] - d.sp[k] / 2 if posisi > 0 else d.c[k] + d.sp[k] / 2
            untung = posisi * lots * OZ * (keluar - entry)
            bal += untung; transaksi.append(untung)
        eq_out[dagang[-1]:z] = bal
    eq_out = pd.Series(eq_out).ffill().fillna(MODAL).to_numpy()
    return Hasil(d.t, eq_out, dep_out, [], transaksi, lewat)


def beli_tahan(d: Data, swap: bool = True) -> Hasil:
    ser = pd.Series(d.c, index=pd.to_datetime(d.t))
    hari = ser.groupby(d.day).last()
    t_hari = ser.index.to_series().groupby(d.day).last()
    eq, out = MODAL, []
    harga0 = d.c[0] + d.sp[0] / 2
    prev = harga0
    for i, (dy, px) in enumerate(hari.items()):
        if i:
            r = px / prev - 1
            bung = 0.0
            if swap:
                m = t_hari.iloc[i].strftime("%Y-%m")
                bung = swap_rate("XAU", "USD", 1, m, MARKUP) * (dy - hari.index[i - 1]) / 365
            eq = eq * (1 + r + bung)
        else:
            eq = MODAL * px / harga0
        out.append(eq)
        prev = px
    return Hasil(t_hari.to_numpy().astype("datetime64[ns]").astype("int64"), np.array(out),
                 np.full(len(out), MODAL), [], [])


def jalankan(nama: str, mulai: str, akhir: str) -> Hasil:
    d = load(mulai, akhir)
    if nama == "E1":
        return grid(d, (1,))
    if nama == "E2":
        return grid(d, (1, -1))
    if nama == "E3":
        return breakout_london(d)
    if nama == "BH":
        return beli_tahan(d, swap=True)
    if nama == "BH_harga":
        return beli_tahan(d, swap=False)
    raise ValueError(nama)
