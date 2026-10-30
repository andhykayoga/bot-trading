# Laporan: saham IPO dan saham backdoor

Aturan dikunci lebih dulu di `reports/RENCANA_IPO_BACKDOOR.md` (di-commit sebelum harga diunduh).

## A. Saham IPO

**Hasil singkat:** dapat jatah lalu jual di hari pertama **lolos** syarat (rata-rata +16,2%, median +20,5%, 79% IPO untung). Membeli di pasar setelah listing lalu menahan setahun **tidak lolos** (median -32,0%; hanya 26% yang mengalahkan IHSG). Persis seperti kata Ko Andri: IPO hanya untuk trading cepat, bukan untuk ditahan.

Data: 202 IPO e-IPO yang listing 1 Januari 2022 – 29 Oktober 2025 (lengkap, termasuk yang ambruk), harga setelah listing dari Yahoo Finance. Biaya beli 0,15% dan jual 0,25% sudah dihitung.

### Dapat jatah di harga IPO, lalu cepat dijual

| Kelompok | Jual | IPO | Rata-rata | Median | Untung | Median 2022–23 / 2024–25 | Lolos |
|---|---|---|---|---|---|---|---|
| Semua IPO | jual hari ke-1 | 201 | +16,2% | +20,5% | 79% | +12,5% / +24,4% | ✓ |
| Semua IPO | jual hari ke-5 | 201 | +38,4% | +15,1% | 69% | +12,9% / +25,2% | ✓ |
| F1 Papan Utama | jual hari ke-1 | 45 | +15,9% | +23,0% | 82% | +14,6% / +24,3% | ✓ |
| F1 Papan Utama | jual hari ke-5 | 45 | +55,7% | +25,6% | 78% | +20,4% / +40,4% | ✓ |
| F2 Dana ≥ Rp500 miliar | jual hari ke-1 | 26 | +15,2% | +18,0% | 85% | +11,7% / +21,8% | ✓ |
| F2 Dana ≥ Rp500 miliar | jual hari ke-5 | 26 | +55,1% | +20,5% | 88% | +14,1% / +39,1% | ✓ |
| F3 Harga IPO ≥ Rp200 | jual hari ke-1 | 65 | +15,1% | +19,4% | 85% | +10,4% / +24,3% | ✓ |
| F3 Harga IPO ≥ Rp200 | jual hari ke-5 | 65 | +37,2% | +19,6% | 74% | +12,8% / +27,3% | ✓ |

### Beli di pasar setelah listing, tahan setahun (250 hari bursa)

Dibeli di penutupan hari pertama yang tidak terkunci ARA (rata-rata hari ke-2,2). "Vs IHSG" = hasil saham dikurangi kenaikan IHSG di tanggal yang sama.

| Kelompok | IPO | Hasil median | Median vs IHSG | Rata-rata vs IHSG | Kalahkan IHSG | Median vs IHSG 2022–23 / 2024–25 | Lolos |
|---|---|---|---|---|---|---|---|
| Semua IPO | 202 | -32,0% | -38,4% | -8,2% | 26% | -42,4% / -31,1% | ✗ |
| F1 Papan Utama | 45 | -24,2% | -23,6% | +5,2% | 27% | -17,7% / -41,3% | ✗ |
| F2 Dana ≥ Rp500 miliar | 26 | -11,9% | -5,5% | +21,7% | 46% | +7,4% / -21,6% | ✗ |
| F3 Harga IPO ≥ Rp200 | 65 | -21,6% | -22,9% | +10,2% | 31% | -15,4% / -46,3% | ✗ |

Ditahan lebih pendek juga kalah: 20 hari bursa median -8,3% (36% mengalahkan IHSG), 60 hari bursa median -15,5% (36%).

### Kenapa rata-rata dan median sangat berbeda

- Dari harga IPO, setahun kemudian: median -16,6%, rata-rata +45,6%. 58% IPO sudah di bawah harga IPO, dan 20% turun lebih dari separuh.
- Rata-rata terangkat oleh segelintir saham: CHIP (+859%), CUAN (+631%), AMMN (+561%), DATA (+296%), AREA (+291%). Sebanyak 20 dari 202 IPO naik lebih dari 2 kali lipat dalam setahun setelah dibeli, tetapi 72 turun lebih dari separuh. Mirip membeli lotre: yang menang besar ada, tetapi kebanyakan kalah, dan tidak ada ciri sebelum listing (papan, besar dana, harga IPO) yang bisa memilih pemenangnya dengan andal.

### Masalah jatah (yang membuat hasil hari pertama terlihat lebih bagus dari kenyataan)

- 104 dari 202 IPO (51%) ARA di hari pertama, rata-rata +29,1%. Justru IPO seperti ini yang kelebihan permintaan puluhan sampai ratusan kali, sehingga pemesan ritel hanya dapat beberapa lot (misalnya pesan 100 lot, dapat 0–1 lot).
- 98 IPO lainnya rata-rata hanya +2,5% (median +2,2%; 56% untung, terburuk -35%). IPO yang sepi inilah yang biasanya memberi jatah penuh.
- Ilustrasi: kalau jatah penuh di IPO sepi tetapi hanya 5% dari pesanan di IPO yang ARA, rata-rata hasil per rupiah yang benar-benar dibelikan turun dari +16,2% menjadi +3,8% (dengan jatah 1%: +2,7%). Dana juga terkunci beberapa hari selama masa penawaran.

### Pemeriksaan data

