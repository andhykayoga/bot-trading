# bot-trading

- [`materi/PETA.md`](materi/PETA.md) — peta materi kelas (kripto, saham, forex, Astronacci) dari transkrip di `materi/mentah/`.
- [`rulebook/`](rulebook/README.md) — rulebook strategi untuk bot forex & kripto, dipisah per mentor dan per setup, lengkap dengan pertanyaan dan jawaban Anda.
- [`reports/LAPORAN_BACKTEST_FOREX.md`](reports/LAPORAN_BACKTEST_FOREX.md) — **hasil backtest semua setup forex** (EURUSD, XAUUSD), dengan dan tanpa filter Astronacci, dalam bahasa sederhana.
- [`reports/LAPORAN_RENCANA_CADANGAN.md`](reports/LAPORAN_RENCANA_CADANGAN.md) — **rencana cadangan**: perbaikan terbatas (diuji di GBPUSD/USDJPY), setup mentor di BTC/ETH, patokan riset time-series momentum, kesimpulan, dan usulan semi-otomatis. Pra-registrasinya di [`reports/RENCANA_CADANGAN.md`](reports/RENCANA_CADANGAN.md).
- [`reports/RENCANA_UNTUNG.md`](reports/RENCANA_UNTUNG.md) — **rencana supaya uang bertambah** berdasarkan riset (bukan trading): portofolio Seimbang 50/40/10, kalkulasi untung per minggu/bulan/tahun, rentang hasil, dan peluang rugi.
- [`reports/LAPORAN_FOREX_CEPAT.md`](reports/LAPORAN_FOREX_CEPAT.md) — **uji forex cepat**: hitungan impas scalping, tiga pola forex dari jurnal (jam sesi, hari FOMC, fixing London) di 7 pair, dan demo otak-atik teknikal. Pra-registrasinya di [`reports/RENCANA_FOREX_CEPAT.md`](reports/RENCANA_FOREX_CEPAT.md).
- [`reports/LAPORAN_EA_XAUUSD.md`](reports/LAPORAN_EA_XAUUSD.md) — **uji tipe EA XAUUSD yang viral** (grid martingale beli saja/dua arah, breakout London) di data emas 2010–2026, plus cara memeriksa EA sebelum membeli. Pra-registrasinya di [`reports/RENCANA_EA_XAUUSD.md`](reports/RENCANA_EA_XAUUSD.md).
- `bot/` — kode bot Python (backtest sekarang, live nanti). Belum terhubung ke broker.

## Struktur kode

| Folder / file | Isi |
|---|---|
| `bot/markets.py` | Pasar = akun: **forex** (EURUSD, XAUUSD), **forex_uji** (GBPUSD, USDJPY) dan **forex_riset** (AUDUSD, USDCAD, USDCHF, NZDUSD), keduanya hanya untuk pengujian, **crypto** (BTC, ETH spot Binance). Instrumen, batas hari D-12, spread/komisi, swap. |
| `bot/data/` | Pengunduh data (`download.py`), pembentuk candle M5→M15/H1/H4/D1/W1/MN dengan batas 17.00 New York (`candles.py`), kalender berita G-13 (`news.py`). |
| `bot/indicators.py` | Indikator dan definisi bersama D-01 – D-08 (swing fractal 2–2, struktur, ATR TradingView, Ichimoku geser 25, Stochastic, KST, CMF, PSAR, dll.). |
| `bot/setups/` | **Satu kelas per setup**, masing-masing berdiri sendiri: `pln01.py` (Pola N), `ichimoku.py` (ICH-01–04), `afs_*.py` (Alvesting), `kms_hki.py` (Wyckoff, Ko Hengki), `improved.py` (versi perbaikan V1–V4). |
| `bot/engine/` | Mesin backtest dengan aturan global G-01, G-03, G-07, G-08, G-13, G-15, G-16 dan biaya (spread + swap). |
| `bot/filters/astro.py` | Filter Astronacci WKT-01 – WKT-04 (fase bulan, Fibonacci waktu, Merkurius retrograde) dengan pustaka `ephem`. |
| `bot/research/` | Pembagian data 60/20/20, pemilihan varian G-17, uji filter waktu, pembanding entry acak, patokan time-series momentum (`tsmom.py`), simulasi portofolio jangka panjang (`investasi.py`), uji forex cepat (`forex_cepat.py`), uji tipe EA XAUUSD (`ea_xauusd.py`). |
| `bot/live.py` | Kerangka live: antarmuka `Broker`, `PaperBroker`, pemeriksaan keselamatan G-15. |
| `scripts/sinyal.py` | **Mode semi-otomatis**: memindai sinyal, menghitung lot, mencatat jurnal; Anda yang mengeksekusi. |
| `config/setups.toml` | **Menyalakan/mematikan setup** satu per satu (daftar `enabled`), per pasar. |
| `config/sinyal.toml` | Saldo, risiko, dan setup yang dipindai mode semi-otomatis. |
| `scripts/rencana_untung.py`, `config/rencana.toml` | Kalkulator rencana investasi: modal, setoran bulanan, pilihan portofolio. |

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

Menguji sebagian setup saja: `python scripts/run_backtest.py --setups PLN-01,ICH-01`. Data mentah disimpan di `data/` dan tidak masuk git.

Rencana cadangan (perbaikan, kripto, patokan riset):

```bash
python -m bot.data.download forex_uji crypto
```

```bash
python scripts/run_cadangan.py
```

```bash
python scripts/run_backtest.py --market crypto
```

```bash
python scripts/run_cadangan.py --crypto-long
```

```bash
python scripts/make_report_cadangan.py
```

Mode semi-otomatis (tanpa broker):

```bash
python scripts/sinyal.py
```

Uji forex cepat (scalping, pola jurnal, demo otak-atik):

```bash
python -m bot.data.download forex forex_uji forex_riset
```

```bash
python scripts/run_forex_cepat.py
```

Uji tipe EA XAUUSD yang viral (±5 menit):

```bash
python scripts/run_ea_xauusd.py --ulang
```

Rencana investasi dan kalkulasi untung (ubah angka di `config/rencana.toml`):

```bash
python -m bot.data.download riset
```

```bash
python scripts/rencana_untung.py --layar
```

## Kripto

Pasar `crypto` sudah aktif untuk backtest: akun, batas hari (00.00 UTC), leverage 1×, dan batas risiko terpisah dari forex (Q-49); pembagian data 60/20/20 dihitung sendiri (Q-50). Biaya memakai komisi spot Binance; sesuaikan `spread_pct` di `bot/markets.py` dengan exchange berizin OJK yang Anda pakai.
