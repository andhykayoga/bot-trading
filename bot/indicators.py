"""Indikator dan definisi bersama (D-01 – D-08), mengikuti rumus bawaan TradingView.

Semua fungsi menerima array numpy dan mengembalikan array sepanjang input; nilai
yang belum bisa dihitung = NaN. Nilai di indeks i hanya memakai candle 0..i
(tidak mengintip masa depan), kecuali swing yang baru diakui 2 candle kemudian
(lihat `swings`).
"""
from __future__ import annotations

import numpy as np
import talib
from numba import njit


# ---------------------------------------------------------------- dasar

def sma(x: np.ndarray, n: int) -> np.ndarray:
    return talib.SMA(np.asarray(x, float), n)


@njit(cache=True)
def _rma(x, n):
    out = np.full(len(x), np.nan)
    s = 0.0
    cnt = 0
    start = -1
    for i in range(len(x)):
        if np.isnan(x[i]):
            continue
        if start < 0:
            s += x[i]
            cnt += 1
            if cnt == n:
                out[i] = s / n
                start = i
        else:
            out[i] = (out[i - 1] * (n - 1) + x[i]) / n
    return out


def rma(x: np.ndarray, n: int) -> np.ndarray:
    """Rata-rata Wilder (RMA TradingView), diawali SMA n nilai pertama."""
    return _rma(np.asarray(x, float), n)


@njit(cache=True)
def _ema(x, n):
    out = np.full(len(x), np.nan)
    a = 2.0 / (n + 1)
    prev = np.nan
    for i in range(len(x)):
        if np.isnan(x[i]):
            continue
        prev = x[i] if np.isnan(prev) else a * x[i] + (1 - a) * prev
        out[i] = prev
    return out


def ema(x: np.ndarray, n: int) -> np.ndarray:
    return _ema(np.asarray(x, float), n)


def true_range(h, l, c) -> np.ndarray:
    pc = np.r_[np.nan, c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    tr[0] = h[0] - l[0]
    return tr


def atr(h, l, c, n: int = 14) -> np.ndarray:
    """ATR(14) TradingView = RMA dari true range (D-03)."""
    return rma(true_range(h, l, c), n)


def highest(x, n):
    return talib.MAX(np.asarray(x, float), n)


def lowest(x, n):
    return talib.MIN(np.asarray(x, float), n)


def shift(x: np.ndarray, k: int) -> np.ndarray:
    """Geser ke kanan k candle (nilai lama muncul di indeks i): out[i] = x[i-k]."""
    out = np.full(len(x), np.nan)
    if k < len(x):
        out[k:] = x[: len(x) - k]
    return out


# ---------------------------------------------------------------- osilator

def stochastic(h, l, c, k: int = 5, smooth_k: int = 3, d: int = 3):
    """Stochastic TradingView: %K = SMA(raw, smooth_k), %D = SMA(%K, d) (D-08)."""
    hh, ll = highest(h, k), lowest(l, k)
    rng = hh - ll
    raw = np.where(rng > 0, 100 * (c - ll) / np.where(rng > 0, rng, 1), 50.0)
    raw[np.isnan(hh)] = np.nan
    kk = sma(raw, smooth_k)
    return kk, sma(kk, d)


def kst(c):
    """KST bawaan TradingView (10,15,20,30 / 10,10,10,15 / sinyal 9)."""
    def roc(n):
        return 100 * (c / shift(c, n) - 1)
    k = sma(roc(10), 10) + 2 * sma(roc(15), 10) + 3 * sma(roc(20), 10) + 4 * sma(roc(30), 15)
    return k, sma(k, 9)


def cmf(h, l, c, v, n: int = 20):
    rng = h - l
    mfm = np.where(rng > 0, ((c - l) - (h - c)) / np.where(rng > 0, rng, 1), 0.0)
    num = talib.SUM(mfm * v, n)
    den = talib.SUM(np.asarray(v, float), n)
    return np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)


# ---------------------------------------------------------------- tren

