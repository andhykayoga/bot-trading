# 01 · ALVESTING (AFS) — Akademi Crypto

Alvesting adalah pengajar teknikal Akademi Crypto. Materinya paling banyak dan paling sistematis, jadi ini **mesin utama** bot. Semua contoh di kelas memakai kripto (terutama BTC), tetapi hampir semuanya berlaku juga di forex. Angka yang khas kripto ditandai **K\*** / **F\***.

Aturan global ([00](00-aturan-global.md)) tetap berlaku di atas semua setup di halaman ini, termasuk definisi bersama ([D-01 – D-12](00-aturan-global.md#definisi-bersama)): swing, zona, retest, candle, volume, osilator, label scalping, dan batas hari & candle. Angka "Q-xx" merujuk ke jawaban Anda di [10](10-jawaban.md).

Setiap kartu setup sekarang punya baris **Label** (scalping/trading, [D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading)) dan **RR minimum** ([G-03](00-aturan-global.md#g-03--rr-minimum-115)).

## Daftar isi

- [A. Fondasi: Technical Research 5 tahap](#a-fondasi-technical-research-5-tahap)
  - [AFS-01 · Versi swing (D1 / H4 / M15)](#afs-01--technical-research-5-tahap-versi-swing)
  - [AFS-02 · Versi scalping (H1 / M15 / M5)](#afs-02--technical-research-5-tahap-versi-scalping)
  - [AFS-03 · Double top/bottom + tembus neckline](#afs-03--double-topbottom--tembus-neckline)
- [B. Fibonacci & area dinamis](#b-fibonacci--area-dinamis)
  - [AFS-04 · Golden pocket 0,5–0,618](#afs-04--pantulan-golden-pocket-fibonacci)
  - [AFS-05 · Money magnet EMA 13 & 21](#afs-05--money-magnet-ema-13--21)
- [C. Smart Money Concept (SMC)](#c-smart-money-concept-smc)
  - [AFS-06 · Stop hunt + break of structure](#afs-06--stop-hunt--break-of-structure)
  - [AFS-07 · CHoCH + retest](#afs-07--change-of-character-choch--retest)
  - [AFS-08 · Revisit order block / FVG](#afs-08--revisit-order-block--fair-value-gap)
- [D. Dow Theory](#d-dow-theory)
  - [AFS-09 · Validasi tembus 3%](#afs-09--validasi-tembus-3-dow-theory)
- [E. Pola harmonic & kamus pola](#e-pola-harmonic--kamus-pola)
  - [AFS-10 · ABCD](#afs-10--pola-abcd)
  - [AFS-11 · Harmonic XABCD](#afs-11--pola-harmonic-xabcd)
  - [AFS-23 · Pola grafik klasik](#afs-23--pola-grafik-klasik)
  - [AFS-24 · Elliott Wave](#afs-24--elliott-wave)
  - [AFS-25 · Andrews Pitchfork](#afs-25--andrews-pitchfork)
- [F. Indikator](#f-indikator)
  - [AFS-12 Pivot](#afs-12--pivot-point-entry-di-garis-p) · [AFS-13 Keltner](#afs-13--keltner-channel) ([13A tren](#afs-13a--mode-tren), [13B pantulan](#afs-13b--mode-pantulan)) · [AFS-14 Ichimoku](#afs-14--ichimoku-di-atasbawah-semua-garis) · [AFS-15 Parabolic SAR](#afs-15--parabolic-sar-titik-ke-2) · [AFS-16 Donchian](#afs-16--donchian-channel) · [AFS-17 KST](#afs-17--kst-silang-di-garis-nol) · [AFS-18 CMF](#afs-18--konfirmasi-chaikin-money-flow) · [AFS-19 POC](#afs-19--pantulan-poc-volume-profile) · [AFS-20 LRC](#afs-20--linear-regression-channel) · [AFS-21 Renko](#afs-21--renko-reversal)
- [G. Order flow (khusus kripto)](#g-order-flow-khusus-kripto)
  - [AFS-22](#afs-22--sinyal-order-flow)
- [H. Filter](#h-filter)
  - [AFS-F1 Screening altcoin & korelasi BTC](#afs-f1--screening-altcoin--korelasi-btc) · [AFS-F2 Konfirmasi volume](#afs-f2--konfirmasi-volume-untuk-breakout) · [AFS-F3 Momentum](#afs-f3--momentum-akselerasi--deselerasi)

---

## A. Fondasi: Technical Research 5 tahap

Kelas gratis Alvesting (5 modul). Ia menyebutnya "fondasi": **tren → area → pola → pemicu → entry/exit**. Setup lain di halaman ini pada dasarnya variasi dari alur ini.

### AFS-01 · Technical Research 5 tahap, versi swing

| | |
|---|---|
| Sumber | [AC_crypto_35](../materi/mentah/AC_crypto_35.txt) (tren), [AC_crypto_58 L1420–L2088](../materi/mentah/AC_crypto_58.txt#L1420-L2088) (area), [AC_crypto_57 L601–L1383](../materi/mentah/AC_crypto_57.txt#L601-L1383) (pola), [AC_crypto_57 L1384–L1873](../materi/mentah/AC_crypto_57.txt#L1384-L1873) (pemicu), [AC_crypto_59 L2640–L3149](../materi/mentah/AC_crypto_59.txt#L2640-L3149) (entry & exit) |
| Pasar | K, F |
| Timeframe | Tren **D1**, pola **H4**, pemicu **M15** ([AC_crypto_35 L250–L279](../materi/mentah/AC_crypto_35.txt#L250-L279)) |
| Arah | Long dan short |
| Label | Trading |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Syarat 1 — Tren (D1).** Tentukan bias dengan struktur ([D-02](00-aturan-global.md#d-02--struktur-dan-tren)).

- **Bullish** = struktur membuat **minimal 2 higher low dan 2 higher high**. Sebuah higher low tetap valid selama low sebelumnya tidak ditembus. Tembusnya high sebelumnya = *break of structure* ke atas ([AC_crypto_35 L370–L429](../materi/mentah/AC_crypto_35.txt#L370-L429)). → bias **long**.
- **Bearish** = minimal 2 lower high dan 2 lower low ([AC_crypto_35 L425–L469](../materi/mentah/AC_crypto_35.txt#L425-L469)). → bias **short**.
- **Sideways** = bukan keduanya (mentor: *equal high* dan *equal low* di range sempit, [AC_crypto_35 L460–L499](../materi/mentah/AC_crypto_35.txt#L460-L499)). → **tidak ada bias**, setup ini tidak dipakai. Mentor: kalau tidak tahu arah pasar, jangan berharap untung ([AC_crypto_35 L80–L99](../materi/mentah/AC_crypto_35.txt#L80-L99)).
- **Alat bantu tren: trendline saja** (poin 3 di daftar 5 poin): garis diagonal lewat minimal 2 titik. Uptrend digambar di bawah harga; harga yang memantul di trendline = peluang long; tembus ke bawah = tanda pembalikan. Downtrend sebaliknya ([AC_crypto_35 L500–L579](../materi/mentah/AC_crypto_35.txt#L500-L579)).
- Mentor juga menyebut **moving average** (contoh MA20/MA10 di D1, MA50 sebagai penolak di downtrend), **Bollinger Bands**, dan **Supertrend** ([AC_crypto_35 L590–L649](../materi/mentah/AC_crypto_35.txt#L590-L649), [AC_crypto_35 L690–L705](../materi/mentah/AC_crypto_35.txt#L690-L705)). **Tidak dipakai di AFS-01** (Q-46): indikator tren setup ini sudah **pita EMA 13–21** (sumber area di syarat 2), dan mentor sendiri bilang memakai dua indikator tren sekaligus, misalnya EMA dan Bollinger, itu salah ([AC_crypto_61 L2210–L2217](../materi/mentah/AC_crypto_61.txt#L2210-L2217)) (G-11).

**Syarat 2 — Area.** Posisi hanya dibuka di area yang tepat.

- Long **hanya** di support/demand. Short **hanya** di resistance/supply. Jangan long di resistance, jangan short di support ([AC_crypto_58 L1475–L1499](../materi/mentah/AC_crypto_58.txt#L1475-L1499)).
- Support/resistance digambar sebagai **zona** (kotak), bukan satu garis, karena harga "pasti copy di sekitar situ" ([AC_crypto_58 L1645–L1699](../materi/mentah/AC_crypto_58.txt#L1645-L1699)). Tebalnya ± 0,5 × ATR(14) ([D-04](00-aturan-global.md#d-04--zona-support-dan-resistance), Q-17).
- Lima cara menemukan area ([AC_crypto_58 L1640–L2060](../materi/mentah/AC_crypto_58.txt#L1640-L2060)). Harga dianggap "di area" kalau menyentuh **minimal satu**:
  1. Zona horizontal dari swing H4 (D-04).
  2. Trendline sebagai support/resistance diagonal: garis lewat 2 swing terakhir (D-01).
  3. Area dinamis dari indikator: pita EMA 13 & 21 ([AFS-05](#afs-05--money-magnet-ema-13--21)).
  4. Pivot point: P, S1–S3, R1–R3 ([AFS-12](#afs-12--pivot-point-entry-di-garis-p)).
  5. Fibonacci: *golden pocket* 0,5–0,618 dari impuls terakhir ([AFS-04](#afs-04--pantulan-golden-pocket-fibonacci)).
- Makin banyak alat yang bertemu di area yang sama (*confluence*), makin bagus setup-nya ([AC_crypto_58 L2063–L2088](../materi/mentah/AC_crypto_58.txt#L2063-L2088)).

**Syarat 3 — Pola (H4).** Ada pola harga yang searah bias di area tersebut. Pola **bukan alat utama**, hanya konfirmasi; tren dan area harus beres dulu ([AC_crypto_57 L1341–L1380](../materi/mentah/AC_crypto_57.txt#L1341-L1380)). Contoh dari mentor: double bottom ([AC_crypto_35 L260–L269](../materi/mentah/AC_crypto_35.txt#L260-L269)) dan falling wedge di support ([AC_crypto_57 L1560–L1569](../materi/mentah/AC_crypto_57.txt#L1560-L1569)). Di versi pertama, pola yang dikenali bot hanya **double/triple top-bottom** ([AFS-03](#afs-03--double-topbottom--tembus-neckline)) dan **ABCD** ([AFS-10](#afs-10--pola-abcd)) (Q-23). Pola **tetap wajib** (Q-46): pola memang bukan alat utama, tetapi menurut mentor di support harus terlihat pola dulu, misalnya double bottom, "baru kamu bisa masuk" ([AC_crypto_57 L1360–L1371](../materi/mentah/AC_crypto_57.txt#L1360-L1371)). Versi **tanpa syarat pola** diuji sebagai pembanding ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)).

**Syarat 4 — Pemicu (M15).** M15 disebut timeframe paling ideal untuk melihat pemicu ([AC_crypto_57 L1484–L1503](../materi/mentah/AC_crypto_57.txt#L1484-L1503)). Pemicu (salah satu cukup):

- **Candlestick** ([D-06](00-aturan-global.md#d-06--candle)): long → *hammer*, *inverted hammer*, *bullish engulfing*. Short → *hanging man*, *shooting star*, *bearish engulfing*. Engulfing dan hanging man dengan volume tinggi dianggap lebih kuat ([AC_crypto_57 L1500–L1713](../materi/mentah/AC_crypto_57.txt#L1500-L1713)).
- **Osilator**: **Stochastic 5,3,3** (setting favorit Alvesting): silang naik di area jenuh jual (< 20) → long; silang turun di area jenuh beli (> 80) → short ([D-08](00-aturan-global.md#d-08--osilator)). Mentor juga menyebut RSI dan MACD ([AC_crypto_57 L1744–L1800](../materi/mentah/AC_crypto_57.txt#L1744-L1800)), tetapi G-11 membatasi satu osilator, jadi bot memakai Stochastic saja.
- **Volume**: breakout tanpa volume cenderung palsu ([AFS-F2](#afs-f2--konfirmasi-volume-untuk-breakout)).

**Daftar 5 poin (Q-18).** Mentor bilang setup "sempurna" kalau kelima poin ini muncul bersamaan ([AC_crypto_35 L650–L729](../materi/mentah/AC_crypto_35.txt#L650-L729)). Bot masuk kalau **minimal 4 poin** terpenuhi, dengan **poin 1, 2, dan 4 wajib**. Versi 5 dari 5 diuji sebagai pembanding.

| Poin | Kata mentor | Cara bot mengukurnya |
|---|---|---|
| 1 | Tren terlihat "secara kasat mata" | Disamakan dengan poin 2 (Q-46). Mentor menyebut keduanya bersamaan: "secara kasat mata dia naik ya, selalu membuat dua higher low" ([AC_crypto_35 L672–L673](../materi/mentah/AC_crypto_35.txt#L672-L673)) |
| 2 | Struktur minimal 2 higher low & 2 higher high | Syarat 1 (D-02) |
| 3 | Trendline dihormati | Garis lewat 2 swing low terakhir (uptrend) atau 2 swing high terakhir (downtrend) di D1; dihormati = belum ada candle close yang menembus garis sejak swing kedua |
| 4 | Harga di area support/resistance | Syarat 2 |
| 5 | Indikator mendukung | **Stochastic 5,3,3** di timeframe pemicu (M15): pada candle pemicu, %K **di bawah 20** untuk long, **di atas 80** untuk short (Q-46) |

Karena poin 1 disamakan dengan poin 2, aturan "4 dari 5" berarti: poin 2 dan 4 wajib, ditambah **minimal satu** dari poin 3 dan 5.

Kenapa Stochastic untuk poin 5 (Q-46): Stochastic 5,3,3 bersama EMA 13/21 adalah kombinasi yang menurut Akademi Crypto sudah mereka riset dan pakai bertahun-tahun ([AC_crypto_61 L2258–L2262](../materi/mentah/AC_crypto_61.txt#L2258-L2262), [AC_crypto_57 L1779–L1782](../materi/mentah/AC_crypto_57.txt#L1779-L1782)). Di contoh lengkap mentor, M15 *oversold* dan ada hammer, "baru execute" ([AC_crypto_57 L1863–L1865](../materi/mentah/AC_crypto_57.txt#L1863-L1865)).

**Contoh lengkap dari mentor:** D1 naik → long di support → H4 ada double bottom → M15 stochastic jenuh jual + hammer → eksekusi ([AC_crypto_57 L1854–L1873](../materi/mentah/AC_crypto_57.txt#L1854-L1873)).

**Entry:** order pasar setelah candle pemicu M15 close.

**Stop loss:** long = swing low H4 terakhir di bawah harga entry − 1 × ATR(14) H4; short = swing high H4 terakhir + 1 × ATR(14) H4 ([G-02](00-aturan-global.md#g-02--stop-loss-wajib-di-titik-analisa-saya-salah), Q-11; mentor: [AC_crypto_59 L2740–L2859](../materi/mentah/AC_crypto_59.txt#L2740-L2859)).

**Take profit:** di area lawan: long → zona resistance H4 **terdekat** yang RR-nya minimal 1:1,5; short → zona support terdekat ([AC_crypto_59 L2710–L2739](../materi/mentah/AC_crypto_59.txt#L2710-L2739); Q-08). Mentor juga menyebut angka psikologis (angka bulat), Fibonacci, dan pivot sebagai alternatif ([AC_crypto_59 L2760–L2809](../materi/mentah/AC_crypto_59.txt#L2760-L2809)); tidak dipakai, karena "angka bulat" tidak punya ukuran dan bot memakai satu jenis target.

**Lama memegang posisi:** mentor menahan long lebih lama saat pasar bull, dan mengambil untung bertahap saat pasar bear ([AC_crypto_35 L120–L149](../materi/mentah/AC_crypto_35.txt#L120-L149)). Tidak dipakai: satu TP, satu SL (Q-08).

**Batal / jangan masuk jika:**

- Pasar sideways (tidak ada bias).
- Harga tidak berada di area yang tepat.
- Tidak ada zona lawan yang memberi RR minimal 1:1,5.

---

### AFS-02 · Technical Research 5 tahap, versi scalping

| | |
|---|---|
| Sumber | [AC_crypto_58 L2825–L3220](../materi/mentah/AC_crypto_58.txt#L2825-L3220) (dasar scalping), [AC_crypto_62 L3589–L3886](../materi/mentah/AC_crypto_62.txt#L3589-L3886) (persiapan teknikal), [AC_crypto_46](../materi/mentah/AC_crypto_46.txt) (mental) |
| Pasar | K, F |
| Timeframe | Tren **H1**, pola **M15**, pemicu **M5** ([AC_crypto_62 L3709–L3728](../materi/mentah/AC_crypto_62.txt#L3709-L3728)) |
| Arah | Dua arah dalam satu hari (long lalu short, atau sebaliknya) ([AC_crypto_62 L3609–L3668](../materi/mentah/AC_crypto_62.txt#L3609-L3668)) |
| Label | **Scalping** |
| RR minimum | 1:2 |
| Status | 🟢 |

**Aturan:** sama persis dengan AFS-01 (termasuk daftar 5 poin), tetapi timeframe-nya "dikompres": tren H1, area & pola M15, pemicu M5. SL dan zona memakai ATR(14) dari timeframe masing-masing. Ditambah aturan khusus scalping:

1. **Risiko:** **0,5%** per transaksi (Q-01). Mentor: 0,5%–1%, maksimal 2% ([AC_crypto_58 L3055–L3104](../materi/mentah/AC_crypto_58.txt#L3055-L3104), [AC_crypto_62 L3669–L3688](../materi/mentah/AC_crypto_62.txt#L3669-L3688)).
2. **RR minimum 1:2.** Mentor: harus lebih dari 1:1 karena biaya transaksi dan *funding*; targetkan 1:2 atau 1:3; 1:4–1:5 sangat sulit ([AC_crypto_58 L3113–L3134](../materi/mentah/AC_crypto_58.txt#L3113-L3134)).
3. **Frekuensi:** mentor: 3–5 transaksi sehari sudah banyak ([AC_crypto_58 L3175–L3194](../materi/mentah/AC_crypto_58.txt#L3175-L3194)). Batas bot: 3 transaksi baru per hari untuk semua instrumen ([G-08](00-aturan-global.md#g-08--jangan-overtrading)).
4. **Durasi:** posisi **ditutup setelah 3 jam** walaupun belum kena TP/SL (Q-19). Mentor: "kalau scalping itu maksimal tiga jam" ([AC_crypto_58 L3053](../materi/mentah/AC_crypto_58.txt#L3053)); lebih dari 24 jam bukan scalping lagi ([AC_crypto_58 L3015–L3054](../materi/mentah/AC_crypto_58.txt#L3015-L3054)). Pembanding di backtest: 24 jam.
5. **Berita:** posisi ditutup sebelum berita besar ([G-13](00-aturan-global.md#g-13--berita-besar)).
6. **Gaya SL:** mentor membandingkan dua gaya. SL tipis + RR besar = menang hanya 30–40% tetapi sekali menang besar. SL lebar + RR 1:2 = menang 70–80%. Untuk trading setiap hari, mentor menyarankan **SL lebar, RR rendah** ([AC_crypto_62 L3765–L3878](../materi/mentah/AC_crypto_62.txt#L3765-L3878)). Ini sejalan dengan SL swing ± 1 × ATR (G-02).

**Contoh dari mentor** ([AC_crypto_62 L3719–L3768](../materi/mentah/AC_crypto_62.txt#L3719-L3768)): H1 masih bearish, tetapi terbentuk *descending broadening wedge* lalu breakout dan retest → bias long. M15: cari area, ada breakout + retest. M5: ada double bottom, breakout → entry. SL di bawah area. TP1, TP2, TP3 → bot memakai satu TP, yaitu target terdekat yang RR-nya minimal 1:2 (Q-08).

**Poin 5** diukur dengan Stochastic 5,3,3 di **M5**, timeframe pemicu versi ini (Q-46).

---

### AFS-03 · Double top/bottom + tembus neckline

| | |
|---|---|
| Sumber | [AC_crypto_58 L3135–L3175](../materi/mentah/AC_crypto_58.txt#L3135-L3175), [AC_crypto_57 L1121–L1189](../materi/mentah/AC_crypto_57.txt#L1121-L1189), [AC_crypto_57 L1271–L1300](../materi/mentah/AC_crypto_57.txt#L1271-L1300) |
| Pasar | K, F |
| Timeframe | M15 (contoh scalping) |
| Arah | Short (double top), long (double bottom) |
| Label | **Scalping** (Q-45): diajarkan di pelajaran scalping, dengan contoh double top di M15 ([AC_crypto_58 L3135–L3153](../materi/mentah/AC_crypto_58.txt#L3135-L3153)) |
| RR minimum | 1:2 (TP mentor) |
| Status | 🟢 |

**Syarat:**

1. Terbentuk double top: dua puncak (swing high, D-01) yang hampir sama tinggi (*equal high*) dan gagal ditembus. **"Hampir sama tinggi"** = selisih kedua puncak paling banyak **0,5 × ATR(14)** (nilai awal; diuji 0,25× · 0,5× · 0,75×) (Q-23). Boleh triple top. **Tidak ada** "quadruple": setelah sentuhan ke-3 harga biasanya memilih arah ([AC_crypto_57 L1131–L1169](../materi/mentah/AC_crypto_57.txt#L1131-L1169)). Kalau muncul puncak ke-4 yang sama tinggi, pola batal.
2. **Neckline** = low terendah di antara puncak-puncak itu.

**Entry — versi konfirmasi (default, Q-09):** order pasar saat candle **close di bawah neckline**.
**SL:** puncak tertinggi + 1 × ATR(14) (G-02).
**TP:** **1:2** dari jarak entry–SL ([AC_crypto_58 L3135–L3159](../materi/mentah/AC_crypto_58.txt#L3135-L3159)).

**Entry — versi antisipasi (pembanding, Q-09):** masuk **sebelum** neckline tembus. Mentor: SL beberapa persen di atas swing high, target sama, RR bisa 1:6; makin besar RR yang diinginkan, makin presisi entry dan makin tipis SL-nya ([AC_crypto_58 L3155–L3179](../materi/mentah/AC_crypto_58.txt#L3155-L3179)). Untuk bot: masuk saat puncak kedua (atau ketiga) **diakui** sebagai swing high (D-01) dan harga masih di atas neckline; SL sama dengan versi konfirmasi; TP di **harga yang sama** dengan TP versi konfirmasi.

Double bottom = cerminannya (long).

**Aturan scalping** ([D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading)): risiko 0,5%, posisi ditutup setelah 3 jam, dan ditutup sebelum berita besar.

---

## B. Fibonacci & area dinamis

### AFS-04 · Pantulan golden pocket Fibonacci

| | |
|---|---|
| Sumber | Fibonacci Secret: [AC_crypto_60 L1–L346](../materi/mentah/AC_crypto_60.txt#L1-L346), [AC_crypto_58 L3476–L3643](../materi/mentah/AC_crypto_58.txt#L3476-L3643), [AC_crypto_59 L824–L953](../materi/mentah/AC_crypto_59.txt#L824-L953), [AC_crypto_62 L2625–L2790](../materi/mentah/AC_crypto_62.txt#L2625-L2790), [AC_crypto_42](../materi/mentah/AC_crypto_42.txt), [AC_crypto_56](../materi/mentah/AC_crypto_56.txt); juga [AC_crypto_58 L1980–L2060](../materi/mentah/AC_crypto_58.txt#L1980-L2060) |
| Pasar | K, F\* |
| Timeframe | Paling valid **W1 / MN**; D1 masih oke. M1–M5 disebut "judi berlogika" ([AC_crypto_56 L41–L80](../materi/mentah/AC_crypto_56.txt#L41-L80)). Bot: **D1 dan W1** |
| Arah | Long saat koreksi dalam uptrend; short saat *relief pump* dalam downtrend |
| Label | Trading |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Syarat (versi long; short cerminannya):**

1. Struktur bullish (D-02). **Impuls** = gerakan dari swing low terakhir ke swing high terakhir (D-01, Q-12), lalu harga koreksi turun.
2. Tarik Fibonacci retracement dari **low ke high** impuls (uptrend) atau **high ke low** (downtrend) ([AC_crypto_60 L141–L169](../materi/mentah/AC_crypto_60.txt#L141-L169)).
3. Harga masuk **golden pocket 0,5–0,618**. Mentor: harga "sampai 80%" mengunjungi area ini ([AC_crypto_60 L191–L230](../materi/mentah/AC_crypto_60.txt#L191-L230)).
4. **Fokus hanya di golden pocket.** Level 0,236 / 0,382 / 0,786 juga bisa jadi pantulan, tetapi menurut rangkuman mentor peluangnya hanya sekitar 20% ([AC_crypto_56 L75–L99](../materi/mentah/AC_crypto_56.txt#L75-L99)).
5. **Wajib confluence**: golden pocket bertumpuk dengan minimal satu support lain: zona horizontal (D-04), trendline (garis lewat 2 swing low terakhir), atau **MA100** (MA biasa, bawaan TradingView). Contoh mentor: golden pocket + MA100 + support horizontal ([AC_crypto_56 L95–L139](../materi/mentah/AC_crypto_56.txt#L95-L139)). Pita EMA 13–21 tidak dipakai di setup ini: G-11 membatasi satu indikator tren per setup, dan contoh mentor untuk setup ini memakai MA100.
6. Ada **pemicu** di area itu, seperti di AFS-01 ([AC_crypto_58 L3525–L3534](../materi/mentah/AC_crypto_58.txt#L3525-L3534)). Pemicu ini dipakai versi antisipasi.

**Dua cara entry yang diajarkan:**

- **Versi konfirmasi (default, Q-09):** setelah harga menyentuh golden pocket, harga berbalik naik **p%** dari low koreksi → order pasar saat candle itu close. Mentor: trendline koreksi tembus atau harga "belok" sekitar **3–5%**; pada titik itu low koreksi sah menjadi higher low ([AC_crypto_60 L201–L219](../materi/mentah/AC_crypto_60.txt#L201-L219), [AC_crypto_62 L2690–L2709](../materi/mentah/AC_crypto_62.txt#L2690-L2709)).
  - Kripto: p diuji **3% · 4% · 5%** (rentang mentor).
  - Forex & emas: p diganti **k × ATR(14) harian** ([D-09](00-aturan-global.md#d-09--angka-persen-kripto-di-forex), Q-10).
- **Versi antisipasi (pembanding):** di golden pocket, saat candle pemicu close.

**SL:**

- Long: low koreksi − 1 × ATR(14) (G-02).
- Short: di atas **level 1** (titik awal impuls turun) + 1 × ATR(14). Kalau level 1 tembus, tren dianggap berbalik ([AC_crypto_59 L884–L903](../materi/mentah/AC_crypto_59.txt#L884-L903)).

**TP:** ekstensi Fibonacci. Mentor menarik Fibonacci dari high ke low impuls, sehingga level **1 = high sebelumnya**, lalu **1,618**, **2,618**, **3,618**, **4,236** ([AC_crypto_60 L231–L262](../materi/mentah/AC_crypto_60.txt#L231-L262), [AC_crypto_60 L321–L340](../materi/mentah/AC_crypto_60.txt#L321-L340)). Rumus untuk long:

```
level_r = low impuls + r × (high impuls − low impuls),   r = 1; 1,618; 2,618; 3,618; 4,236
```

Bot memakai **satu TP**: level terdekat yang RR-nya minimal 1:1,5 (Q-08). Pembanding: 50% di TP itu, sisanya SL ke titik impas dan mengincar level berikutnya.

Mentor juga menyebut *trend-based Fib extension* (impuls utama + koreksi) sebagai alat yang lebih praktis ([AC_crypto_62 L2685–L2744](../materi/mentah/AC_crypto_62.txt#L2685-L2744)). Tidak dipakai, supaya hanya ada satu cara menghitung target.

**Saat harga menembus ATH/ATL** (*price discovery*, tidak ada level harga di kiri), target tetap dari ekstensi 1,618 / 2,618 / 3,618 ([AC_crypto_58 L3586–L3643](../materi/mentah/AC_crypto_58.txt#L3586-L3643), [AC_crypto_59 L914–L953](../materi/mentah/AC_crypto_59.txt#L914-L953)).

**Batal:** harga menembus low impuls (level 0) sebelum entry.

---

### AFS-05 · Money magnet EMA 13 & 21

| | |
|---|---|
| Sumber | [AC_crypto_58 L1745–L1789](../materi/mentah/AC_crypto_58.txt#L1745-L1789); setting diklaim sudah diriset bertahun-tahun: [AC_crypto_61 L2253–L2262](../materi/mentah/AC_crypto_61.txt#L2253-L2262) |
| Pasar | K, F |
| Timeframe | Tidak disebut mentor → diuji **H1, H4, D1** (setara), dipilih dengan aturan G-17 (Q-47) |
| Arah | Long dalam uptrend (cerminannya untuk downtrend) |
| Label | Trading |
| RR minimum | TP tetap: 1:2 (entry H1) / 1:3 (H4, D1) (Q-07) |
| Status | 🟢 |

**Aturan:** dua EMA, **13 dan 21**, bekerja seperti magnet. Dalam uptrend, setiap koreksi "selalu mencari" area EMA 13–21 lalu memantul → **long di area EMA**. Mentor menyebutnya *dynamic support*, lebih cocok dengan pergerakan kripto yang sangat volatil dibanding garis horizontal atau diagonal ([AC_crypto_58 L1765–L1819](../materi/mentah/AC_crypto_58.txt#L1765-L1819)).

Setup ini terutama dipakai sebagai **sumber area** di AFS-01. Kalau berdiri sendiri:

- **Tren:** struktur bullish (D-02) untuk long, bearish untuk short.
- **Entry (Q-47):** harga menyentuh pita EMA 13–21, lalu **tunggu pemicu** di pita itu, di timeframe yang sama. Pemicunya sama dengan syarat 4 AFS-01: candle pemicu ([D-06](00-aturan-global.md#d-06--candle)), atau Stochastic 5,3,3 silang di area jenuh ([D-08](00-aturan-global.md#d-08--osilator)) → order pasar saat candle pemicu close. Di contoh WLD, mentor masuk di area EMA 13–21 setelah Stochastic *oversold* dan silang, ditambah pola ([AC_crypto_33 L1849–L1900](../materi/mentah/AC_crypto_33.txt#L1849-L1900)).
- **SL:** swing low terakhir − 1 × ATR(14) (G-02).
- **TP:** mentor tidak menyebut target → TP tetap 1:2 atau 1:3 sesuai timeframe entry (Q-07).

---

## C. Smart Money Concept (SMC)

Fokus SMC adalah **likuiditas** (kumpulan stop loss), bukan tren. Hanya relevan untuk aset likuid besar ([AC_crypto_61 L1–L129](../materi/mentah/AC_crypto_61.txt#L1-L129)). Forex mayor sangat likuid, jadi cocok.

**Istilah:**

- **BSL** (*buy-side liquidity*): tumpukan SL di **atas** high. Lokasinya: high bulan lalu (PMH), minggu lalu (PWH), kemarin (PDH), dan swing high sebelumnya ([AC_crypto_34 L190–L209](../materi/mentah/AC_crypto_34.txt#L190-L209)).
- **SSL** (*sell-side liquidity*): tumpukan SL di **bawah** low: PML, PWL, PDL, swing low sebelumnya ([AC_crypto_34 L330–L349](../materi/mentah/AC_crypto_34.txt#L330-L349)).
- **Stop hunt (SH)**: harga menembus BSL/SSL dengan agresif, lalu **kembali ke dalam range** (*return to origin*, RTO) ([AC_crypto_34 L565–L589](../materi/mentah/AC_crypto_34.txt#L565-L589)).
- **BOS / BMS** (*break of structure*): harga **close** di atas high atau di bawah low tertentu. Hanya wick tidak dihitung ([AC_crypto_36 L41–L59](../materi/mentah/AC_crypto_36.txt#L41-L59)).

**Aturan umum SMC** ([AC_crypto_34 L461–L560](../materi/mentah/AC_crypto_34.txt#L461-L560)):

1. Tren timeframe besar tetap lebih penting (D1 > H1, H4 > M15).
2. Perhatikan support/resistance dan *equal high* / *equal low*.
3. Tunggu pullback supaya RR lebih baik; antisipasi breakout, jangan dikejar.
4. Kombinasi waktu: **H4 untuk arah, M15 untuk pemicu**.

**Aturan bersama AFS-06 – AFS-08 (Q-20):**

- **Timeframe:** pola dan entry di **M15**. Arah tidak boleh melawan struktur **H4** (D-02): short tidak diambil kalau H4 bullish, long tidak diambil kalau H4 bearish. *(Terjemahan saya dari "H4 untuk arah".)*
- **Likuiditas acuan:** BSL = PDH, PWH, PMH, dan swing high M15 sebelumnya; SSL = PDL, PWL, PML, dan swing low M15 sebelumnya. Batas hari, minggu, dan bulannya mengikuti [D-12](00-aturan-global.md#d-12--batas-hari-minggu-dan-candle).
- **TP:** likuiditas **terdekat** di sisi lawan: PDH/PDL, PWH/PWL, atau swing high/low. Masuk **hanya** kalau RR ke sana minimal **1:2** (mentor: 1:2 jangka pendek, [AC_crypto_58 L730–L739](../materi/mentah/AC_crypto_58.txt#L730-L739)). Bot tidak mencari target yang lebih jauh.
- **SL:** swing (puncak/lembah) yang menjadi titik invalidasi ± 1 × ATR(14) M15 (G-02).
- **Label:** trading. **RR minimum:** 1:2.

### AFS-06 · Stop hunt + break of structure

| | |
|---|---|
| Sumber | [AC_crypto_34 L560–L824](../materi/mentah/AC_crypto_34.txt#L560-L824), [AC_crypto_58 L1010–L1040](../materi/mentah/AC_crypto_58.txt#L1010-L1040), [AC_crypto_59 L255–L370](../materi/mentah/AC_crypto_59.txt#L255-L370) |
| Pasar | K (aset besar), F |
| Timeframe | H4 arah, M15 pemicu; makin besar timeframe makin valid |
| Arah | Short setelah BSL disapu; long setelah SSL disapu |
| Label | Trading |
| RR minimum | 1:2 |
| Status | 🟢 |

Mentor menyebut ini "kombinasi paling ampuh" dan menyarankan fokus di sini saja: "keep it simple" ([AC_crypto_59 L351–L370](../materi/mentah/AC_crypto_59.txt#L351-L370)). Klaim tingkat menang 70–80%, makin tinggi di timeframe besar ([AC_crypto_34 L705–L724](../materi/mentah/AC_crypto_34.txt#L705-L724)).

**Short:**

1. Harga sedang naik, membentuk higher low (M15).
2. **Stop hunt:** harga menembus **high acuan** (BSL) minimal **0,1 × ATR(14)** (nilai awal; diuji 0,05× · 0,1× · 0,15×) (Q-20). Short yang terlalu awal dan long yang ikut breakout sama-sama tersapu.
3. **Kembali ke range (RTO):** sebuah candle **close kembali di bawah** high acuan dalam **3 candle atau kurang** sejak tembus (nilai awal; diuji 2 · 3 · 4) (Q-20).
4. **BMS:** candle **close di bawah higher low terakhir** ([D-02](00-aturan-global.md#d-02--struktur-dan-tren)).
5. → **Short** ([AC_crypto_34 L665–L700](../materi/mentah/AC_crypto_34.txt#L665-L700), [AC_crypto_34 L720–L760](../materi/mentah/AC_crypto_34.txt#L720-L760)).

**Dua cara masuk, keduanya dari mentor dan keduanya diuji** (Q-20):

- **(a)** Order pasar saat candle BMS close ("keep it simple", [AC_crypto_59 L351–L370](../materi/mentah/AC_crypto_59.txt#L351-L370)).
- **(b)** Order limit di FVG bearish ([AFS-08](#afs-08--revisit-order-block--fair-value-gap)) yang terbentuk di gerakan turun penyebab BMS ("BOS + order block = perfect combo", [AC_crypto_59 L385–L400](../materi/mentah/AC_crypto_59.txt#L385-L400)). Order **batal** kalau tidak terisi dalam **20 candle M15** (nilai awal; diuji 10 · 20 · 30) atau kalau harga sudah menyentuh TP lebih dulu.

**SL:** di atas puncak stop hunt + 1 × ATR(14) ([AC_crypto_59 L351–L360](../materi/mentah/AC_crypto_59.txt#L351-L360)).

**Batal:** harga membuat high baru di atas puncak stop hunt sebelum BMS terjadi.

**Long:** cerminannya. Harga turun → menembus **low acuan** (SSL) → close kembali di atasnya → **lower high terakhir ditembus** → long, SL di bawah lembah stop hunt − 1 × ATR ([AC_crypto_34 L700–L719](../materi/mentah/AC_crypto_34.txt#L700-L719), [AC_crypto_34 L765–L819](../materi/mentah/AC_crypto_34.txt#L765-L819)).

**Variasi yang disebut mentor jarang terjadi** (*liquidity pattern*: CHoCH + quick RTO, CHoCH + late RTO, *confirmation entry*, SH + *fake* BMS). Mentor sendiri bilang sekitar 80% tidak terjadi, jadi cukup fokus ke SH + BMS ([AC_crypto_58 L840–L1040](../materi/mentah/AC_crypto_58.txt#L840-L1040), [AC_crypto_59 L331–L350](../materi/mentah/AC_crypto_59.txt#L331-L350)). Tidak dijadikan aturan.

---

### AFS-07 · Change of character (CHoCH) + retest

| | |
|---|---|
| Sumber | [AC_crypto_58 L597–L809](../materi/mentah/AC_crypto_58.txt#L597-L809) |
| Pasar | K, F |
| Timeframe | H4 arah, M15 pemicu (aturan umum SMC) |
| Arah | Short (CHoCH bearish), long (CHoCH bullish) |
| Label | Trading |
| RR minimum | 1:2 |
| Status | 🟢 |

**Short (bullish berubah jadi bearish):**

1. Struktur M15 bullish: higher high dan higher low (D-02).
2. Candle **close di bawah higher low terakhir** → CHoCH.
3. **Retest** ([D-05](00-aturan-global.md#d-05--retest)): harga kembali masuk zona level yang ditembus (level ± 0,5 × ATR) dalam maksimal **10 candle** (nilai awal; diuji 5 · 10 · 15) (Q-20).
4. → Short: order limit di tepi bawah zona itu ([D-10](00-aturan-global.md#d-10--konvensi-eksekusi)). Kalau 10 candle lewat tanpa retest, batal.
5. **SL:** di atas swing high terakhir + 1 × ATR(14). Mentor: SL boleh dimodifikasi asal RR minimal **1:2** untuk jangka pendek dan **lebih dari 1:3** untuk swing ([AC_crypto_58 L685–L739](../materi/mentah/AC_crypto_58.txt#L685-L739)). Bot tidak memodifikasi SL (Q-11).

**Long:** cerminannya. Lower high terakhir ditembus → retest → long, SL di bawah swing low terakhir − 1 × ATR ([AC_crypto_58 L740–L769](../materi/mentah/AC_crypto_58.txt#L740-L769)).

**Kegunaan lain menurut mentor:** CHoCH berlawanan arah dipakai untuk **mengamankan sebagian atau seluruh profit** posisi yang sedang terbuka ([AC_crypto_58 L645–L669](../materi/mentah/AC_crypto_58.txt#L645-L669)). Tidak dipakai di versi pertama: satu TP, satu SL (Q-08, G-07).

**Catatan alat:** indikator gratis "Smart Money Concepts" dari LuxAlgo di TradingView bisa menandai BOS/CHoCH otomatis. Mentor mengingatkan algoritmanya sering salah membaca *noise* ([AC_crypto_58 L770–L809](../materi/mentah/AC_crypto_58.txt#L770-L809)). Bot memakai definisi swing D-01, bukan indikator itu.

---

### AFS-08 · Revisit order block / fair value gap

| | |
|---|---|
| Sumber | [AC_crypto_58 L290–L596](../materi/mentah/AC_crypto_58.txt#L290-L596), [AC_crypto_59 L300–L330](../materi/mentah/AC_crypto_59.txt#L300-L330), [AC_crypto_59 L370–L405](../materi/mentah/AC_crypto_59.txt#L370-L405) |
| Pasar | K, F |
| Timeframe | H4 arah, M15 pemicu (aturan umum SMC) |
| Arah | Long di bullish OB/FVG, short di bearish OB/FVG |
| Label | Trading |
| RR minimum | 1:2 |
| Status | 🟢 |

**Dari mentor:**

1. **Bullish order block** = area konsolidasi tepat sebelum candle besar yang mendorong harga naik dengan volume tinggi. Celah yang ditinggalkan candle besar itu disebut *imbalance* / *fair value gap* (FVG) ([AC_crypto_58 L310–L359](../materi/mentah/AC_crypto_58.txt#L310-L359)). **Bearish OB** = kebalikannya.
2. Mentor **menyamakan** OB dan FVG ("konsepnya sama") ([AC_crypto_58 L380–L399](../materi/mentah/AC_crypto_58.txt#L380-L399)), dan mendeteksinya dengan indikator **FVG dari LuxAlgo** ([AC_crypto_58 L400–L439](../materi/mentah/AC_crypto_58.txt#L400-L439)).
3. Harga cenderung **kembali mengisi** celah itu. Long saat harga kembali ke bullish OB/FVG; short saat kembali ke bearish OB/FVG ([AC_crypto_58 L439–L465](../materi/mentah/AC_crypto_58.txt#L439-L465), [AC_crypto_58 L490–L590](../materi/mentah/AC_crypto_58.txt#L490-L590)).
4. Paling kuat setelah **break of structure** ("perfect combo") ([AC_crypto_59 L385–L400](../materi/mentah/AC_crypto_59.txt#L385-L400)).

**Definisi FVG untuk bot (Q-21)**, meniru cara kerja indikator [Fair Value Gap LuxAlgo](https://www.tradingview.com/script/jWY4Uiez-Fair-Value-Gap-LuxAlgo/) (t = candle sekarang, t−2 = dua candle sebelumnya):

| | Syarat |
|---|---|
| FVG **bullish** | low[t] > high[t−2], **dan** close[t−1] > high[t−2], **dan** celah (low[t] − high[t−2]) ÷ high[t−2] > ambang |
| FVG **bearish** | high[t] < low[t−2], **dan** close[t−1] < low[t−2], **dan** celah (low[t−2] − high[t]) relatif terhadap harga > ambang |
| **Ambang "Auto"** | rata-rata kumulatif (high − low) ÷ low dari semua candle sejauh ini. Celah yang lebih kecil diabaikan. |
| Zona FVG | bullish: dari high[t−2] sampai low[t]; bearish: dari high[t] sampai low[t−2] |

*Rumus ambang diambil dari deskripsi dan kode sumber terbuka skrip LuxAlgo; cocokkan lagi dengan kode aslinya saat menulis bot.*

**Long (short cerminannya):**

1. Candle M15 **close di atas swing high terakhir** (BOS bullish, D-02), dan gerakan naik penyebab BOS itu meninggalkan FVG bullish.
2. Pasang order limit di **tepi atas FVG** ([D-10](00-aturan-global.md#d-10--konvensi-eksekusi)).
3. Order **batal** kalau tidak terisi dalam **20 candle M15** (nilai awal; diuji 10 · 20 · 30), atau harga menyentuh TP lebih dulu (Q-20).

**SL:** di bawah swing low awal gerakan naik itu − 1 × ATR(14). Mentor: short di atas swing high / di atas bearish OB ([AC_crypto_58 L555–L565](../materi/mentah/AC_crypto_58.txt#L555-L565)); bot memakai swing supaya sama dengan G-02.

---

## D. Dow Theory

Dow Theory hanya membahas tren (naik atau turun; **sideways tidak dihitung**) di timeframe besar (MN, W1, D1). Scalper diminta "minggir dulu" ([AC_crypto_60 L1232–L1319](../materi/mentah/AC_crypto_60.txt#L1232-L1319)). Enam prinsipnya ([AC_crypto_60 L1302–L1359](../materi/mentah/AC_crypto_60.txt#L1302-L1359)):

1. Tren harus signifikan.
2. Tren punya fase primer, sekunder, minor.
3. Yang naik pasti turun (selalu ada koreksi).
4. Tren harus dikonfirmasi **volume**. Breakout tanpa volume, atau harga naik saat volume turun, sebaiknya dihindari.
5. Konfirmasi dari indeks lain. Di kripto: dominasi BTC dan *total market cap*.
6. Tren berlanjut sampai ada tanda jelas bahwa ia berbalik.

### AFS-09 · Validasi tembus 3% (Dow Theory)

| | |
|---|---|
| Sumber | [AC_crypto_47 L231–L410](../materi/mentah/AC_crypto_47.txt#L231-L410) |
| Pasar | K, F\* |
| Timeframe | D1 ke atas (swing / investasi). Bot: **D1** |
| Arah | Long dan short |
| Label | Trading |
| RR minimum | TP tetap 1:3 (entry D1, mentor tidak menyebut target; Q-07) |
| Status | 🟢 |

**MA yang dipakai:** **MA21 D1**, sesuai contoh mentor untuk long maupun short. Mentor menyebut jangka pendek **13 dan 21**, jangka panjang **50 dan 100** ([AC_crypto_47 L261–L290](../materi/mentah/AC_crypto_47.txt#L261-L290)); contoh yang ia jalankan memakai MA21. Jenis MA: *simple* (bawaan "Moving Average" TradingView), karena mentor menyebut "moving average", bukan EMA.

**Long (pembalikan naik):**

1. Tren sebelumnya turun (struktur bearish, D-02); harga berkonsolidasi **di bawah MA21**.
2. Harga close di atas MA21.
3. **Baru dianggap valid kalau harga close sudah 3% di atas MA21** → long saat candle itu close ([AC_crypto_47 L321–L369](../materi/mentah/AC_crypto_47.txt#L321-L369)).
   - Kripto: 3% apa adanya.
   - Forex & emas: **k × ATR(14) harian** di atas MA21 ([D-09](00-aturan-global.md#d-09--angka-persen-kripto-di-forex), Q-10).
4. **Batal** kalau harga close kembali di bawah MA21 sebelum syarat 3 terpenuhi.

**Short:** cerminannya: tembus ke bawah MA21, valid setelah 3% di bawahnya ([AC_crypto_47 L369–L395](../materi/mentah/AC_crypto_47.txt#L369-L395)).

**SL:** swing low terakhir − 1 × ATR(14) D1 (G-02). **TP:** 1:3.

Mentor juga menyebut versi "3% di atas trendline downtrend". Tidak dipakai, supaya bot memakai satu acuan saja (MA21).

**Catatan mentor:** untuk scalper, 3% itu terlambat. Untuk swing trader dan investor, menunggu 3% sepadan dengan kepastiannya ([AC_crypto_47 L391–L410](../materi/mentah/AC_crypto_47.txt#L391-L410)).

**Juga dari Dow, tetapi tidak dijadikan aturan (🔴):**

- Titik tren A-B-C-D ([AC_crypto_47 L1–L230](../materi/mentah/AC_crypto_47.txt#L1-L230)): definisi titiknya terlalu kabur untuk dikodekan.
- "Tiga lini masa" (tren berlawanan biasanya baru tembus di periode ke-3, contoh satuan 7 hari) ([AC_crypto_62 L3887–L4001](../materi/mentah/AC_crypto_62.txt#L3887-L4001)): satuan dan cara mengukurnya tidak jelas.
- Fase akumulasi → partisipasi publik → euforia → distribusi → panik ([AC_crypto_57 L2207–L2410](../materi/mentah/AC_crypto_57.txt#L2207-L2410)): konteks investasi jangka panjang.

---

## E. Pola harmonic & kamus pola

Pola harmonic memakai rasio Fibonacci untuk memastikan pola. Mentor sendiri menyebut kelemahannya: butuh rasio yang sangat presisi, banyak *noise* di timeframe kecil, terlalu banyak jenis pola, dan sangat subjektif ([AC_crypto_58 L3449–L3473](../materi/mentah/AC_crypto_58.txt#L3449-L3473), [AC_crypto_60 L2663–L2730](../materi/mentah/AC_crypto_60.txt#L2663-L2730)).

**Aturan umum harmonic** ([AC_crypto_60 L2553–L2662](../materi/mentah/AC_crypto_60.txt#L2553-L2662), [AC_crypto_60 L2743–L2812](../materi/mentah/AC_crypto_60.txt#L2743-L2812)):

1. Cari pola dulu, lalu validasi rasionya dengan Fibonacci.
2. Tentukan titik invalidasi (SL).
3. Risiko 0,5–1%.
4. Entry di **PRZ** (*potential reversal zone*), biasanya titik D. Jangan kejar breakout.
5. Di PRZ tetap **tunggu pemicu**: candle (hammer, inverted hammer, bullish engulfing / hanging man, shooting star, bearish engulfing) dan/atau indikator (stochastic jenuh jual lalu silang naik, RSI, sentuh band Bollinger, silang EMA/SMA) ([AC_crypto_62 L3460–L3588](../materi/mentah/AC_crypto_62.txt#L3460-L3588)).
6. Untuk swing: entry dianggap valid setelah harga memantul **3% dari PRZ** ([AC_crypto_60 L2790–L2812](../materi/mentah/AC_crypto_60.txt#L2790-L2812)).

### AFS-10 · Pola ABCD

| | |
|---|---|
| Sumber | [AC_crypto_57 L2411–L2620](../materi/mentah/AC_crypto_57.txt#L2411-L2620) |
| Pasar | K, F |
| Timeframe | **M15, H1** ("sangat works di timeframe kecil") ([AC_crypto_57 L2600–L2609](../materi/mentah/AC_crypto_57.txt#L2600-L2609)) |
| Arah | Long di D (bullish ABCD), short di D (bearish ABCD) |
| Label | Trading |
| RR minimum | TP tetap 1:2 (entry M15/H1, mentor tidak menyebut target; Q-07) |
| Status | 🟢 |

**Seperti yang tertulis di transkrip:** empat titik A → B → C → D, bentuk seperti petir; rasio "AC" 0,382–0,886; rasio "BD" 1,232–2,618; contoh mentor AC 0,85 dan BD 1,477 → valid ([AC_crypto_57 L2451–L2499](../materi/mentah/AC_crypto_57.txt#L2451-L2499)).

**Aturan untuk bot (Q-23)**, versi bullish (untuk long di D):

1. A, B, C, D adalah swing berurutan (D-01): A = swing high, B = swing low, C = swing high yang lebih rendah dari A, D = titik di bawah B.
2. **Titik C:** BC = **0,382–0,886 × AB**. Ini angka transkrip dan sama dengan versi longgar di buku.
3. **Titik D:** CD = BC × pasangan resiprok dari rasio C: C 0,618 → D 1,618; C 0,786 → D 1,27. Rentang yang sah: CD = **1,13–2,618 × BC**. Angka "1,232" di transkrip dianggap salah dengar.

   Catatan hitungan: pasangan resiprok berarti CD/BC = 1 ÷ (BC/AB), sehingga panjang CD = panjang AB. Jadi titik D yang diharapkan:

   ```
   D = C − (A − B)        (bullish)
   ```

4. **Entry:** candle konfirmasi long (*hammer*, *bullish engulfing*, *inverted hammer*; [D-06](00-aturan-global.md#d-06--candle)) close di dalam zona D (D ± 0,5 × ATR(14), [D-04](00-aturan-global.md#d-04--zona-support-dan-resistance)) → order pasar. Mentor: "harus tetap lihat konfirmasi dulu" ([AC_crypto_57 L2515–L2535](../materi/mentah/AC_crypto_57.txt#L2515-L2535)).
5. **Batal:** harga turun melewati batas CD = 2,618 × BC sebelum ada konfirmasi.

**SL:** low terendah di sekitar D − 1 × ATR(14). Mentor: di bawah D / swing low, "kalau bingung pakai ATR" ([AC_crypto_57 L2515–L2535](../materi/mentah/AC_crypto_57.txt#L2515-L2535)).

**TP:** 1:2.

Bearish ABCD (short di D) = cerminannya.

---

### AFS-11 · Pola harmonic XABCD

| | |
|---|---|
| Sumber | Gartley [AC_crypto_60 L347–L579](../materi/mentah/AC_crypto_60.txt#L347-L579) · Bat [AC_crypto_62 L2246–L2481](../materi/mentah/AC_crypto_62.txt#L2246-L2481) · Crab [AC_crypto_43](../materi/mentah/AC_crypto_43.txt) · rasio dasar, Shark, Butterfly [AC_crypto_61 L618–L851](../materi/mentah/AC_crypto_61.txt#L618-L851) · harmonic H&S, 5-0 [AC_crypto_54 L162–L322](../materi/mentah/AC_crypto_54.txt#L162-L322) |
| Pasar | K, F |
| Timeframe | Umumnya timeframe besar. Gartley disebut paling cocok H1/M15 ([AC_crypto_60 L367–L386](../materi/mentah/AC_crypto_60.txt#L367-L386)) |
| Status | ⏸ ditunda di versi pertama (Q-23) |

**Rasio persis seperti yang diucapkan mentor:**

| Pola | Rasio di transkrip | Entry & SL dari mentor |
|---|---|---|
| **Gartley** | Titik B ditarik dari X ke A harus berada di golden pocket 0,5–0,618 dan tidak boleh lewat | Entry di D (atau tunggu pemicu); SL di bawah swing low; TP resistance psikologis / horizontal / harmonic, RR minimal 1:2–1:3 ([AC_crypto_60 L437–L555](../materi/mentah/AC_crypto_60.txt#L437-L555)) |
| **Bat** | B di golden pocket dan tidak boleh tembus; "rasio XB 0,516"; rasio atas 0,92 dan bawah 0,85 (bullish), 0,96 dan 0,88 (bearish); selisih 0,01–0,1 "nggak apa-apa" | Entry di D + pemicu; SL di bawah swing low; TP swing high atau resistance harmonic ([AC_crypto_62 L2336–L2405](../materi/mentah/AC_crypto_62.txt#L2336-L2405), [AC_crypto_62 L2436–L2465](../materi/mentah/AC_crypto_62.txt#L2436-L2465)) |
| **Crab** | B di golden pocket; D di **1,618** dari XA | Entry di D; lebih aman tunggu konfirmasi (contoh: bullish engulfing M15 dengan volume tinggi); SL di bawah D; TP bertahap di tiap support ([AC_crypto_43 L41–L129](../materi/mentah/AC_crypto_43.txt#L41-L129), [AC_crypto_43 L211–L232](../materi/mentah/AC_crypto_43.txt#L211-L232)) |
| **Butterfly** | A→C 0,382–0,886; X→B 0,786; B→D 1,618–2,24; X→D 1,27 | D = titik masuk ([AC_crypto_61 L808–L848](../materi/mentah/AC_crypto_61.txt#L808-L848)) |
| **Shark** | A→C 1,13–"1,168"; X→B 0,382–0,618; B→D 1,618–2,24; X→D 0,886–1,13 | D = PRZ ([AC_crypto_61 L758–L797](../materi/mentah/AC_crypto_61.txt#L758-L797)) |
| **Harmonic extension** (W/M) | Fokus A→C = 1,13 | D = PRZ ([AC_crypto_61 L628–L690](../materi/mentah/AC_crypto_61.txt#L628-L690)) |
| **Harmonic impulse** | X→B 1,13–1,618; A→C 1,618–2,24 | C = titik balik ([AC_crypto_61 L690–L727](../materi/mentah/AC_crypto_61.txt#L690-L727)) |
| **Harmonic H&S** | Bahu kiri → kepala 1,618; kepala → bahu kanan 0,618 | Entry di bahu kanan ([AC_crypto_54 L200–L265](../materi/mentah/AC_crypto_54.txt#L200-L265)) |
| **5-0** | "Double bottom" 1,13 lalu jarak 0,5 | Deskripsinya sangat kabur ([AC_crypto_54 L265–L320](../materi/mentah/AC_crypto_54.txt#L265-L320)) |

Mentor sendiri, untuk Gartley, menunggu pemicu dulu sebelum masuk di D ("tunggu kepastian") ([AC_crypto_60 L527–L555](../materi/mentah/AC_crypto_60.txt#L527-L555)).

**Kenapa ditunda:** Anda memilih hanya ABCD dan double/triple top-bottom untuk versi pertama (Q-23). Alasan awalnya:

- Penamaan kaki rasio di transkrip tidak konsisten (A→C, X→B, "rasio atas/bawah").
- Ada pernyataan yang saling bertentangan: harmonic extension disebut "W = bullish" tetapi harga di D "turun" ([AC_crypto_61 L648–L690](../materi/mentah/AC_crypto_61.txt#L648-L690)).
- Mentor sendiri menyebut pola ini sangat subjektif.

---

### AFS-23 · Pola grafik klasik

| | |
|---|---|
| Sumber | [AC_crypto_57 L601–L1383](../materi/mentah/AC_crypto_57.txt#L601-L1383) (Technical Research 3), Kamus Pattern Crypto ([PETA 5.F3](../materi/PETA.md#f3-kamus-pattern-crypto-kpk)) |
| Pasar | K, F |
| Status | ⏸ ditunda di versi pertama (Q-23), kecuali **double/triple top-bottom** yang dipakai di [AFS-03](#afs-03--double-topbottom--tembus-neckline) dan sebagai pola di AFS-01 |

Ringkasan aturan tiap pola yang disebut mentor:

| Pola | Aturan dari mentor | Sumber |
|---|---|---|
| Bull/bear **pennant** | Didahului *flagpole*; minimal **2 sentuhan** di sisi bawah/atas. Target = panjang *flagpole* dari titik breakout. | [AC_crypto_57 L705–L769](../materi/mentah/AC_crypto_57.txt#L705-L769) |
| **Ascending / descending triangle** | Pola favorit Alvesting untuk altcoin: sisi atas datar, low makin tinggi; breakout impulsif dengan volume tinggi. Masuk **sebelum** breakout ("anticipating the breakout, not chasing"). | [AC_crypto_57 L771–L850](../materi/mentah/AC_crypto_57.txt#L771-L850), [AC_crypto_57 L941–L985](../materi/mentah/AC_crypto_57.txt#L941-L985) |
| Bull/bear **flag** | Channel paralel berlawanan arah. Disebut sering palsu, jarang dipakai. | [AC_crypto_57 L851–L890](../materi/mentah/AC_crypto_57.txt#L851-L890) |
| **Head & shoulders** (dan inverse) | Tembus *neckline* = pembalikan. | [AC_crypto_57 L1061–L1119](../materi/mentah/AC_crypto_57.txt#L1061-L1119), [AC_crypto_57 L1231–L1270](../materi/mentah/AC_crypto_57.txt#L1231-L1270) |
| **Double/triple top & bottom** | Maksimal 3 sentuhan; tidak ada "quadruple". | [AC_crypto_57 L1121–L1189](../materi/mentah/AC_crypto_57.txt#L1121-L1189) |
| **Rising / falling wedge** | Rising wedge setelah uptrend → short di resistance wedge. Falling wedge, 3 sentuhan → long. | [AC_crypto_57 L1191–L1230](../materi/mentah/AC_crypto_57.txt#L1191-L1230), [AC_crypto_57 L1301–L1340](../materi/mentah/AC_crypto_57.txt#L1301-L1340) |
| **Broadening** (megaphone) | Netral. Masuk di sisi bawah (long) atau atas (short) sebelum breakout; idealnya 3 sentuhan. Cocok D1/H4/W1, kurang cocok untuk scalping. | [AC_crypto_60 L587–L836](../materi/mentah/AC_crypto_60.txt#L587-L836) |
| **Diamond** | Netral. Masuk saat breakout kecil; SL di bawah swing low; batal kalau *false breakout*. | [AC_crypto_59 L1685–L1804](../materi/mentah/AC_crypto_59.txt#L1685-L1804) |
| **Rectangle channel** | Panjang kotak AB = CD (contoh 3% = 3%), dipakai untuk menghitung target. | [AC_crypto_57 L2621–L2712](../materi/mentah/AC_crypto_57.txt#L2621-L2712) |

Pola juga bisa menjadi **alat invalidasi**: kalau muncul pola berlawanan, posisi boleh ditutup. Namun mentor tetap menyarankan setia pada trading plan ([AC_crypto_59 L1625–L1644](../materi/mentah/AC_crypto_59.txt#L1625-L1644)). Bot tidak memakai invalidasi ini (G-07).

---

### AFS-24 · Elliott Wave

| | |
|---|---|
| Sumber | [AC_crypto_62 L3094–L3307](../materi/mentah/AC_crypto_62.txt#L3094-L3307), [AC_crypto_54 L1–L161](../materi/mentah/AC_crypto_54.txt#L1-L161) |
| Status | 🔴 (penghitungan gelombang sangat subjektif) |

Aturan dari mentor:

- Uptrend: **long di akhir gelombang 2 dan 4** (*buy on weakness*). Downtrend: short di gelombang 2 dan 4 ([AC_crypto_62 L3204–L3233](../materi/mentah/AC_crypto_62.txt#L3204-L3233), [AC_crypto_62 L3264–L3290](../materi/mentah/AC_crypto_62.txt#L3264-L3290)).
- Setelah gelombang 5 dan ada CHoCH: **short di titik B** koreksi, SL beberapa persen di atas swing high ([AC_crypto_62 L3234–L3260](../materi/mentah/AC_crypto_62.txt#L3234-L3260)).
- Akhir koreksi C biasanya di golden pocket 0,5–0,618 dari gelombang 1–5 ([AC_crypto_54 L50–L90](../materi/mentah/AC_crypto_54.txt#L50-L90)).
- Panjang gelombang 3 ≈ **1,618 × gelombang 1** → target ([AC_crypto_54 L95–L155](../materi/mentah/AC_crypto_54.txt#L95-L155)).

---

### AFS-25 · Andrews Pitchfork

| | |
|---|---|
| Sumber | [AC_crypto_58 L1043–L1221](../materi/mentah/AC_crypto_58.txt#L1043-L1221) |
| Status | 🔴 (pemilihan 3 titik pivot subjektif) |

Aturan: harga "80%" kembali ke garis tengah (*median*). Long di garis bawah → TP di median. Short di garis atas. Tembus ke bawah garis + retest → short.

---

## F. Indikator

Semua indikator memakai **setting default TradingView** kecuali disebut lain, karena mentor berulang kali menyuruh "pakai default". Ingat **G-11**: maksimal satu indikator per kategori.

### AFS-12 · Pivot point: entry di garis P

| | |
|---|---|
| Sumber | [AC_crypto_44 L1–L299](../materi/mentah/AC_crypto_44.txt#L1-L299) |
| Pasar | K, F |
| Timeframe | **H1, M15, M5** ([AC_crypto_44 L285–L295](../materi/mentah/AC_crypto_44.txt#L285-L295)); mentor mengaitkan pivot dengan "yang suka intraday trading, suka scalping" ([AC_crypto_44 L118–L125](../materi/mentah/AC_crypto_44.txt#L118-L125)) |
| Label | **Scalping di M5/M15** (pivot harian), **trading di H1** (pivot mingguan, targetnya bisa butuh beberapa hari). Label ditentukan dari timeframe saat posisi dibuka (Q-45) |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Indikator:** *Pivot Points Standard*, tipe **Traditional**, setting bawaan TradingView, sesuai pesan mentor "settingnya default aja" ([AC_crypto_44 L60–L90](../materi/mentah/AC_crypto_44.txt#L60-L90)). Dengan *Pivots Timeframe* "Auto": chart **M5/M15 memakai pivot harian**, chart **H1 memakai pivot mingguan** (Q-22). Batas hari dan minggu mengikuti [D-12](00-aturan-global.md#d-12--batas-hari-minggu-dan-candle). Rumus ([AC_crypto_44 L35–L65](../materi/mentah/AC_crypto_44.txt#L35-L65)):

```
P  = (High + Low + Close) ÷ 3            ← periode sebelumnya
R1 = 2P − Low        S1 = 2P − High
R2 = P + (High − Low)  S2 = P − (High − Low)
```

Hanya pakai **P, S1–S3, R1–R3**. Level di luar itu terlalu jauh ([AC_crypto_44 L110–L129](../materi/mentah/AC_crypto_44.txt#L110-L129)).

**Long:**

1. Harga di atas P dan sedang berkonsolidasi di area R. **Jangan long di R.**
2. Tunggu harga turun ke **P**.
3. → Long: order limit tepat di P ([AC_crypto_44 L160–L199](../materi/mentah/AC_crypto_44.txt#L160-L199)).
4. **SL** — dua versi dari mentor, **keduanya diuji** (Q-22) ([AC_crypto_44 L195–L249](../materi/mentah/AC_crypto_44.txt#L195-L249)):
   - agresif: P − 1 × ATR(14) (mentor: di bawah P, contoh BTC ±0,3%);
   - konservatif: S1 − 1 × ATR(14) (mentor: di bawah S1, ±1–2%).
5. **TP:** R1, R2, R3 ([AC_crypto_44 L250–L270](../materi/mentah/AC_crypto_44.txt#L250-L270)) → satu TP: level terdekat yang RR-nya minimal 1:1,5 (Q-08).

**Short:**

1. Harga close di bawah P.
2. Tunggu harga naik kembali ke P.
3. → Short: order limit tepat di P.
4. **SL:** P + 1 × ATR(14), atau R1 + 1 × ATR(14) (keduanya diuji).
5. **TP:** S1, S2 ([AC_crypto_44 L210–L230](../materi/mentah/AC_crypto_44.txt#L210-L230), [AC_crypto_44 L270–L290](../materi/mentah/AC_crypto_44.txt#L270-L290)) → level terdekat yang RR-nya minimal 1:1,5.

Mentor: tunggu setup pivot-nya siap, jangan asal masuk ([AC_crypto_44 L285–L295](../materi/mentah/AC_crypto_44.txt#L285-L295)).

**Label (Q-45):** di M5/M15 posisinya scalping (risiko 0,5%, ditutup setelah 3 jam dan sebelum berita besar); di H1 posisinya trading (risiko 1%). Mentor mengaitkan pivot dengan intraday dan scalping ([AC_crypto_44 L123–L125](../materi/mentah/AC_crypto_44.txt#L123-L125)), di H1, M15, dan M5 ([AC_crypto_44 L292–L293](../materi/mentah/AC_crypto_44.txt#L292-L293)).

---

### AFS-13 · Keltner Channel

| | |
|---|---|
| Sumber | [AC_crypto_44 L300–L489](../materi/mentah/AC_crypto_44.txt#L300-L489) |
| Pasar | K, F |
| Timeframe | Tidak disebut mentor → diuji **H1, H4, D1** (setara), dipilih dengan aturan G-17 (Q-47) |
| Label | Trading |
| Status | 🟢 (AFS-13A dan AFS-13B) |

**Setting (Q-24):** bawaan TradingView yang dipakai mentor: garis tengah **EMA 20**, ATR **10**, pengali **2**. Pita atas = EMA + 2 × ATR, pita bawah = EMA − 2 × ATR ([AC_crypto_44 L340–L369](../materi/mentah/AC_crypto_44.txt#L340-L369)). Mentor sempat menyebut SMA, tetapi angka yang ia sebut persis setting bawaan TradingView yang memakai EMA ([AC_crypto_44 L362–L365](../materi/mentah/AC_crypto_44.txt#L362-L365)).

Mode tren dan mode pantulan bisa memberi sinyal berlawanan di saat yang sama. Karena itu keduanya dijadikan **dua setup terpisah** dan diuji sendiri-sendiri. **Di live, hanya satu yang aktif per instrumen**, dipilih dari hasil di data pemilihan ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)) (Q-24).

#### AFS-13A · Mode tren

RR minimum **1:2** (mentor: RR 1:2–1:3).

- **Long:** harga di atas garis tengah. Mentor: masuk saat breakout yang dikonfirmasi volume, **atau lebih baik** saat harga turun lagi menyentuh garis tengah (retest); kalau ketinggalan, jangan kejar ([AC_crypto_44 L390–L425](../materi/mentah/AC_crypto_44.txt#L390-L425)). Bot memakai versi yang disebut mentor "lebih baik": **retest** garis tengah ([D-05](00-aturan-global.md#d-05--retest)) → order limit tepat di garis tengah.
  - **SL:** garis tengah − 1 × ATR(14). **TP:** pita atas (nilai saat entry).
- **Short:** harga di bawah garis tengah, retest garis tengah dari bawah, lalu ada **pemicu melemah** (candle pemicu short, [D-06](00-aturan-global.md#d-06--candle)) → order pasar saat candle pemicu close ([AC_crypto_44 L425–L455](../materi/mentah/AC_crypto_44.txt#L425-L455)).
  - **SL:** garis tengah + 1 × ATR(14). **TP:** pita bawah.

#### AFS-13B · Mode pantulan

RR minimum **1:1,5**.

- **Long:** harga menyentuh pita bawah (jenuh jual) → order limit tepat di pita bawah. **SL:** swing low terakhir − 1 × ATR(14) (mentor: di bawah swing low / pita bawah). **TP:** TP1 garis tengah, TP2 pita atas ([AC_crypto_44 L450–L480](../materi/mentah/AC_crypto_44.txt#L450-L480)) → satu TP: yang terdekat dengan RR minimal 1:1,5 (Q-08).
- **Short:** harga menyentuh pita atas. TP1 garis tengah, TP2 pita bawah ([AC_crypto_44 L475–L489](../materi/mentah/AC_crypto_44.txt#L475-L489)).

---

### AFS-14 · Ichimoku "di atas/bawah semua garis"

| | |
|---|---|
| Sumber | [AC_crypto_44 L490–L714](../materi/mentah/AC_crypto_44.txt#L490-L714) |
| Pasar | K, F |
| Timeframe | D1 |
| Label | Trading |
| RR minimum | TP tetap 1:3 (entry D1; Q-07) |
| Status | 🟢 |

**Setting:** Tenkan 9, Kijun 26, Senkou Span B 52 ([AC_crypto_44 L520–L575](../materi/mentah/AC_crypto_44.txt#L520-L575)). Chikou dan Kumo digeser **25 candle** (candle sekarang dihitung 1), sama dengan perhitungan Ichimoku Rafał (Q-36, [06 · bagian B](06-mentor-forex.md#b-ichimoku--rafał-zuchowicz-forex_3)).

**Long:** candle D1 **close di atas semua garis**: Kumo (awan), Tenkan, Kijun, dan Chikou di atasnya → order pasar saat candle itu close. Contoh mentor disertai volume tinggi ([AC_crypto_44 L590–L660](../materi/mentah/AC_crypto_44.txt#L590-L660)).

- **SL:** tepi bawah Kumo − 1 × ATR(14) D1.

**Short:** candle D1 **close di bawah semua garis**, lalu harga **retest Kumo dari bawah** → order limit di tepi bawah Kumo; batal kalau tidak tersentuh dalam 10 candle ([D-05](00-aturan-global.md#d-05--retest)) ([AC_crypto_44 L665–L700](../materi/mentah/AC_crypto_44.txt#L665-L700)).

- **SL:** tepi atas Kumo + 1 × ATR(14) D1.

**TP:** mentor menyebut "beberapa target" di garis-garis Ichimoku sebagai *dynamic resistance*, tetapi garisnya ditunjuk di layar dan tidak bisa dipastikan dari transkrip ([AC_crypto_44 L651–L665](../materi/mentah/AC_crypto_44.txt#L651-L665)). Jadi TP = **1:3** (setup tanpa target, entry D1; Q-07).

Lihat juga versi Ichimoku yang jauh lebih lengkap dari Rafał di [06 · ICH-01–04](06-mentor-forex.md#b-ichimoku--rafał-zuchowicz-forex_3).

---

### AFS-15 · Parabolic SAR titik ke-2

| | |
|---|---|
| Sumber | [AC_crypto_59 L3401–L3555](../materi/mentah/AC_crypto_59.txt#L3401-L3555) |
| Pasar | K, F |
| Timeframe | Konfirmasi di H1/H4 ([AC_crypto_59 L3491–L3500](../materi/mentah/AC_crypto_59.txt#L3491-L3500)) |
| Label | Trading |
| RR minimum | TP tetap: 1:2 di H1, 1:3 di H4 (Q-07) |
| Status | 🟢 |

**Setting:** default TradingView.

**Long:** titik PSAR muncul **di bawah** harga. Masuk pada **titik ke-2** (sedang): order pasar saat candle dengan titik PSAR kedua di bawah harga close. Titik ke-1 = agresif; titik ke-3 = konfirmasi kuat tetapi sering sudah kehilangan momentum ([AC_crypto_59 L3451–L3500](../materi/mentah/AC_crypto_59.txt#L3451-L3500)).
**SL:** swing low terakhir − 1 × ATR(14). Mentor: di bawah titik PSAR atau swing low, sebaiknya di balik support supaya tidak tersapu *stop hunt* ([AC_crypto_59 L3471–L3490](../materi/mentah/AC_crypto_59.txt#L3471-L3490)).
**TP:** mentor menyebut resistance horizontal, psikologis, atau harmonic, dengan RR minimal 1:2 (1:2, 1:3, 1:5) ([AC_crypto_59 L3461–L3470](../materi/mentah/AC_crypto_59.txt#L3461-L3470)). Karena levelnya tidak pasti, bot memakai TP tetap: **1:2** kalau entry di H1, **1:3** kalau di H4 (Q-07).

**Short:** cerminannya ([AC_crypto_59 L3501–L3540](../materi/mentah/AC_crypto_59.txt#L3501-L3540)).

---

### AFS-16 · Donchian Channel

| | |
|---|---|
| Sumber | [AC_crypto_59 L3556–L3718](../materi/mentah/AC_crypto_59.txt#L3556-L3718) |
| Pasar | K, F |
| Timeframe | Tidak disebut mentor → diuji **H1, H4, D1** (setara), dipilih dengan aturan G-17 (Q-47) |
| Label | Trading |
| Status | 🟢 |

**Setting (Q-24):** bawaan TradingView, **panjang 20**. Atas = high tertinggi 20 candle; bawah = low terendah 20 candle; tengah = rata-rata keduanya ([AC_crypto_59 L3586–L3610](../materi/mentah/AC_crypto_59.txt#L3586-L3610)).

**Dipakai dengan cara mentor** (pantulan & silang garis tengah). Mode **breakout** yang umum dipakai orang **tidak dipakai** (Q-24). Kedua mode di bawah diuji sendiri-sendiri.

**Mode pantulan** ([AC_crypto_59 L3640–L3680](../materi/mentah/AC_crypto_59.txt#L3640-L3680)), RR minimum 1:1,5:

- **Long:** low candle menyentuh pita bawah → order pasar saat candle itu close. **SL:** low candle itu − 1 × ATR(14). **TP:** TP1 garis tengah, TP2 pita atas → satu TP: yang terdekat dengan RR minimal 1:1,5 (Q-08).
- **Short:** cerminannya di pita atas.

**Mode tren** ([AC_crypto_59 L3680–L3710](../materi/mentah/AC_crypto_59.txt#L3680-L3710)):

- **Long:** candle close menyilang ke atas garis tengah → order pasar saat candle itu close. **SL:** swing low terakhir − 1 × ATR(14). **TP:** mentor: target 1:3–1:5 → bot memakai **1:3** (batas bawahnya).
- **Short:** close di bawah garis tengah, lalu **retest** garis tengah ([D-05](00-aturan-global.md#d-05--retest)) → order limit tepat di garis tengah. **SL:** swing high terakhir + 1 × ATR(14). **TP:** pita bawah (nilai saat entry); RR minimal 1:1,5.

---

### AFS-17 · KST silang di garis nol

| | |
|---|---|
| Sumber | [AC_crypto_61 L2513–L2646](../materi/mentah/AC_crypto_61.txt#L2513-L2646) |
| Pasar | K, F |
| Timeframe | **D1** |
| Label | Trading |
| RR minimum | TP tetap 1:3 (entry D1; Q-07) |
| Status | 🟢 |

**Setting:** default TradingView ([AC_crypto_61 L2545–L2560](../materi/mentah/AC_crypto_61.txt#L2545-L2560)).

- **Long:** KST **di bawah nol**, lalu garis KST **silang naik** garis sinyalnya.
- **Short:** KST **di atas nol**, lalu silang turun.
- Tunggu silang **valid** (candle selesai), jangan masuk sebelum silang ([AC_crypto_61 L2590–L2640](../materi/mentah/AC_crypto_61.txt#L2590-L2640)) → order pasar saat candle silang close.

**SL:** swing low terakhir − 1 × ATR(14) D1 untuk long; swing high + 1 × ATR untuk short (G-02). **TP:** 1:3.

---

### AFS-18 · Konfirmasi Chaikin Money Flow

| | |
|---|---|
| Sumber | [AC_crypto_62 L2482–L2624](../materi/mentah/AC_crypto_62.txt#L2482-L2624) |
| Pasar | K, F\* (forex memakai tick volume, atau setup ini mati; [D-07](00-aturan-global.md#d-07--volume)) |
| Timeframe | Makin besar makin valid (H4, D1) |
| Label | Trading |
| RR minimum | TP tetap 1:3 (entry H4/D1; Q-07). Mentor: RR 1:2–1:3 |
| Status | 🟢 |

**Setting:** CMF periode **20** ([AC_crypto_62 L2522–L2530](../materi/mentah/AC_crypto_62.txt#L2522-L2530)).

- **Long (breakout):** candle close di atas zona resistance ([D-04](00-aturan-global.md#d-04--zona-support-dan-resistance)) **dan** CMF close di atas 0 → order pasar saat candle itu close ([AC_crypto_62 L2542–L2571](../materi/mentah/AC_crypto_62.txt#L2542-L2571)). SL: swing low terakhir − 1 × ATR(14).
- **Short (breakdown):** candle close di bawah zona support **dan** CMF di bawah 0 ([AC_crypto_62 L2572–L2591](../materi/mentah/AC_crypto_62.txt#L2572-L2591)). SL: swing high terakhir + 1 × ATR(14).
- **Divergensi bullish:** dua swing low terakhir (D-01): harga membuat low lebih rendah, tetapi CMF di swing kedua lebih tinggi daripada di swing pertama → long saat swing kedua diakui (2 candle sesudahnya close). SL: swing low itu − 1 × ATR(14). **Divergensi bearish:** cerminannya di dua swing high terakhir ([AC_crypto_62 L2592–L2615](../materi/mentah/AC_crypto_62.txt#L2592-L2615)).
- **TP:** 1:3.

---

### AFS-19 · Pantulan POC (volume profile)

| | |
|---|---|
| Sumber | [AC_crypto_58 L3223–L3318](../materi/mentah/AC_crypto_58.txt#L3223-L3318), [AC_crypto_39](../materi/mentah/AC_crypto_39.txt) |
| Pasar | K, F\* (forex memakai tick volume, atau setup ini mati; [D-07](00-aturan-global.md#d-07--volume)) |
| Timeframe | H1, H4, D1 (mengikuti rentang POC di bawah) |
| Label | Trading |
| RR minimum | 1:2 (mentor: RR 1:2–1:3) |
| Status | 🟢 |

**Indikator:** *Volume Profile Fixed Range* (mentor memakai versi komunitas "LonesomeTheBlue"). **POC** = level harga dengan volume terbanyak ([AC_crypto_58 L3233–L3270](../materi/mentah/AC_crypto_58.txt#L3233-L3270)). Jumlah baris profil memakai bawaan indikatornya; angkanya dicek di dialog setting saat kode ditulis.

**Rentang yang diukur (Q-24), dua-duanya diuji:**

| Chart | Rentang POC |
|---|---|
| H1 | **minggu lalu** |
| H4 / D1 | **bulan lalu** |

- **Long:** harga koreksi turun ke POC dari atas → order limit tepat di POC. **SL:** POC − 1 × ATR(14). **TP:** mentor hanya menyebut RR 1:2–1:3 → TP tetap **1:2** di H1, **1:3** di H4/D1 (Q-07).
- **Short:** harga naik ke POC dari bawah → order limit di POC. **SL:** POC + 1 × ATR(14). **TP:** zona support terdekat yang RR-nya minimal 1:2 ([AC_crypto_58 L3283–L3310](../materi/mentah/AC_crypto_58.txt#L3283-L3310)).
- POC dari timeframe besar lebih relevan. Di timeframe kecil, POC yang sama bisa berperan sebaliknya ([AC_crypto_39 L60–L105](../materi/mentah/AC_crypto_39.txt#L60-L105)).

---

### AFS-20 · Linear Regression Channel

| | |
|---|---|
| Sumber | [AC_crypto_61 L852–L976](../materi/mentah/AC_crypto_61.txt#L852-L976) |
| Pasar | K, F |
| Timeframe | **H4**, sesuai contoh mentor "lrc dalam h 4 bitcoin" ([AC_crypto_61 L903](../materi/mentah/AC_crypto_61.txt#L903)) (Q-47). M15 dan H1 tidak diuji |
| Label | **Trading** (Q-45). Mentor menyebutnya cocok untuk intraday dan "yang suka scalping", tetapi contohnya di H4 dengan tiap gerakan selesai sekitar satu hari ([AC_crypto_61 L882–L890](../materi/mentah/AC_crypto_61.txt#L882-L890), [AC_crypto_61 L903–L916](../materi/mentah/AC_crypto_61.txt#L903-L916)), sedangkan menurut Alvesting scalping hanya beberapa menit sampai beberapa jam, maksimal 3 jam ([AC_crypto_58 L3018–L3036](../materi/mentah/AC_crypto_58.txt#L3018-L3036), [AC_crypto_58 L3053](../materi/mentah/AC_crypto_58.txt#L3053)) |
| RR minimum | 1:1,5; mode breakout TP tetap 1:3 (entry H4) |
| Status | 🟢 |

**Setting (Q-24):** bawaan TradingView, **100 candle**, deviasi **2** (garis atas dan bawah).

- **Mode range:** long di sisi bawah channel → TP sisi atas; short di sisi atas → TP sisi bawah ([AC_crypto_61 L912–L940](../materi/mentah/AC_crypto_61.txt#L912-L940)). Entry: order limit tepat di garis. SL: swing terakhir ± 1 × ATR(14) (G-02).
- **Mode breakout:** candle close di bawah channel + **retest** ([D-05](00-aturan-global.md#d-05--retest)) → short, SL di atas swing high + 1 × ATR. Keluar ke atas → bias long, cerminannya ([AC_crypto_61 L940–L960](../materi/mentah/AC_crypto_61.txt#L940-L960)). Mentor tidak menyebut target → TP tetap **1:3** (entry H4; Q-07).

---

### AFS-21 · Renko reversal

| | |
|---|---|
| Sumber | [AC_crypto_61 L2293–L2512](../materi/mentah/AC_crypto_61.txt#L2293-L2512) |
| Pasar | K, F |
| Timeframe | D1 lebih akurat daripada H4/H1 ([AC_crypto_61 L2443–L2450](../materi/mentah/AC_crypto_61.txt#L2443-L2450)). Bot: **D1** |
| Label | Trading |
| RR minimum | 1:1,5 |
| Status | 🟢 |

**Setting (Q-24):** ukuran bata dari **ATR(14)**, cara bawaan TradingView.

- **Breakout valid** = bata (brick) penuh menembus level ([AC_crypto_61 L2400–L2422](../materi/mentah/AC_crypto_61.txt#L2400-L2422)).
- **Reversal bullish** = setelah deret bata merah (minimal 2 berturut-turut), muncul bata hijau dengan wick di bawah → long saat bata hijau itu selesai ([AC_crypto_61 L2423–L2470](../materi/mentah/AC_crypto_61.txt#L2423-L2470)).
  - **SL:** swing low − 1 × ATR(14).
  - **TP:** mentor: resistance psikologis/harmonic/area jual → bot: zona resistance ([D-04](00-aturan-global.md#d-04--zona-support-dan-resistance)) terdekat yang RR-nya minimal 1:1,5 (Q-08).
- **Reversal bearish** = cerminannya, SL di atas swing high + 1 × ATR ([AC_crypto_61 L2470–L2510](../materi/mentah/AC_crypto_61.txt#L2470-L2510)).

---

## G. Order flow (khusus kripto)

Order flow butuh data transaksi per level harga (*footprint*). Data ini tersedia di bursa kripto terpusat (contoh di kelas: Binance dan Bybit lewat aplikasi ATAS). **Tidak tersedia di forex spot**, karena forex tidak punya bursa pusat ([PETA bagian 8](../materi/PETA.md#8-dari-kelas-saham--crypto-ke-bot-forex)).

### AFS-22 · Sinyal order flow

| | |
|---|---|
| Sumber | [AC_crypto_57 L2713–L3272](../materi/mentah/AC_crypto_57.txt#L2713-L3272), [AC_crypto_59 L2360–L2639](../materi/mentah/AC_crypto_59.txt#L2360-L2639), [AC_crypto_58 L3879–L3946](../materi/mentah/AC_crypto_58.txt#L3879-L3946) |
| Pasar | K |
| Status | 🟡 (definisinya jelas, tetapi entry/SL/TP tidak disebut; paling cocok sebagai sinyal tambahan) → [Q-51](09-pertanyaan-untuk-anda.md#q-51--order-flow-afs-22) |

| Sinyal | Definisi dari mentor | Arti |
|---|---|---|
| **Delta** | Volume beli agresif − volume jual agresif per candle | Positif = condong naik; negatif = condong turun ([AC_crypto_57 L2773–L2850](../materi/mentah/AC_crypto_57.txt#L2773-L2850)) |
| **Divergensi delta** | Candle **merah** tetapi delta **positif** → bullish. Candle **hijau** tetapi delta **negatif** (di resistance) → bearish. | Contoh mentor: BTC +10% dan −8% sesudahnya ([AC_crypto_57 L2913–L2990](../materi/mentah/AC_crypto_57.txt#L2913-L2990)) |
| **Imbalance** | Volume *ask* di satu sel **≥300%** volume *bid* di sel diagonalnya (atau sebaliknya) | Satu sisi sangat agresif ([AC_crypto_59 L2390–L2439](../materi/mentah/AC_crypto_59.txt#L2390-L2439)) |
| **Stacked imbalance** | **3 sel imbalance berturut-turut** | Menjadi zona support/resistance ([AC_crypto_59 L2440–L2489](../materi/mentah/AC_crypto_59.txt#L2440-L2489)) |
| **Unfinished auction** | Ujung atas/bawah *footprint* berisi angka 0 di salah satu sisi (terlihat sebagai wick) | Harga cenderung kembali ke level itu ("magnet") → bisa jadi target ([AC_crypto_59 L2490–L2639](../materi/mentah/AC_crypto_59.txt#L2490-L2639)) |
| **Big trades + delta bar** | Penjual agresif + order jual besar → harga justru sering naik (*short squeeze*), dan sebaliknya | Tanda pembalikan ([AC_crypto_57 L3223–L3265](../materi/mentah/AC_crypto_57.txt#L3223-L3265)) |
| **HVN** | Level volume tertinggi di *footprint*; timeframe besar lebih penting | Area penting ([AC_crypto_57 L2713–L2775](../materi/mentah/AC_crypto_57.txt#L2713-L2775)) |
| **Heatmap** | Area oranye = order besar asli (bukan order palsu) | Area penting ([AC_crypto_58 L3909–L3946](../materi/mentah/AC_crypto_58.txt#L3909-L3946)) |

---

## H. Filter

### AFS-F1 · Screening altcoin & korelasi BTC

| | |
|---|---|
| Sumber | [AC_crypto_57 L1–L600](../materi/mentah/AC_crypto_57.txt#L1-L600) |
| Pasar | K (altcoin) |
| Status | ⏸ ditunda: versi pertama hanya BTC dan ETH (Q-25) |

Menurut mentor, yang paling penting: **(1) volume**, **(2) korelasi dengan BTC dan dominasi BTC**, **(3) pasar saham AS** jika trading malam. *Funding rate*, *open interest*, dan *long/short ratio* "tidak terlalu membantu" kecuali untuk timeframe besar ([AC_crypto_57 L55–L80](../materi/mentah/AC_crypto_57.txt#L55-L80), [AC_crypto_57 L590–L600](../materi/mentah/AC_crypto_57.txt#L590-L600)).

**1. Volume:** urutkan pasar futures berdasarkan volume 24 jam; pilih yang tertinggi ([AC_crypto_57 L81–L129](../materi/mentah/AC_crypto_57.txt#L81-L129)).

**2. Tabel korelasi BTC** ([AC_crypto_57 L181–L260](../materi/mentah/AC_crypto_57.txt#L181-L260)):

| Setup altcoin | Kondisi BTC | Tindakan |
|---|---|---|
| Bullish | Bullish | Long ("long maksimal") |
| Bullish | Sideways dalam range 1–2% | Masih boleh long |
| Bullish | Bearish | **Jangan masuk dulu** (rawan *false breakout*) |
| Bearish | Bearish | Short |
| Bearish | Sideways | Masih short |
| Bearish | Bullish | **Waspada** ("awas ketarik", rawan *false breakdown*) |

**3. Pasar saham AS** (jika trading di atas jam 19.00 WIB; cek mulai 17.00 WIB). Long altcoin saat pasar AS hijau ±50% berhasil; saat pasar AS merah hanya ±20% ([AC_crypto_57 L281–L335](../materi/mentah/AC_crypto_57.txt#L281-L335)). Angka ini perkiraan mentor, bukan hasil uji.

**4. Dominasi BTC (BTC.D)** ([AC_crypto_57 L365–L435](../materi/mentah/AC_crypto_57.txt#L365-L435)):

| BTC.D | Harga BTC | Altcoin |
|---|---|---|
| Naik | Naik | Turun (uang pindah ke BTC) |
| Naik | Turun | Turun drastis |
| Turun | Naik | Naik drastis (*altseason*) |
| Turun | Stabil | Naik |

**5. Data derivatif** (pelengkap) ([AC_crypto_57 L460–L589](../materi/mentah/AC_crypto_57.txt#L460-L589)):

- *Funding* positif = mayoritas long (bullish); negatif = mayoritas short. Sebagai kontrarian tetap waspada.
- *Open interest*: harga naik + OI naik = naik kuat; harga naik + OI turun = lemah; harga turun + OI naik = turun kuat; harga turun + OI turun = turun lemah.

Kalau nanti altcoin dibuka, "BTC bullish/bearish/sideways" bisa memakai definisi struktur [D-02](00-aturan-global.md#d-02--struktur-dan-tren). Untuk BTC dan ETH sendiri, kemiripan geraknya sudah ditangani di [G-08](00-aturan-global.md#g-08--jangan-overtrading): posisi searah dihitung satu posisi.

---

### AFS-F2 · Konfirmasi volume untuk breakout

| | |
|---|---|
| Sumber | [AC_crypto_57 L1794–L1843](../materi/mentah/AC_crypto_57.txt#L1794-L1843); Dow: [AC_crypto_60 L1322–L1340](../materi/mentah/AC_crypto_60.txt#L1322-L1340) |
| Pasar | K, F\* |
| Status | ⚪ 🟢 |

**Aturan:** breakout **tanpa** kenaikan volume cenderung palsu → setup breakout dibatalkan. Breakout **dengan** volume naik → valid. Prinsip yang sama diulang Kalimasada (Wyckoff) dan Ko Hengki ([HKI-F2](04-ko-hengki-remora.md#hki-f2--breakout-pola-harus-bervolume)).

- **Volume naik** = volume candle breakout di atas rata-rata 20 candle terakhir ([D-07](00-aturan-global.md#d-07--volume), Q-26).
- **Forex:** tick volume, dibandingkan dengan versi tanpa filter ini (Q-14).
- Berlaku untuk setup yang masuk saat **breakout**: AFS-03 (tembus neckline), AFS-09, AFS-20 (mode breakout), KMS-02, HKI-01 (*buy on breakout*). Tidak dipasang di AFS-18 (sudah memakai CMF; G-11) dan PLN-01 (mentornya tidak memakai volume). *(Daftar ini penerapan saya atas kata "breakout" di aturan mentor.)*

---

### AFS-F3 · Momentum: akselerasi & deselerasi

| | |
|---|---|
| Sumber | [AC_crypto_59 L1–L195](../materi/mentah/AC_crypto_59.txt#L1-L195) |
| Status | ⚪ 🔴 (tidak ada angka) |

- **Akselerasi:** candle besar, wick sedikit, jarak harga ditempuh dalam waktu singkat → tren kuat, berlanjut.
- **Deselerasi:** banyak wick, butuh lebih banyak candle untuk jarak yang sama → tanda keraguan, potensi koreksi atau pembalikan ([AC_crypto_59 L71–L185](../materi/mentah/AC_crypto_59.txt#L71-L185)).

Mentor tidak memberi ukuran angka (rasio wick/body, jumlah candle). Kalau ingin dipakai, ambangnya harus dicari lewat backtest.
