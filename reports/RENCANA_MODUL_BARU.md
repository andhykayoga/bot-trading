# Pra-registrasi: rancangan saya sendiri + semua modul mentor yang belum diuji

Ditulis 29 Oktober 2026, **sebelum hasil dihitung**, dan di-commit lebih dulu. Hasilnya ditulis di
`reports/LAPORAN_MODUL_BARU.md`, apa pun hasilnya.

Permintaan Anda: *"tanpa mentor, kamu yang buatkan cara supaya untung — kamu sudah tahu batasannya, jadi hindari
risiko dan masalah yang sudah ketemu; sekalian uji semua modul yang belum diuji."*

## Pelajaran dari uji sebelumnya → batasan rancangan

| Masalah yang sudah ketemu | Batasan untuk rancangan baru |
|---|---|
| Jual-beli cepat kalah oleh biaya | Transaksi jarang (harian sampai bulanan) |
| Teknikal yang diotak-atik hanya cocok di data lama | Aturan sederhana dari riset, satu pengaturan, tanpa penyetelan |
| Martingale/grid pasti habis suatu saat | Tanpa menambah lot saat rugi, tanpa leverage di kripto |
| Keunggulan per pasar kecil | Sebar ke banyak pasar sekaligus |
| Kripto turun 70–80% di pasar bear | Ada aturan keluar saat tren turun |

## Data dan biaya umum

- **Kripto:** candle harian spot Binance (00.00 UTC) dari `data-api.binance.vision`. BTCUSDT sejak 17 Agustus 2017,
  koin lain sejak listing. Biaya per sisi: BTC/ETH 0,11% (komisi 0,1% + setengah spread), koin lain 0,2%.
  Uang tunai/stablecoin tidak berbunga (0%). Sinyal dari close hari ini, eksekusi di open hari berikutnya.
- **Fear & Greed Index:** alternative.me, harian sejak Februari 2018, memakai label resminya
  ("Extreme Fear" / "Extreme Greed").
- **Multi-aset:** candle harian OANDA (Hugging Face `bunqi/OANDA_*`).
- Periode kripto: seluruh data sampai 28 Oktober 2026; sub-periode 2017–2020, 2021–2023, 2024–2026; dan periode
  uji akhir laporan sebelumnya (29 Desember 2024 – 28 Oktober 2026) sebagai pembanding.

## Bagian A — rancangan saya sendiri

**A1 · Kripto spot dengan filter tren (tanpa leverage).** BTC dan ETH, modal dibagi dua. Masing-masing dipegang
selama close harian di atas rata-rata 200 hari (SMA 200); kalau close di bawahnya, pindah ke stablecoin.
Dilaporkan juga versi BTC saja.

**A2 · Trend-following multi-aset terdiversifikasi** (versi riset yang sebenarnya dari time-series momentum,
Moskowitz-Ooi-Pedersen 2012 dan Hurst-Ooi-Pedersen 2017, yang di laporan sebelumnya hanya diuji dengan 2 instrumen):
- 34 instrumen CFD OANDA: 10 indeks saham (SPX500, NAS100, US2000, DE30, UK100, FR40, EU50, JP225, AU200, HK33),
  6 obligasi (US 2, 5, 10, 30 tahun, Bund, Gilt), 11 komoditas (emas, perak, platinum, tembaga, WTI, Brent, gas
  alam, jagung, kedelai, gandum, gula), 7 forex mayor.
- Akhir tiap bulan: arah = tanda return 252 hari bursa terakhir. Bobot awal tiap instrumen = arah × (10% ÷ √N) ÷
  volatilitas tahunannya (EWMA, pusat massa 60 hari). Lalu seluruh portofolio diskalakan supaya perkiraan
  volatilitasnya (kovarians 252 hari) 10% per tahun, dengan total nilai posisi maksimal 6× modal.
- Instrumen ikut setelah punya ≥ 300 hari data. Evaluasi 1 Januari 2006 – Oktober 2026; sub-periode 2006–2011,
  2012–2018, 2019–2026.