def ichimoku(h, l, shift_n: int = 25, tenkan_n=9, kijun_n=26, span_b_n=52):
    """Ichimoku Hosoda dengan pergeseran Rafał (Q-36): Kumo di candle t = Senkou yang
    dihitung di t-25. Chikou dibandingkan dengan harga 25 candle sebelumnya (dipakai
    di setup)."""
    tenkan = (highest(h, tenkan_n) + lowest(l, tenkan_n)) / 2
    kijun = (highest(h, kijun_n) + lowest(l, kijun_n)) / 2
    span_a_raw = (tenkan + kijun) / 2
    span_b_raw = (highest(h, span_b_n) + lowest(l, span_b_n)) / 2
    kumo_a = shift(span_a_raw, shift_n)
    kumo_b = shift(span_b_raw, shift_n)
    return {"tenkan": tenkan, "kijun": kijun, "kumo_a": kumo_a, "kumo_b": kumo_b,
            "kumo_top": np.fmax(kumo_a, kumo_b), "kumo_bot": np.fmin(kumo_a, kumo_b),
            "span_a_raw": span_a_raw, "span_b_raw": span_b_raw}


@njit(cache=True)
def _psar(h, l, start, inc, mx):
    n = len(h)
    out = np.full(n, np.nan)
    trend = np.zeros(n, np.int8)
    if n < 2:
        return out, trend
    up = h[1] >= h[0]
    sar = l[0] if up else h[0]
    ep = h[1] if up else l[1]
    af = start
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, l[i - 1], l[i - 2] if i >= 2 else l[i - 1])
            if l[i] < sar:
                up = False
                sar = ep
                ep = l[i]
                af = start
            elif h[i] > ep:
                ep = h[i]
                af = min(af + inc, mx)
        else:
            sar = max(sar, h[i - 1], h[i - 2] if i >= 2 else h[i - 1])
            if h[i] > sar:
                up = True
                sar = ep
                ep = h[i]
                af = start
            elif l[i] < ep:
                ep = l[i]
                af = min(af + inc, mx)
        out[i] = sar
        trend[i] = 1 if up else -1
    return out, trend


def psar(h, l, start=0.02, inc=0.02, mx=0.2):
    """Parabolic SAR bawaan TradingView. Mengembalikan (nilai SAR, arah +1/-1)."""
    return _psar(np.asarray(h, float), np.asarray(l, float), start, inc, mx)


@njit(cache=True)
def _linreg(c, n, dev):
    m = len(c)
    mid = np.full(m, np.nan)
    up = np.full(m, np.nan)
    lo = np.full(m, np.nan)
    x = np.arange(n, dtype=np.float64)
    xm = x.mean()
    sxx = ((x - xm) ** 2).sum()
    for i in range(n - 1, m):
        y = c[i - n + 1: i + 1]
        ym = y.mean()
        b = ((x - xm) * (y - ym)).sum() / sxx
        a = ym - b * xm
        fit = a + b * x
        sd = np.sqrt(((y - fit) ** 2).sum() / n)
        mid[i] = a + b * (n - 1)
        up[i] = mid[i] + dev * sd
        lo[i] = mid[i] - dev * sd
    return mid, up, lo


def linreg_channel(c, n: int = 100, dev: float = 2.0):
    """Linear Regression Channel bawaan TradingView (100, deviasi 2), nilai di candle terakhir."""
    return _linreg(np.asarray(c, float), n, dev)


def keltner(h, l, c, n: int = 20, atr_n: int = 10, mult: float = 2.0):
    mid = ema(c, n)
    a = atr(h, l, c, atr_n)
    return mid, mid + mult * a, mid - mult * a


def donchian(h, l, n: int = 20):
    up, lo = highest(h, n), lowest(l, n)
    return up, (up + lo) / 2, lo


# ---------------------------------------------------------------- swing & struktur

def swings(h, l, k: int = 2):
    """Swing fractal 2 kiri 2 kanan (D-01). Mengembalikan boolean (is_high, is_low)
    per candle swing. Swing di candle i baru diakui setelah candle i+k close."""
    n = len(h)
    sh = np.zeros(n, bool)
    sl = np.zeros(n, bool)
    if n < 2 * k + 1:
        return sh, sl
    core = slice(k, n - k)
    hh = np.ones(n - 2 * k, bool)
    ll = np.ones(n - 2 * k, bool)
    for j in range(1, k + 1):
        hh &= (h[core] > h[k - j: n - k - j]) & (h[core] > h[k + j: n - k + j])
        ll &= (l[core] < l[k - j: n - k - j]) & (l[core] < l[k + j: n - k + j])
    sh[core] = hh
    sl[core] = ll
    return sh, sl


