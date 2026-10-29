# 01 · ALVESTING (AFS) — Akademi Crypto

Alvesting adalah pengajar teknikal Akademi Crypto. Materinya paling banyak dan paling sistematis, jadi ini **mesin utama** bot. Semua contoh di kelas memakai kripto (terutama BTC), tetapi hampir semuanya berlaku juga di forex. Angka yang khas kripto ditandai **K\*** / **F\***.

Aturan global ([00](00-aturan-global.md)) tetap berlaku di atas semua setup di halaman ini.

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
  - [AFS-12 Pivot](#afs-12--pivot-point-entry-di-garis-p) · [AFS-13 Keltner](#afs-13--keltner-channel) · [AFS-14 Ichimoku](#afs-14--ichimoku-di-atasbawah-semua-garis) · [AFS-15 Parabolic SAR](#afs-15--parabolic-sar-titik-ke-2) · [AFS-16 Donchian](#afs-16--donchian-channel) · [AFS-17 KST](#afs-17--kst-silang-di-garis-nol) · [AFS-18 CMF](#afs-18--konfirmasi-chaikin-money-flow) · [AFS-19 POC](#afs-19--pantulan-poc-volume-profile) · [AFS-20 LRC](#afs-20--linear-regression-channel) · [AFS-21 Renko](#afs-21--renko-reversal)
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
| Status | 🟡 |

**Syarat 1 — Tren (D1).** Tentukan bias.

- **Bullish** = struktur membuat **minimal 2 higher low dan 2 higher high**. Sebuah higher low tetap valid selama low sebelumnya tidak ditembus. Tembusnya high sebelumnya = *break of structure* ke atas ([AC_crypto_35 L370–L429](../materi/mentah/AC_crypto_35.txt#L370-L429)). → bias **long**.
- **Bearish** = minimal 2 lower high dan 2 lower low ([AC_crypto_35 L425–L469](../materi/mentah/AC_crypto_35.txt#L425-L469)). → bias **short**.
- **Sideways** = *equal high* dan *equal low* di range sempit ([AC_crypto_35 L460–L499](../materi/mentah/AC_crypto_35.txt#L460-L499)). → **tidak ada bias**, setup ini tidak dipakai. Mentor: kalau tidak tahu arah pasar, jangan berharap untung ([AC_crypto_35 L80–L99](../materi/mentah/AC_crypto_35.txt#L80-L99)).
- Alat bantu tren (boleh dipakai, **maksimal satu**, lihat G-11):
  - **Trendline**: garis diagonal lewat minimal 2 titik. Uptrend digambar di bawah harga; harga yang memantul di trendline = peluang long; tembus ke bawah = tanda pembalikan. Downtrend sebaliknya ([AC_crypto_35 L500–L579](../materi/mentah/AC_crypto_35.txt#L500-L579)).
  - **Moving average**: harga di atas MA → bias long; tembus ke bawah → tanda pembalikan. Contoh MA20/MA10 di D1, dan MA50 sebagai penolak di downtrend ([AC_crypto_35 L590–L615](../materi/mentah/AC_crypto_35.txt#L590-L615), [AC_crypto_35 L690–L705](../materi/mentah/AC_crypto_35.txt#L690-L705)).
  - **Bollinger Bands** (tengahnya MA20): menyentuh band bawah = jenuh jual, band atas = jenuh beli ([AC_crypto_35 L612–L635](../materi/mentah/AC_crypto_35.txt#L612-L635)).
  - **Supertrend**: harga di atas (hijau) → bias long; di bawah (merah) → bias short ([AC_crypto_35 L635–L649](../materi/mentah/AC_crypto_35.txt#L635-L649)).

**Syarat 2 — Area.** Posisi hanya dibuka di area yang tepat.

- Long **hanya** di support/demand. Short **hanya** di resistance/supply. Jangan long di resistance, jangan short di support ([AC_crypto_58 L1475–L1499](../materi/mentah/AC_crypto_58.txt#L1475-L1499)).
- Di kripto, support/resistance digambar sebagai **zona** (kotak), bukan satu garis, karena harga "pasti copy di sekitar situ" ([AC_crypto_58 L1645–L1699](../materi/mentah/AC_crypto_58.txt#L1645-L1699)).
- Lima cara menemukan area ([AC_crypto_58 L1640–L2060](../materi/mentah/AC_crypto_58.txt#L1640-L2060)):
  1. Zona horizontal.
  2. Trendline sebagai support/resistance diagonal.
  3. Area dinamis dari indikator: EMA 13 & 21 ([AFS-05](#afs-05--money-magnet-ema-13--21)), Bollinger, Supertrend.
  4. Pivot point: P = (High + Low + Close periode sebelumnya) ÷ 3 ([AFS-12](#afs-12--pivot-point-entry-di-garis-p)).
  5. Fibonacci: *golden pocket* 0,5–0,618 ([AFS-04](#afs-04--pantulan-golden-pocket-fibonacci)).
- Makin banyak alat yang bertemu di area yang sama (*confluence*), makin bagus setup-nya ([AC_crypto_58 L2063–L2088](../materi/mentah/AC_crypto_58.txt#L2063-L2088)).

**Syarat 3 — Pola (H4).** Ada pola harga yang searah bias di area tersebut. Pola **bukan alat utama**, hanya konfirmasi; tren dan area harus beres dulu ([AC_crypto_57 L1341–L1380](../materi/mentah/AC_crypto_57.txt#L1341-L1380)). Contoh dari mentor: double bottom ([AC_crypto_35 L260–L269](../materi/mentah/AC_crypto_35.txt#L260-L269)) dan falling wedge di support ([AC_crypto_57 L1560–L1569](../materi/mentah/AC_crypto_57.txt#L1560-L1569)). Daftar pola ada di [AFS-23](#afs-23--pola-grafik-klasik).

**Syarat 4 — Pemicu (M15).** M15 disebut timeframe paling ideal untuk melihat pemicu ([AC_crypto_57 L1484–L1503](../materi/mentah/AC_crypto_57.txt#L1484-L1503)). Pemicu bisa dari:

- **Candlestick**: long → *hammer*, *inverted hammer*, *bullish engulfing*. Short → *hanging man*, *shooting star*, *bearish engulfing*. Engulfing dan hanging man dengan volume tinggi dianggap lebih kuat ([AC_crypto_57 L1500–L1713](../materi/mentah/AC_crypto_57.txt#L1500-L1713)).
- **Osilator**: **Stochastic 5,3,3** (setting favorit Alvesting): silang naik di area jenuh jual → long; silang turun di area jenuh beli → short. Juga RSI (jenuh beli/jual) dan MACD (silang) ([AC_crypto_57 L1744–L1800](../materi/mentah/AC_crypto_57.txt#L1744-L1800)).
- **Volume**: breakout tanpa volume cenderung palsu ([AFS-F2](#afs-f2--konfirmasi-volume-untuk-breakout)).

**Contoh lengkap dari mentor:** D1 naik → long di support → H4 ada double bottom → M15 stochastic jenuh jual + hammer → eksekusi ([AC_crypto_57 L1854–L1873](../materi/mentah/AC_crypto_57.txt#L1854-L1873)).

**Entry:** setelah candle pemicu M15 selesai terbentuk (*close*).

**Stop loss:** long di bawah swing low / area support; short di atas swing high / area resistance, dengan jarak tambahan ATR (G-02) ([AC_crypto_59 L2740–L2859](../materi/mentah/AC_crypto_59.txt#L2740-L2859)).

**Take profit:** di area lawan (long → resistance terdekat; short → support terdekat) ([AC_crypto_59 L2710–L2739](../materi/mentah/AC_crypto_59.txt#L2710-L2739)). Alternatif yang disebut mentor: angka psikologis (angka bulat), Fibonacci, pivot ([AC_crypto_59 L2760–L2809](../materi/mentah/AC_crypto_59.txt#L2760-L2809)).

**Lama memegang posisi:** saat pasar bull, posisi long boleh ditahan lama. Saat pasar bear, posisi long diambil untungnya bertahap selama harga naik ([AC_crypto_35 L120–L149](../materi/mentah/AC_crypto_35.txt#L120-L149)).

**Batal / jangan masuk jika:**

- Pasar sideways (tidak ada bias).
- Harga tidak berada di area yang tepat.
- RR di bawah batas (G-03).

**Belum jelas:**

- Mentor bilang setup "sempurna" kalau **kelima poin** muncul bersamaan: tren terlihat, struktur 2HL/2HH, trendline dihormati, di area support, indikator mendukung ([AC_crypto_35 L650–L729](../materi/mentah/AC_crypto_35.txt#L650-L729)). Tidak ada ambang minimal → **Q-18**.
- Cara bot mengenali swing high/low → **Q-12**. Lebar zona → **Q-17**. Level jenuh beli/jual stochastic → **Q-13**. Definisi candle pemicu → **Q-16**. Deteksi pola → **Q-23**. Jarak ATR untuk SL → **Q-11**.

---

### AFS-02 · Technical Research 5 tahap, versi scalping

| | |
|---|---|
| Sumber | [AC_crypto_58 L2825–L3220](../materi/mentah/AC_crypto_58.txt#L2825-L3220) (dasar scalping), [AC_crypto_62 L3589–L3886](../materi/mentah/AC_crypto_62.txt#L3589-L3886) (persiapan teknikal), [AC_crypto_46](../materi/mentah/AC_crypto_46.txt) (mental) |
| Pasar | K, F |
| Timeframe | Tren **H1**, pola **M15**, pemicu **M5** ([AC_crypto_62 L3709–L3728](../materi/mentah/AC_crypto_62.txt#L3709-L3728)) |
| Arah | Dua arah dalam satu hari (long lalu short, atau sebaliknya) ([AC_crypto_62 L3609–L3668](../materi/mentah/AC_crypto_62.txt#L3609-L3668)) |
| Status | 🟡 |

**Aturan:** sama persis dengan AFS-01, tetapi timeframe-nya "dikompres", plus aturan khusus scalping:

1. **Risiko:** 0,5%–1% per transaksi, maksimal 2% ([AC_crypto_58 L3055–L3104](../materi/mentah/AC_crypto_58.txt#L3055-L3104), [AC_crypto_62 L3669–L3688](../materi/mentah/AC_crypto_62.txt#L3669-L3688)).
2. **RR:** harus lebih dari 1:1 karena biaya transaksi dan *funding*; targetkan 1:2 atau 1:3. 1:4–1:5 disebut sangat sulit ([AC_crypto_58 L3113–L3134](../materi/mentah/AC_crypto_58.txt#L3113-L3134)).
3. **Frekuensi:** 3–5 transaksi sehari sudah banyak ([AC_crypto_58 L3175–L3194](../materi/mentah/AC_crypto_58.txt#L3175-L3194)).
4. **Durasi:** menit sampai beberapa jam. Contoh mentor: "maksimal tiga jam". Lebih dari 24 jam bukan scalping lagi ([AC_crypto_58 L3015–L3054](../materi/mentah/AC_crypto_58.txt#L3015-L3054)).
5. **Gaya SL:** mentor membandingkan dua gaya. SL tipis + RR besar = menang hanya 30–40% tetapi sekali menang besar. SL lebar + RR 1:2 = menang 70–80%. Untuk trading setiap hari, mentor menyarankan **SL lebar, RR rendah** ([AC_crypto_62 L3765–L3878](../materi/mentah/AC_crypto_62.txt#L3765-L3878)).

**Contoh dari mentor** ([AC_crypto_62 L3719–L3768](../materi/mentah/AC_crypto_62.txt#L3719-L3768)): H1 masih bearish, tetapi terbentuk *descending broadening wedge* lalu breakout dan retest → bias long. M15: cari area, ada breakout + retest. M5: ada double bottom, breakout → entry. SL di bawah area. TP1, TP2, TP3.

**Belum jelas:**

- Apakah bot wajib menutup posisi scalping setelah batas waktu tertentu (misalnya 3 jam) → **Q-19**.
- Porsi TP1/TP2/TP3 → **Q-08**.
- Sama dengan AFS-01: Q-11, Q-12, Q-13, Q-16, Q-17, Q-23.

---

### AFS-03 · Double top/bottom + tembus neckline

| | |
|---|---|
| Sumber | [AC_crypto_58 L3135–L3175](../materi/mentah/AC_crypto_58.txt#L3135-L3175), [AC_crypto_57 L1121–L1189](../materi/mentah/AC_crypto_57.txt#L1121-L1189), [AC_crypto_57 L1271–L1300](../materi/mentah/AC_crypto_57.txt#L1271-L1300) |
| Pasar | K, F |
| Timeframe | M15 (contoh scalping) |
| Arah | Short (double top), long (double bottom) |
| Status | 🟡 |

**Syarat:**

1. Terbentuk double top: dua puncak yang hampir sama tinggi (*equal high*) yang gagal ditembus. Boleh triple top. **Tidak ada** "quadruple": setelah sentuhan ke-3 harga biasanya memilih arah ([AC_crypto_57 L1131–L1169](../materi/mentah/AC_crypto_57.txt#L1131-L1169)).
2. Tarik garis **neckline** (lembah di antara kedua puncak).

**Entry (versi konfirmasi):** setelah neckline **jebol**.
**SL:** di atas swing high (puncak).
**TP:** 1:2 dari jarak entry–SL ([AC_crypto_58 L3135–L3159](../materi/mentah/AC_crypto_58.txt#L3135-L3159)).

**Entry (versi agresif):** masuk **sebelum** neckline tembus, SL beberapa persen di atas swing high, target sama → RR bisa 1:6. Makin besar RR yang diinginkan, makin presisi entry dan makin tipis SL-nya ([AC_crypto_58 L3155–L3179](../materi/mentah/AC_crypto_58.txt#L3155-L3179)).

Double bottom = cerminannya (long).

**Belum jelas:** versi mana yang dipakai bot → **Q-09**. Batas "hampir sama tinggi" → **Q-23**.

---

## B. Fibonacci & area dinamis

### AFS-04 · Pantulan golden pocket Fibonacci

| | |
|---|---|
| Sumber | Fibonacci Secret: [AC_crypto_60 L1–L346](../materi/mentah/AC_crypto_60.txt#L1-L346), [AC_crypto_58 L3476–L3643](../materi/mentah/AC_crypto_58.txt#L3476-L3643), [AC_crypto_59 L824–L953](../materi/mentah/AC_crypto_59.txt#L824-L953), [AC_crypto_62 L2625–L2790](../materi/mentah/AC_crypto_62.txt#L2625-L2790), [AC_crypto_42](../materi/mentah/AC_crypto_42.txt), [AC_crypto_56](../materi/mentah/AC_crypto_56.txt); juga [AC_crypto_58 L1980–L2060](../materi/mentah/AC_crypto_58.txt#L1980-L2060) |
| Pasar | K, F\* |
| Timeframe | Paling valid **W1 / MN**; D1 masih oke. M1–M5 disebut "judi berlogika" ([AC_crypto_56 L41–L80](../materi/mentah/AC_crypto_56.txt#L41-L80)) |
| Arah | Long saat koreksi dalam uptrend; short saat *relief pump* dalam downtrend |
| Status | 🟡 |

**Syarat:**

1. Ada impuls yang jelas (gerakan pertama), lalu koreksi.
2. Tarik Fibonacci retracement dari **low ke high** impuls (uptrend) atau **high ke low** (downtrend) ([AC_crypto_60 L141–L169](../materi/mentah/AC_crypto_60.txt#L141-L169)).
3. Harga masuk **golden pocket 0,5–0,618**. Mentor: harga "sampai 80%" mengunjungi area ini ([AC_crypto_60 L191–L230](../materi/mentah/AC_crypto_60.txt#L191-L230)).
4. **Fokus hanya di golden pocket.** Level 0,236 / 0,382 / 0,786 juga bisa jadi pantulan, tetapi menurut rangkuman mentor peluangnya hanya sekitar 20% ([AC_crypto_56 L75–L99](../materi/mentah/AC_crypto_56.txt#L75-L99)).
5. **Wajib confluence**: golden pocket bertemu support horizontal, diagonal, atau dinamis. Contoh mentor: golden pocket + MA100 + support horizontal ([AC_crypto_56 L95–L139](../materi/mentah/AC_crypto_56.txt#L95-L139)).
6. Ada **pemicu** di area itu, seperti di AFS-01 ([AC_crypto_58 L3525–L3534](../materi/mentah/AC_crypto_58.txt#L3525-L3534)).

**Dua cara entry yang diajarkan:**

- **Varian A (antisipasi):** di golden pocket, setelah ada pemicu.
- **Varian B (konfirmasi):** setelah harga berbalik dan menembus trendline koreksi sekitar **3–5%**. Pada titik itu low koreksi dianggap sudah sah menjadi higher low ([AC_crypto_60 L201–L219](../materi/mentah/AC_crypto_60.txt#L201-L219), [AC_crypto_62 L2690–L2709](../materi/mentah/AC_crypto_62.txt#L2690-L2709)).

**SL:**

- Long: di bawah swing low (G-02).
- Short di level retracement: di atas **level 1** (titik awal impuls). Kalau level 1 tembus, tren dianggap berbalik ([AC_crypto_59 L884–L903](../materi/mentah/AC_crypto_59.txt#L884-L903)).

**TP:** ekstensi Fibonacci. Tarik dari high ke low (dibalik) supaya level ekstensi muncul. TP bertahap di **1 (high sebelumnya)**, **1,618**, **2,618**, **3,618**, **4,236** ([AC_crypto_60 L231–L262](../materi/mentah/AC_crypto_60.txt#L231-L262), [AC_crypto_60 L321–L340](../materi/mentah/AC_crypto_60.txt#L321-L340)). Alat yang lebih praktis menurut mentor: *trend-based Fib extension* (impuls utama + koreksi) ([AC_crypto_62 L2685–L2744](../materi/mentah/AC_crypto_62.txt#L2685-L2744)).

**Saat harga menembus ATH/ATL** (*price discovery*, tidak ada level harga di kiri), target diambil dari ekstensi 1,618 / 2,618 / 3,618 ([AC_crypto_58 L3586–L3643](../materi/mentah/AC_crypto_58.txt#L3586-L3643), [AC_crypto_59 L914–L953](../materi/mentah/AC_crypto_59.txt#L914-L953)).

**Belum jelas:**

- Angka **3–5%** di Varian B berasal dari kripto. Untuk forex → **Q-10**.
- Impuls mana yang ditarik (swing yang mana) → **Q-12**.
- Porsi tiap TP → **Q-08**.

---

### AFS-05 · Money magnet EMA 13 & 21

| | |
|---|---|
| Sumber | [AC_crypto_58 L1745–L1789](../materi/mentah/AC_crypto_58.txt#L1745-L1789); setting diklaim sudah diriset bertahun-tahun: [AC_crypto_61 L2253–L2262](../materi/mentah/AC_crypto_61.txt#L2253-L2262) |
| Pasar | K, F |
| Arah | Long dalam uptrend (cerminannya untuk downtrend) |
| Status | 🟡 |

**Aturan:** dua EMA, **13 dan 21**, bekerja seperti magnet. Dalam uptrend, setiap koreksi "selalu mencari" area EMA 13–21 lalu memantul → **long di area EMA**. Mentor menyebutnya *dynamic support*, lebih cocok dengan pergerakan kripto yang sangat volatil dibanding garis horizontal atau diagonal ([AC_crypto_58 L1795–L1819](../materi/mentah/AC_crypto_58.txt#L1795-L1819)).

Setup ini terutama dipakai sebagai **sumber area** di AFS-01. Kalau berdiri sendiri, SL dan TP tidak disebut mentor → memakai G-02 dan G-03.

**Belum jelas:** RR untuk versi berdiri sendiri → **Q-07**.

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

### AFS-06 · Stop hunt + break of structure

| | |
|---|---|
| Sumber | [AC_crypto_34 L560–L824](../materi/mentah/AC_crypto_34.txt#L560-L824), [AC_crypto_58 L1010–L1040](../materi/mentah/AC_crypto_58.txt#L1010-L1040), [AC_crypto_59 L255–L370](../materi/mentah/AC_crypto_59.txt#L255-L370) |
| Pasar | K (aset besar), F |
| Timeframe | H4 arah, M15 pemicu; makin besar timeframe makin valid |
| Arah | Short setelah BSL disapu; long setelah SSL disapu |
| Status | 🟡 |

Mentor menyebut ini "kombinasi paling ampuh" dan menyarankan fokus di sini saja: "keep it simple" ([AC_crypto_59 L351–L370](../materi/mentah/AC_crypto_59.txt#L351-L370)). Klaim tingkat menang 70–80%, makin tinggi di timeframe besar ([AC_crypto_34 L705–L724](../materi/mentah/AC_crypto_34.txt#L705-L724)).

**Short:**

1. Harga sedang naik, membentuk higher low.
2. Harga menembus **high acuan** (BSL) dengan agresif. Short yang terlalu awal dan long yang ikut breakout sama-sama tersapu.
3. Harga **kembali ke dalam range** (RTO).
4. **Higher low terakhir ditembus** (BMS, berdasarkan close).
5. → **Short** ([AC_crypto_34 L665–L700](../materi/mentah/AC_crypto_34.txt#L665-L700), [AC_crypto_34 L720–L760](../materi/mentah/AC_crypto_34.txt#L720-L760)).
6. **SL:** di atas swing high, yaitu puncak stop hunt ([AC_crypto_59 L351–L360](../materi/mentah/AC_crypto_59.txt#L351-L360)).

**Long:** cerminannya. Harga turun → menembus **low acuan** (SSL) → kembali ke range → **lower high terakhir ditembus** → long, SL di bawah swing low ([AC_crypto_34 L700–L719](../materi/mentah/AC_crypto_34.txt#L700-L719), [AC_crypto_34 L765–L819](../materi/mentah/AC_crypto_34.txt#L765-L819)).

**Variasi yang disebut mentor jarang terjadi** (*liquidity pattern*: CHoCH + quick RTO, CHoCH + late RTO, *confirmation entry*, SH + *fake* BMS). Mentor sendiri bilang sekitar 80% tidak terjadi, jadi cukup fokus ke SH + BMS ([AC_crypto_58 L840–L1040](../materi/mentah/AC_crypto_58.txt#L840-L1040), [AC_crypto_59 L331–L350](../materi/mentah/AC_crypto_59.txt#L331-L350)). Tidak dijadikan aturan.

**Belum jelas** → **Q-20**:

- Entry langsung saat candle BMS close, atau menunggu harga kembali ke order block/FVG? Mentor menyebut "BOS + order block = perfect combo" ([AC_crypto_59 L385–L400](../materi/mentah/AC_crypto_59.txt#L385-L400)).
- TP: mentor tidak menyebut. Hanya RR minimal 1:2 (jangka pendek) / >1:3 (swing).
- Seberapa jauh harga harus menembus high/low acuan supaya dihitung *stop hunt*, dan berapa lama maksimal untuk kembali ke range.

---

### AFS-07 · Change of character (CHoCH) + retest

| | |
|---|---|
| Sumber | [AC_crypto_58 L597–L809](../materi/mentah/AC_crypto_58.txt#L597-L809) |
| Pasar | K, F |
| Arah | Short (CHoCH bearish), long (CHoCH bullish) |
| Status | 🟡 |

**Short (bullish berubah jadi bearish):**

1. Uptrend: higher high dan higher low.
2. **Higher low terakhir ditembus** → CHoCH.
3. Tunggu harga **retest** area yang ditembus.
4. → Short di retest.
5. **SL:** di atas swing high terakhir. Boleh dimodifikasi, asal RR minimal **1:2** untuk jangka pendek dan **lebih dari 1:3** untuk swing ([AC_crypto_58 L685–L739](../materi/mentah/AC_crypto_58.txt#L685-L739)).

**Long:** cerminannya. Lower high terakhir ditembus → retest → long, SL di bawah swing low terakhir ([AC_crypto_58 L740–L769](../materi/mentah/AC_crypto_58.txt#L740-L769)).

**Kegunaan lain:** CHoCH berlawanan arah dipakai untuk **mengamankan sebagian atau seluruh profit** posisi yang sedang terbuka ([AC_crypto_58 L645–L669](../materi/mentah/AC_crypto_58.txt#L645-L669)).

**Catatan alat:** indikator gratis "Smart Money Concepts" dari LuxAlgo di TradingView bisa menandai BOS/CHoCH otomatis. Mentor mengingatkan algoritmanya sering salah membaca *noise* ([AC_crypto_58 L770–L809](../materi/mentah/AC_crypto_58.txt#L770-L809)).

**Belum jelas:** apa yang dihitung "retest" (seberapa dekat, berapa lama ditunggu) → **Q-20**. Definisi swing → **Q-12**.

---

### AFS-08 · Revisit order block / fair value gap

| | |
|---|---|
| Sumber | [AC_crypto_58 L290–L596](../materi/mentah/AC_crypto_58.txt#L290-L596), [AC_crypto_59 L300–L330](../materi/mentah/AC_crypto_59.txt#L300-L330), [AC_crypto_59 L370–L405](../materi/mentah/AC_crypto_59.txt#L370-L405) |
| Pasar | K, F |
| Arah | Long di bullish OB, short di bearish OB |
| Status | 🟡 |

**Aturan:**

1. **Bullish order block** = area konsolidasi tepat sebelum candle besar yang mendorong harga naik dengan volume tinggi. Celah yang ditinggalkan candle besar itu disebut *imbalance* / *fair value gap* (FVG) ([AC_crypto_58 L310–L359](../materi/mentah/AC_crypto_58.txt#L310-L359)). **Bearish OB** = kebalikannya.
2. Mentor **menyamakan** OB dan FVG ("konsepnya sama") ([AC_crypto_58 L380–L399](../materi/mentah/AC_crypto_58.txt#L380-L399)), dan mendeteksinya dengan indikator **FVG dari LuxAlgo** ([AC_crypto_58 L400–L439](../materi/mentah/AC_crypto_58.txt#L400-L439)).
3. Harga cenderung **kembali mengisi** celah itu. Long saat harga kembali ke bullish OB/FVG; short saat kembali ke bearish OB/FVG ([AC_crypto_58 L439–L465](../materi/mentah/AC_crypto_58.txt#L439-L465), [AC_crypto_58 L490–L590](../materi/mentah/AC_crypto_58.txt#L490-L590)).
4. Paling kuat setelah **break of structure** di timeframe besar ("perfect combo") ([AC_crypto_59 L385–L400](../materi/mentah/AC_crypto_59.txt#L385-L400)).

**SL:** short di atas swing high / di atas bearish OB ([AC_crypto_58 L555–L565](../materi/mentah/AC_crypto_58.txt#L555-L565)). Long cerminannya.

**Belum jelas:** definisi persis OB/FVG untuk bot → **Q-21**. TP → **Q-20**.

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
| Timeframe | D1 ke atas (swing / investasi) |
| Arah | Long dan short |
| Status | 🟡 |

**Long (pembalikan naik):**

1. Tren sebelumnya turun; harga berkonsolidasi **di bawah MA**.
2. Harga menembus MA ke atas.
3. **Baru dianggap valid kalau harga sudah 3% di atas MA** (atau 3% di atas trendline downtrend). → long ([AC_crypto_47 L321–L369](../materi/mentah/AC_crypto_47.txt#L321-L369)).

**Short:** cerminannya. Tembus ke bawah MA21 atau trendline uptrend, valid setelah 3% di bawahnya ([AC_crypto_47 L369–L395](../materi/mentah/AC_crypto_47.txt#L369-L395)).

**MA yang dipakai:** jangka pendek **13 dan 21** (contoh mentor: MA21 D1); jangka panjang **50 dan 100** ([AC_crypto_47 L261–L290](../materi/mentah/AC_crypto_47.txt#L261-L290)).

**Catatan mentor:** untuk scalper, 3% itu terlambat. Untuk swing trader dan investor, menunggu 3% sepadan dengan kepastiannya ([AC_crypto_47 L391–L410](../materi/mentah/AC_crypto_47.txt#L391-L410)).

**Juga dari Dow, tetapi tidak dijadikan aturan (🔴):**

- Titik tren A-B-C-D ([AC_crypto_47 L1–L230](../materi/mentah/AC_crypto_47.txt#L1-L230)): definisi titiknya terlalu kabur untuk dikodekan.
- "Tiga lini masa" (tren berlawanan biasanya baru tembus di periode ke-3, contoh satuan 7 hari) ([AC_crypto_62 L3887–L4001](../materi/mentah/AC_crypto_62.txt#L3887-L4001)): satuan dan cara mengukurnya tidak jelas.
- Fase akumulasi → partisipasi publik → euforia → distribusi → panik ([AC_crypto_57 L2207–L2410](../materi/mentah/AC_crypto_57.txt#L2207-L2410)): konteks investasi jangka panjang.

**Belum jelas:** SL dan TP tidak disebut → G-02/G-03. Angka 3% untuk forex → **Q-10**.

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
| Status | 🟡 |

**Syarat (seperti yang tertulis di transkrip):**

1. Empat titik A → B → C → D, bentuk seperti petir.
2. Rasio "**AC**" berada di **0,382–0,886**.
3. Rasio "**BD**" berada di **1,232–2,618**.
4. Contoh mentor: AC 0,85 dan BD 1,477 → valid ([AC_crypto_57 L2451–L2499](../materi/mentah/AC_crypto_57.txt#L2451-L2499)).

**Entry:** di titik D, **setelah** konfirmasi candle (hammer, bullish engulfing, inverted hammer).
**SL:** beberapa persen di bawah D / swing low, atau pakai ATR persen ([AC_crypto_57 L2515–L2535](../materi/mentah/AC_crypto_57.txt#L2515-L2535)).

**Belum jelas** → **Q-23**: transkrip menyebut "AB" dan "AC" bergantian untuk rasio pertama, dan angka "1,232" tidak lazim. Bot butuh kepastian kaki mana diukur terhadap kaki mana, serta toleransi rasio.

---

### AFS-11 · Pola harmonic XABCD

| | |
|---|---|
| Sumber | Gartley [AC_crypto_60 L347–L579](../materi/mentah/AC_crypto_60.txt#L347-L579) · Bat [AC_crypto_62 L2246–L2481](../materi/mentah/AC_crypto_62.txt#L2246-L2481) · Crab [AC_crypto_43](../materi/mentah/AC_crypto_43.txt) · rasio dasar, Shark, Butterfly [AC_crypto_61 L618–L851](../materi/mentah/AC_crypto_61.txt#L618-L851) · harmonic H&S, 5-0 [AC_crypto_54 L162–L322](../materi/mentah/AC_crypto_54.txt#L162-L322) |
| Pasar | K, F |
| Timeframe | Umumnya timeframe besar. Gartley disebut paling cocok H1/M15 ([AC_crypto_60 L367–L386](../materi/mentah/AC_crypto_60.txt#L367-L386)) |
| Status | 🔴 |

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

**Kenapa 🔴:**

- Penamaan kaki rasio di transkrip tidak konsisten (A→C, X→B, "rasio atas/bawah").
- Ada pernyataan yang saling bertentangan: harmonic extension disebut "W = bullish" tetapi harga di D "turun" ([AC_crypto_61 L648–L690](../materi/mentah/AC_crypto_61.txt#L648-L690)).
- Mentor sendiri menyebut pola ini sangat subjektif.

**Pertanyaan** → **Q-23**: pakai rasio persis transkrip, rasio standar buku Scott Carney, atau tunda pola harmonic ke versi berikutnya?

---

### AFS-23 · Pola grafik klasik

| | |
|---|---|
| Sumber | [AC_crypto_57 L601–L1383](../materi/mentah/AC_crypto_57.txt#L601-L1383) (Technical Research 3), Kamus Pattern Crypto ([PETA 5.F3](../materi/PETA.md#f3-kamus-pattern-crypto-kpk)) |
| Pasar | K, F |
| Status | 🔴 sebagai setup mandiri; dipakai sebagai **konfirmasi** di AFS-01 |

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

Pola juga bisa menjadi **alat invalidasi**: kalau muncul pola berlawanan, posisi boleh ditutup. Namun mentor tetap menyarankan setia pada trading plan ([AC_crypto_59 L1625–L1644](../materi/mentah/AC_crypto_59.txt#L1625-L1644)).

**Pertanyaan** → **Q-23**: apakah pola grafik ditunda dulu di bot versi pertama?

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
| Timeframe | **H1, M15, M5** (intraday / scalping) ([AC_crypto_44 L285–L295](../materi/mentah/AC_crypto_44.txt#L285-L295)) |
| Status | 🟡 |

**Indikator:** *Pivot Points Standard*, tipe **Traditional**, default ([AC_crypto_44 L65–L89](../materi/mentah/AC_crypto_44.txt#L65-L89)). Rumus ([AC_crypto_44 L35–L65](../materi/mentah/AC_crypto_44.txt#L35-L65)):

```
P  = (High + Low + Close) ÷ 3            ← periode sebelumnya
R1 = 2P − Low        S1 = 2P − High
R2 = P + (High − Low)  S2 = P − (High − Low)
```

Hanya pakai **P, S1–S3, R1–R3**. Level di luar itu terlalu jauh ([AC_crypto_44 L110–L129](../materi/mentah/AC_crypto_44.txt#L110-L129)).

**Long:**

1. Harga di atas P dan sedang berkonsolidasi di area R. **Jangan long di R.**
2. Tunggu harga turun ke **P**.
3. → Long di P ([AC_crypto_44 L160–L199](../materi/mentah/AC_crypto_44.txt#L160-L199)).
4. **SL:** di bawah P (agresif, contoh BTC ±0,3%) **atau** di bawah S1 (konservatif, ±1–2%) ([AC_crypto_44 L195–L249](../materi/mentah/AC_crypto_44.txt#L195-L249)).
5. **TP:** R1, R2, R3 ([AC_crypto_44 L250–L270](../materi/mentah/AC_crypto_44.txt#L250-L270)).

**Short:**

1. Harga tembus ke bawah P.
2. Tunggu harga naik kembali ke P.
3. → Short di P.
4. **SL:** di atas P atau di atas R1.
5. **TP:** S1, S2 ([AC_crypto_44 L210–L230](../materi/mentah/AC_crypto_44.txt#L210-L230), [AC_crypto_44 L270–L290](../materi/mentah/AC_crypto_44.txt#L270-L290)).

Mentor: tunggu setup pivot-nya siap, jangan asal masuk ([AC_crypto_44 L285–L295](../materi/mentah/AC_crypto_44.txt#L285-L295)).

**Belum jelas** → **Q-22**: pivot dihitung dari periode harian atau mingguan? SL versi agresif atau konservatif? Porsi TP → **Q-08**.

---

### AFS-13 · Keltner Channel

| | |
|---|---|
| Sumber | [AC_crypto_44 L300–L489](../materi/mentah/AC_crypto_44.txt#L300-L489) |
| Pasar | K, F |
| Status | 🟡 |

**Setting dari mentor:** garis tengah **SMA 20**, ATR **10**, pengali **2**. Pita atas = SMA + 2×ATR, pita bawah = SMA − 2×ATR ([AC_crypto_44 L340–L369](../materi/mentah/AC_crypto_44.txt#L340-L369)).

**Mode tren:**

- **Long:** harga di atas garis tengah. Entry saat breakout yang dikonfirmasi volume, **atau lebih baik** saat harga turun lagi menyentuh garis tengah (retest). Kalau ketinggalan, jangan kejar. SL di bawah garis tengah. TP pita atas. RR 1:2–1:3 ([AC_crypto_44 L390–L425](../materi/mentah/AC_crypto_44.txt#L390-L425)).
- **Short:** harga di bawah garis tengah, retest garis tengah dari bawah + pemicu melemah. SL di atas garis tengah. TP pita bawah ([AC_crypto_44 L425–L455](../materi/mentah/AC_crypto_44.txt#L425-L455)).

**Mode pantulan:**

- **Long:** harga menyentuh pita bawah (jenuh jual). SL di bawah swing low / pita bawah. TP1 garis tengah, TP2 pita atas ([AC_crypto_44 L450–L480](../materi/mentah/AC_crypto_44.txt#L450-L480)).
- **Short:** harga menyentuh pita atas. TP1 garis tengah, TP2 pita bawah ([AC_crypto_44 L475–L489](../materi/mentah/AC_crypto_44.txt#L475-L489)).

**Belum jelas** → **Q-24**:

- Mode tren dan mode pantulan bisa memberi sinyal berlawanan di saat yang sama. Mana yang dipakai bot?
- Mentor menyebut garis tengah SMA **dan** "pakai default". Default Keltner di TradingView memakai EMA. Mana yang benar?

---

### AFS-14 · Ichimoku "di atas/bawah semua garis"

| | |
|---|---|
| Sumber | [AC_crypto_44 L490–L714](../materi/mentah/AC_crypto_44.txt#L490-L714) |
| Pasar | K, F |
| Timeframe | D1 |
| Status | 🟢 (logika lengkap; TP mengikuti G-03) |

**Setting:** Tenkan 9, Kijun 26, Senkou Span B 52 ([AC_crypto_44 L520–L575](../materi/mentah/AC_crypto_44.txt#L520-L575)).

**Long:** candle D1 **close di atas semua garis**: Kumo (awan), Tenkan, Kijun, dan Chikou di atasnya. Contoh mentor disertai volume tinggi. **SL di bawah Kumo** ([AC_crypto_44 L590–L660](../materi/mentah/AC_crypto_44.txt#L590-L660)).

**TP:** mentor menyebut "beberapa target" di garis-garis Ichimoku sebagai *dynamic resistance*, tetapi garisnya ditunjuk di layar dan tidak bisa dipastikan dari transkrip ([AC_crypto_44 L651–L665](../materi/mentah/AC_crypto_44.txt#L651-L665)). Jadi TP mengikuti RR minimum (**Q-07**).

**Short:** candle D1 **close di bawah semua garis**. Entry saat harga **retest Kumo dari bawah**. **SL di atas Kumo** ([AC_crypto_44 L665–L700](../materi/mentah/AC_crypto_44.txt#L665-L700)).

Lihat juga versi Ichimoku yang jauh lebih lengkap dari Rafał di [06 · ICH-01–04](06-mentor-forex.md#c-ichimoku--rafał-zuchowicz-forex_3).

---

### AFS-15 · Parabolic SAR titik ke-2

| | |
|---|---|
| Sumber | [AC_crypto_59 L3401–L3555](../materi/mentah/AC_crypto_59.txt#L3401-L3555) |
| Pasar | K, F |
| Timeframe | Konfirmasi di H1/H4 ([AC_crypto_59 L3491–L3500](../materi/mentah/AC_crypto_59.txt#L3491-L3500)) |
| Status | 🟡 |

**Setting:** default TradingView.

**Long:** titik PSAR muncul **di bawah** harga. Masuk pada **titik ke-2** (sedang). Titik ke-1 = agresif; titik ke-3 = konfirmasi kuat tetapi sering sudah kehilangan momentum ([AC_crypto_59 L3451–L3500](../materi/mentah/AC_crypto_59.txt#L3451-L3500)).
**SL:** di bawah titik PSAR atau swing low, sebaiknya di balik support supaya tidak tersapu *stop hunt* ([AC_crypto_59 L3471–L3490](../materi/mentah/AC_crypto_59.txt#L3471-L3490)).
**TP:** resistance horizontal, psikologis, atau harmonic. RR minimal 1:2 (1:2, 1:3, 1:5) ([AC_crypto_59 L3461–L3470](../materi/mentah/AC_crypto_59.txt#L3461-L3470)).

**Short:** cerminannya ([AC_crypto_59 L3501–L3540](../materi/mentah/AC_crypto_59.txt#L3501-L3540)).

**Belum jelas:** level TP mana yang dipilih bot → **Q-07**.

---

### AFS-16 · Donchian Channel

| | |
|---|---|
| Sumber | [AC_crypto_59 L3556–L3718](../materi/mentah/AC_crypto_59.txt#L3556-L3718) |
| Pasar | K, F |
| Status | 🟡 |

**Setting:** default TradingView. Atas = high tertinggi N periode; bawah = low terendah N periode; tengah = rata-rata keduanya ([AC_crypto_59 L3586–L3610](../materi/mentah/AC_crypto_59.txt#L3586-L3610)).

**Cara yang diajarkan mentor:**

- **Pantulan:** long di pita bawah, SL di bawah swing low, TP1 garis tengah, TP2 pita atas. Short di pita atas, cerminannya ([AC_crypto_59 L3640–L3680](../materi/mentah/AC_crypto_59.txt#L3640-L3680)).
- **Tren:** harga silang ke atas garis tengah → uptrend → long, target 1:3–1:5. Tembus ke bawah garis tengah + retest → short, SL di atas swing high, TP pita bawah ([AC_crypto_59 L3680–L3710](../materi/mentah/AC_crypto_59.txt#L3680-L3710)).

**Belum jelas** → **Q-24**: Donchian biasanya dipakai untuk **breakout**, sedangkan mentor memakainya untuk pantulan dan silang garis tengah. Mode mana yang dipakai bot?

---

### AFS-17 · KST silang di garis nol

| | |
|---|---|
| Sumber | [AC_crypto_61 L2513–L2646](../materi/mentah/AC_crypto_61.txt#L2513-L2646) |
| Pasar | K, F |
| Timeframe | **D1** |
| Status | 🟢 (logika lengkap; SL/TP mengikuti G-02/G-03) |

**Setting:** default TradingView ([AC_crypto_61 L2545–L2560](../materi/mentah/AC_crypto_61.txt#L2545-L2560)).

- **Long:** KST **di bawah nol**, lalu garis KST **silang naik** garis sinyalnya.
- **Short:** KST **di atas nol**, lalu silang turun.
- Tunggu silang **valid** (candle selesai), jangan masuk sebelum silang ([AC_crypto_61 L2590–L2640](../materi/mentah/AC_crypto_61.txt#L2590-L2640)).

---

### AFS-18 · Konfirmasi Chaikin Money Flow

| | |
|---|---|
| Sumber | [AC_crypto_62 L2482–L2624](../materi/mentah/AC_crypto_62.txt#L2482-L2624) |
| Pasar | K, F\* (butuh volume, lihat Q-14) |
| Timeframe | Makin besar makin valid (H4, D1) |
| Status | 🟡 |

**Setting:** CMF periode **20** ([AC_crypto_62 L2522–L2530](../materi/mentah/AC_crypto_62.txt#L2522-L2530)).

- **Long:** harga menembus resistance **dan** CMF close di atas 0 ([AC_crypto_62 L2542–L2571](../materi/mentah/AC_crypto_62.txt#L2542-L2571)).
- **Short:** harga jebol support **dan** CMF di bawah 0 ([AC_crypto_62 L2572–L2591](../materi/mentah/AC_crypto_62.txt#L2572-L2591)).
- **Divergensi bullish:** harga turun tetapi CMF naik → long, SL di bawah swing low. **Divergensi bearish:** harga naik tetapi CMF turun → short, SL di atas swing high. RR 1:2–1:3 ([AC_crypto_62 L2592–L2615](../materi/mentah/AC_crypto_62.txt#L2592-L2615)).

**Belum jelas:** cara bot mengukur divergensi (swing mana dibandingkan) → **Q-12**. Volume di forex → **Q-14**.

---

### AFS-19 · Pantulan POC (volume profile)

| | |
|---|---|
| Sumber | [AC_crypto_58 L3223–L3318](../materi/mentah/AC_crypto_58.txt#L3223-L3318), [AC_crypto_39](../materi/mentah/AC_crypto_39.txt) |
| Pasar | K, F\* |
| Status | 🟡 |

**Indikator:** *Volume Profile Fixed Range* (versi komunitas "LonesomeTheBlue"). **POC** = level harga dengan volume terbanyak ([AC_crypto_58 L3233–L3270](../materi/mentah/AC_crypto_58.txt#L3233-L3270)).

- **Long:** harga koreksi turun ke POC. SL di bawah POC. RR 1:2–1:3.
- **Short:** harga naik ke POC dari bawah. TP di support ([AC_crypto_58 L3283–L3310](../materi/mentah/AC_crypto_58.txt#L3283-L3310)).
- POC dari timeframe besar lebih relevan. Di timeframe kecil, POC yang sama bisa berperan sebaliknya ([AC_crypto_39 L60–L105](../materi/mentah/AC_crypto_39.txt#L60-L105)).

**Belum jelas** → **Q-24**: rentang waktu "fixed range" dipilih dari mana sampai mana? → **Q-14** untuk forex.

---

### AFS-20 · Linear Regression Channel

| | |
|---|---|
| Sumber | [AC_crypto_61 L852–L976](../materi/mentah/AC_crypto_61.txt#L852-L976) |
| Pasar | K, F |
| Timeframe | Intraday ("selesai dalam satu hari") ([AC_crypto_61 L882–L890](../materi/mentah/AC_crypto_61.txt#L882-L890)) |
| Status | 🟡 |

- **Mode range:** long di sisi bawah channel → TP sisi atas; short di sisi atas → TP sisi bawah ([AC_crypto_61 L912–L940](../materi/mentah/AC_crypto_61.txt#L912-L940)).
- **Mode breakout:** harga keluar ke bawah channel + retest → short, SL di atas swing high. Keluar ke atas → bias long ([AC_crypto_61 L940–L960](../materi/mentah/AC_crypto_61.txt#L940-L960)).

**Belum jelas** → **Q-24**: panjang periode regresi dan lebar channel tidak disebut.

---

### AFS-21 · Renko reversal

| | |
|---|---|
| Sumber | [AC_crypto_61 L2293–L2512](../materi/mentah/AC_crypto_61.txt#L2293-L2512) |
| Pasar | K, F |
| Timeframe | D1 lebih akurat daripada H4/H1 ([AC_crypto_61 L2443–L2450](../materi/mentah/AC_crypto_61.txt#L2443-L2450)) |
| Status | 🟡 |

- **Breakout valid** = bata (brick) penuh menembus level ([AC_crypto_61 L2400–L2422](../materi/mentah/AC_crypto_61.txt#L2400-L2422)).
- **Reversal bullish** = setelah deret bata merah, muncul bata hijau dengan wick di bawah → long, SL di bawah swing low, TP resistance psikologis/harmonic/area jual ([AC_crypto_61 L2423–L2470](../materi/mentah/AC_crypto_61.txt#L2423-L2470)).
- **Reversal bearish** = cerminannya, SL di atas swing high ([AC_crypto_61 L2470–L2510](../materi/mentah/AC_crypto_61.txt#L2470-L2510)).

**Belum jelas** → **Q-24**: ukuran bata tidak disebut.

---

## G. Order flow (khusus kripto)

Order flow butuh data transaksi per level harga (*footprint*). Data ini tersedia di bursa kripto terpusat (contoh di kelas: Binance dan Bybit lewat aplikasi ATAS). **Tidak tersedia di forex spot**, karena forex tidak punya bursa pusat ([PETA bagian 8](../materi/PETA.md#8-dari-kelas-saham--crypto-ke-bot-forex)).

### AFS-22 · Sinyal order flow

| | |
|---|---|
| Sumber | [AC_crypto_57 L2713–L3272](../materi/mentah/AC_crypto_57.txt#L2713-L3272), [AC_crypto_59 L2360–L2639](../materi/mentah/AC_crypto_59.txt#L2360-L2639), [AC_crypto_58 L3879–L3946](../materi/mentah/AC_crypto_58.txt#L3879-L3946) |
| Pasar | K |
| Status | 🟡 (definisinya jelas, tetapi entry/SL/TP tidak disebut; paling cocok sebagai sinyal tambahan) |

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
| Status | ⚪ 🟡 |

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

**Belum jelas:** apakah bot memperdagangkan altcoin sama sekali → **Q-25**. Cara bot memutuskan "BTC bullish/bearish/sideways" bisa memakai definisi struktur AFS-01; jika Anda setuju, tidak ada pertanyaan tambahan.

---

### AFS-F2 · Konfirmasi volume untuk breakout

| | |
|---|---|
| Sumber | [AC_crypto_57 L1794–L1843](../materi/mentah/AC_crypto_57.txt#L1794-L1843); Dow: [AC_crypto_60 L1322–L1340](../materi/mentah/AC_crypto_60.txt#L1322-L1340) |
| Pasar | K, F\* |
| Status | ⚪ 🟡 |

**Aturan:** breakout **tanpa** kenaikan volume cenderung palsu → setup breakout dibatalkan. Breakout **dengan** volume naik → valid. Prinsip yang sama diulang Kalimasada (Wyckoff) dan Ko Hengki ([HKI-F2](04-ko-hengki-remora.md#hki-f2--breakout-pola-harus-bervolume)).

**Belum jelas:** berapa kenaikan volume yang dianggap "naik" → **Q-26**. Volume di forex → **Q-14**.

---

### AFS-F3 · Momentum: akselerasi & deselerasi

| | |
|---|---|
| Sumber | [AC_crypto_59 L1–L195](../materi/mentah/AC_crypto_59.txt#L1-L195) |
| Status | ⚪ 🔴 (tidak ada angka) |

- **Akselerasi:** candle besar, wick sedikit, jarak harga ditempuh dalam waktu singkat → tren kuat, berlanjut.
- **Deselerasi:** banyak wick, butuh lebih banyak candle untuk jarak yang sama → tanda keraguan, potensi koreksi atau pembalikan ([AC_crypto_59 L71–L185](../materi/mentah/AC_crypto_59.txt#L71-L185)).

Mentor tidak memberi ukuran angka (rasio wick/body, jumlah candle). Kalau ingin dipakai, ambangnya harus dicari lewat backtest.
