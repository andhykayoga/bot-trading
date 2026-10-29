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

Sektor tiap saham tidak perlu dikirim: saya kelompokkan sendiri memakai klasifikasi sektor resmi BEI (IDX-IC).

**Cara pengganti: screenshot.** Kalau menyalin tabel merepotkan, screenshot juga bisa saya baca. Cukup **2 screenshot
per saham** (Cash Flow tidak perlu):

1. **Income Statement**, Annual, mode layar penuh, sampai tabel **Key Ratio** di bawahnya ikut terlihat (Share
   Outstanding, EPS, PE, ROE).
2. **Balance Sheet**, Annual, mode layar penuh, sampai baris **Total Liabilitas**, **Kepentingan Non Pengendali**, dan
   **Total Ekuitas** terlihat.

Supaya angkanya terbaca tepat:

- Ketik kode saham di kotak *Symbol* sebelum screenshot (kodenya harus ikut terlihat), atau beri nama file
  `KODE_1.png` dan `KODE_2.png`.
- Semua kolom tahun (2008/2014–2025) harus masuk, jangan dipotong, dan jangan diperkecil sampai angkanya buram.
- Saya akan mencocokkan angka antarbaris (misalnya EPS × jumlah saham ≈ laba bersih). Kalau ada yang tidak cocok,
  saya minta ulang saham itu saja.

Kalau 45 saham terlalu banyak sekaligus, kirim bertahap (misalnya 5–10 saham per kiriman). Saya mulai menghitung
setelah semuanya lengkap.

## Paket 2 — harga harian, dividen, dan split (2014–2026): **tidak perlu dikirim**

Sudah saya ambil sendiri dari Yahoo Finance (`python -m bot.data.download idx`): 43 dari 45 saham plus IHSG, lengkap
dengan dividen dan stock split. Dua saham yang sudah dihapus Yahoo (SRIL dan WSKT, keduanya disuspensi lalu
bermasalah) akan saya lengkapi dari pengumuman suspensi/delisting, dan perlakuannya ditulis di pra-registrasi.

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

## Yang akan saya uji setelah data masuk

Aturan uji valuasi Ko Andri sudah dikunci sebelum data masuk, di
[`RENCANA_SAHAM_KO_ANDRI.md`](RENCANA_SAHAM_KO_ANDRI.md). Bandarmologi Ko Hengki menunggu contoh broker summary.
