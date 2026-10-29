# 09 · PERTANYAAN UNTUK ANDA

Bagian-bagian di bawah ini **tidak saya tebak**, karena mentor tidak menyebutnya, menyebutnya dengan kabur, atau para mentor berbeda pendapat. Jawaban Anda akan mengubah label 🟡 di rulebook menjadi 🟢.

> **Status:** Q-01 – Q-48 **sudah dijawab**. Jawabannya ada di [10-jawaban.md](10-jawaban.md) dan sudah diterapkan ke rulebook. Teks pertanyaannya dibiarkan seperti aslinya sebagai catatan. Yang **masih terbuka** hanya [Bagian 9 (Q-49 – Q-51)](#bagian-9--pertanyaan-lanjutan-kedua). Tidak ada setup lain yang menunggu bagian ini, kecuali AFS-22.

**Cara menjawab:** cukup tulis nomornya dan pilihan Anda, misalnya `Q-01: A, scalping 0,5%`. Kalau tidak ada pilihan yang cocok, tulis jawaban sendiri. Kalau belum yakin, tulis "uji dulu" — artinya angka itu akan dicari lewat backtest.

## Daftar isi

1. [Wajib dijawab sebelum mulai (Q-01 – Q-10)](#bagian-1--wajib-dijawab-sebelum-mulai)
2. [Aturan teknis umum (Q-11 – Q-17)](#bagian-2--aturan-teknis-umum)
3. [Setup Alvesting (Q-18 – Q-25)](#bagian-3--setup-alvesting)
4. [Kalimasada & analis live (Q-26 – Q-30)](#bagian-4--kalimasada--analis-live)
5. [Forex (Q-31 – Q-36)](#bagian-5--forex)
6. [Saham (Q-37)](#bagian-6--saham)
7. [Filter waktu Astronacci & Hosoda (Q-38 – Q-41)](#bagian-7--filter-waktu)
8. [Pertanyaan lanjutan (Q-42 – Q-48)](#bagian-8--pertanyaan-lanjutan)
9. [**Pertanyaan lanjutan kedua (Q-49 – Q-51) — masih terbuka**](#bagian-9--pertanyaan-lanjutan-kedua)

---

## Bagian 1 — Wajib dijawab sebelum mulai

*Sudah dijawab → [10 · Bagian 1 — Wajib dijawab sebelum mulai](10-jawaban.md#bagian-1--wajib).*

### Q-01 · Risiko per transaksi: 1% dari apa?

**Pertanyaannya:** misalkan saldo akun bot Rp10 juta. Kalau satu transaksi kena stop loss, berapa maksimal uang yang rela hilang?

**Yang dikatakan mentor:** hampir semua mentor bilang **1%**. Tapi Kalimasada pernah bilang 1% dari **seluruh** portofolio, dan di modul lain 1% dari **porsi trading** saja (portofolio dibagi 70% simpan BTC, 30% trading). Untuk scalping, Alvesting menyebut **0,5%–1%**. Lihat [G-01](00-aturan-global.md#g-01--risiko-per-transaksi-maksimal-1).

**Pilihan:**

- **A.** 1% dari **seluruh saldo akun bot** → maksimal rugi Rp100 ribu per transaksi.
- **B.** 1% dari "uang trading" saja, kalau akun bot juga menyimpan uang investasi.
- **C.** Lainnya: ___

Dan untuk setup **scalping**: 0,5% atau 1%?

---

### Q-02 · Pair dan koin apa saja?

**Pertanyaannya:** bot boleh trading di instrumen apa saja?

**Yang dikatakan mentor:** hanya yang **paling ramai/likuid** ([G-09](00-aturan-global.md#g-09--hanya-instrumen-yang-likuid)). Instrumen yang muncul di materi: **EURUSD** (FXcopet), **XAUUSD/emas** (Pola N, Astronacci), **BTC & ETH** (Akademi Crypto). Ichimoku Rafał memakai AUD/CHF, USD/JPY, USD/TRY.

**Pilihan:** sebutkan daftarnya. Contoh: "EURUSD, XAUUSD, BTC, ETH". Altcoin dibahas terpisah di Q-25.

---

### Q-03 · Kripto: spot, futures, atau keduanya?

**Pertanyaannya:** untuk kripto, bot hanya **membeli lalu menjual** (spot), atau juga boleh memakai **kontrak berjangka** (futures/perpetual) yang bisa untung saat harga turun?

**Kenapa penting:** di spot, bot **tidak bisa short**. Semua setup "short" hanya bisa jalan di futures.

**Pilihan:** A. Spot saja · B. Futures saja · C. Keduanya.

---

### Q-04 · Leverage maksimum

**Pertanyaannya:** berapa leverage tertinggi yang diizinkan?

**Yang dikatakan mentor:** Timothy: "jangan pakai leverage". Kalimasada: derivatif boleh untuk porsi kecil (30%) bagi yang agresif. FXcopet: hati-hati; standar broker 1:100, ada yang sampai 1:400.

**Catatan sederhana:** dengan aturan risiko 1% dan stop loss yang selalu terpasang, leverage hanya mengubah **uang jaminan** yang dipakai, bukan besar kerugian per transaksi. Pengecualiannya saat harga melompat melewati stop loss (misalnya saat berita besar atau akhir pekan); di situ leverage besar membuat rugi lebih dalam.

**Pilihan:** A. Tanpa leverage (1×) · B. Maksimal ___× · C. Ikut standar broker.

---

### Q-05 · Rem darurat

**Pertanyaannya:** apakah bot perlu **berhenti otomatis** kalau rugi terlalu banyak dalam waktu singkat? Tidak ada mentor yang menyebut ini ([G-15](00-aturan-global.md#g-15--rem-darurat)).

**Contoh bentuknya:**

- Rugi hari ini mencapai ___% → berhenti sampai besok.
- Rugi minggu ini mencapai ___% → berhenti sampai minggu depan.
- Saldo turun ___% dari titik tertingginya → berhenti total, menunggu Anda memeriksa.

**Pilihan:** A. Ya, dengan angka: ___ · B. Tidak perlu.

---

### Q-06 · Berapa transaksi per hari, dan berapa posisi sekaligus?

**Yang dikatakan mentor** ([G-08](00-aturan-global.md#g-08--jangan-overtrading)):

| Mentor | Batas |
|---|---|
| Alvesting ("orang kantoran") | ±1 transaksi per hari |
| FXcopet | maksimal 2 per hari; kalau sudah untung sekali, berhenti hari itu |
| Alvesting (scalping) | 3–5 per hari sudah banyak |

**Pertanyaannya:**

1. Maksimal transaksi per hari: A. 1 · B. 2 · C. 3–5 · D. ikut mentor masing-masing setup.
2. Maksimal posisi terbuka **bersamaan**: ___ (contoh: 1 per instrumen, total maksimal 3).

---

### Q-07 · Perbandingan untung:rugi (RR) minimum

**Pertanyaannya:** target untung paling kecil berapa kali besar risikonya? Contoh RR 1:2 = mempertaruhkan Rp100 ribu untuk mengincar Rp200 ribu.

**Yang dikatakan mentor** ([G-03](00-aturan-global.md#g-03--rr-minimum-115)): Pola N 1:1,5–1:2 · Alvesting minimal 1:2 (jangka pendek), di atas 1:3 (swing) · contoh Kalimasada 1:3. Semua sepakat: di bawah 1:1 = judi.

**Pilihan:** A. 1:1,5 · B. 1:2 · C. 1:3 · D. ikut mentor masing-masing setup.

Juga dipakai untuk setup yang mentornya **tidak menyebut target** (AFS-05, AFS-09, AFS-15, AFS-17, KMS-02): target = RR minimum ini?

---

### Q-08 · Ambil untung bertahap dan "titik impas"

**Pertanyaannya:** setelah harga bergerak menguntungkan, apakah bot boleh:

- menutup **sebagian** posisi lebih dulu (TP1, TP2, TP3), dan/atau
- memindahkan stop loss ke harga masuk ("titik impas"/BE), supaya kalau berbalik tidak rugi?

**Yang dikatakan mentor:** mentor Pola N **melarang** keduanya ("merusak psikologi"). Alvesting memakai TP1/TP2/TP3. Rafał (Ichimoku) mengambil 50–90% lalu sisanya ke titik impas.

**Pilihan:**

- **A.** Tidak boleh. Satu TP, satu SL, *set and forget*.
- **B.** Boleh, dengan porsi ___ (contoh: 50% di TP1, sisanya ke titik impas).
- **C.** Ikut mentor masing-masing setup.

---

### Q-09 · Masuk sebelum atau sesudah harga menembus?

**Pertanyaannya:** saat harga mendekati batas atas sebuah pola, bot masuk **lebih dulu** (menebak akan tembus, untung lebih besar tapi lebih sering salah), atau **menunggu** harga benar-benar tembus (lebih pasti, tapi masuk di harga lebih jelek)?

**Yang dikatakan mentor:** Alvesting: antisipasi, "jangan kejar breakout". FXcopet, Pola N, Dow Theory: masuk saat/ setelah tembus. Ko Hengki: dua-duanya sah, soal karakter.

**Pilihan:** A. Antisipasi · B. Tunggu tembus (candle **close** di luar level) · C. Ikut mentor masing-masing setup.

---

### Q-10 · Angka persen dari kelas kripto, dipakai di forex?

**Pertanyaannya:** beberapa aturan kripto memakai angka persen:

- Dow Theory: tembus dianggap sah setelah **3%** ([AFS-09](01-alvesting-akademi-crypto.md#afs-09--validasi-tembus-3-dow-theory)).
- Fibonacci: koreksi dianggap selesai setelah memantul **3–5%** ([AFS-04](01-alvesting-akademi-crypto.md#afs-04--pantulan-golden-pocket-fibonacci)).
- Harmonic: entry sah setelah memantul **3%** dari zona pembalikan.
- Trailing stop Ko Andri **5–10%**.

Di kripto, angka itu wajar. Tapi EURUSD biasanya bergerak kurang dari 1% sehari, jadi 3% bisa makan waktu berminggu-minggu.

**Pilihan:**

- **A.** Di forex, ganti dengan ukuran yang mengikuti "kegesitan" pasarnya (kelipatan ATR); angkanya dicari lewat backtest.
- **B.** Tetap pakai persen yang sama di forex.
- **C.** Aturan berbasis persen hanya dipakai di kripto.

---

## Bagian 2 — Aturan teknis umum

*Sudah dijawab → [10 · Bagian 2 — Aturan teknis umum](10-jawaban.md#bagian-2--aturan-teknis-umum).*

### Q-11 · Seberapa jauh stop loss dari titik "analisa salah"?

**Pertanyaannya:** stop loss ditaruh di bawah swing low, **plus** jarak tambahan supaya tidak mudah tersapu. Mentor bilang jarak tambahannya diukur dengan **ATR** (rata-rata besar pergerakan per candle), tapi tidak menyebut berapa. Ada juga dua cara yang berbeda ([G-02](00-aturan-global.md#g-02--stop-loss-wajib-di-titik-analisa-saya-salah)).

**Pilihan:**

- **A.** SL = swing low − (___ × ATR). Catatan: setting ATR bawaan di kebanyakan platform adalah 14 periode.
- **B.** SL = harga masuk − 1 × ATR (seperti contoh BTC 3,36% di kelas).
- **C.** Uji dulu.

---

### Q-12 · Bagaimana bot mengenali puncak dan lembah?

**Pertanyaannya:** banyak aturan bergantung pada "swing high" dan "swing low" (puncak dan lembah). Mentor menunjuknya dengan mata. Bot butuh definisi pasti.

**Pilihan:**

- **A.** Puncak = candle yang high-nya lebih tinggi dari **2 candle di kiri dan 2 di kanan** (definisi Astronacci, sama dengan indikator *fractal*).
- **B.** Sama, tapi lebih besar (misalnya 3–3 atau 5–5), supaya hanya puncak besar yang dihitung.
- **C.** Puncak/lembah baru dihitung kalau harga sudah berbalik minimal ___ × ATR.

**Pertanyaan tambahan terkait:**

- Ko Hengki memakai tren "sekunder" dan "minor" ([HKI-01](04-ko-hengki-remora.md#hki-01--ikuti-tren-sekunder--minor-keluar-saat-struktur-patah)). Timeframe berapa untuk masing-masing? (contoh: sekunder = D1, minor = H4)
- Titik awal hitungan waktu Hosoda ([WKT-05](07-filter-waktu.md#wkt-05--angka-waktu-hosoda-ichimoku)) dan titik A/B/C target harga Ichimoku ([ICH-04](06-mentor-forex.md#ich-04--target-harga-hosoda-untuk-tp)): pakai puncak/lembah dari definisi yang sama?

---

### Q-13 · "Jenuh beli" dan "jenuh jual" di angka berapa?

**Pertanyaannya:** Alvesting memakai Stochastic **5,3,3**, tapi tidak menyebut angka "jenuh beli" (overbought) dan "jenuh jual" (oversold). Begitu juga RSI.

**Pilihan:** A. Standar umum: Stochastic 80/20, RSI 70/30 · B. Lainnya: ___

---

### Q-14 · Volume di forex

**Pertanyaannya:** forex tidak punya bursa pusat, jadi tidak ada data volume asli. Yang ada hanya "tick volume" (berapa kali harga berubah). Beberapa aturan butuh volume: Wyckoff, VSA, CMF, POC, dan "breakout harus bervolume".

**Pilihan:**

- **A.** Tetap pakai tick volume dari broker.
- **B.** Pakai data kontrak berjangka di bursa CME (misalnya 6E untuk EURUSD, GC untuk emas). Butuh sumber data tambahan.
- **C.** Matikan aturan berbasis volume khusus di forex.

---

### Q-15 · Jadwal berita

**Pertanyaannya** ([G-13](00-aturan-global.md#g-13--berita-besar)):

1. Berapa menit **sebelum** dan **sesudah** berita besar bot tidak boleh membuka posisi? (contoh: 30 menit sebelum, 30 menit sesudah)
2. Berita apa saja? (contoh: NFP, keputusan suku bunga, inflasi/CPI)
3. Posisi yang sudah terbuka saat berita: **dibiarkan** atau **ditutup**?
4. Apakah kripto juga ikut aturan ini?

---

### Q-16 · Definisi candle pemicu

**Pertanyaannya:** mentor menyebut *hammer*, *engulfing*, *shooting star*, "candle kuat", dan lain-lain, tanpa angka. Contoh definisi baku: *hammer* = ekor bawah minimal 2× badan dan ekor atas sangat kecil.

**Pilihan:** A. Boleh pakai definisi baku dari buku/platform · B. Saya punya definisi sendiri: ___

---

### Q-17 · Seberapa tebal "zona" support/resistance?

**Pertanyaannya:** Alvesting menyarankan support/resistance digambar sebagai **zona** (kotak), bukan satu garis. Seberapa tebal?

**Pilihan:** A. Setebal ___ × ATR · B. Dari ujung wick sampai badan candle yang membentuk level itu · C. Uji dulu.

---

## Bagian 3 — Setup Alvesting

*Sudah dijawab → [10 · Bagian 3 — Setup Alvesting](10-jawaban.md#bagian-3--setup-alvesting).*

### Q-18 · AFS-01: berapa "poin" minimal?

**Pertanyaannya:** setup "sempurna" punya 5 poin: (1) tren terlihat jelas, (2) struktur minimal 2 higher low & 2 higher high, (3) trendline dihormati, (4) harga di area support/resistance, (5) indikator mendukung. Mentor bilang yang lengkap 5 itu jarang. Bot masuk kalau minimal berapa poin?

**Pilihan:** A. Wajib 5 dari 5 · B. Minimal 4, dengan poin 1, 2, dan 4 wajib · C. Uji dulu.

---

### Q-19 · Batas waktu posisi scalping

**Pertanyaannya:** apakah posisi scalping wajib ditutup setelah sekian jam walaupun belum kena TP/SL? Mentor: scalping berlangsung menit sampai beberapa jam, contohnya "maksimal 3 jam"; lebih dari 24 jam bukan scalping.

**Pilihan:** A. Tutup setelah 3 jam · B. Tutup setelah 24 jam · C. Tidak ada batas waktu.

---

### Q-20 · Smart Money: kapan masuk, di mana keluar?

Untuk [AFS-06](01-alvesting-akademi-crypto.md#afs-06--stop-hunt--break-of-structure), [AFS-07](01-alvesting-akademi-crypto.md#afs-07--change-of-character-choch--retest), [AFS-08](01-alvesting-akademi-crypto.md#afs-08--revisit-order-block--fair-value-gap):

1. **Masuk:** langsung saat candle penembus struktur selesai, atau menunggu harga kembali ke *order block*/FVG?
2. **Target untung:** pakai RR tetap (Q-07), atau ke tumpukan stop loss di sisi lawan (high/low berikutnya)?
3. **"Stop hunt"**: harga harus menembus high/low acuan sejauh berapa, dan kembali ke dalam range dalam berapa candle? (atau "uji dulu")
4. **"Retest"** setelah CHoCH: seberapa dekat harga harus kembali, dan ditunggu maksimal berapa candle?

---

### Q-21 · Definisi order block / FVG

**Pertanyaannya:** mentor menyamakan *order block* dan *fair value gap* dan mendeteksinya dengan indikator LuxAlgo. Bot butuh satu definisi.

**Pilihan:**

- **A.** FVG = celah antara high candle ke-1 dan low candle ke-3 dalam rangkaian 3 candle (definisi umum).
- **B.** Order block = candle terakhir yang berlawanan arah sebelum gerakan besar.
- **C.** Tiru cara kerja indikator LuxAlgo seperti mentor.

---

### Q-22 · Pivot point

Untuk [AFS-12](01-alvesting-akademi-crypto.md#afs-12--pivot-point-entry-di-garis-p):

1. Pivot dihitung dari data **harian** atau **mingguan**?
2. Stop loss versi **agresif** (tepat di bawah P) atau **konservatif** (di bawah S1)?

---

### Q-23 · Pola grafik dan pola harmonic

**Pertanyaannya:** mentor sendiri menyebut pola harmonic dan pola grafik "sangat subjektif". Selain itu, penamaan rasio harmonic di transkrip tidak konsisten (lihat [AFS-10](01-alvesting-akademi-crypto.md#afs-10--pola-abcd) dan [AFS-11](01-alvesting-akademi-crypto.md#afs-11--pola-harmonic-xabcd)).

**Pilihan untuk bot versi pertama:**

- **A.** Tunda semua pola grafik & harmonic.
- **B.** Masukkan pola **ABCD** dan double top/bottom saja.
- **C.** Masukkan semua, memakai rasio standar dari buku Scott Carney, dengan toleransi ±___%.
- **D.** Masukkan semua, memakai angka persis seperti di transkrip.

Untuk double/triple top: "hampir sama tinggi" boleh selisih berapa?

---

### Q-24 · Setting indikator yang rancu

| Indikator | Yang perlu dipastikan |
|---|---|
| **Keltner** (AFS-13) | Garis tengah SMA (kata mentor) atau EMA (default TradingView)? Mode tren, mode pantulan, atau keduanya? |
| **Donchian** (AFS-16) | Dipakai untuk pantulan & silang garis tengah (cara mentor), atau untuk breakout (cara umum)? |
| **Linear Regression Channel** (AFS-20) | Panjang periode dan lebar channel? |
| **Renko** (AFS-21) | Ukuran bata? |
| **Volume profile / POC** (AFS-19) | Rentang waktu yang diukur (contoh: minggu lalu, bulan lalu, sejak swing terakhir)? |

Untuk semua baris ini, jawaban "uji dulu" juga boleh.

---

### Q-25 · Altcoin

**Pertanyaannya:** apakah bot juga trading altcoin, atau hanya BTC & ETH?

Kalau ya:

1. Cara memilih koin: volume futures 24 jam tertinggi, ambil berapa teratas?
2. Pakai tabel korelasi BTC dan dominasi BTC dari [AFS-F1](01-alvesting-akademi-crypto.md#afs-f1--screening-altcoin--korelasi-btc)?
3. Perlu ingat: menurut Alvesting, Smart Money Concept tidak relevan untuk koin kecil/meme.

---

## Bagian 4 — Kalimasada & analis live

*Sudah dijawab → [10 · Bagian 4 — Kalimasada & analis live](10-jawaban.md#bagian-4--kalimasada--analis-live).*

### Q-26 · Seberapa besar yang disebut "volume naik"?

**Pertanyaannya:** Wyckoff, VSA, Ko Hengki, dan filter breakout semuanya bilang "volume naik/tinggi" atau "candle besar/kecil", tanpa angka.

**Pilihan:** A. Volume di atas rata-rata 20 candle terakhir · B. Di atas rata-rata × ___ · C. Uji dulu.

Pertanyaan yang sama untuk "candle besar/kecil" (dibanding rata-rata ukuran candle).

---

### Q-27 · Siklus halving: jual kapan?

**Pertanyaannya:** analis live menyebut dua patokan yang berbeda: "jual **setahun** setelah halving" dan "puncak sekitar **500 hari** setelah halving". Selisihnya ±4–5 bulan ([LIVE-01](03-analis-live-akademi-crypto.md#live-01--siklus-halving-bitcoin-spot-jangka-panjang)).

**Pilihan:** A. Setahun · B. 500 hari · C. Mulai jual bertahap dari setahun sampai 500 hari · D. Bot tidak mengelola investasi jangka panjang.

---

### Q-28 · "Grey area": seberapa dekat dengan resistance?

**Pertanyaannya:** [LIVE-F1](03-analis-live-akademi-crypto.md#live-f1--filter-grey-area) melarang masuk kalau harga "dekat resistance" dan stochastic sudah silang turun. "Dekat" itu berapa?

**Pilihan:** A. Dalam ___ × ATR dari resistance · B. Dalam ___% · C. Uji dulu.

---

### Q-29 · Modul investasi spot kripto

**Pertanyaannya:** apakah bot juga mengelola **investasi spot jangka panjang** (bukan hanya trading)? Kalau tidak, seluruh [modul investasi Kalimasada](02-kalimasada-akademi-crypto.md#b-modul-investasi-spot-kripto-ditunda) dan [LIVE-01](03-analis-live-akademi-crypto.md#live-01--siklus-halving-bitcoin-spot-jangka-panjang) dilewati.

Kalau ya:

1. **Alokasi:** 70% BTC + 15% altcoin + 15% meme, **atau** 70% spot + 30% cash/stablecoin?
2. **Cicilan 5 kali:** jaraknya setiap minggu, atau setiap harga turun ___%?
3. **Fear & Greed:** "extreme" di angka berapa? Sebagai gambaran, kategori resmi indeksnya menyebut kira-kira di bawah 25 = *extreme fear*, di atas 75 = *extreme greed*.

---

### Q-30 · Token baru (TGE)

**Pertanyaannya:** [LIVE-02](03-analis-live-akademi-crypto.md#live-02--token-baru-tge-30-saat-listing-70-di-base) butuh angka "harga lantai" dari valuasi investor yang harus Anda cari dan masukkan sendiri. Mau dimasukkan sebagai fitur setengah-otomatis (Anda isi lantai & target, bot yang mengeksekusi 30/70, cut loss, moon bag)?

**Pilihan:** A. Ya · B. Tidak.

---

## Bagian 5 — Forex

*Sudah dijawab → [10 · Bagian 5 — Forex](10-jawaban.md#bagian-5--forex).*

### Q-31 · Indikator FXcopet

*Jawaban akhir: FXcopet di-skip sepenuhnya; FXC-01 dipindahkan ke [08](08-tidak-dijadikan-aturan.md#g-fxcopet-forex_1-tidak-dipakai). Q-32 dan Q-33 jadi tidak relevan.*

**Pertanyaannya:** setup FXcopet bergantung pada garis merah/aqua dari indikator khusus mereka, yang cara kerjanya tidak dijelaskan di video ([FXC-01](08-tidak-dijadikan-aturan.md#fxc-01--tembus-garis-merahaqua-eurusd-m1-arsip)).

1. Apakah Anda punya file indikator FXcopet ("copet"/"kompas") untuk MetaTrader?
2. Kalau tidak: **A.** tiru dengan garis horizontal di puncak/lembah terakhir M1 (ini **perkiraan**, belum tentu sama dengan aslinya), atau **B.** tunda setup FXcopet.
3. Setting TMA (*Triangular Moving Average*) yang dipakai, kalau Anda tahu.

---

### Q-32 · Teknik "recover" FXcopet

*Tidak relevan lagi (Q-31).*

**Pertanyaannya:** setelah kena stop loss, FXcopet langsung membuka posisi **arah sebaliknya** dengan target 2× kerugian, untuk "menutup rugi". Ini bertentangan dengan larangan *revenge trading* dari Kalimasada dan Alvesting ([G-06](00-aturan-global.md#g-06--dilarang-revenge-trading)). Mentor juga tidak menyebut stop loss untuk posisi recover ini.

**Pilihan:** A. Jangan dipakai · B. Dipakai, dengan ukuran posisi tetap mengikuti G-01 dan stop loss ___ · C. Uji dulu terpisah.

---

### Q-33 · Jam tutup FXcopet

*Tidak relevan lagi (Q-31).*

**Pertanyaannya:** transkrip menyebut posisi ditutup manual "di penutupan sesi Eropa, jam **5.00 sampai 6.00 WIB**". Pagi atau sore? Sesi Eropa (London) biasanya tutup sekitar 23.00–24.00 WIB, jadi angka ini tidak cocok untuk keduanya.

**Pilihan:** A. 05.00–06.00 WIB · B. 17.00–18.00 WIB · C. Ikut jam tutup London · D. Tidak pakai tutup manual; hanya TP/SL.

---

### Q-34 · Pola N: angka-angka yang belum disebut

Untuk [PLN-01](06-mentor-forex.md#pln-01--pola-n-impuls--koreksi-sempit--tembus):

1. **Koreksi "sedikit"**: maksimal berapa candle? Dan sedalam apa dibanding impulsnya (contoh: tidak lebih dari 50% panjang impuls)?
2. **Candle "kuat"**: wick boleh sebesar apa dibanding badan?
3. **Stop loss** di "candle wick ke-2": maksudnya ujung bawah koreksi (untuk buy)?
4. **Timeframe trading:** H1?

---

### Q-35 · Ichimoku: di mana stop loss?

**Pertanyaannya:** Rafał tidak menyebut letak stop loss ([ICH-01](06-mentor-forex.md#ich-01--tren-penuh-harga-tenkankijun-kumo-chikou)).

**Pilihan:** A. Di balik Kijun · B. Di balik Kumo (seperti versi Alvesting di AFS-14) · C. Di balik puncak/lembah terakhir · D. Uji dulu.

---

### Q-36 · Ichimoku: Chikou digeser 26 atau 25?

**Pertanyaannya:** menurut Rafał, banyak platform menggeser Chikou keliru satu candle, dan ia membetulkannya ([forex_3 L2449–L2570](../materi/mentah/forex_3.txt#L2449-L2570)).

**Pilihan:** A. Ikuti koreksi Rafał (tepat 26 candle) · B. Ikuti bawaan platform.

---

## Bagian 6 — Saham

*Sudah dijawab → [10 · Bagian 6 — Saham](10-jawaban.md#bagian-6--saham).*

### Q-37 · Trailing stop Ko Andri

**Pertanyaannya:** Ko Andri menyarankan *trailing stop* 5–10% bagi yang tidak memantau pasar ([AND-02](05-ko-andri-andre-hakim.md#and-02--trailing-stop-510)). Mau dipakai?

**Pilihan:** A. Tidak · B. Ya, hanya untuk kripto spot, ___% · C. Ya, untuk semua, dengan ukuran ATR (lihat Q-10).

---

## Bagian 7 — Filter waktu

*Sudah dijawab → [10 · Bagian 7 — Filter waktu](10-jawaban.md#bagian-7--filter-waktu).*

### Q-38 · Apa efek filter waktu pada bot?

**Pertanyaannya:** kalau nanti filter waktu Astronacci atau Hosoda lolos uji ([07](07-filter-waktu.md)), apa yang dilakukan bot pada tanggal "rawan/kandidat titik balik"?

**Pilihan:**

- **A.** Tidak membuka posisi baru di tanggal itu.
- **B.** Hanya mengizinkan setup **pembalikan** (bukan setup ikut tren) di tanggal itu.
- **C.** Hanya mencatat/menandai, tanpa mengubah keputusan (untuk mengumpulkan data).
- **D.** Dipakai untuk mengatur waktu ambil untung.

---

### Q-39 · Fase bulan

1. Jendela waktu: **±1 hari** atau **±2 hari** dari New Moon/Full Moon?
2. Instrumen yang diuji: EURUSD, XAUUSD, BTC? (PETA menyarankan EURUSD dan XAUUSD.)
3. Berlaku untuk setup timeframe berapa? (Jendela harian kurang berarti untuk scalping M5.)

---

### Q-40 · Fibonacci waktu

1. Puncak/lembah diambil dari timeframe apa (D1?) dan berapa titik ke belakang?
2. "Bertumpuk" artinya proyeksi jatuh di hari yang sama, atau boleh selisih ±1 hari?
3. Proyeksinya: jumlah hari Fibonacci (13, 21, 34, …) dihitung langsung **dari** titik balik, atau **kelipatan Fibonacci** dari jarak antar-titik balik? PETA tidak merinci.

---

### Q-41 · Mercury retrograde

**Pertanyaannya:** selama Merkurius *retrograde* (±24 hari, 3–4 kali setahun), apa yang dilakukan bot?

**Pilihan:** A. Setup breakout dimatikan · B. Ukuran posisi dikecilkan ___% · C. Hanya dicatat · D. Tidak dipakai sama sekali.

---

## Bagian 8 — Pertanyaan lanjutan

*Sudah dijawab → [10 · Bagian 8](10-jawaban.md#bagian-8--pertanyaan-lanjutan).*

Pertanyaan ini muncul saat menerapkan jawaban Anda. Cara menjawabnya sama: tulis nomor dan pilihan, misalnya `Q-45: B`.

### Q-42 · Data mana yang disisihkan untuk memilih varian?

**Pertanyaannya:** Anda minta varian dipilih dari hasil di data yang **tidak dipakai saat menyusun strategi** ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)). Data dibagi menurut waktu: bagian lama untuk menyusun dan memeriksa kode, bagian terbaru disimpan dan baru dipakai untuk memilih. Berapa bagian terbaru yang disisihkan?

**Pilihan:**

- **A.** 30% terakhir dari periode data. Contoh: data 10 tahun → 7 tahun pertama untuk menyusun, 3 tahun terakhir untuk memilih.
- **B.** 12 bulan terakhir.
- **C.** Lainnya: ___

**Catatan:** mentor forex_2 minta data H1 minimal 2 tahun ([G-14](00-aturan-global.md#g-14--backtest-dulu-dan-nilai-hasilnya-dengan-data)). Batas itu saya pakai untuk bagian penyusunan, jadi data totalnya harus lebih panjang.

---

### Q-43 · "Hasil lebih baik" diukur dengan apa?

**Pertanyaannya:** saat dua varian dibandingkan (misalnya SL 1× ATR lawan 1,5× ATR, atau tick volume lawan tanpa volume di Q-14), angka apa yang menentukan pemenangnya?

**Pilihan:**

- **A.** Untung bersih setelah biaya, dibagi drawdown terburuk ("untung per rasa sakit").
- **B.** Untung bersih setelah biaya saja.
- **C.** Rata-rata untung per transaksi dalam satuan risiko (R). Contoh: +0,3R = rata-rata tiap transaksi menghasilkan 0,3 kali risikonya.
- **D.** Lainnya: ___

**Tambahan:** varian dengan transaksi terlalu sedikit sulit dinilai. Minimal berapa transaksi di data pemilihan supaya hasilnya dihitung? (contoh: 30)

---

### Q-44 · "Hari" dan "rugi" dihitung bagaimana?

Untuk rem darurat ([G-15](00-aturan-global.md#g-15--rem-darurat)) dan batas 3 transaksi per hari ([G-08](00-aturan-global.md#g-08--jangan-overtrading)):

1. **Hari dan minggu mulai jam berapa?**
   - **A.** 00.00 WIB; minggu mulai Senin 00.00 WIB.
   - **B.** Ikut pergantian candle harian sumber data (kripto biasanya 07.00 WIB; forex biasanya 04.00 atau 05.00 WIB).
   - **C.** Lainnya: ___
2. **"Rugi hari ini 3%"** dihitung dari: **A.** saldo awal hari, **termasuk** rugi posisi yang masih terbuka · **B.** hanya transaksi yang sudah ditutup.
3. **Saat bot berhenti total**, posisi yang masih terbuka: **A.** dibiarkan sampai kena TP/SL · **B.** langsung ditutup semua.
4. **"Koneksi putus lama"** = putus lebih dari ___ menit (contoh: 15 menit).
5. **Pola N** ([PLN-01](06-mentor-forex.md#pln-01--pola-n-impuls--koreksi-sempit--tembus)) hanya masuk "mulai 18.00 WIB", tanpa batas akhir dari mentor. Sementara saya pakai sampai **23.59 WIB**. **A.** Setuju · **B.** Sampai jam ___ WIB.

---

### Q-45 · Setup mana yang dihitung "scalping"?

**Kenapa penting:** label scalping berarti risiko **0,5%**, posisi **ditutup setelah 3 jam**, dan **ditutup sebelum berita besar** ([D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading)). AFS-02 jelas scalping. Tiga setup lain belum jelas:

| Setup | Kata mentor |
|---|---|
| [AFS-03](01-alvesting-akademi-crypto.md#afs-03--double-topbottom--tembus-neckline) Double top/bottom | Contohnya diberikan di pelajaran scalping, di M15 |
| [AFS-12](01-alvesting-akademi-crypto.md#afs-12--pivot-point-entry-di-garis-p) Pivot point | Fokus H1, M15, M5; "yang suka intraday trading, suka scalping" |
| [AFS-20](01-alvesting-akademi-crypto.md#afs-20--linear-regression-channel) Linear Regression Channel | "Cocok buat kalian yang suka scalping", "selesai dalam satu hari" |

**Pilihan:**

- **A.** Ketiganya scalping.
- **B.** Hanya AFS-03 scalping; AFS-12 dan AFS-20 trading biasa (1%, tanpa batas 3 jam).
- **C.** Ketiganya trading biasa.
- **D.** Lainnya: ___

---

### Q-46 · AFS-01: indikator untuk poin 5

Untuk [AFS-01](01-alvesting-akademi-crypto.md#afs-01--technical-research-5-tahap-versi-swing) dan AFS-02. Anda memilih minimal 4 dari 5 poin, dengan poin 1, 2, dan 4 wajib (Q-18).

1. **Poin 5, "indikator mendukung".** G-11 membatasi satu indikator per kategori. Indikator mana?
   - **A.** Bollinger Bands (20, 2): long kalau harga menyentuh band bawah, short kalau menyentuh band atas. Ini contoh mentor saat menjelaskan 5 poin.
   - **B.** Stochastic 5,3,3 (setting favorit mentor) di area jenuh jual/beli.
   - **C.** MA50: harga di atas MA50 untuk long, di bawahnya untuk short. Contoh mentor untuk downtrend ("ditolak MA50").
   - **D.** Uji ketiganya, pilih di data pemilihan.
2. **Poin 1, "tren terlihat secara kasat mata".** Tidak ada ukurannya, jadi saya samakan dengan poin 2 (minimal 2 higher high & 2 higher low). Akibatnya: poin 2 dan 4 wajib, ditambah minimal satu dari poin 3 dan 5. **A.** Setuju · **B.** Tidak: ___
3. **Syarat pola (H4).** Di versi pertama, pola yang dikenali hanya double/triple top-bottom dan ABCD (Q-23), jadi setup ini akan jarang muncul. **A.** Pola tetap wajib · **B.** Pola tidak wajib.

---

### Q-47 · Timeframe dan cara masuk yang belum disebut

Mentor tidak menyebut timeframe untuk setup berikut:

| Setup | Yang perlu dipastikan |
|---|---|
| [AFS-05](01-alvesting-akademi-crypto.md#afs-05--money-magnet-ema-13--21) EMA 13 & 21 (berdiri sendiri) | Timeframe, **dan** cara masuk: langsung saat harga menyentuh pita EMA, atau menunggu candle pemicu ([D-06](00-aturan-global.md#d-06--candle)) |
| [AFS-13A / AFS-13B](01-alvesting-akademi-crypto.md#afs-13--keltner-channel) Keltner | Timeframe |
| [AFS-16](01-alvesting-akademi-crypto.md#afs-16--donchian-channel) Donchian | Timeframe |
| [AFS-20](01-alvesting-akademi-crypto.md#afs-20--linear-regression-channel) Linear Regression Channel | Timeframe chart (mentor hanya bilang "intraday") |

**Pilihan untuk timeframe:**

- **A.** Uji beberapa timeframe dan pilih di data pemilihan: H1, H4, D1 (AFS-20: M15 dan H1).
- **B.** Saya tentukan sendiri per setup: ___

**Pilihan untuk cara masuk AFS-05:** **A.** Langsung saat harga menyentuh pita EMA · **B.** Tunggu candle pemicu di pita EMA.

---

### Q-48 · Wyckoff KMS-02: range seperti apa?

[KMS-02](02-kalimasada-akademi-crypto.md#kms-02--wyckoff-breakout-range--retest) butuh definisi "range konsolidasi yang lama". Mentor hanya memberi contoh: range akumulasi BTC sekitar 10–20% ([AC_crypto_60 L2824–L3104](../materi/mentah/AC_crypto_60.txt#L2824-L3104)).

1. **Timeframe:** **A.** D1 · **B.** H4 · **C.** Uji keduanya.
2. **Lama minimal range:** ___ candle (contoh: 20).
3. **Lebar maksimal range:** **A.** 20% (batas atas contoh mentor) · **B.** ___ × ATR(14) · **C.** Uji dulu, nilai awal ___.

---

## Bagian 9 — Pertanyaan lanjutan kedua

Pertanyaan ini muncul saat menerapkan jawaban Q-42 – Q-48. Tidak ada yang menghambat setup, kecuali Q-51 untuk AFS-22.

### Q-49 · Forex dan kripto: batas digabung atau terpisah?

**Pertanyaannya:** forex berjalan di akun broker, kripto di exchange spot, jadi saldonya terpisah. Hari forex mulai 17.00 New York, hari kripto 00.00 UTC ([D-12](00-aturan-global.md#d-12--batas-hari-minggu-dan-candle), Q-44). Batas-batas berikut dihitung bagaimana?

- risiko per transaksi 1% / 0,5% ([G-01](00-aturan-global.md#g-01--risiko-per-transaksi-maksimal-1));
- 3 transaksi baru per hari, 3 posisi bersamaan, risiko terbuka 3% ([G-08](00-aturan-global.md#g-08--jangan-overtrading));
- rem darurat harian 3%, mingguan 6%, dan batas drawdown ([G-15](00-aturan-global.md#g-15--rem-darurat)).

**Pilihan:**

- **A.** Terpisah per akun. Tiap akun memakai saldonya sendiri dan batas harinya sendiri: masing-masing maksimal 3 transaksi baru per hari, 3 posisi, dan risiko terbuka 3% dari saldonya. Rem darurat satu akun tidak menghentikan akun lain.
- **B.** Gabungan. Satu set batas untuk kedua akun, dihitung dari jumlah equity keduanya. "Hari" untuk batas gabungan memakai: batas forex (17.00 New York) / batas kripto (00.00 UTC) — pilih satu.
- **C.** Lainnya: ___

---

### Q-50 · Pemilihan varian: per instrumen atau gabungan?

1. **Pilihan nilai parameter dan varian (G-17) dibuat untuk apa?**
   - **A.** Satu pilihan untuk semua instrumen setup itu. Transaksi semua instrumen digabung saat menghitung Recovery Factor dan syarat 30 transaksi.
   - **B.** Per instrumen. Tiap instrumen punya pilihan sendiri dan harus memenuhi 30 transaksi sendiri. Lebih cocok dengan karakter tiap pasar, tetapi jumlah percobaannya 4× lebih banyak dan syarat 30 transaksi lebih sulit dipenuhi.
   - **C.** Per pasar: satu pilihan untuk forex (EURUSD, XAUUSD), satu untuk kripto (BTC, ETH).

   Catatan: untuk Keltner, Anda sudah menulis "di live hanya satu yang aktif per instrumen" (Q-24). Jawaban di sini menentukan apakah aturan "per instrumen" itu juga berlaku untuk setup lain.

2. **Data kripto tidak ada sejak 2010.** ETH baru diperdagangkan sejak Agustus 2015, dan Binance (exchange terbesar sekarang) baru buka Juli 2017. Padahal Anda minta tanggal potong 60/20/20 sama untuk semua instrumen (Q-42).
   - **A.** Semua instrumen memakai periode bersama, mulai dari tanggal data kripto yang rapi tersedia (contoh: 2017). Forex jadi sekitar 9 tahun.
   - **B.** Forex sejak 2010, kripto sejak datanya ada; tanggal potong 60/20/20 dihitung per pasar.
   - **C.** Tanggal potong sama untuk semua, dihitung dari periode forex (2010–sekarang). Kripto mendapat bagian penyusunan yang lebih pendek (contoh: 2017–2019).
   - **D.** Lainnya: ___

---

### Q-51 · Order flow (AFS-22)

**Pertanyaannya:** [AFS-22](01-alvesting-akademi-crypto.md#afs-22--sinyal-order-flow) adalah satu-satunya setup 🟡 yang belum punya pertanyaan. Mentor mendefinisikan sinyalnya (delta, imbalance ≥300%, stacked imbalance, unfinished auction), tetapi **tidak menyebut entry, SL, dan TP**. Datanya (*footprint*, volume per level harga) hanya ada di exchange kripto, dan jauh lebih besar daripada data candle biasa.

**Pilihan:**

- **A.** Tunda (⏸) di versi pertama.
- **B.** Pakai sebagai filter tambahan untuk setup kripto, misalnya long hanya diizinkan kalau delta candle pemicu positif. Rinciannya perlu ditentukan lagi.
- **C.** Lainnya: ___