- Return harga harian dipakai sebagai perkiraan return berjangka (dividen indeks dan bunga dianggap saling
  menutup; ketidakpastian ±1–2% per tahun, dicatat di laporan).
- **Dua tingkat biaya:**
  - *Biaya institusi (futures):* setengah spread per perubahan posisi — indeks 1,5 bp, obligasi 2 bp, logam 2 bp,
    minyak 4 bp, gas alam & pertanian 10 bp, forex 1 bp.
  - *Biaya ritel (CFD):* spread 2× angka di atas, ditambah biaya pembiayaan 2,5% per tahun dari nilai posisi
    (forex 1%), seperti swap/financing broker CFD. **Ini ukuran utama**, karena itu yang bisa Anda pakai.

**Syarat layak A1** (investasi spot tanpa leverage, dibandingkan dengan beli-dan-tahan): rasio hasil/naik-turun
(Sharpe) lebih tinggi **dan** penurunan terdalam lebih kecil daripada beli-dan-tahan BTC+ETH 50/50, serta untung di
≥ 2 dari 3 sub-periode.

**Syarat layak A2** (di biaya ritel): t-stat return harian ≥ 2,0; untung di ≥ 2 dari 3 sub-periode; hasil ≥ 2% per
tahun; penurunan terdalam ≤ 20%.

## Bagian B — modul mentor yang belum diuji

Aturan diambil dari rulebook. Bagian yang tidak disebut mentor saya tandai *(pilihan saya)*.

**B1 · KMS-I1 Alokasi portofolio** (Kalimasada). Rebalance tiap awal kuartal *(pilihan saya: frekuensi tidak
disebut)*.
- I1a: 70% BTC, 15% altcoin, 15% meme coin. Altcoin = 5 koin dengan volume USDT 90 hari terbesar di Binance pada
  tanggal rebalance, dari daftar 40 altcoin besar termasuk yang kemudian ambruk/delisting (LUNA, FTT, dll.),
  tanpa BTC, stablecoin, dan meme. Meme = semua dari DOGE, SHIB, PEPE, FLOKI, BONK, WIF yang sudah listing, bobot
  sama; sebelum ada, porsinya stablecoin. *(Catatan: meme coin yang mati sebelum listing di Binance tidak ada di
  data, jadi hasil meme cenderung terlalu bagus.)*
- I1b pasif: 100% spot BTC + ETH (50/50).
- I1c (target LIVE-01): 70% BTC + 30% stablecoin.

**B2 · KMS-I2 Moon bag.** Cicilan bulanan tetap ke komposisi I1a. Kalau nilai satu koin ≥ 2× modal yang masuk ke
koin itu, jual 50%; sisanya jadi moon bag yang tidak dijual. Dibandingkan dengan cicilan yang sama tanpa moon bag.

**B3 · KMS-I3 Cicil 5× masuk, 5× keluar** (BTC dan ETH masing-masing). Candle mingguan, RSI(14) (D-08: jenuh jual
< 30, jenuh beli > 70). Tiap minggu RSI < 30: beli 1/5 modal (maksimal 5 kali). Tiap minggu RSI > 70: jual 1/5
posisi *(pilihan saya: satu cicilan per candle mingguan)*.

**B4 · KMS-I4 Fear & Greed** (BTC). Beli semua saat label "Extreme Fear", jual semua saat "Extreme Greed".

**B5 · LIVE-01 Siklus halving** (BTC). Pegang BTC dari 365 hari sebelum halving sampai 365 hari sesudahnya (versi
mentor 1) atau 500 hari sesudahnya (versi mentor 2); di luar itu stablecoin. Halving dalam data: 11 Mei 2020 dan
20 April 2024. *(Hanya 2 siklus — bukti sangat lemah apa pun hasilnya.)*

