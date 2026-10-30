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


def test_ea_grid_basket_math():
    from bot.research.ea_xauusd import OZ, Keranjang, lot_round
    assert lot_round(0.015) == 0.02 and lot_round(0.001) == 0.01 and lot_round(0.0225) == 0.02
    k = Keranjang(1, base=0.01, lots=[0.01, 0.02], harga=[2000.0, 1990.0])
    assert np.isclose(k.rata(), (0.01 * 2000 + 0.02 * 1990) / 0.03)
    # ditutup di harga tengah 2000 dengan spread 0,4 → keluar di bid 1999,8
    assert np.isclose(k.nilai(2000.0, 0.4), OZ * (0.01 * -0.2 + 0.02 * 9.8))


def test_harmonic_ratios_follow_rulebook():
    from bot.setups.pola import AFS11B, AFS11C, AFS11F, AFS11G
    assert AFS11G().rasio_ok(0.55, 0.6, 0.79, 1.5) and not AFS11G().rasio_ok(0.7, 0.6, 0.79, 1.5)
    assert AFS11B().rasio_ok(0.6, 0.5, 0.88, 2.0) and not AFS11B().rasio_ok(0.6, 0.5, 0.80, 2.0)
    assert AFS11C().rasio_ok(0.5, 0.5, 1.6, 2.5) and not AFS11C().rasio_ok(0.5, 0.5, 1.4, 2.5)
    assert AFS11F().rasio_ok(0.79, 0.5, 1.27, 2.0) and not AFS11F().rasio_ok(0.79, 0.95, 1.27, 2.0)


def test_zigzag_keeps_most_extreme_of_same_kind():
    from types import SimpleNamespace
    from bot.setups.pola import zigzag_events
    h = np.array([1, 2, 5, 3, 4, 3, 6, 2, 1, 0, 1, 2.0])
    lo = h - 0.5
    sh, sl = ind.swings(h, lo)
    memo = {}
    ctx = SimpleNamespace(b=SimpleNamespace(h=h, l=lo), sw=SimpleNamespace(sh=sh, sl=sl),
                          _memo=lambda k, fn: memo.setdefault(k, fn()))
    ev = zigzag_events(ctx)
    t_last, seq = ev[-1]
    # high 5 (indeks 2) dan high 6 (indeks 6) berurutan tanpa low yang diakui di antaranya → disimpan yang 6
    assert [s[2] for s in seq] == [1, -1] and seq[0][:2] == (6, 6.0) and t_last == seq[-1][0] + 2


def test_new_layak_rules():
    from bot.research.kripto_investasi import layak
    from bot.research.multi_aset import layak as layak_ma
    pat = {"sharpe": 0.6, "dd": 80.0}
    st = {"sharpe": 0.7, "dd": 60.0, "sub": {"a": 1, "b": -1, "c": 2}}
    assert layak(st, pat)["lolos"] and not layak(dict(st, dd=85.0), pat)["lolos"]
    ok = {"t": 2.1, "sub": {"a": 1, "b": 1, "c": -1}, "cagr": 3.0, "dd": 19.0}
    assert layak_ma(ok)["lolos"] and not layak_ma(dict(ok, dd=24.0))["lolos"]


def test_tsmom_stats_cagr():
    import pandas as pd
    from bot.research.tsmom import stats
    idx = pd.date_range("2020-01-01", "2022-01-01", freq="D")
    eq = pd.Series(np.linspace(1.0, 1.21, len(idx)), index=idx)
    st = stats(eq, 365)
    assert abs(st["cagr_pct"] - 10.0) < 0.2 and st["max_dd_pct"] == 0


def _candle_tge(c, low=None):
    import pandas as pd
    c = np.asarray(c, float)
    o = np.r_[c[0], c[:-1]]
    lo = np.minimum(o, c) - 0.1 if low is None else np.asarray(low, float)
    return pd.DataFrame({"o": o, "h": np.maximum(o, c) + 0.1, "l": lo, "c": c},
                        index=pd.date_range("2024-01-01", periods=len(c), freq="D"))


def test_tge_base_entry_then_target():
    from bot.research.tge import simulasi
    c = [10, 8, 7, 6, 5.5, 4.8] + [4.8] * 20 + [6, 8, 10, 12, 14] + [14] * 9
    low = np.minimum(np.r_[c[0], c[:-1]], c) - 0.1
    low[5], low[6:26] = 4.5, 4.7                 # low terendah di hari 5, base dibeli setelah 14 hari (hari 19 → open 20)
    r = simulasi(_candle_tge(c, low), lantai=4.0)
    units = 0.3 * 0.998 / 10 + 0.7 * 0.998 / 4.8
    assert str(r["tgl_base"]) == "2024-01-21" and r["alasan"] == "target" and r["hari_keluar"] == 31
    assert abs(r["hasil"] - (units * 14 * 0.998 - 1)) < 1e-9


def test_tge_cut_loss_below_floor():
    from bot.research.tge import simulasi
    r = simulasi(_candle_tge([10, 8, 6, 4, 3.2, 3.0, 3.0]), lantai=4.0)
    assert r["alasan"] == "cut loss" and r["tgl_base"] is None and r["hari_keluar"] == 5
    assert abs(r["hasil"] - (0.3 * 0.998 / 10 * 3.2 * 0.998 - 0.3)) < 1e-9