- Daftar IPO cocok dengan jumlah IPO resmi BEI per tahun (2022: 59, 2023: 79, 2024: 41).
- Cek silang: per 22 Desember 2023, 51 dari 79 IPO 2023 di bawah harga IPO menurut data ini, sama persis dengan Bisnis.com ("51 saham baru membukukan kinerja negatif"). Hasil setahun dari harga IPO juga mirip penelitian Economina (Mei 2026, 190 IPO 2022–2025: rata-rata +44%, median −22,5%).
- Kolom "Return D1" di dataset salah untuk saham yang kemudian split (misalnya CUAN); yang dipakai harga Yahoo yang sudah dicocokkan dengan split. KRYA tidak punya harga hari listing di Yahoo, jadi tidak ikut A1/A5.
- IPO di periode utama yang disuspensi lebih dari 6 bulan pada akhir masa tahan setahun (dihitung 0): 0.
- Tambahan 2021 (31 IPO, tidak menentukan): jual hari pertama median +20,5%; beli setelah listing dan tahan setahun median -28,9%, hasilnya searah.

## B. Saham backdoor (ganti pengendali)

**Hasil singkat: TIDAK LOLOS.** Dari 48 peristiwa ganti pengendali Agustus 2023 – Oktober 2025 (dari arsip pengumuman resmi BEI), membeli sehari setelah pengumuman lalu menahan setahun menghasilkan median -3,9%; 48% mengalahkan IHSG. Kelompok pengendali kuat (konglomerat, perusahaan besar, bank besar): median -1,5%, 42% mengalahkan IHSG.

| Kelompok | Peristiwa | Hasil median | Median vs IHSG | Rata-rata vs IHSG | Kalahkan IHSG | Median vs IHSG Agu 2023–Sep 2024 / Okt 2024–Okt 2025 | Lolos |
|---|---|---|---|---|---|---|---|
| Semua peristiwa | 48 | -3,9% | -4,3% | +129,8% | 48% | +0,0% / -8,3% | ✗ |
| Pengendali kuat | 12 | -1,5% | -8,8% | +35,5% | 42% | -23,4% / +1,2% | ✗ |
| Pengendali lain | 36 | -4,8% | +5,6% | +161,2% | 50% | +50,6% / -11,8% | ✗ |

- Naik paling tinggi dalam setahun: MINA (+1844%), KARW (+1187%), FUTR (+759%), IRSX (+533%), CNKO (+527%). 13 peristiwa naik lebih dari 2 kali lipat, 7 turun lebih dari separuh.
- Ditahan dua tahun (hanya peristiwa yang sudah genap dua tahun, 18): median +71,1%, 72% mengalahkan IHSG.
- **Kenyataannya lebih sulit lagi:** 19 dari 48 saham langsung ARA setelah berita, jadi tidak bisa dibeli di penutupan hari pertama. Kalau baru bisa membeli setelah ARA-nya berhenti: median -8,7%, 44% mengalahkan IHSG.
- Tanpa data harga (sudah dihapus dari Yahoo atau tidak pernah bertransaksi lagi): 0 peristiwa; disuspensi lebih dari 6 bulan di akhir masa tahan (dihitung 0): 1 (PTMR, disuspensi sehari setelah dibeli). Belum genap setahun (dihitung sampai data terakhir): 2 (TGUK baru bisa dibeli setelah suspensinya dibuka Agustus 2026, PADA).
- Tidak dihitung karena berita pertamanya sebelum Agustus 2023: SMMT, VOKS, MFIN (Juli 2023), LPGI (2022), INCO. Juga tidak dihitung: perpindahan di dalam grup atau keluarga (GEMS, INTP, CITY, INKP, BTON, WIRG), pengendali lama yang menambah saham (BACA, SULI, SMMF), merger (EXCL), restrukturisasi BUMN (APIA, KRAS), dan penjualan tanpa pengendali baru yang jelas (AKKU, GDST).
- Contoh lama yang terkenal (hanya ilustrasi, tidak ikut dihitung): ARTO setelah masuknya Jerry Ng dan Patrick Walujo (Bank Jago): setahun +2181%, dua tahun +13845%; BBHI setelah masuknya CT Corp (Allo Bank): setahun +9098%, dua tahun +5119%; PANI setelah masuknya Agung Sedayu (PIK 2): setahun +2337%, dua tahun +12448%. Kasus seperti ini nyata, tetapi dipilih setelah tahu hasilnya.
- Daftar lengkap, pengendali baru, dan sumbernya: `bot/research/backdoor_peristiwa.csv`; hasil per peristiwa: `reports/hasil_ipo_backdoor/backdoor_per_peristiwa.csv`.

### Artinya

- Membeli setiap saham yang ganti pengendali **seperti melempar koin**: separuh menang, separuh kalah, dan medianya sedikit di bawah IHSG. Rata-ratanya terlihat besar hanya karena segelintir saham gocapan yang naik puluhan kali lipat (MINA, KARW, FUTR, IRSX, CNKO), yang tidak bisa dikenali lebih dulu.
- **"Pilih orangnya" (pengendali kuat) tidak membantu** di periode ini: dari 12 peristiwa, hanya 5 yang mengalahkan IHSG. Pemenang besar justru dari pembeli yang tidak dikenal, yang juga paling sering ambruk.
- Ditahan dua tahun hasilnya lebih baik, tetapi baru 18 peristiwa (semuanya Agustus 2023 – Oktober 2024), terlalu sedikit untuk dipercaya, dan tidak termasuk syarat lolos.
- Batasan: hanya 26 bulan dan 48 peristiwa (arsip BEI yang bisa dicari baru mulai Agustus 2023), dan 2026 adalah tahun berat bagi IHSG.

## Cara mengulang

```bash
python -m bot.data.download ipo backdoor
python scripts/run_ipo_backdoor.py
```
