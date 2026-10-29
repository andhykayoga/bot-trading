# Pra-registrasi: order flow (AFS-22) dan token baru (LIVE-02)

Ditulis 29 Oktober 2026, **sebelum hasil dihitung**, dan di-commit lebih dulu. Hasilnya ditulis di
`reports/LAPORAN_ORDERFLOW_TGE.md`, apa pun hasilnya. Bagian yang tidak disebut mentor dilengkapi dari riset dan
ditandai *(pelengkap)*.

## A. Order flow (AFS-22, Alvesting)

### Riset yang dipakai untuk melengkapi

- Cont, Kukanov & Stoikov (2014): ketidakseimbangan order (beli agresif − jual agresif) menjelaskan perubahan harga
  **pada saat yang sama**, hubungannya kira-kira lurus; daya ramalnya ke depan kecil.
- Kim & Hansen (2026, arXiv 2607.09426, perpetual Binance 2021–2024): ketidakseimbangan order di awal tiap
  15 menit meramal arah harga 4–12 jam ke depan (searah), tetapi besarnya ±0,5 bp, sekitar sepersepuluh biaya taker,
  dan penulisnya menyebut ini **bukan strategi yang berdiri sendiri**.
- Kesimpulan untuk desain: delta dipakai sebagai **konfirmasi** di titik yang sudah punya alasan (zona support/
  resistance, breakout), bukan sebagai sinyal tunggal, dan di timeframe yang biayanya masih masuk akal (H1/H4).

### Data

Candle 1 jam spot Binance BTCUSDT dan ETHUSDT 2017–2026 dengan volume beli taker. **Delta** candle = volume beli
taker − volume jual taker; **rasio delta** = delta ÷ volume. Candle 4 jam = gabungan 4 candle 1 jam (00.00 UTC).
Data per level harga (footprint) tidak dipakai: ukurannya puluhan GB per bulan, jadi imbalance 300%, stacked
imbalance, unfinished auction, dan HVN tidak diuji.

### AFS-22D · Divergensi delta di zona (aturan mentor + pelengkap)

- Mentor: candle **merah** tetapi delta **positif** → bullish; candle **hijau** tetapi delta **negatif** di
  resistance → bearish.
- *(Pelengkap)* Harus terjadi di zona support (long) / resistance (short) = swing low/high terakhir ± 0,5 ATR (D-04),
  sama dengan setup pembalikan lain. Masuk di open candle berikutnya. SL di luar ujung candle sinyal ± sl_atr × ATR.
  TP RR 1:2.
- Dijalankan lewat pemilihan G-17 yang sama dengan setup lain (pasar kripto, BTC & ETH): timeframe H1 vs H4,
  lalu sl_atr ∈ {0,5; 1; 1,5}. Syarat lolos sama: lolos pemilihan, lalu untung bersih dengan ≥ 30 transaksi di uji
  akhir (29 Des 2024 – 28 Okt 2026).

### AFS-22F · Delta sebagai filter (rencana Q-51)

- Empat setup tren/breakout kripto yang paling mendekati di laporan sebelumnya (AFS-16T, AFS-18, AFS-20B, HKI-01-H4),
  dengan parameter yang sudah terkunci dari pemilihan sebelumnya.
- Filter: long hanya kalau rasio delta candle sinyal > 0; short hanya kalau < 0.
- **Lolos** kalau, di uji akhir, versi dengan filter untung bersih dengan ≥ 30 transaksi **dan** lebih baik dari versi
  tanpa filter. Hasil di data penyusunan & pemilihan dilaporkan juga.

## B. Token baru / TGE (LIVE-02, analis live Akademi Crypto)

### Aturan mentor

1. Jangan beli di pre-market; tunggu listing spot.
2. **Lantai** = valuasi investor terakhir ÷ jumlah token maksimum.
3. Masuk **30%** di harga listing.
4. Setelah listing harga biasanya turun 50–66% lalu membentuk base; masuk **70%** di base dekat lantai.
5. **Cut loss** di bawah lantai (contoh mentor: lantai $1,5 → cut $1,25, yaitu 16,7% di bawah lantai).
6. Target dari perkiraan FDV dan pendapatan (contoh mentor: $5–10 untuk lantai $1,5).

### Pelengkap (karena tidak dibakukan mentor)

- Harga listing = close hari pertama di Binance spot (open menit pertama tidak realistis untuk diikuti).
- **Base**: close ≤ 50% harga listing, close ≤ 1,3 × lantai, dan harga terendah sejak listing sudah berumur ≥ 14 hari
  (harga berhenti mencetak low baru selama 2 minggu). Masuk 70% di open hari berikutnya.
- Cut loss: close < 0,833 × lantai (rasio contoh mentor) → semua posisi dijual di open berikutnya.
- Target: close ≥ 3,33 × lantai (batas bawah contoh mentor, $5 ÷ $1,5) → semua dijual. Batas waktu 730 hari; setelah
  itu dijual di harga pasar. Uang yang belum terpakai tidak berbunga. Biaya 0,2% per transaksi.

### Sampel

- Token yang **pertama kali diperdagangkan** di Binance spot antara 1 Januari 2023 dan 30 Juni 2025 (supaya ada ≥ 1
  tahun data sesudah listing), dari proyek yang punya **valuasi putaran pendanaan terakhir sebelum TGE yang
  diberitakan publik**. Valuasi dan jumlah token maksimum dicatat beserta sumbernya. Token tanpa valuasi yang bisa
  diverifikasi tidak dipakai (dicatat jumlahnya).
- Pembanding: beli 100% di close hari pertama dan tahan 365 hari; dan BTC di tanggal yang sama.

### Syarat lolos

Minimal 20 token; rata-rata **dan** median hasil per token positif; dan rata-rata lebih baik dari pembanding beli di
hari listing.
