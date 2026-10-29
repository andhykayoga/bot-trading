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


def test_usdjpy_conversion_to_usd():
    inst = INSTRUMENTS["USDJPY"]
    assert np.isclose(inst.usd_per_quote(150.0), 1 / 150.0)
    assert np.isclose(inst.notional_usd(1000, 150.0), 1000)       # 1000 unit USDJPY = 1000 USD
    assert np.isclose(INSTRUMENTS["GBPUSD"].notional_usd(1000, 1.3), 1300)


def test_crypto_spot_has_no_swap_and_round_trip_cost():
    btc = INSTRUMENTS["BTCUSD"]
    assert not btc.swap
    assert np.isclose(btc.spread(100_000.0) / 100_000.0, 0.0022)


def test_proyeksi_without_return_is_just_deposits():
    from bot.research.investasi import proyeksi
    sal = proyeksi(np.zeros((1, 2)), 10e6, 1e6, inflasi=0.0)
    assert sal.shape == (1, 25) and np.isclose(sal[0, -1], 10e6 + 24 * 1e6)


def test_proyeksi_compounds_monthly_to_annual_rate():
    from bot.research.investasi import proyeksi
    sal = proyeksi(np.full((1, 3), 0.05), 100.0, 0.0, inflasi=0.0)
    assert np.isclose(sal[0, 12], 105.0) and np.isclose(sal[0, -1], 100 * 1.05 ** 3)


def test_bootstrap_keeps_five_year_blocks_in_order():
    from bot.research.investasi import bootstrap
    r = np.arange(20, dtype=float)
    bs = bootstrap(r, 10, n=50, blok=5, seed=1)
    assert bs.shape == (50, 10)
    for row in bs:
        for k in (0, 5):
            assert all((row[k + i + 1] - row[k + i]) % 20 == 1 for i in range(4))


def test_forex_cepat_session_windows_eurusd_winter():
    import pandas as pd
    from bot.research.forex_cepat import posisi
    t = pd.date_range("2025-01-15 00:00", "2025-01-15 23:55", freq="5min", tz="UTC")
    p = pd.Series(posisi("S1", "EURUSD", t.as_unit("ns").asi8), index=t.strftime("%H:%M"))
    # Frankfurt buka sendiri 07–13 UTC → jual; New York buka sendiri 16–22 UTC → beli; rollover 21.55 tutup
    assert p["06:55"] == 0 and p["07:00"] == -1 and p["12:55"] == -1 and p["13:00"] == 0
    assert p["16:00"] == 1 and p["21:50"] == 1 and p["21:55"] == 0
    assert (posisi("S1", "USDCAD", t.as_unit("ns").asi8) == 0).all()


def test_tsmom_stats_cagr():
    import pandas as pd
    from bot.research.tsmom import stats
    idx = pd.date_range("2020-01-01", "2022-01-01", freq="D")
    eq = pd.Series(np.linspace(1.0, 1.21, len(idx)), index=idx)
    st = stats(eq, 365)
    assert abs(st["cagr_pct"] - 10.0) < 0.2 and st["max_dd_pct"] == 0
