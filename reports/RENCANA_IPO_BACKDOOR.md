# Pra-registrasi: uji saham IPO dan saham backdoor (ganti pengendali)

Ditulis 30 Oktober 2026 dan di-commit **sebelum harga setelah listing dan setelah pergantian pengendali diunduh**.
Satu-satunya angka hasil yang sudah terlihat: ringkasan "Return D1" (kenaikan hari pertama) di data e-IPO, yang memang
sudah umum diberitakan. Hasilnya ditulis di `reports/LAPORAN_IPO_BACKDOOR.md`, apa pun hasilnya. Bagian yang tidak
dibakukan mentor ditandai *(pelengkap)*.

## Kata mentor

**IPO (Ko Andri, transkrip AndreHakim_saham_3 dan _4):** "hindari saham IPO", "jangan invest di saham IPO"; "kalau mau
masuk saham IPO boleh, tapi trading, buru-buru take profit". Alasannya: harga IPO dipasang setinggi-tingginya, rekam
jejak belum ada, dan IPO sering dipakai untuk menjebak ritel. Ko Andri mengaku rugi Rp500 juta kurang dari sehari di
IPO Bukalapak.

**Backdoor (Ko Andri, transkrip AndreHakim_saham_2):** "kalau ada perusahaan jelek tapi diambil sama orang yang jago …
pilih yang pertama, pilih orang dulu baru perusahaan". Contohnya membeli ARTO setelah keluar berita Jerry Ng dan
Patrick Walujo masuk, BBHI setelah dijual ke CT (Chairul Tanjung), PANI sebelum PIK 2 masuk. Ia sendiri menyebutnya
"pure tebak-tebakan, cuma karena yakin".

## A. Saham IPO

### Data

- **Daftar IPO dan harga IPO:** dataset Kaggle "e-IPO Indonesia Data" (Fahmi Rizal Kurnia, dari e-ipo.co.id), versi
  29 Oktober 2026, status *Closed*. Kolom yang dipakai: kode, harga final, jumlah saham ditawarkan, papan pencatatan,
  tanggal listing.
- **Periode utama:** listing 1 Januari 2022 – 29 Oktober 2025: **202 IPO** (2022: 59, 2023: 79, 2024: 41, 2025: 23).
  Jumlah per tahun 2022–2024 sama dengan jumlah IPO resmi BEI, jadi daftarnya lengkap, termasuk yang kemudian ambruk.
  Batas akhir dipilih supaya tiap IPO bisa ditahan setahun penuh sampai 29 Oktober 2026.
- **Tambahan (tidak menentukan lolos):** 31 IPO e-IPO tahun 2021 (belum semua IPO 2021 lewat e-IPO).
- **Harga harian setelah listing:** Yahoo Finance (`KODE.JK`), harga penutupan dan harga yang disesuaikan dengan
  dividen dan split. IHSG dari Yahoo (`^JKSE`, indeks harga, tanpa dividen).
- **Pemeriksaan:** harga penutupan hari pertama dari Yahoo dibanding "Return D1" dataset; selisih lebih dari 1 poin
  persen dicek ke berita. Papan pencatatan yang kosong (9 IPO Juli–September 2025) dilengkapi dari berita.
- IPO yang tidak ada di Yahoo dicari statusnya. Yang disuspensi lebih dari 6 bulan pada akhir masa tahan, atau
  dihapus dari bursa, dianggap bernilai **0**.

### Strategi *(pelengkap, mengikuti kata mentor)*

- **A1: dapat jatah IPO, jual di hari pertama** (versi "trading, buru-buru take profit"): beli di harga IPO, jual di
  harga penutupan hari pertama. **A5:** jual di penutupan hari ke-5.
- **B: beli di pasar setelah listing, tahan setahun** (yang bisa dilakukan siapa saja, berapa pun modalnya): beli di
  penutupan hari pertama yang **tidak terkunci ARA**, tahan 250 hari bursa, jual di penutupan. Dilaporkan juga tahan
  20 dan 60 hari bursa.
  - Terkunci ARA = penutupan sama dengan harga tertinggi hari itu **dan** kenaikan dari penutupan sebelumnya (hari
    pertama: dari harga IPO) ≥ batas ARA − 1,5 poin persen. Batas ARA: harga sebelumnya ≤ Rp200: 35%; Rp200–5.000: 25%;
    > Rp5.000: 20%; Papan Akselerasi: 10%.
- Biaya: beli 0,15%, jual 0,25%.
- **Hasil lebih** (B) = hasil saham (termasuk dividen, setelah biaya) dikurangi kenaikan IHSG di tanggal yang sama.

### Kelompok "IPO bagus" (diketahui sebelum listing)

