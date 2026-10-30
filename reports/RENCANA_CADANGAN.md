# Rencana cadangan — pra-registrasi

Dokumen ini ditulis dan di-commit **sebelum** versi baru dijalankan di data uji yang belum pernah disentuh. Tujuannya supaya tidak ada penyesuaian setelah melihat hasil ("jangan mengubah-ubah sampai hasilnya terlihat bagus"). Hasilnya nanti ada di [`LAPORAN_RENCANA_CADANGAN.md`](LAPORAN_RENCANA_CADANGAN.md).

Latar belakang: di [backtest tahap 2](LAPORAN_BACKTEST_FOREX.md) tidak ada setup yang lolos di EURUSD/XAUUSD, dan data uji akhir EURUSD/XAUUSD (Jun 2023 – Okt 2026) sudah terpakai.

## Pemakaian data

| Data | Status | Dipakai untuk |
|---|---|---|
| EURUSD, XAUUSD 2010–2026 | **sudah terlihat** (termasuk uji akhir tahap 2) | Merancang versi perbaikan dan memeriksa kode. Tidak dipakai sebagai bukti. |
| **GBPUSD, USDJPY** 2010-01-04 – 2026-10-29 (5 menit, OANDA) | **belum pernah disentuh** | **Penilaian sekali** untuk versi perbaikan (tahap 1) dan patokan TSMOM forex (tahap 3). |
| **BTC, ETH** spot Binance 2017-09-01 – 2026-10-28 (5 menit) | **belum pernah disentuh** | Tahap 2: setup mentor saham–kripto di pasar asalnya, dengan prosedur G-17 (60/20/20, uji akhir sekali). Juga patokan TSMOM kripto. |

GBPUSD dan USDJPY bukan instrumen trading bot (G-09 tetap EURUSD, XAUUSD); keduanya hanya dipakai sebagai data uji yang bersih. Catatan: periode waktunya sama dengan data rancangan, jadi ini uji "pasar lain", bukan "waktu lain". GBPUSD bergerak cukup mirip EURUSD; USDJPY jauh lebih berbeda.

## Tahap 1 — perbaikan terbatas (4 versi, dikunci)

Pilihan perbaikan berdasarkan temuan tahap 2: (a) biaya per transaksi jauh lebih kecil di timeframe besar; (b) setup tren lebih dekat ke impas daripada setup pembalikan/scalping; (c) banyak setup untung di 2020–2023 tetapi rugi di 2010–2020, tanda bergantung kondisi pasar.

| Versi | Isi | Jenis perbaikan |
|---|---|---|
| **V1** | ICH-01 (Rafał) dipindah ke **D1**, bias W1; SL Kijun ± 1 ATR; TP target Hosoda terdekat RR ≥ 1:1,5 | timeframe lebih besar |
| **V2** | **Konsensus tren D1**: struktur D-02 + harga di luar Kumo + harga di sisi MA21 sama-sama searah; masuk saat pullback ke pita EMA 13/21 + pemicu (cara AFS-05) di D1; SL swing ± 1 ATR; TP 1:3 | gabungan beberapa setup |
| **V3** | AFS-05 (EMA 13/21) di **H4**, hanya searah **struktur D1** (D-02); TP 1:3 | filter kondisi pasar |
| **V4** | AFS-06 (stop hunt + BMS) di **H1**, hanya searah **struktur D1**; TP likuiditas terdekat RR ≥ 1:2 | timeframe lebih besar + filter |

- Semua angka lain = nilai awal rulebook. **Tidak ada pencarian parameter**; jumlah varian tahap 1 = **4**.
- Aturan global sama dengan tahap 2 (risiko 1%, maks 3 transaksi/hari, jendela berita, rem harian/mingguan, spread & swap).
- Spread pair uji: GBPUSD 1,8 pip, USDJPY 1,4 pip (akun standar ritel). Untung/rugi USDJPY dikonversi ke USD.
- Kalau setelah dijalankan ditemukan **kesalahan kode** (bukan perubahan aturan), perbaikannya dicatat dan jalan ulangnya dihitung sebagai varian tambahan.

**Aturan penilaian (ditetapkan sekarang):**

1. Keempat versi dijalankan sekali di data rancangan (EURUSD+XAUUSD) dan sekali di data uji (GBPUSD+USDJPY, digabung). Semua hasil dilaporkan, tidak ada yang disembunyikan.
2. **Lolos** = di data uji: untung bersih setelah biaya **dan** minimal 30 transaksi (definisi lolos rulebook G-17).
3. **Layak untuk bot otomatis** = lolos **dan** semua ini terpenuhi:
   - untung bersih juga di data rancangan;
   - di data uji, untung di minimal 2 dari 3 periode (2010–2020, 2020–2023, 2023–2026);
   - di data uji, hasil per tahun (CAGR) minimal **2%** (kira-kira bunga deposito/obligasi jangka pendek USD rata-rata periode ini);
   - di data uji, drawdown terburuk maksimal **20%**.
4. Karena 4 versi diuji, satu versi bisa lolos karena kebetulan; laporan akan menyebut ini.

## Tahap 2 — setup mentor saham–kripto di BTC & ETH

- Setup: 26 setup Alvesting, Kalimasada, dan Ko Hengki (AFS-01 – AFS-21 termasuk 13A/13B, 16P/16T, 20R/20B; KMS-02; HKI-01 D1 & H4), aturan sama dengan rulebook. Angka persen dipakai apa adanya di kripto (D-09): pantulan golden pocket 3/4/5%, Dow 3%, lebar range Wyckoff 20%.
- Data dibagi 60/20/20 menurut tanggal untuk pasar kripto (Q-50), pemilihan varian G-17, uji akhir sekali. Jumlah varian per setup dicatat otomatis.
- Biaya: komisi 0,1% per sisi + setengah spread 0,01% (biaya pulang-pergi 0,22%); tanpa swap untuk spot; posisi short di backtest dihitung seperti futures 1× tanpa funding (datanya tidak dipakai). Leverage maks 1× (G-16). Berita: hanya FOMC, CPI AS, NFP (G-13).
- **Lolos** = definisi G-17 (untung bersih di uji akhir dengan ≥ 30 transaksi). Laporan juga menunjukkan hasil versi long saja, karena akun kripto versi pertama hanya spot (G-16).
- Filter Astronacci tidak diuji ulang di tahap ini.

## Tahap 3 — patokan sistematis dari riset

- **Time-series momentum** (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017): tiap akhir bulan arah = tanda return 12 bulan; ukuran posisi berdasarkan volatilitas (target ±10%/tahun untuk portofolio); dipegang sebulan. Satu varian, parameter dari makalah, **tanpa penyetelan**.
- Dijalankan di: GBPUSD+USDJPY (data uji yang sama dengan tahap 1), BTC+ETH (seluruh periode dan periode uji akhir tahap 2; juga versi long saja), dan EURUSD+XAUUSD sebagai pembanding.
- Biaya sama: setengah spread per perubahan posisi, swap harian di forex.

## Kesimpulan yang akan ditulis

- Pilihan mana yang realistis untuk bot full otomatis, berdasarkan aturan "layak" di atas.
- Berapa hasil per tahun yang wajar, dari angka data uji (bukan data rancangan) dan dibandingkan dengan patokan riset.
- Kalau tidak ada yang layak: usulan versi semi-otomatis (bot memberi sinyal, Anda yang mengeksekusi), tanpa koneksi broker.
