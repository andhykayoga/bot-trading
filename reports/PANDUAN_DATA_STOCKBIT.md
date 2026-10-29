# Panduan mengambil data saham untuk uji Ko Andri & Ko Hengki

Tujuannya: menguji **valuasi Ko Andri** (PBV, PER, ROE, DER, dividen) dan, kalau datanya memungkinkan,
**bandarmologi Ko Hengki**, di saham BEI dengan cara yang sama seperti uji lain — aturan dikunci dulu, lalu diuji
sekali.

## Daftar saham (sudah ditetapkan, jangan diganti)

45 konstituen **LQ45 periode Agustus 2018 – Januari 2019**. Daftar ini sengaja diambil dari masa lalu, termasuk saham
yang kemudian ambruk atau disuspensi (SRIL, WSKT, WIKA, PTPP, LPKR, dll.). Kalau hanya memakai saham yang bagus
sekarang, hasil uji pasti terlihat terlalu bagus.

ADHI, ADRO, AKRA, ANTM, ASII, BBCA, BBNI, BBRI, BBTN, BJBR, BKSL, BMRI, BRPT, BSDE, ELSA, EXCL, GGRM, HMSP, ICBP, INCO,
INDF, INDY, INKP, INTP, ITMG, JSMR, KLBF, LPKR, LPPF, MEDC, MNCN, PGAS, PTBA, PTPP, SCMA, SMGR, SRIL, SSMS, TLKM, TPIA,
UNTR, UNVR, WIKA, WSBP, WSKT

## Paket 1 — data keuangan tahunan dari Stockbit (untuk valuasi Ko Andri)

Paling mudah di **Stockbit versi web di komputer** (stockbit.com), bukan di HP. Fitur Financials 10 tahun mungkin
butuh Stockbit Pro.

Untuk **setiap** saham di daftar:

1. Buka halaman saham (misalnya BBCA) → tab **Financials**.
2. Pilih tampilan **Annual / Tahunan** (bukan kuartal), rentang sejauh mungkin (idealnya 2014–2025).
3. Ambil tiga tabel: **Income Statement**, **Balance Sheet**, **Cash Flow**.
   - Cek dulu apakah ada tombol **Export / Download / ikon unduh**. Kalau ada, pakai itu.
   - Kalau tidak ada: blok seluruh tabel (termasuk baris judul tahun) → salin (Ctrl+C) → tempel ke Google Sheets
     atau Excel → simpan sebagai CSV.
   - **Salin semua baris apa adanya**, jangan dipilih-pilih. Yang paling saya butuhkan: laba bersih yang
     diatribusikan ke pemilik entitas induk, EPS, total liabilitas, total ekuitas, jumlah saham beredar, dan
     dividen yang dibayar — tapi namanya bisa berbeda, jadi salin semuanya.
4. Simpan dengan nama: `KODE_income.csv`, `KODE_balance.csv`, `KODE_cashflow.csv` (contoh `BBCA_income.csv`).
5. Satu file tambahan untuk semua saham: `sektor.csv` berisi dua kolom `kode,sektor` (sektor tertulis di halaman
   profil/Keystats tiap saham). Ko Andri membandingkan valuasi **dengan sektor sejenis**, jadi ini wajib.

Kalau 45 saham terlalu banyak sekaligus, kirim bertahap. Saya mulai menghitung setelah semuanya lengkap.

## Paket 2 — harga harian, dividen, dan split (2014–2026)

Stockbit tidak menyediakan unduhan harga historis, jadi pakai salah satu cara ini:

- **Cara A (paling lengkap, perlu Python di komputer Anda):** ambil file `scripts/ambil_data_idx.py` dari repo,
  lalu jalankan:

  ```bash
  pip install yfinance pandas
  ```

  ```bash
  python ambil_data_idx.py
  ```

  Hasilnya `data_idx.zip` (harga, dividen, split, dan IHSG untuk 45 saham).
- **Cara B (tanpa Python):** Google Sheets, satu sheet per saham, isi sel A1 dengan
  `=GOOGLEFINANCE("IDX:BBCA"; "all"; DATE(2014;1;1); TODAY(); "DAILY")` (ganti kodenya; kalau `IDX:` tidak jalan,
  coba tanpa awalan). Lalu File → Download → CSV, beri nama `KODE.csv`. Cara ini tidak memuat dividen, jadi untuk
  dividen salin riwayatnya dari Stockbit (tab Corporate Action / Keystats → Dividen) ke `KODE_dividen.csv`.

## Paket 3 — bandarmologi Ko Hengki (broker summary harian)

Jujur saja: ini bagian tersulit.

- Uji yang jujur butuh **broker summary per saham per hari** selama bertahun-tahun (siapa beli/jual, berapa lot,
  harga rata-rata). Untuk 45 saham × ±2 tahun, itu ±22.000 tabel harian.
- Saya tidak menemukan fitur ekspor broker summary di Stockbit. Menyalin satu per satu tidak realistis, dan sampel
  kecil (beberapa hari/saham) tidak cukup untuk membedakan keahlian dari kebetulan.
- Pilihan yang realistis:
  1. **Alat sumber terbuka** yang mengambil broker summary dari data publik broker dan menyimpannya ke CSV (contoh:
     `idx-cli`, `fzn0x/idx` di GitHub). Saya bisa menyiapkan skrip yang menjalankannya untuk daftar saham di atas,
     di komputer Anda. Baca dulu syarat penggunaan sumber datanya.
  2. Kalau Anda punya langganan data lain yang bisa mengekspor broker summary harian (misalnya terminal broker),
     kirim contoh satu file dulu supaya saya cek formatnya.
  3. Kalau tidak memungkinkan, bandarmologi tetap dicatat "tidak bisa diuji" — lebih baik daripada diuji dengan data
     yang tidak cukup.

Sebelum mengambil Paket 3, kirim dulu **satu contoh** (satu saham, satu hari) supaya saya pastikan formatnya terbaca.

## Cara mengirim file

- Lampirkan file di chat ini (dijadikan satu `.zip`), **atau**
- unggah ke repo GitHub di branch `claude/confident-newton-sa3u9i`, folder `data_stockbit/` (GitHub → Add file →
  Upload files). Pastikan repo **privat**, karena data Stockbit tidak boleh disebarkan ulang.

## Yang akan saya uji setelah data masuk (dikunci dulu sebelum hasil dihitung)

- **Valuasi Ko Andri:** tiap akhir April (setelah laporan tahunan terbit, supaya tidak memakai data yang belum
  ada), pilih saham dari daftar di atas dengan PBV < 1 dan PER rendah dibanding sektornya, ROE > 5%, DER lebih kecil
  dari median sektor, dan membagi dividen. Bandingkan dengan membeli semua 45 saham (bobot sama) dan dengan IHSG,
  setelah biaya transaksi saham (beli ±0,15%, jual ±0,25%). Detailnya ditulis di pra-registrasi sebelum dihitung.
- **Bandarmologi Ko Hengki** (kalau datanya ada): akumulasi broker besar vs ritel (XL, XC, YP, PD, dll.) sebelum
  kenaikan harga, dibanding saham yang sama tanpa sinyal.
