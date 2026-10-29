"""Tes cepat untuk definisi bersama dan biaya (tidak butuh data unduhan)."""
import numpy as np
import talib

from bot import indicators as ind
from bot.engine.costs import policy_rate, swap_rate
from bot.markets import INSTRUMENTS
from bot.setups import REGISTRY
from bot.setups.afs_indicators import renko


def test_atr_converges_to_talib():
    # Awal hitungan mengikuti TradingView (TR candle pertama = high − low), jadi hanya
    # sama dengan TA-Lib setelah pemanasan.
    rng = np.random.default_rng(0)
    c = np.cumsum(rng.normal(0, 1, 600)) + 100
    h, l = c + rng.random(600), c - rng.random(600)
    assert np.nanmax(np.abs(ind.atr(h, l, c, 14)[300:] - talib.ATR(h, l, c, 14)[300:])) < 1e-6


def test_swings_fractal_2_2():
    h = np.array([1, 2, 3, 2, 1, 2, 5, 4, 3, 4, 3.0])
    sh, sl = ind.swings(h, h - 0.5)
    assert list(np.flatnonzero(sh)) == [2, 6]
    assert list(np.flatnonzero(sl)) == [4]


def test_swing_state_only_after_confirmation():
    h = np.array([1, 2, 3, 2, 1, 2, 5, 4, 3, 4, 3.0])
    st = ind.SwingState(h, h - 0.5, h - 0.25)
    assert np.isnan(st.hp[3, 0])      # swing high di indeks 2 belum diakui di candle 3
    assert st.hp[4, 0] == 3           # diakui setelah candle 4 close


def test_kumo_shift_25():
    rng = np.random.default_rng(1)
    c = np.cumsum(rng.normal(0, 1, 200)) + 100
    ic = ind.ichimoku(c + 1, c - 1)
    assert np.isclose(ic["kumo_a"][120], ic["span_a_raw"][95])


def test_spread_and_swap():
    assert INSTRUMENTS["EURUSD"].spread(1.1) == 0.00014
    assert np.isclose(INSTRUMENTS["XAUUSD"].spread(4000.0), 0.6)
    assert policy_rate("USD", "2024-01") > policy_rate("EUR", "2024-01")
    # 2024: long EURUSD membayar selisih bunga + biaya admin
    assert swap_rate("EUR", "USD", 1, "2024-01", 0.01) < 0


def test_renko_reversal_needs_two_boxes():
    c = np.array([100, 101, 102, 103, 102.5, 101.5, 100.9])
    box = np.full(len(c), 1.0)
    bricks = renko(c, box)
    assert [b[1] for b in bricks] == [1, 1, 1, -1]


def test_every_setup_has_plan_and_defaults():
    for sid, cls in REGISTRY.items():
        st = cls()
        assert st.id == sid and st.defaults
        st.plan()