@njit(cache=True)
def _swing_state(h, l, c, sh, sl, k):
    """Untuk setiap candle t (setelah close), simpan 3 swing high & 3 swing low terakhir
    yang sudah diakui (harga dan indeks), serta status struktur D-02."""
    n = len(c)
    hp = np.full((n, 3), np.nan)   # harga swing high: [terbaru, sebelumnya, sebelumnya lagi]
    hi = np.full((n, 3), -1)
    lp = np.full((n, 3), np.nan)
    li = np.full((n, 3), -1)
    trend = np.zeros(n, np.int8)
    cur_hp = np.full(3, np.nan); cur_hi = np.full(3, -1)
    cur_lp = np.full(3, np.nan); cur_li = np.full(3, -1)
    for t in range(n):
        j = t - k                     # swing di j baru diakui saat t = j + k
        if j >= 0:
            if sh[j]:
                cur_hp[2] = cur_hp[1]; cur_hi[2] = cur_hi[1]
                cur_hp[1] = cur_hp[0]; cur_hi[1] = cur_hi[0]
                cur_hp[0] = h[j]; cur_hi[0] = j
            if sl[j]:
                cur_lp[2] = cur_lp[1]; cur_li[2] = cur_li[1]
                cur_lp[1] = cur_lp[0]; cur_li[1] = cur_li[0]
                cur_lp[0] = l[j]; cur_li[0] = j
        hp[t] = cur_hp; hi[t] = cur_hi; lp[t] = cur_lp; li[t] = cur_li
        bull = (cur_hp[0] > cur_hp[1]) and (cur_hp[1] > cur_hp[2]) and \
               (cur_lp[0] > cur_lp[1]) and (cur_lp[1] > cur_lp[2])
        bear = (cur_hp[0] < cur_hp[1]) and (cur_hp[1] < cur_hp[2]) and \
               (cur_lp[0] < cur_lp[1]) and (cur_lp[1] < cur_lp[2])
        # struktur patah (CHoCH) kalau close menembus higher low / lower high terakhir
        if bull and c[t] < cur_lp[0]:
            bull = False
        if bear and c[t] > cur_hp[0]:
            bear = False
        trend[t] = 1 if bull else (-1 if bear else 0)
    return hp, hi, lp, li, trend


class SwingState:
    """Swing terakhir yang sudah diakui pada setiap candle + struktur D-02.

    hp[t, 0] = harga swing high terbaru yang diketahui saat candle t close, hi[t, 0] = indeksnya.
    trend[t] = +1 bullish, -1 bearish, 0 sideways (minimal 2 higher high & 2 higher low).
    """

    def __init__(self, h, l, c, k: int = 2):
        self.sh, self.sl = swings(h, l, k)
        self.hp, self.hi, self.lp, self.li, self.trend = _swing_state(
            np.asarray(h, float), np.asarray(l, float), np.asarray(c, float), self.sh, self.sl, k)


# ---------------------------------------------------------------- candle (D-06)

def candle_patterns(o, h, l, c):
    """Pola candle TA-Lib (Q-16). Mengembalikan (bull_trigger, bear_trigger) boolean."""
    o, h, l, c = (np.asarray(x, float) for x in (o, h, l, c))
    eng = talib.CDLENGULFING(o, h, l, c)
    bull = (talib.CDLHAMMER(o, h, l, c) != 0) | (talib.CDLINVERTEDHAMMER(o, h, l, c) != 0) | (eng > 0)
    bear = (talib.CDLHANGINGMAN(o, h, l, c) != 0) | (talib.CDLSHOOTINGSTAR(o, h, l, c) != 0) | (eng < 0)
    return bull, bear


def strong_candle(o, h, l, c, ratio: float = 0.7):
    """Candle kuat: badan ≥ 70% panjang (D-06)."""
    rng = h - l
    return (rng > 0) & (np.abs(c - o) >= ratio * rng)


def big_candle(h, l, n: int = 20):
    """Candle besar: panjang di atas rata-rata panjang 20 candle terakhir (D-06)."""
    rng = h - l
    return rng > shift(sma(rng, n), 1)


def volume_high(v, n: int = 20):
    """Volume naik/tinggi: di atas rata-rata 20 candle terakhir (D-07)."""
    return np.asarray(v, float) > shift(sma(v, n), 1)


def stoch_cross(k, d, zone: str):
    """Silang naik di jenuh jual (%K memotong %D ke atas saat %K < 20) atau silang
    turun di jenuh beli (%K > 80) (D-08)."""
    pk, pd_ = shift(k, 1), shift(d, 1)
    if zone == "oversold":
        return (pk <= pd_) & (k > d) & (k < 20)
    return (pk >= pd_) & (k < d) & (k > 80)