def test_saham_angka_and_ko_andri_rules():
    import pandas as pd
    from bot.research.saham import _angka, syarat
    assert _angka("12.238,94") == 12238.94 and _angka("12,238.94") == 12238.94 and _angka("764,65") == 764.65
    assert _angka("(1,234)") == -1234 and _angka("764.65") == 764.65 and np.isnan(_angka("-")) and _angka(5) == 5.0
    m = pd.DataFrame({"kode": list("ABCD"), "sektor": ["X"] * 4, "pbv": [0.8, 0.9, 1.2, 0.5],
                      "per": [5.0, 9.0, 4.0, np.nan], "roe": [0.10, 0.04, 0.2, -0.1],
                      "der": [1.0, 3.0, 0.5, 2.0], "dividen": [10.0, 5.0, 0.0, 0.0]})
    s = syarat(m).set_index("kode")
    # median PER dari laba positif = 5; median DER = 1,5
    assert s.loc["A", "skor"] == 4 and not s.loc["A", "s_per"] and s.loc["A", "s_der"]
    assert s.loc["C", "s_per"] and not s.loc["C", "s_pbv"] and not s.loc["D", "s_per"]


def test_ipo_ara_and_split_and_holding():
    import pandas as pd
    from bot.research.ipo import batas_ara, faktor_split, hari_ara, tahan
    assert batas_ara(150, "Pengembangan") == 0.35 and batas_ara(1000, "Utama") == 0.25
    assert batas_ara(6000, "Utama") == 0.20 and batas_ara(150, "Akselerasi") == 0.10
    # hari 1 ARA 35% dari harga IPO 100; hari 2 naik 30% tapi tutup di bawah tertinggi; hari 3 naik 35% tutup
    # tertinggi; hari 4 naik 25% dari harga di atas Rp200 (batas 25%) tutup tertinggi; hari 5 naik 20% saja
    c = np.array([135.0, 175.5, 236.9, 296.1, 355.3])
    h = np.array([135.0, 180.0, 236.9, 296.1, 355.3])
    ara = hari_ara(c, h, np.r_[100.0, c[:-1]], np.r_[100.0, c[:-1]], "Pengembangan")
    assert ara.tolist() == [True, False, True, True, False]
    t = pd.DatetimeIndex(["2023-01-02", "2023-06-01", "2024-01-02"])
    f = faktor_split(pd.DataFrame({"tanggal": ["2023-03-01"], "nilai": [5.0]}), t)
    assert f.tolist() == [5.0, 1.0, 1.0]
    hari = pd.bdate_range("2024-01-01", periods=300)
    ihsg = pd.Series(np.linspace(100, 110, 300), index=hari)
    p = pd.DataFrame({"adj": np.linspace(50, 100, 300), "v": 1.0}, index=hari)
    r = tahan(p, ihsg, hari[0], (250,))
    assert abs(r["B250"] - (p.adj.iloc[250] / 50 * 0.9975 / 1.0015 - 1)) < 1e-12 and not r["B250_nol"]
    p.loc[hari[100]:, "v"] = 0.0                  # tidak bertransaksi 150 hari bursa sebelum keluar → dianggap 0
    assert tahan(p, ihsg, hari[0], (250,))["B250"] == -1.0


def test_sinyal_harian_pesan_telegram():
    import importlib.util
    import pandas as pd
    spec = importlib.util.spec_from_file_location("sinyal_harian", "scripts/sinyal_harian.py")
    sh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sh)
    senin = pd.Timestamp("2026-11-02")
    jual = {"aksi": "JUAL ke stablecoin", "pegang": False, "close": 77500.0, "pemicu": 79800.0, "puncak": 86620.0}
    tetap = {"aksi": "TETAP PEGANG", "pegang": True, "close": 2600.0, "pemicu": 2340.0, "puncak": 2600.0}
    teks, penting = sh.pesan(senin, {"BTC": jual, "ETH": tetap}, [], [], "2026-11-01", [])
    assert penting and "JUAL BTC" in teks and "Jual BTC → USDT" in teks and "$77.500" in teks
    assert "tetap pegang" in teks and "turun 10,0% lagi" in teks and "&amp;q=" in teks
    ipo = {"jenis": "listing", "kode": "AB&C", "nama": "PT A & B Tbk", "papan": "Utama", "harga": 250, "bawah": 200,
           "atas": 260, "bb": None, "bb_akhir": None, "tawar": None, "tawar_akhir": None, "listing": senin}
    teks, penting = sh.pesan(senin, {"BTC": tetap}, [ipo], [], "", ["data contoh <x>"])
    assert penting and "AB&amp;C" in teks and "PT A &amp; B Tbk" in teks and "jual hari ini" in teks
    assert "&lt;x&gt;" in teks
    teks, penting = sh.pesan(senin, {"BTC": tetap}, [], [], "2026-11-01", [])
    assert not penting and "Laporan mingguan" in teks
