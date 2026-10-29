# bot-trading

- [`materi/PETA.md`](materi/PETA.md) — peta materi kelas (kripto, saham, forex, Astronacci) dari transkrip di `materi/mentah/`.
- [`rulebook/`](rulebook/README.md) — rulebook strategi untuk bot forex & kripto, dipisah per mentor dan per setup, lengkap dengan pertanyaan dan jawaban Anda.
- [`reports/LAPORAN_BACKTEST_FOREX.md`](reports/LAPORAN_BACKTEST_FOREX.md) — **hasil backtest semua setup forex** (EURUSD, XAUUSD), dengan dan tanpa filter Astronacci, dalam bahasa sederhana.
- `bot/` — kode bot Python (backtest sekarang, live nanti). Belum terhubung ke broker.

## Struktur kode

| Folder / file | Isi |
|---|---|
| `bot/markets.py` | Pasar = akun: **forex** (aktif) dan **kripto** (sudah didefinisikan, belum aktif). Instrumen, batas hari D-12, spread, swap. |
| `bot/data/` | Pengunduh data (`download.py`), pembentuk candle M5→M15/H1/H4/D1/W1/MN dengan batas 17.00 New York (`candles.py`), kalender berita G-13 (`news.py`). |
| `bot/indicators.py` | Indikator dan definisi bersama D-01 – D-08 (swing fractal 2–2, struktur, ATR TradingView, Ichimoku geser 25, Stochastic, KST, CMF, PSAR, dll.). |
| `bot/setups/` | **Satu kelas per setup**, masing-masing berdiri sendiri: `pln01.py` (Pola N), `ichimoku.py` (ICH-01–04), `afs_*.py` (Alvesting), `kms_hki.py` (Wyckoff, Ko Hengki). |
| `bot/engine/` | Mesin backtest dengan aturan global G-01, G-03, G-07, G-08, G-13, G-15, G-16 dan biaya (spread + swap). |
| `bot/filters/astro.py` | Filter Astronacci WKT-01 – WKT-04 (fase bulan, Fibonacci waktu, Merkurius retrograde) dengan pustaka `ephem`. |
| `bot/research/` | Pembagian data 60/20/20, pemilihan varian G-17, uji filter waktu, pembanding entry acak. |
| `bot/live.py` | Kerangka live: antarmuka `Broker`, `PaperBroker`, pemeriksaan keselamatan G-15. |
| `config/setups.toml` | **Menyalakan/mematikan setup** satu per satu (daftar `enabled`), per pasar. |

## Menjalankan

```bash
pip install -r requirements.txt
```

```bash
python -m bot.data.download
```

```bash
python scripts/run_backtest.py --jobs 4
```

```bash
python scripts/make_report.py
```

Menguji sebagian setup saja: `python scripts/run_backtest.py --setups PLN-01,ICH-01`. Data mentah (±90 MB) disimpan di `data/` dan tidak masuk git.

## Menambah kripto nanti

1. Aktifkan pasar `crypto` di `bot/markets.py` (`active=True`) dan isi biaya BTC/ETH (spread/komisi exchange, funding).
2. Isi daftar `enabled` di bagian `[crypto]` `config/setups.toml`.
3. Jalankan pengunduh data dan backtest untuk pasar kripto. Akun, batas hari (00.00 UTC), dan batas risiko kripto terpisah dari forex (Q-49); pembagian data 60/20/20 dihitung sendiri untuk kripto (Q-50).
