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

Daftar peristiwa sedang dikumpulkan.

## Cara mengulang

```bash
python -m bot.data.download ipo backdoor
python scripts/run_ipo_backdoor.py
```
