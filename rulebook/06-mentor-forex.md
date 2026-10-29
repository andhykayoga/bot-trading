# 06 · MENTOR FOREX

Dua sumber forex yang dipakai berasal dari orang yang **berbeda** dan tidak saling terkait ([PETA bagian 7](../materi/PETA.md#7-peta-forex)):

- [A. Pola N](#a-pola-n-forex_2) — breakout di emas (XAUUSD). Nama mentornya tidak disebut; filosofi "pola N" ia sebut berasal dari "Pak Tito".
- [B. Ichimoku — Rafał Zuchowicz](#b-ichimoku--rafał-zuchowicz-forex_3) — kursus Ichimoku dari tulisan asli Goichi Hosoda (bahasa Inggris).

Sumber forex ketiga, **FXcopet** (forex_1), **tidak dipakai**: bukan dari mentor utama Anda dan indikatornya tidak diketahui (Q-31). Isinya disimpan di [08 · bagian G](08-tidak-dijadikan-aturan.md#g-fxcopet-forex_1-tidak-dipakai).

Instrumen untuk semua setup di halaman ini: **EURUSD** dan **XAUUSD**; setup Ichimoku juga **BTC** dan **ETH** ([G-09](00-aturan-global.md#g-09--hanya-instrumen-yang-likuid)).

---

## A. Pola N (forex_2)

### PLN-01 · Pola N: impuls → koreksi sempit → tembus

| | |
|---|---|
| Sumber | [forex_2 L460–L945](../materi/mentah/forex_2.txt#L460-L945) (price action), [forex_2 L945–L1105](../materi/mentah/forex_2.txt#L945-L1105) (manajemen risiko), [forex_2 L1105–L1465](../materi/mentah/forex_2.txt#L1105-L1465) (backtest), [forex_2 L1465–L2300](../materi/mentah/forex_2.txt#L1465-L2300) (rangkuman pola N) |
| Pasar | F (contoh mentor di XAUUSD) |
| Timeframe | **H1**, timeframe backtest mentor ([forex_2 L1119–L1129](../materi/mentah/forex_2.txt#L1119-L1129)) (Q-34) |
| Arah | Buy dan sell, **searah arus** |
| Label | Trading |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Prinsip:** ikuti arus pasar, jangan melawan. Mentor mengklaim mengikuti arus menang ±70–80% ([forex_2 L585–L609](../materi/mentah/forex_2.txt#L585-L609), [forex_2 L925–L934](../materi/mentah/forex_2.txt#L925-L934)).

**Syarat (versi buy; sell adalah cerminannya):**

1. **Impuls:** candle bullish **kuat**, yaitu badan ≥ 70% dari panjang candle ([D-06](00-aturan-global.md#d-06--candle), Q-34). Mentor: badan penuh, wick sangat kecil, close menembus dengan "sempurna" ([forex_2 L615–L640](../materi/mentah/forex_2.txt#L615-L640)). Tiga candle badan searah berturut-turut disebut tanda pembeli masih dominan ±80% ([forex_2 L655–L670](../materi/mentah/forex_2.txt#L655-L670)).
2. **Koreksi kecil** sesudah impuls (Q-34):
   - paling banyak **3 candle** (nilai awal; diuji 2 · 3 · 4), dan
   - tidak lebih dalam dari **50% panjang impuls** (nilai awal; diuji 25% · 50% · 75%). Mentor sendiri memakai 50% candle impuls untuk varian limit order ([forex_2 L848–L850](../materi/mentah/forex_2.txt#L848-L850)).

   Mentor: penjual melawan **sedikit**, ruangnya **sempit**, tidak lama "bertarung" ([forex_2 L1515–L1580](../materi/mentah/forex_2.txt#L1515-L1580), [forex_2 L1700–L1715](../materi/mentah/forex_2.txt#L1700-L1715)).
3. Bentuknya tidak harus huruf N; yang penting urutannya: **naik → turun sedikit → naik** ([forex_2 L1590–L1650](../materi/mentah/forex_2.txt#L1590-L1650)).
4. **Jam:** order hanya dipasang mulai **18.00 WIB**, sesuai pesan "trading malam hari aja di atas 6.00 sore" ([forex_2 L2206](../materi/mentah/forex_2.txt#L2206)) (Q-34). Mentor tidak menyebut batas akhirnya; bot memakai **23.59 WIB** (tafsiran saya, lihat [Q-44](09-pertanyaan-untuk-anda.md#q-44--hari-dan-rugi-dihitung-bagaimana)). Pembanding di backtest: tanpa batas jam.

**Entry:** **buy stop** di atas wick tertinggi koreksi. Order terisi ketika harga menembus ([forex_2 L1650–L1659](../materi/mentah/forex_2.txt#L1650-L1659), [forex_2 L1200–L1229](../materi/mentah/forex_2.txt#L1200-L1229)).

**Stop loss:** tepat di **ujung wick candle sebelum candle breakout**, yaitu ujung koreksi (Q-34; [forex_2 L1911–L1928](../materi/mentah/forex_2.txt#L1911-L1928)). Tanpa tambahan ATR; ini pengecualian di [G-02](00-aturan-global.md#g-02--stop-loss-wajib-di-titik-analisa-saya-salah).

**Take profit:** **1:1,5 atau 1:2** dari jarak SL. SL ditentukan dulu, baru TP ([forex_2 L1930–L1959](../materi/mentah/forex_2.txt#L1930-L1959)). Kedua angka dari mentor, jadi keduanya diuji ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)).

**Manajemen posisi:** *set and forget*. **Tanpa** TP1/TP2, **tanpa** geser ke titik impas ([forex_2 L1360–L1379](../materi/mentah/forex_2.txt#L1360-L1379), [forex_2 L1850–L1889](../materi/mentah/forex_2.txt#L1850-L1889)).

**Risiko:** maksimal 1% per transaksi; lot dihitung dengan kalkulator risiko ([forex_2 L1040–L1089](../materi/mentah/forex_2.txt#L1040-L1089)).

**Jangan ambil jika:**

- Konsolidasi **terlalu lama atau terlalu lebar**: rawan *fake out*, RR jelek ([forex_2 L1530–L1560](../materi/mentah/forex_2.txt#L1530-L1560), [forex_2 L1710–L1760](../materi/mentah/forex_2.txt#L1710-L1760), [forex_2 L2230–L2245](../materi/mentah/forex_2.txt#L2230-L2245)). Di bot, ini sudah tercakup batas koreksi 3 candle dan 50% di syarat 2. Termasuk breakout **lemah** (hanya wick) dari konsolidasi seperti itu ([forex_2 L1745–L1760](../materi/mentah/forex_2.txt#L1745-L1760)).
- Hanya breakout resistance biasa tanpa koreksi kecil; itu bukan pola N dan SL-nya terlalu jauh ([forex_2 L1670–L1699](../materi/mentah/forex_2.txt#L1670-L1699)).
- Sedang ada jendela berita besar ([G-13](00-aturan-global.md#g-13--berita-besar)). Mentor: berita hanya mempercepat TP/SL; kalau mau aman, jangan trading saat berita ([forex_2 L2185–L2209](../materi/mentah/forex_2.txt#L2185-L2209)).

**Tidak dipakai di versi pertama:** varian limit order di 50% candle impuls "kalau breakout sudah terlalu jauh" ([forex_2 L840–L869](../materi/mentah/forex_2.txt#L840-L869)), karena mentor tidak menyebut kapan breakout dianggap "terlalu jauh". Juga "pasar sedang tidak jelas: diemin aja" ([forex_2 L2140–L2149](../materi/mentah/forex_2.txt#L2140-L2149)), karena tidak ada ukurannya.

**Data backtest mentor** (contoh): tingkat menang ±67%, rugi beruntun terpanjang 5 kali, untung beruntun bisa 12–14 kali ([forex_2 L1410–L1449](../materi/mentah/forex_2.txt#L1410-L1449)).

**Pendapat lain mentor yang tidak dijadikan setup:**

- Support/resistance = area yang memantul **lebih dari 2 kali**. Dipakai untuk pandangan arah, **bukan** untuk entry ([forex_2 L31–L60](../materi/mentah/forex_2.txt#L31-L60), [forex_2 L355–L365](../materi/mentah/forex_2.txt#L355-L365)).
- Supply & demand tidak ia sukai: menunggu lama, sering kena SL dulu, tingkat menang di bawah 50% ([forex_2 L230–L345](../materi/mentah/forex_2.txt#L230-L345)).

---

## B. Ichimoku — Rafał Zuchowicz (forex_3)

Kursus "Ichimoku King". Rafał mengaku belajar dari buku asli Goichi Hosoda ([forex_3 L1185–L1240](../materi/mentah/forex_3.txt#L1185-L1240)). Contoh-contohnya di AUD/CHF, USD/JPY, USD/TRY, minyak, dan DAX; pair itu tidak dipakai bot versi pertama (Q-02).

**Setting baku:** Tenkan **9**, Kijun **26**, Senkou Span B **52**. "Jangan diubah" ([forex_3 L3281–L3300](../materi/mentah/forex_3.txt#L3281-L3300), [forex_3 L3391–L3398](../materi/mentah/forex_3.txt#L3391-L3398)).

**Pergeseran Chikou dan Kumo (Q-36):** banyak platform menggeser Chikou keliru satu candle. Bot mengikuti koreksi Rafał: **geser 25 candle**, dengan candle sekarang dihitung sebagai candle ke-1. Artinya Chikou candle sekarang dibandingkan dengan harga **25 candle sebelumnya**, dan Senkou A/B yang dihitung sekarang digambar **25 candle ke depan**. Trik Rafał: matikan Chikou bawaan, lalu buat Chikou sendiri dengan pergeseran 25, atau SMA periode 1 yang digeser −25 ([forex_3 L2449–L2570](../materi/mentah/forex_3.txt#L2449-L2570)). Kumo juga ikut dikoreksi ([forex_3 L2809–L2835](../materi/mentah/forex_3.txt#L2809-L2835)). Perhitungan yang sama dipakai untuk [AFS-14](01-alvesting-akademi-crypto.md#afs-14--ichimoku-di-atasbawah-semua-garis).

**Arti tiap garis:**

| Garis | Rumus | Arti |
|---|---|---|
| **Tenkan** | (High + Low) ÷ 2 dari 9 candle terakhir | Trader jangka pendek ([forex_3 L1958–L2140](../materi/mentah/forex_3.txt#L1958-L2140)) |
| **Kijun** | (High + Low) ÷ 2 dari 26 candle | "Garis pasar / keseimbangan". Di atas = buy yang benar; di bawah = sell yang benar ([forex_3 L3399–L3420](../materi/mentah/forex_3.txt#L3399-L3420), [forex_3 L3499–L3520](../materi/mentah/forex_3.txt#L3499-L3520)) |
| **Senkou A** | (Tenkan + Kijun) ÷ 2, digeser ke depan | Batas Kumo |
| **Senkou B** | (High + Low) ÷ 2 dari 52 candle, digeser ke depan | Batas Kumo yang paling lambat berubah ([forex_3 L3589–L3630](../materi/mentah/forex_3.txt#L3589-L3630)) |
| **Kumo** | Ruang antara Senkou A dan B | Zona support/resistance ([forex_3 L3629–L3660](../materi/mentah/forex_3.txt#L3629-L3660)) |
| **Chikou** | Harga close digeser ke belakang | "Ingatan pasar": dibandingkan dengan harga di masa lalu ([forex_3 L2569–L2610](../materi/mentah/forex_3.txt#L2569-L2610)) |

**Aturan yang sama untuk ICH-01 – ICH-03:**

- **Stop loss (Q-35):** di balik **Kijun**, ditambah **1 × ATR(14)** ([G-02](00-aturan-global.md#g-02--stop-loss-wajib-di-titik-analisa-saya-salah)). Long: SL = Kijun − 1 × ATR; short: SL = Kijun + 1 × ATR. Dasarnya Rafał: close di bawah Kijun = tanda bahaya ([forex_3 L3475–L3490](../materi/mentah/forex_3.txt#L3475-L3490)). Rafał sendiri hanya bilang "selalu pasang stop loss yang tidak takut Anda pakai" ([forex_3 L355–L365](../materi/mentah/forex_3.txt#L355-L365)). Pembanding di backtest: SL di balik swing terakhir + 1 × ATR.
- **Take profit (Q-08):** target harga [ICH-04](#ich-04--target-harga-hosoda-untuk-tp) yang **terdekat** dan RR-nya minimal **1:1,5**. Kalau tidak ada, jangan masuk. Rafał sendiri mengambil 50–90% di target lalu sisanya digeser ke titik impas ([forex_3 L611–L705](../materi/mentah/forex_3.txt#L611-L705)); versi ini diuji sebagai **pembanding**: 50% ditutup di target pertama, SL sisanya ke titik impas, sisanya mengincar target Hosoda berikutnya.
- **Label:** trading.

### ICH-01 · Tren penuh (harga, Tenkan–Kijun, Kumo, Chikou)

| | |
|---|---|
| Sumber | [forex_3 L2439–L2843](../materi/mentah/forex_3.txt#L2439-L2843), [forex_3 L3519–L3685](../materi/mentah/forex_3.txt#L3519-L3685), praktik live [forex_3 L1–L712](../materi/mentah/forex_3.txt#L1-L712) |
| Pasar | F, K |
| Timeframe | Bias dari **W1 & D1**, entry di **H4** ([forex_3 L1–L240](../materi/mentah/forex_3.txt#L1-L240)) |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Short (contoh yang paling lengkap di kursus), semua dicek di H4 saat candle close:**

1. Harga **di bawah Kumo**.
2. **Chikou di bawah Kumo** dan di bawah harga 25 candle sebelumnya (Q-36).
3. **Tenkan di bawah Kijun** (*death cross*).
4. Rafał menyebutnya "sinyal jelas untuk jual" ([forex_3 L2689–L2700](../materi/mentah/forex_3.txt#L2689-L2700)).

**Bias W1 & D1:** harga di **W1 dan D1** juga berada di bawah Kumo. *(Terjemahan saya dari alur praktik live di bawah, supaya "bias dari timeframe besar" punya ukuran.)*

**Long:** cerminannya. Rafał menambahkan: **buy hanya boleh** jika Chikou **di atas harga di masa lalu**, lebih baik juga di atas Kumo ([forex_3 L2655–L2665](../materi/mentah/forex_3.txt#L2655-L2665)).

**Entry:** order pasar saat candle H4 yang memenuhi semua syarat close ([D-10](00-aturan-global.md#d-10--konvensi-eksekusi)).

**Jangan masuk jika:** sudah *golden cross* tetapi harga **masih di dalam Kumo** atau tertahan Senkou B — tunggu ([forex_3 L2729–L2760](../materi/mentah/forex_3.txt#L2729-L2760)).

**Untuk posisi jangka panjang** Rafał juga menunggu **Kumo twist** (Kumo di masa depan sudah berbalik arah) ([forex_3 L3659–L3680](../materi/mentah/forex_3.txt#L3659-L3680)). Bot versi pertama tidak memegang posisi jangka panjang, jadi syarat ini tidak dipakai.

**Alur dari praktik live (USD/TRY), sebagai gambaran** ([forex_3 L1–L360](../materi/mentah/forex_3.txt#L1-L360)):

1. W1: candle **close di bawah Tenkan** dan gagal close kembali di atasnya → sinyal jual dari timeframe besar ([forex_3 L51–L90](../materi/mentah/forex_3.txt#L51-L90)).
2. D1: Chikou turun di bawah harga; harga sempat masuk Kumo lalu gagal ([forex_3 L101–L150](../materi/mentah/forex_3.txt#L101-L150)).
3. H4: hitung **waktu** (angka Hosoda, [WKT-05](07-filter-waktu.md#wkt-05--angka-waktu-hosoda-ichimoku)) dan **target harga** ([ICH-04](#ich-04--target-harga-hosoda-untuk-tp)).
4. **Entry:** candle **open dan close di bawah** level target NT (bekas support) + *death cross* + Chikou di bawah harga → "no brainer" ([forex_3 L311–L360](../materi/mentah/forex_3.txt#L311-L360)).

---

### ICH-02 · Retest Kijun

| | |
|---|---|
| Sumber | [forex_3 L3429–L3500](../materi/mentah/forex_3.txt#L3429-L3500) |
| Pasar | F, K |
| Timeframe | D1 / H4 |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Long:**

1. Harga sudah menembus ke atas Kijun (candle close di atasnya).
2. Harga kembali turun **menyentuh Kijun** dan **tidak close di bawahnya**.
3. → Buy saat candle yang menyentuh itu close. Rafał: "di situlah peluang beli yang bagus" ([forex_3 L3449–L3475](../materi/mentah/forex_3.txt#L3449-L3475)).

**Tanda bahaya / batal:** candle **close di bawah Kijun** ([forex_3 L3475–L3490](../materi/mentah/forex_3.txt#L3475-L3490)).

**Short:** cerminannya.

---

### ICH-03 · Pullback ke Tenkan dalam tren kuat

| | |
|---|---|
| Sumber | [forex_3 L2148–L2438](../materi/mentah/forex_3.txt#L2148-L2438) |
| Pasar | F, K |
| Timeframe | Contoh di D1 |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Sinyal awal:** candle **kuat** ([D-06](00-aturan-global.md#d-06--candle)) close di atas Tenkan, dan Tenkan mulai naik. Candle kecil yang menembus lalu ditolak keesokan harinya = pasar belum siap ([forex_3 L2160–L2245](../materi/mentah/forex_3.txt#L2160-L2245)).

**Entry:** setelah sinyal awal dan selama belum ada tanda berakhir, setiap **pullback yang menyentuh Tenkan dan bertahan** (tidak close di bawahnya) → buy saat candle itu close ([forex_3 L2245–L2345](../materi/mentah/forex_3.txt#L2245-L2345)).

**Tanda berakhir (tidak ada entry baru):**

- Close kuat di bawah Tenkan selama 2 hari = kapitulasi ([forex_3 L2385–L2395](../materi/mentah/forex_3.txt#L2385-L2395)).
- Harga bolak-balik menembus Tenkan ke atas dan ke bawah = **sideways**; setup ini tidak berlaku ([forex_3 L2395–L2410](../materi/mentah/forex_3.txt#L2395-L2410)).

**Short:** cerminannya.

**Catatan:** Rafał juga memakai pullback ke Tenkan untuk **menambah** posisi yang sedang untung. Itu tidak dipakai di versi pertama, karena [G-08](00-aturan-global.md#g-08--jangan-overtrading) membatasi 1 posisi per instrumen.

---

### ICH-04 · Target harga Hosoda untuk TP

| | |
|---|---|
| Sumber | [forex_3 L2844–L3043](../materi/mentah/forex_3.txt#L2844-L3043) |
| Pasar | F, K (semua timeframe) |
| Status | 🟢 |

Notasi: **A** = awal impuls, **B** = akhir impuls, **C** = akhir koreksi. Ketiganya adalah swing ([D-01](00-aturan-global.md#d-01--swing-high-dan-swing-low)) di timeframe entry, diambil dari urutan swing terakhir (Q-12). Untuk tren naik:

| Target | Rumus | Arti |
|---|---|---|
| **V** | B + (B − C) | Pantulan sejauh dalamnya koreksi |
| **N** | C + (B − A) | Gelombang kedua sama panjang dengan yang pertama |
| **E** | B + (B − A) | Target terjauh |
| **NT** | C + (C − A) | Target terdekat |
| **S** | level B lama | Bekas resistance menjadi support; dipakai untuk mengukur sejauh mana pullback bisa turun |

Untuk tren turun, rumusnya dicerminkan ([forex_3 L2864–L3035](../materi/mentah/forex_3.txt#L2864-L3035)).

Target "M" adalah istilah buatan Rafał sendiri (double top 1:1); rumusnya di transkrip tidak jelas, jadi tidak dipakai.

**Kegunaan di rulebook:** TP untuk ICH-01 – ICH-03. Target harga yang bertepatan dengan target **waktu** Hosoda dibahas di [WKT-05](07-filter-waktu.md#wkt-05--angka-waktu-hosoda-ichimoku).

---

### Konteks: teori gelombang Hosoda (tidak dijadikan aturan)

| Gelombang | Bentuk |
|---|---|
| **I** | Satu impuls |
| **V** | Impuls + pullback |
| **N** | Naik–turun–naik dengan higher high & higher low (dasar semua gelombang) |
| **P** | Higher low + lower high (mengerucut) |
| **Y** | Higher high + lower low (melebar; menyapu SL dua arah; sulit ditradingkan) |
| **S** | Koreksi berhenti tepat di bekas resistance/support |

Rafał: pasar dihitung dalam **5 gerakan** (2 gelombang N); ambil untung setelah 5 gerakan. Gerakan 7 dan 9 "untuk profesional" ([forex_3 L1548–L1650](../materi/mentah/forex_3.txt#L1548-L1650), [forex_3 L1785–L1815](../materi/mentah/forex_3.txt#L1785-L1815)). Tidak dijadikan aturan karena penghitungan gerakannya subjektif, sama seperti Elliott Wave ([AFS-24](01-alvesting-akademi-crypto.md#afs-24--elliott-wave)).

Teori **waktu** Hosoda ada di [07 · WKT-05](07-filter-waktu.md#wkt-05--angka-waktu-hosoda-ichimoku).
