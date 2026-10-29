# 06 · MENTOR FOREX

Tiga sumber forex di folder Anda berasal dari orang yang **berbeda** dan tidak saling terkait ([PETA bagian 7](../materi/PETA.md#7-peta-forex)):

- [A. FXcopet](#a-fxcopet-forex_1) — scalping EURUSD M1 (2012).
- [B. Pola N](#b-pola-n-forex_2) — breakout di emas (XAUUSD). Nama mentornya tidak disebut; filosofi "pola N" ia sebut berasal dari "Pak Tito".
- [C. Ichimoku — Rafał Zuchowicz](#c-ichimoku--rafał-zuchowicz-forex_3) — kursus Ichimoku dari tulisan asli Goichi Hosoda (bahasa Inggris).

---

## A. FXcopet (forex_1)

### FXC-01 · Tembus garis merah/aqua, EURUSD M1

| | |
|---|---|
| Sumber | Aturan akhir: [forex_1 L3295–L3450](../materi/mentah/forex_1.txt#L3295-L3450); sesi live: [forex_1 L331–L3245](../materi/mentah/forex_1.txt#L331-L3245) |
| Pasar | F — **hanya EURUSD** |
| Timeframe | **M1** saja ("nggak perlu lihat timeframe lain") ([forex_1 L3305–L3314](../materi/mentah/forex_1.txt#L3305-L3314)) |
| Arah | Buy dan sell |
| Status | 🔴 (garisnya dari indikator khusus yang cara kerjanya tidak dijelaskan) |

**Alat:** indikator "copet" milik FXcopet, terdiri dari:

1. **Garis horizontal** otomatis: **merah** di atas, **aqua** di bawah. Ada juga garis miring merah/aqua. Garis merah dan aqua adalah **batas sideways**; di antaranya pasar belum punya arah ([forex_1 L731–L790](../materi/mentah/forex_1.txt#L731-L790), [forex_1 L811–L830](../materi/mentah/forex_1.txt#L811-L830)).
2. **TMA** (*Triangular Moving Average*) dengan pita, untuk membaca "gelombang dari high ke high, low ke low" ([forex_1 L299–L310](../materi/mentah/forex_1.txt#L299-L310), [forex_1 L431–L445](../materi/mentah/forex_1.txt#L431-L445)).

**Syarat:**

1. Garis merah (atas) dan garis aqua (bawah) **sudah terbentuk**. Kalau garis target belum terbentuk, sinyal dianggap palsu ([forex_1 L1011–L1029](../materi/mentah/forex_1.txt#L1011-L1029)).
2. Jarak garis merah–aqua **maksimal 15 pip**. Lebih dari 15 pip: **jangan trading** ([forex_1 L3355–L3374](../materi/mentah/forex_1.txt#L3355-L3374)).
3. Waktu: **sesi Eropa** (utama). Kalau tidak ada sinyal di sesi Eropa, boleh di sesi Asia ([forex_1 L3435–L3444](../materi/mentah/forex_1.txt#L3435-L3444)).
4. Tidak sedang ada berita besar (G-13).
5. Konfirmasi tambahan dari sesi live: buy saat harga di area **pita bawah TMA** (lembah), sell di area pita atas (puncak) ([forex_1 L1011–L1029](../materi/mentah/forex_1.txt#L1011-L1029), [forex_1 L1101–L1115](../materi/mentah/forex_1.txt#L1101-L1115)).

**Entry:**

- Harga **menembus garis merah ke atas** → **buy**.
- Harga **menembus garis aqua ke bawah** → **sell** ([forex_1 L3314–L3334](../materi/mentah/forex_1.txt#L3314-L3334)).

**Take profit** (pilih salah satu):

- **Minimal 10 pip** ([forex_1 L3334–L3350](../materi/mentah/forex_1.txt#L3334-L3350)).
- Di **garis horizontal berikutnya, dikurangi spread** (contoh spread 2 pip) ([forex_1 L611–L620](../materi/mentah/forex_1.txt#L611-L620), [forex_1 L925–L935](../materi/mentah/forex_1.txt#L925-L935)).
- **Tutup manual** di penutupan sesi Eropa. Transkrip menulis "**5.00 sampai 6.00 WIB**"; bisa mencapai 30–60 pip ([forex_1 L3350–L3364](../materi/mentah/forex_1.txt#L3350-L3364)).

**Stop loss:** di **garis horizontal berlawanan**, ditambah/dikurangi spread. Contoh buy: SL = garis aqua di bawahnya − 2 pip ([forex_1 L391–L400](../materi/mentah/forex_1.txt#L391-L400), [forex_1 L695–L705](../materi/mentah/forex_1.txt#L695-L705)). Kalau garis untuk SL belum terbentuk, posisi ditahan; kalau harga berbalik, **cut loss manual** ([forex_1 L626–L635](../materi/mentah/forex_1.txt#L626-L635), [forex_1 L861–L865](../materi/mentah/forex_1.txt#L861-L865)).

**Keluar lebih awal:** kalau garis target **menghilang** sebelum TP tercapai = tanda harga akan berbalik → *cut profit* atau *cut loss* ([forex_1 L1161–L1175](../materi/mentah/forex_1.txt#L1161-L1175)).

**Frekuensi:** maksimal 2 transaksi sehari; kalau sudah kena TP sekali, berhenti hari itu ([forex_1 L645–L659](../materi/mentah/forex_1.txt#L645-L659)). Sinyal bagus muncul maksimal ±3 kali seminggu ([forex_1 L3375–L3389](../materi/mentah/forex_1.txt#L3375-L3389)).

**Teknik "recover"** (⚠️ bertentangan dengan G-06): kalau posisi berbalik dan kena SL, tutup, lalu **buka arah sebaliknya** dengan target **2× kerugian**. Contoh: rugi 12 pip → target sell 24 pip ([forex_1 L3405–L3430](../materi/mentah/forex_1.txt#L3405-L3430)). Di sesi live, contoh lain: rugi 36 pip → target "40-an" ([forex_1 L705–L720](../materi/mentah/forex_1.txt#L705-L720)).

**Catatan:**

- Data dari 2012 (spread dan kondisi pasar berbeda). Klaim hasil "hampir 70%" dalam ±2 bulan, tanpa data tingkat menang ([forex_1 L3255–L3265](../materi/mentah/forex_1.txt#L3255-L3265)).
- Mentor sendiri: "tidak ada sistem yang sempurna"; kuncinya disiplin, money management, dan psikologi ([forex_1 L381–L390](../materi/mentah/forex_1.txt#L381-L390)).

**Belum jelas:**

- Cara indikator menggambar garis merah/aqua dan parameter TMA → **Q-31**.
- Teknik recover dipakai atau tidak → **Q-32**.
- "5.00–6.00 WIB" itu pagi atau sore → **Q-33**. Sesi Eropa (London) tutup sekitar 23.00–24.00 WIB, jadi angka ini perlu dipastikan. [PETA bagian 7.2](../materi/PETA.md#72-forex_1--tutorial-scalping-fxcopet-2012) menulis 17.00–18.00 WIB; itu tafsiran, bukan kata mentor.

---

## B. Pola N (forex_2)

### PLN-01 · Pola N: impuls → koreksi sempit → tembus

| | |
|---|---|
| Sumber | [forex_2 L460–L945](../materi/mentah/forex_2.txt#L460-L945) (price action), [forex_2 L945–L1105](../materi/mentah/forex_2.txt#L945-L1105) (manajemen risiko), [forex_2 L1105–L1465](../materi/mentah/forex_2.txt#L1105-L1465) (backtest), [forex_2 L1465–L2300](../materi/mentah/forex_2.txt#L1465-L2300) (rangkuman pola N) |
| Pasar | F (contoh di XAUUSD) |
| Timeframe | Backtest di **H1** (minimal 2 tahun) atau D1 ([forex_2 L1110–L1139](../materi/mentah/forex_2.txt#L1110-L1139)) |
| Arah | Buy dan sell, **searah arus** |
| Status | 🟡 |

**Prinsip:** ikuti arus pasar, jangan melawan. Mentor mengklaim mengikuti arus menang ±70–80% ([forex_2 L585–L609](../materi/mentah/forex_2.txt#L585-L609), [forex_2 L925–L934](../materi/mentah/forex_2.txt#L925-L934)).

**Syarat (versi buy; sell adalah cerminannya):**

1. **Impuls:** candle bullish kuat — badan penuh, wick sangat kecil, close menembus dengan "sempurna" ([forex_2 L615–L640](../materi/mentah/forex_2.txt#L615-L640)). Tiga candle badan searah berturut-turut disebut tanda pembeli masih dominan ±80% ([forex_2 L655–L670](../materi/mentah/forex_2.txt#L655-L670)).
2. **Koreksi kecil:** penjual melawan **sedikit** — hanya sedikit candle, ruangnya **sempit**, tidak lama "bertarung" ([forex_2 L1515–L1580](../materi/mentah/forex_2.txt#L1515-L1580), [forex_2 L1700–L1715](../materi/mentah/forex_2.txt#L1700-L1715)).
3. Bentuknya tidak harus huruf N; yang penting urutannya: **naik → turun sedikit → naik** ([forex_2 L1590–L1650](../materi/mentah/forex_2.txt#L1590-L1650)).

**Entry:** **buy stop** di atas wick tertinggi koreksi. Order terisi ketika harga menembus ([forex_2 L1650–L1659](../materi/mentah/forex_2.txt#L1650-L1659), [forex_2 L1200–L1229](../materi/mentah/forex_2.txt#L1200-L1229)).

**Varian:** kalau candle breakout sudah terlalu jauh, boleh **limit order di 50% candle impuls**, SL di atasnya (untuk sell) ([forex_2 L840–L869](../materi/mentah/forex_2.txt#L840-L869)).

**Stop loss:** di **"candle wick ke-2"**, yaitu candle sebelum *break of structure* — ekstrem dari koreksi ([forex_2 L1905–L1935](../materi/mentah/forex_2.txt#L1905-L1935), [forex_2 L2105–L2115](../materi/mentah/forex_2.txt#L2105-L2115)).

**Take profit:** dihitung dari RR **1:1,5 atau 1:2**. SL ditentukan dulu, baru TP ([forex_2 L1930–L1959](../materi/mentah/forex_2.txt#L1930-L1959)).

**Manajemen posisi:** *set and forget*. **Tanpa** TP1/TP2, **tanpa** geser ke titik impas ([forex_2 L1360–L1379](../materi/mentah/forex_2.txt#L1360-L1379), [forex_2 L1850–L1889](../materi/mentah/forex_2.txt#L1850-L1889)).

**Risiko:** maksimal 1% per transaksi; lot dihitung dengan kalkulator risiko ([forex_2 L1040–L1089](../materi/mentah/forex_2.txt#L1040-L1089)).

**Jangan ambil jika:**

- Konsolidasi **terlalu lama atau terlalu lebar** — rawan *fake out*, RR jelek ([forex_2 L1530–L1560](../materi/mentah/forex_2.txt#L1530-L1560), [forex_2 L1710–L1760](../materi/mentah/forex_2.txt#L1710-L1760), [forex_2 L2230–L2245](../materi/mentah/forex_2.txt#L2230-L2245)).
- Breakout-nya **lemah** (ditembus hanya oleh wick) ([forex_2 L1745–L1760](../materi/mentah/forex_2.txt#L1745-L1760)).
- Hanya breakout resistance biasa tanpa koreksi kecil; itu bukan pola N dan SL-nya terlalu jauh ([forex_2 L1670–L1699](../materi/mentah/forex_2.txt#L1670-L1699)).
- Pasar sedang tidak jelas: "diemin aja, jangan trading dulu" ([forex_2 L2140–L2149](../materi/mentah/forex_2.txt#L2140-L2149)).

**Waktu:** berita hanya mempercepat TP/SL; kalau mau aman, jangan trading saat berita. Mentor trading malam, di atas jam 18.00 ([forex_2 L2185–L2209](../materi/mentah/forex_2.txt#L2185-L2209)).

**Data backtest mentor** (contoh): tingkat menang ±67%, rugi beruntun terpanjang 5 kali, untung beruntun bisa 12–14 kali ([forex_2 L1410–L1449](../materi/mentah/forex_2.txt#L1410-L1449)).

**Pendapat lain mentor yang tidak dijadikan setup:**

- Support/resistance = area yang memantul **lebih dari 2 kali**. Dipakai untuk pandangan arah, **bukan** untuk entry ([forex_2 L31–L60](../materi/mentah/forex_2.txt#L31-L60), [forex_2 L355–L365](../materi/mentah/forex_2.txt#L355-L365)).
- Supply & demand tidak ia sukai: menunggu lama, sering kena SL dulu, tingkat menang di bawah 50% ([forex_2 L230–L345](../materi/mentah/forex_2.txt#L230-L345)).

**Belum jelas** → **Q-34**:

- "Koreksi sedikit / ruang sempit": berapa candle maksimal dan seberapa dalam (dibanding impuls)?
- "Candle kuat": seberapa kecil wick dibanding badan?
- Titik SL persis ("candle wick ke-2").
- Timeframe trading (H1?).

---

## C. Ichimoku — Rafał Zuchowicz (forex_3)

Kursus "Ichimoku King". Rafał mengaku belajar dari buku asli Goichi Hosoda ([forex_3 L1185–L1240](../materi/mentah/forex_3.txt#L1185-L1240)). Contoh-contohnya di AUD/CHF, USD/JPY, USD/TRY, minyak, dan DAX.

**Setting baku:** Tenkan **9**, Kijun **26**, Senkou Span B **52**. "Jangan diubah" ([forex_3 L3281–L3300](../materi/mentah/forex_3.txt#L3281-L3300), [forex_3 L3391–L3398](../materi/mentah/forex_3.txt#L3391-L3398)).

**Catatan teknis penting:** banyak platform menggeser **Chikou** keliru satu candle (menghitung candle hari ini sebagai nomor 1). Seharusnya tepat 26. Trik dari Rafał: matikan Chikou bawaan, lalu buat Chikou sendiri dengan pergeseran 25, atau SMA periode 1 yang digeser −25 ([forex_3 L2449–L2570](../materi/mentah/forex_3.txt#L2449-L2570)). Kumo juga bisa ikut tergeser keliru ([forex_3 L2809–L2835](../materi/mentah/forex_3.txt#L2809-L2835)) → **Q-36**.

**Arti tiap garis:**

| Garis | Rumus | Arti |
|---|---|---|
| **Tenkan** | (High + Low) ÷ 2 dari 9 candle terakhir | Trader jangka pendek ([forex_3 L1958–L2140](../materi/mentah/forex_3.txt#L1958-L2140)) |
| **Kijun** | (High + Low) ÷ 2 dari 26 candle | "Garis pasar / keseimbangan". Di atas = buy yang benar; di bawah = sell yang benar ([forex_3 L3399–L3420](../materi/mentah/forex_3.txt#L3399-L3420), [forex_3 L3499–L3520](../materi/mentah/forex_3.txt#L3499-L3520)) |
| **Senkou A** | (Tenkan + Kijun) ÷ 2, digeser 26 ke depan | Batas Kumo |
| **Senkou B** | (High + Low) ÷ 2 dari 52 candle, digeser 26 ke depan | Batas Kumo yang paling lambat berubah ([forex_3 L3589–L3630](../materi/mentah/forex_3.txt#L3589-L3630)) |
| **Kumo** | Ruang antara Senkou A dan B | Zona support/resistance ([forex_3 L3629–L3660](../materi/mentah/forex_3.txt#L3629-L3660)) |
| **Chikou** | Harga close digeser 26 ke belakang | "Ingatan pasar": dibandingkan dengan harga 26 periode lalu ([forex_3 L2569–L2610](../materi/mentah/forex_3.txt#L2569-L2610)) |

### ICH-01 · Tren penuh (harga, Tenkan–Kijun, Kumo, Chikou)

| | |
|---|---|
| Sumber | [forex_3 L2439–L2843](../materi/mentah/forex_3.txt#L2439-L2843), [forex_3 L3519–L3685](../materi/mentah/forex_3.txt#L3519-L3685), praktik live [forex_3 L1–L712](../materi/mentah/forex_3.txt#L1-L712) |
| Pasar | F, K |
| Timeframe | Bias dari **W1 & D1**, entry di **H4** ([forex_3 L1–L240](../materi/mentah/forex_3.txt#L1-L240)) |
| Status | 🟡 |

**Short (contoh yang paling lengkap di kursus):**

1. Harga **di bawah Kumo**.
2. **Chikou di bawah Kumo** dan di bawah harga 26 periode lalu.
3. **Tenkan di bawah Kijun** (*death cross*).
4. (Untuk posisi jangka panjang) **Kumo twist**: Kumo di masa depan sudah berbalik turun.
5. Rafał menyebutnya "sinyal jelas untuk jual" ([forex_3 L2689–L2700](../materi/mentah/forex_3.txt#L2689-L2700)).

**Long:** cerminannya. Rafał menambahkan: **buy hanya boleh** jika Chikou **di atas harga 26 periode lalu**, lebih baik juga di atas Kumo ([forex_3 L2655–L2665](../materi/mentah/forex_3.txt#L2655-L2665)). Kumo yang masih menurun = belum waktunya beli; tunggu Kumo twist ([forex_3 L3659–L3680](../materi/mentah/forex_3.txt#L3659-L3680)).

**Jangan masuk jika:** sudah *golden cross* tetapi harga **masih di dalam Kumo** atau tertahan Senkou B — tunggu ([forex_3 L2729–L2760](../materi/mentah/forex_3.txt#L2729-L2760)).

**Alur dari praktik live (USD/TRY)** ([forex_3 L1–L360](../materi/mentah/forex_3.txt#L1-L360)):

1. W1: candle **close di bawah Tenkan** dan gagal close kembali di atasnya → sinyal jual dari timeframe besar ([forex_3 L51–L90](../materi/mentah/forex_3.txt#L51-L90)).
2. D1: Chikou turun di bawah harga; harga sempat masuk Kumo lalu gagal ([forex_3 L101–L150](../materi/mentah/forex_3.txt#L101-L150)).
3. H4: hitung **waktu** (angka Hosoda, [WKT-05](07-filter-waktu.md#wkt-05--angka-waktu-hosoda-ichimoku)) dan **target harga** ([ICH-04](#ich-04--target-harga-hosoda-untuk-tp)).
4. **Entry:** candle **open dan close di bawah** level target NT (bekas support) + *death cross* + Chikou di bawah harga → "no brainer" ([forex_3 L311–L360](../materi/mentah/forex_3.txt#L311-L360)).

**Stop loss:** Rafał hanya bilang "selalu pasang stop loss yang tidak takut Anda pakai", **tanpa menyebut letaknya** ([forex_3 L355–L365](../materi/mentah/forex_3.txt#L355-L365)) → **Q-35**.

**Take profit:** di target harga ICH-04, terutama saat **target waktu bertepatan dengan target harga** atau level support/resistance. Boleh ambil 50–90% lalu sisanya digeser ke titik impas ([forex_3 L611–L705](../materi/mentah/forex_3.txt#L611-L705)) → **Q-08**.

---

### ICH-02 · Retest Kijun

| | |
|---|---|
| Sumber | [forex_3 L3429–L3500](../materi/mentah/forex_3.txt#L3429-L3500) |
| Pasar | F, K |
| Status | 🟡 |

**Long:**

1. Harga sudah menembus ke atas Kijun.
2. Harga kembali turun **menyentuh Kijun** dan **tidak close di bawahnya**.
3. → Buy. Rafał: "di situlah peluang beli yang bagus" ([forex_3 L3449–L3475](../materi/mentah/forex_3.txt#L3449-L3475)).

**Tanda bahaya:** candle **close di bawah Kijun** ([forex_3 L3475–L3490](../materi/mentah/forex_3.txt#L3475-L3490)).

**Short:** cerminannya.

**Belum jelas:** SL → **Q-35**.

---

### ICH-03 · Pullback ke Tenkan dalam tren kuat

| | |
|---|---|
| Sumber | [forex_3 L2148–L2438](../materi/mentah/forex_3.txt#L2148-L2438) |
| Pasar | F, K |
| Timeframe | Contoh di D1 |
| Status | 🟡 |

**Sinyal awal:** candle **kuat** close di atas Tenkan, dan Tenkan mulai naik. Candle kecil yang menembus lalu ditolak keesokan harinya = pasar belum siap ([forex_3 L2160–L2245](../materi/mentah/forex_3.txt#L2160-L2245)).

**Entry:** dalam tren kuat, setiap **pullback ke Tenkan yang bertahan** (tidak close di bawahnya) adalah tempat membuka atau menambah posisi ([forex_3 L2245–L2345](../materi/mentah/forex_3.txt#L2245-L2345)).

**Tanda berakhir:**

- Close kuat di bawah Tenkan selama 2 hari = kapitulasi ([forex_3 L2385–L2395](../materi/mentah/forex_3.txt#L2385-L2395)).
- Harga bolak-balik menembus Tenkan ke atas dan ke bawah = **sideways**; setup ini tidak berlaku ([forex_3 L2395–L2410](../materi/mentah/forex_3.txt#L2395-L2410)).

**Catatan:** "menambah posisi" di sini adalah menambah posisi yang **sedang untung** di pullback, bukan average down (G-04).

**Belum jelas:** SL → **Q-35**. Batas "candle kuat" → **Q-16**.

---

### ICH-04 · Target harga Hosoda untuk TP

| | |
|---|---|
| Sumber | [forex_3 L2844–L3043](../materi/mentah/forex_3.txt#L2844-L3043) |
| Pasar | F, K (semua timeframe) |
| Status | 🟢 (rumus lengkap; pemilihan titik A/B/C mengikuti Q-12) |

Notasi: **A** = awal impuls, **B** = akhir impuls, **C** = akhir koreksi. Untuk tren naik:

| Target | Rumus | Arti |
|---|---|---|
| **V** | B + (B − C) | Pantulan sejauh dalamnya koreksi |
| **N** | C + (B − A) | Gelombang kedua sama panjang dengan yang pertama |
| **E** | B + (B − A) | Target terjauh |
| **NT** | C + (C − A) | Target terdekat |
| **S** | level B lama | Bekas resistance menjadi support; dipakai untuk mengukur sejauh mana pullback bisa turun |

Untuk tren turun, rumusnya dicerminkan ([forex_3 L2864–L3035](../materi/mentah/forex_3.txt#L2864-L3035)).

Target "M" adalah istilah buatan Rafał sendiri (double top 1:1); rumusnya di transkrip tidak jelas, jadi tidak dipakai.

**Kegunaan di rulebook:** sebagai pilihan TP untuk setup lain ([ICH-01](#ich-01--tren-penuh-harga-tenkankijun-kumo-chikou), [KMS-02](02-kalimasada-akademi-crypto.md#kms-02--wyckoff-breakout-range--retest), dan lain-lain).

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
