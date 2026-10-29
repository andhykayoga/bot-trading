# Pra-registrasi: uji forex "cepat" dan strategi forex berbasis riset

Ditulis 29 Oktober 2026, **sebelum satu pun hasil dihitung**. Dokumen ini di-commit lebih dulu supaya aturan
tidak bisa diubah setelah melihat hasil (prinsip Anda sendiri: *"jangan mengubah-ubah sampai hasilnya terlihat
bagus"*). Hasilnya akan ditulis di `reports/LAPORAN_FOREX_CEPAT.md`, apa pun hasilnya.

## Pertanyaan

Bisakah bot forex dibuat untung dengan cara apa pun: mengotak-atik teknikal, jual-beli cepat (scalping), atau
pola yang ditemukan riset? Setup mentor sudah diuji dan gagal (laporan sebelumnya), jadi di sini diuji tiga hal
lain:

- **Bagian A** — seberapa besar keunggulan yang dibutuhkan supaya jual-beli cepat bisa untung setelah biaya.
- **Bagian B** — tiga pola forex jangka sangat pendek yang **sudah diterbitkan di jurnal**, diuji apa adanya.
- **Bagian C** — demonstrasi apa yang terjadi kalau teknikal diotak-atik sampai backtest terlihat bagus.

## Data

- Candle 5 menit OANDA (harga tengah), 7 pair mayor: EURUSD, GBPUSD, USDJPY, serta **AUDUSD, USDCAD, USDCHF,
  NZDUSD yang belum pernah dipakai** di uji mana pun.
- Periode uji: **1 Januari 2014 sampai data terakhir**. Sub-periode: 2014–2017, 2018–2021, 2022–2026.
- Tidak ada data uji yang dipakai untuk menyusun aturan; aturan diambil dari makalah.

## Biaya (dua tingkat)

Biaya pulang-pergi per transaksi 1 lot, dalam pip:

| Pair | ECN (spread mentah rata-rata + komisi USD 7/lot) | Standar (spread ritel tanpa komisi) |
|---|---|---|
| EURUSD | 0,9 | 1,4 |
| GBPUSD | 1,2 | 1,8 |
| USDJPY | 1,0 | 1,4 |
| AUDUSD | 1,0 | 1,6 |
| USDCAD | 1,2 | 2,0 |
| USDCHF | 1,2 | 1,8 |
| NZDUSD | 1,3 | 2,0 |

- **ECN adalah ukuran utama** (akun termurah yang realistis untuk bot). Hasil di biaya standar dilaporkan juga.
- Setiap perubahan posisi 1 unit dikenai setengah biaya pulang-pergi (masuk atau keluar).
- Semua posisi wajib tutup antara 16.55–17.05 New York (rollover, spread melebar), jadi tidak ada swap.
- Slippage tidak dimodelkan (hasil sebenarnya bisa lebih buruk).

## Bagian A — hitungan impas jual-beli cepat (bukan strategi)

Untuk tiap pair dan rentang waktu 5 menit, 15 menit, 1 jam, 4 jam, 1 hari (jendela tidak tumpang tindih,
2014–2026): rata-rata dan median besar gerak harga (|close − close sebelumnya|) dalam pip, dibanding biaya.

**Tingkat benar minimum untuk impas** = 50% + biaya ÷ (2 × rata-rata gerak), dengan asumsi untung saat benar =
rugi saat salah = rata-rata gerak. Gerak per 1 detik diperkirakan dari gerak 5 menit dengan aturan akar waktu
(÷ √300), diberi label "perkiraan". Tidak ada lolos/gagal; ini hitungan biaya.

## Bagian B — tiga strategi dari riset (satu varian masing-masing, tanpa penyetelan)

Posisi berlaku untuk candle 5 menit yang **waktu bukanya** berada di dalam jendela. Ukuran 1× nilai pair saat
aktif.

**S1 — Pola jam sesi** (Ranaldo 2009, *Journal of Banking & Finance*; Breedon & Ranaldo 2013, *Journal of Money,
Credit and Banking*): mata uang cenderung melemah saat jam kerja negaranya sendiri dan menguat saat jam kerja
negara lain.
- Jam kerja = Senin–Jumat waktu setempat, 08.00 ≤ jam < 17.00. Pusat: USD New York, EUR Frankfurt, GBP London,
  JPY Tokyo, AUD Sydney, CAD Toronto, CHF Zurich, NZD Wellington.
- Tiap candle: hanya pusat mata uang dasar yang buka → **jual** pair; hanya pusat mata uang kuotasi yang buka →
  **beli** pair; keduanya buka atau keduanya tutup → tidak pegang posisi.
- USDCAD tidak pernah aktif (New York dan Toronto berjam sama) dan dilaporkan sebagai "tidak berlaku".

**S2 — Dolar melemah di hari FOMC** (Mueller, Tahbaz-Salehi & Vedolin 2017, *Journal of Finance*): jual USD
terhadap semua mata uang lain dari 17.05 New York sehari sebelum pengumuman FOMC terjadwal sampai 16.55 New York
di hari pengumuman. Tanggal: 102 rapat terjadwal Januari 2014 – Oktober 2026 dari jadwal resmi Fed (dicek silang
dengan kalender ekonomi; rapat darurat Maret 2020 tidak ikut).

**S3 — Pola sekitar fixing London 16.00** (Krohn, Mueller & Whelan 2024, *Journal of Finance*): dolar cenderung
menguat menjelang fixing dan melemah sesudahnya. Tiap Senin–Jumat: **beli USD** 15.00–16.00 London, **jual USD**
16.00–17.00 London.

**Hasil per strategi:** return harian portofolio = rata-rata return 7 pair (pair yang tidak aktif = 0), lalu
diskalakan supaya naik-turunnya 10% per tahun (penskalaan tidak mengubah Sharpe maupun t-stat).

**Syarat "lolos"** (semua harus terpenuhi, di biaya ECN):
1. t-stat return harian ≥ 2,4 (setara 5% setelah koreksi Bonferroni untuk 3 strategi);
2. untung di ≥ 2 dari 3 sub-periode;
3. drawdown terburuk ≤ 20% pada skala 10% volatilitas;
4. untung di ≥ 2/3 pair yang aktif.

Kalau lolos di ECN tetapi rugi di biaya standar, kesimpulannya "hanya layak dengan akun ECN". Strategi yang lolos
berikutnya wajib dijalankan di akun demo/paper minimal 3 bulan sebelum uang sungguhan.

## Bagian C — demonstrasi "diotak-atik" (bukan kandidat strategi)

EURUSD candle 1 jam, posisi = arah (SMA cepat − SMA lambat) dari harga close, selalu di pasar, biaya standar.
Kombinasi: cepat ∈ {2, 3, …, 50}, lambat ∈ {10, 15, …, 300}, hanya cepat < lambat. "Data penyusunan" 2014–2019,
"data baru" 2020–2026. Dilaporkan: kombinasi terbaik di data penyusunan dan hasilnya di data baru, rata-rata 10
terbaik, porsi kombinasi yang untung di masing-masing periode, dan korelasi peringkat keduanya. Apa pun hasilnya,
kombinasi terbaik **tidak** menjadi kandidat, karena dipilih dari ribuan percobaan.

## Hitungan varian

Bagian B: 3 strategi, masing-masing 1 varian, 7 pair, 2 tingkat biaya (biaya hanya pelaporan). Bagian C:
semua kombinasi grid di atas, hanya sebagai ilustrasi. Tidak ada varian lain yang akan dicoba setelah hasil
terlihat.
