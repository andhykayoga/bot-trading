# Skor semua cara yang sudah diuji (kripto dan saham)

Ditulis 30 Oktober 2026 atas permintaan: syarat "lolos/tidak lolos" diganti **skor 0–100** supaya tidak terlalu
ketat. Penting: skor ini dibuat **setelah** hasil uji diketahui, jadi ini ringkasan, bukan uji baru. Angka di
bawahnya tidak berubah; yang berubah hanya cara membacanya. Forex tidak dimasukkan (sudah Anda skip; semua versi
forex di bawah 50).

## Cara menghitung

Empat pertanyaan, masing-masing **25** (ya), **12** (sebagian), atau **0** (tidak):

1. **Lebih untung dari pembanding setelah biaya?** Ya: ≥ 2 poin per tahun di atas pembanding (atau median ≥ +2% per
   peristiwa). Sebagian: selisih −2 sampai +2. Tidak: lebih rendah dari −2.
2. **Tetap bagus di data baru?** Ya: lebih baik dari pembanding di periode terakhir yang tidak dipakai menyusun aturan,
   atau menang di ≥ 60% periode/peristiwa. Sebagian: 40–59%, atau untung tetapi di bawah pembanding. Tidak: selain itu.
3. **Risikonya tidak lebih buruk?** Ya: turun terdalam ≥ 10 poin lebih ringan dari pembanding (untuk peristiwa:
   ≤ 10% peristiwa rugi lebih dari separuh). Sebagian: dalam ±10 poin (10–25%). Tidak: lebih buruk.
4. **Buktinya cukup?** Ya: aturan dikunci sebelum diuji **dan** ≥ 30 transaksi/peristiwa atau ≥ 8 tahun data.
   Sebagian: salah satunya. Tidak: keduanya tidak.

**Arti skor:** 75–100 = boleh dipakai dengan porsi kecil · 50–74 = hanya uang belajar atau diamati · di bawah 50 =
jangan. Kalau pertanyaan 4 bernilai 0, paling tinggi "diamati", berapa pun skornya.

## Kripto

Pembanding: beli-dan-tahan BTC + ETH, +20,3% per tahun, turun terdalam −81%, periode terakhir (Des 2024 – Okt 2026)
−18,5%. Sumber: `reports/LAPORAN_MODUL_BARU.md`, `reports/LAPORAN_RENCANA_CADANGAN.md`,
`reports/LAPORAN_ORDERFLOW_TGE.md`.

| Cara | 1 Untung | 2 Data baru | 3 Risiko | 4 Bukti | Skor | Arti |
|---|---|---|---|---|---|---|
| **B6 trailing stop 10% BTC+ETH (sinyal bot sekarang)** | 25 (+29,5%/thn) | 25 (+27,2%) | 25 (−42%) | 25 (±25 sinyal/thn) | **100** | boleh, porsi kecil |
| B6 trailing stop 5% BTC+ETH | 25 (+33,8%) | 25 (+11,7%) | 25 (−38%) | 25 | **100** | boleh, porsi kecil |
| A1 pegang hanya di atas rata-rata 200 hari | 25 (+28,5%) | 25 (−0,7%) | 25 (−61%) | 25 | **100** | boleh, porsi kecil |
| B1 70% BTC + 30% stablecoin | 25 (+25,1%) | 25 (−6,0%) | 25 (−61%) | 25 | **100** | boleh, porsi kecil |
| B3 cicil 5× pakai RSI mingguan (Kalimasada) | 12 (+18,4%) | 25 (+5,7%) | 25 (−42%) | 25 | **87** | boleh, porsi kecil |
| Momentum riset (TSMOM) BTC+ETH, beli saja | 0 (+7,0%) | 25 (−7,1%) | 25 (−15%) | 25 | **75** | boleh, porsi kecil |
| B5 siklus halving BTC | 25 (+42,9%) | 25 (+19,0%) | 25 (−63%) | 0 (2 siklus) | 75 | **diamati saja** |
| B1 70/15/15 dengan altcoin dan meme | 25 (+45,3%) | 0 (−25,5%) | 12 (−80%) | 12 (data meme bias) | **49** | jangan |
| Setup mentor H4 (AFS-16T, AFS-18, AFS-20B, HKI-01) | 12 | 0 (semua rugi) | 12 | 12 | **36** | jangan |
| Token baru LIVE-02 (24 token) | 12 (median −1,9%) | 0 | 12 | 12 (24 token) | **36** | jangan |
| Order flow AFS-22 | 0 | 0 | 0 (rugi 83–99%) | 12 | **12** | jangan |

## Saham

Pembanding: 45 saham besar bobot sama (Ko Andri) atau IHSG (IPO, backdoor). Sumber:
`reports/LAPORAN_SAHAM_KO_ANDRI.md`, `reports/LAPORAN_IPO_BACKDOOR.md`.

| Cara | 1 Untung | 2 Data baru | 3 Risiko | 4 Bukti | Skor | Arti |
|---|---|---|---|---|---|---|
| **IPO: dapat jatah, jual di hari pertama** | 25 (median +20,5%; ±+4% kalau jatah kecil) | 25 (kedua kelompok tahun untung) | 25 (tidak ada yang rugi > separuh) | 25 (202 IPO) | **100** | boleh, porsi kecil |
| Checklist Ko Andri, 5 syarat | 12 (+1,6% vs +1,3%) | 12 (menang 4 dari 8 tahun) | 12 (−55% vs −46%) | 12 (8 pemilihan) | **48** | jangan |
| Checklist Ko Andri, cukup 4 dari 5 syarat | 12 (+0,4%) | 0 (menang 3 dari 8) | 12 (−45%) | 12 | **36** | jangan |
| Backdoor, pengendali kuat | 0 (median −8,8% vs IHSG) | 12 (42% menang) | 25 | 12 (12 peristiwa) | **49** | jangan |
| Backdoor, semua ganti pengendali | 0 (−4,3%) | 12 (48% menang) | 12 (15% rugi > separuh) | 25 (48 peristiwa) | **49** | jangan |
| IPO: beli setelah listing, tahan setahun | 0 (median −38%) | 0 (26% menang) | 0 (36% rugi > separuh) | 25 (202 IPO) | **25** | jangan |

## Kesimpulan

- Dengan penilaian yang lebih longgar pun, yang layak tetap **aturan BTC/ETH yang keluar saat pasar turun** dan **IPO
  yang dijual di hari pertama**. Altcoin dan meme, memilih saham dengan checklist, dan backdoor tetap di bawah 50.
  Jadi mengganti skor **tidak menambah koin atau saham baru** ke daftar layak; skor hanya menunjukkan seberapa jauh
  masing-masing dari layak.
- B6 10% dan 5% sama-sama 100. Sinyal bot tetap memakai 10% seperti yang sudah dipilih; aturan tidak diganti karena
  skor yang dibuat belakangan.
- Nilai 100 artinya lebih baik dari beli-dan-tahan kripto di data lama, **bukan** aman: versi terbaik pun pernah turun
  38–42%.