- **F1:** Papan Utama.
- **F2:** dana IPO (saham ditawarkan × harga final) ≥ Rp500 miliar.
- **F3:** harga IPO ≥ Rp200 (Ko Andri: IPO "jarang yang mulainya 200 ke atas, karena naiknya cuma bisa 25%").

### Syarat lolos

- **A1 (dan A5) lolos** kalau di periode utama: rata-rata hasil > 0, median hasil > 0, ≥ 60% IPO untung, dan median
  > 0 di kedua kelompok tahun (2022–2023 dan 2024–2025).
  - Catatan penting yang tidak bisa diuji: jatah IPO ritel. IPO yang ramai (yang biasanya ARA) kelebihan permintaan
    puluhan sampai ratusan kali, sehingga jatahnya hanya beberapa lot; IPO yang sepi dapat penuh. Karena itu dilaporkan
    juga (tidak menentukan lolos) hasil terpisah untuk IPO yang ARA di hari pertama dan yang tidak, serta ilustrasi
    "dapat penuh di IPO sepi, dapat 5% di IPO ramai".
- **B lolos** kalau di periode utama: median hasil lebih > 0, rata-rata hasil lebih > 0, ≥ 50% IPO mengalahkan IHSG,
  dan median hasil lebih > 0 di kedua kelompok tahun.
- Syarat yang sama dipakai untuk F1, F2, F3 (masing-masing di A1 dan B). Karena ada 8 kombinasi, satu kombinasi yang
  lolos tipis belum cukup untuk dijadikan sinyal; harus konsisten di kedua kelompok tahun.

## B. Saham backdoor (ganti pengendali)

### Peristiwa

- **Definisi:** pihak baru, yang **bukan satu grup** dengan pengendali lama, menjadi pemegang saham pengendali emiten
  BEI (biasanya membeli ≥ 50% saham atau disebut "pengendali baru", dan wajib *tender offer*). Tidak termasuk:
  restrukturisasi di dalam satu grup, pengalihan antar-BUMN/holding pemerintah, dan merger yang pengendali akhirnya
  tetap sama.
- **Tanggal peristiwa:** tanggal pertama publik tahu **siapa** pengendali barunya (pengumuman perjanjian jual beli,
  keterbukaan informasi, atau berita pertama), karena di situ Ko Andri membeli ("udah ada keluar berita").
- **Periode:** peristiwa 1 Januari 2019 – 29 Oktober 2025.

### Cara mengumpulkan daftar *(pelengkap)*

- Pencarian per tahun di Kontan, Bisnis, CNBC Indonesia, IDX Channel, Investor.id, dan Kabar Bursa dengan kata kunci
  "ganti pengendali", "pengendali baru", "tender offer wajib", "penawaran tender wajib", dan "backdoor listing", plus
  artikel rangkuman tahunan. **Semua** peristiwa yang ditemukan dimasukkan, termasuk yang kemudian gagal. Sumber dan
  tanggal dicatat di `bot/research/backdoor_peristiwa.csv`.
- Daftar dibekukan dan di-commit **sebelum** harga sahamnya diunduh.
- Tiap peristiwa diberi label **pengendali kuat** kalau pembeli atau induk akhirnya: (a) perusahaan tercatat (BEI atau
  bursa lain) dengan nilai pasar ≥ Rp10 triliun saat itu; (b) dikendalikan orang/keluarga yang masuk daftar Forbes 50
  orang terkaya Indonesia (tahun mana pun 2019–2025); atau (c) bank/lembaga keuangan dengan aset ≥ Rp100 triliun.
  Label diberikan dari berita, sebelum harga dilihat. Ini versi terukur dari "pilih orang yang jago".

### Strategi dan syarat lolos

- Beli di penutupan hari bursa pertama **setelah** tanggal peristiwa (kalau sedang disuspensi: penutupan pertama
  setelah suspensi dibuka), tahan 250 hari bursa (dilaporkan juga 500 hari bila datanya ada), biaya dan aturan suspensi
  sama dengan uji IPO. Pembanding: IHSG di tanggal yang sama.
- **Lolos** kalau, untuk semua peristiwa **dan** untuk kelompok pengendali kuat: median hasil lebih > 0, rata-rata
  hasil lebih > 0, ≥ 50% mengalahkan IHSG, dan median hasil lebih > 0 di kedua kelompok tahun (2019–2021 dan
  2022–2025).
- Batasan yang sudah diketahui: daftar dari berita bisa melewatkan pengambilalihan perusahaan sangat kecil yang tidak
  diberitakan, dan saham yang sudah dihapus tidak ada di Yahoo. Jumlah yang hilang dilaporkan.

## Cara mengulang

```bash
python -m bot.data.download ipo
python scripts/run_ipo_backdoor.py
```