**B6 · AND-02 Trailing stop 5–10%** (Ko Andri; BTC dan ETH). Beli, jual kalau close turun 10% (versi 2: 5%) dari
close tertinggi sejak beli. Masuk lagi saat close mencetak tertinggi 20 hari *(pilihan saya: mentor tidak
menyebut kapan masuk lagi)*.

Syarat layak B1–B6 sama dengan A1 (dibanding beli-dan-tahan yang sesuai: BTC untuk B4–B5, BTC+ETH untuk lainnya;
B2 dibanding cicilan tanpa moon bag).

**B7 · Pola grafik (ditunda di versi pertama, Q-23)** — dibuat sebagai setup biasa dan dijalankan dengan
pemilihan G-17 yang sama persis seperti 30 setup sebelumnya, di pasar forex (EURUSD, XAUUSD) dan kripto (BTC,
ETH), timeframe H4 dan D1:
- **AFS-11 Harmonic**: Gartley (B di 0,5–0,618 XA; D di 0,786 XA *(pilihan saya: rasio D Gartley tidak disebut)*),
  Bat (B di 0,5–0,618; D di 0,85–0,92), Crab (B di 0,5–0,618; D di 1,618), Butterfly (XB 0,786; AC 0,382–0,886; BD
  1,618–2,24; XD 1,27). Toleransi ±0,05 untuk rasio satu angka (mentor: selisih 0,01–0,1 "nggak apa-apa"). Titik
  X-A-B-C-D = 5 swing berselang-seling terakhir (D-01). Masuk setelah D diakui dan ada pemicu (D-06/Stochastic);
  SL 1×ATR di luar D; TP RR 1:2.
- **AFS-23 Pola klasik**: head & shoulders (dan kebalikannya; masuk saat close menembus neckline), ascending /
  descending triangle (masuk *sebelum* breakout di pantulan low yang makin tinggi, sesuai mentor), rising/falling
  wedge (3 sentuhan, masuk di sentuhan ketiga), broadening (3 sentuhan, masuk di sisi luar). SL 1×ATR di luar titik
  terakhir; TP RR 1:2 *(pilihan saya: target tidak disebut seragam)*. Flag/pennant (mentor: "sering palsu, jarang
  dipakai"), diamond, dan rectangle tidak dibuat karena tidak punya aturan yang bisa diukur.
- Syarat lolos sama dengan laporan backtest forex: lolos pemilihan G-17, lalu untung bersih dengan ≥ 30 transaksi di
  uji akhir.

## Tidak bisa diuji (dan alasannya)

| Modul | Alasan |
|---|---|
| AFS-24 Elliott Wave, AFS-25 Andrews Pitchfork | Penghitungan gelombang / pemilihan titik pivot subjektif; aturan yang saya buat bukan aturan mentor |
| AFS-F3 akselerasi/deselerasi | Mentor tidak memberi angka sama sekali |
| KMS-01 Wyckoff spring/UTAD | Mengenali tahap A–E butuh penilaian; versi yang bisa dikodekan (stop hunt + BOS, AFS-06) sudah diuji |
| AFS-22 Order flow | Mentor tidak menyebut entry, SL, dan TP |
| LIVE-02 Token baru (TGE) | Butuh data valuasi investor tiap token (harga lantai) yang tidak tersedia |
| AFS-F1 Screening altcoin | Filter untuk setup trading altcoin; butuh data dominasi BTC historis |
| Saham: valuasi Ko Andri (PER, PBV, dividen), bandarmologi Ko Hengki, ARA/ARB | Data saham BEI yang tersedia hanya 61 saham besar yang masih ada sekarang, sejak 2023, tanpa riwayat data fundamental dan tanpa broker summary — hasilnya pasti bias |

## Hitungan varian

A: 2 rancangan (A2 dengan 2 tingkat biaya, hanya ritel yang menentukan). B1–B6: 10 versi (I1a, I1b, I1c, moon bag,
5×5 BTC & ETH, Fear & Greed, halving 365 & 500, trailing 10% & 5%). B7: 8 setup × pemilihan G-17. Tidak ada
pengaturan lain yang dicoba setelah hasil terlihat.
