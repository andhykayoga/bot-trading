# Pra-registrasi: uji valuasi Ko Andri di saham BEI

Ditulis 29 Oktober 2026, **sebelum data laporan keuangan diterima**, dan di-commit lebih dulu. Hasilnya ditulis di
`reports/LAPORAN_SAHAM_KO_ANDRI.md`, apa pun hasilnya. Bagian yang tidak dibakukan mentor ditandai *(pelengkap)*.

## Aturan mentor (transkrip AndreHakim_saham_3)

1. **PBV** di bawah 1; makin kecil makin baik; dibandingkan dengan sektor sejenis.
2. **PER** rendah ("cepat balik modal"), dibandingkan dengan sektor sejenis.
3. **ROE** di atas 5% sudah cukup, di atas 15% bagus.
4. **DER** (liabilitas ÷ ekuitas) makin kecil makin baik, dibandingkan dengan sektor sejenis.
5. Perusahaan **membagi dividen**; makin besar makin baik.

## Data

- **Saham:** 45 konstituen LQ45 periode Agustus 2018 – Januari 2019 (daftar di `reports/PANDUAN_DATA_STOCKBIT.md`),
  tidak diganti apa pun yang terjadi kemudian.
- **Laporan keuangan tahunan:** Stockbit (Income Statement + Key Ratio, Balance Sheet), dalam rupiah, dikirim pengguna.
- **Harga, dividen, split:** Yahoo Finance (`python -m bot.data.download idx`). SRIL dan WSKT tidak ada di Yahoo; harga
  dan tanggal suspensinya diambil dari pengumuman bursa/pemberitaan, dengan sumber dicatat.

## Definisi *(pelengkap)*

- Laba = laba bersih yang dapat diatribusikan ke pemilik entitas induk. Ekuitas induk = total ekuitas − kepentingan
  non-pengendali. Jumlah saham dari Key Ratio Stockbit, disesuaikan dengan stock split supaya cocok dengan harga Yahoo.
- PBV = harga ÷ (ekuitas induk ÷ jumlah saham). PER = harga ÷ (laba ÷ jumlah saham), hanya kalau laba positif.
  ROE = laba ÷ ekuitas induk. DER = total liabilitas ÷ total ekuitas. Dividen = dividen tunai yang dibayar (tanggal
  ex) dalam 12 bulan sebelum tanggal pemilihan.
- **Sektor** (klasifikasi IDX-IC, digabung supaya tiap kelompok berisi ≥ 3 saham):

  | Kelompok | Saham |
  |---|---|
  | Bank | BBCA, BBRI, BMRI, BBNI, BBTN, BJBR |
  | Konstruksi & properti | ADHI, PTPP, WIKA, WSKT, WSBP, BSDE, LPKR, BKSL |
  | Infrastruktur | TLKM, EXCL, JSMR |
  | Energi | ADRO, INDY, ITMG, PTBA, MEDC, PGAS, ELSA, AKRA |
  | Barang baku | ANTM, INCO, INTP, SMGR, INKP, BRPT, TPIA |
  | Konsumen primer & kesehatan | ICBP, INDF, UNVR, GGRM, HMSP, KLBF, SSMS |
  | Konsumen non-primer & industri | ASII, UNTR, LPPF, MNCN, SCMA, SRIL |

  Median sektor dihitung dari saham sekelompok yang datanya tersedia di tahun itu.

## Cara memilih *(pelengkap)*

- Pemilihan tiap **hari bursa terakhir bulan April** (laporan tahunan wajib terbit paling lambat akhir Maret), memakai
  laporan tahun buku sebelumnya. Saham yang laporannya belum ada atau sedang disuspensi tidak dipilih tahun itu.
- **Portofolio Ko Andri:** saham yang memenuhi **kelima** syarat sekaligus: PBV < 1; PER positif dan di bawah median
  PER sektornya; ROE > 5%; DER di bawah median DER sektornya; membagi dividen. Bobot sama, ditahan sampai pemilihan
  berikutnya. Kalau tidak ada satu pun yang lolos, uang disimpan dengan bunga deposito tetap 4% per tahun.
- Dividen yang diterima disimpan tunai (tanpa bunga) dan ikut diinvestasikan di pemilihan berikutnya.
- Biaya: beli 0,15%, jual 0,25% (termasuk pajak penjualan 0,1%), dihitung hanya untuk bagian yang berubah.
- Saham yang disuspensi saat dipegang: nilainya dibekukan di harga terakhir; kalau suspensi lebih dari 6 bulan atau
  berakhir pailit/delisting, nilainya dianggap **0** sejak tanggal suspensi.

## Periode

- **Utama:** April 2019 – 28 Oktober 2026 (8 pemilihan, April 2019 s.d. April 2026). Dimulai April 2019 karena daftar
  saham ditetapkan Juli 2018; memakai periode sebelumnya berarti memilih saham dengan pengetahuan masa depan.
- **Tambahan (tidak menentukan lolos):** April 2015 – April 2019, dengan catatan bias tadi.

## Pembanding dan syarat lolos

- Pembanding utama: **45 saham bobot sama**, dipilih ulang tiap April dengan aturan biaya, dividen, dan suspensi yang
  sama. Pembanding tambahan: IHSG (indeks harga, belum termasuk dividen) dan deposito 4%.
- **Lolos** kalau di periode utama, portofolio Ko Andri:
  1. hasil per tahun (termasuk dividen, setelah biaya) lebih tinggi dari 45 saham bobot sama;
  2. menang dari 45 saham bobot sama di sedikitnya 5 dari 8 periode tahunan (April–April; periode terakhir April –
     Oktober 2026); dan
  3. turun terdalam (drawdown) tidak lebih buruk dari 45 saham bobot sama ditambah 10 poin persen.
- Dilaporkan juga, tetapi tidak menentukan lolos: jumlah saham yang lolos tiap tahun, hasil per saham, dan versi
  "lolos minimal 4 dari 5 syarat".

## Pemeriksaan data

Angka dari screenshot dicek silang sebelum dipakai: EPS × jumlah saham ≈ laba bersih (selisih ≤ 2%), total liabilitas +
total ekuitas = total aset, dan PBV/PER hasil hitungan dibanding Key Ratio Stockbit pada harga akhir tahun. Saham yang
tidak lolos pemeriksaan diminta ulang, bukan ditebak.
