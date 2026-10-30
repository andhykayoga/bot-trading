# Pra-registrasi: uji tipe EA XAUUSD yang viral

Ditulis 29 Oktober 2026, **sebelum hasil dihitung**, dan di-commit lebih dulu. Hasilnya akan ditulis di
`reports/LAPORAN_EA_XAUUSD.md`, apa pun hasilnya.

## Pertanyaan

Anda bilang EA (robot MetaTrader) XAUUSD yang viral itu bagus. Isi EA berbayar tidak bisa dilihat, tetapi
hampir semua EA emas yang dipasarkan masuk ke beberapa tipe yang sama. Di sini tiga tipe itu dibuat ulang dengan
pengaturan khas iklannya, lalu dijalankan di seluruh data emas 2010–2026, bukan hanya di periode yang dipilih
penjual.

## Data, akun, biaya

- XAUUSD candle 5 menit OANDA (harga tengah), 4 Januari 2010 – 29 Oktober 2026.
- Akun USD 1.000, leverage 1:500 (umum di broker yang dipakai EA), stop-out saat margin level ≤ 50%.
  1 lot = 100 oz. Lot minimum 0,01, dibulatkan ke 0,01 terdekat.
- Biaya: spread model yang sama dengan laporan sebelumnya (maks USD 0,30 atau 0,015% harga), swap harian
  (selisih suku bunga + biaya admin 2,5% per tahun; posisi beli emas membayar swap). Slippage tidak dimodelkan.
- Dalam satu candle, kejadian yang merugikan diproses dulu (untuk posisi beli: harga terendah dulu, baru
  tertinggi). Kalau kena stop-out, posisi ditutup di harga terburuk candle itu dan saldo tidak bisa minus.
- Kalau akun habis, dicatat sebagai "akun habis", lalu diisi lagi USD 1.000 dan EA jalan terus (untuk
  menghitung seberapa sering terjadi).

## Tipe yang diuji (satu pengaturan masing-masing, tanpa penyetelan)

**E1 — Grid martingale beli saja** (tipe paling umum: "averaging", "recovery"):
- Tidak ada posisi → beli lot dasar di candle berikutnya. Lot dasar = 0,01 per USD 1.000 ekuitas.
- Setiap harga turun 0,5% dari harga beli terakhir → beli lagi dengan lot × 1,5. Maksimal 10 posisi.
- Semua ditutup saat harga ≥ harga rata-rata tertimbang + 0,3%. Tanpa stop loss.

**E2 — Grid martingale dua arah** ("hedging grid"): keranjang beli seperti E1, ditambah keranjang jual yang
dicerminkan (jual lagi tiap harga naik 0,5%, tutup saat harga ≤ rata-rata − 0,3%). Kedua keranjang berjalan
bersamaan dengan satu ekuitas.

**E3 — Breakout sesi London** (tipe "gold scalper/breakout" tanpa martingale): rentang Asia = tertinggi/terendah
00.00–06.55 London. Pukul 07.00 London pasang buy stop di batas atas dan sell stop di batas bawah; yang pertama
tersentuh dipakai, satunya dibatalkan. Stop loss di sisi seberang rentang, take profit = 1× lebar rentang,
tutup paksa 20.00 London. Satu transaksi per hari, Senin–Jumat, risiko 1% ekuitas per transaksi.

**Patokan — beli dan tahan emas**: CFD 1× tanpa leverage (bayar swap), dan harga emas saja.

## Periode dan syarat

- Seluruh periode, tiga sub-periode (2010–2015, 2016–2020, 2021–2026), dan "periode viral" 2024 – 2026
  (emas naik dari ±USD 2.000 ke ±USD 4.000).
- Syarat "layak": tidak pernah habis, untung di ≥ 2 dari 3 sub-periode, hasil ≥ 2% per tahun, drawdown
  terburuk ≤ 20%. Sama dengan syarat laporan sebelumnya, ditambah "tidak pernah habis".

## Hitungan varian

3 tipe EA + 1 patokan, masing-masing satu pengaturan. Tidak ada pengaturan lain yang dicoba setelah hasil terlihat.
