# PETA MATERI TRADING

Peta ini dibuat dari 86 file transkrip di folder [`materi/mentah/`](mentah/). **Isi file asli tidak diubah sama sekali.** Semua pemilahan dan urutan hanya ada di dokumen ini.

Cara pakai: klik nama file untuk membukanya. Kalau satu file berisi banyak video, tautannya langsung menunjuk ke **nomor baris** video yang dimaksud. Di GitHub, baris tersebut akan disorot.

---

## Daftar isi

1. [Cara membaca peta ini](#1-cara-membaca-peta-ini)
2. [Gambaran besar: isi folder dalam 1 menit](#2-gambaran-besar-isi-folder-dalam-1-menit)
3. [Masalah kualitas transkrip: dobel, terpotong, sambungan, hilang](#3-masalah-kualitas-transkrip)
4. [Jalur belajar yang disarankan (dasar → lanjutan)](#4-jalur-belajar-yang-disarankan)
5. [Peta CRYPTO (Akademi Crypto)](#5-peta-crypto--akademi-crypto)
6. [Peta SAHAM (Remora & Andre Hakim)](#6-peta-saham)
7. [Peta FOREX](#7-peta-forex)
8. [Dari kelas saham & crypto ke bot forex: apa yang bisa dipakai](#8-dari-kelas-saham--crypto-ke-bot-forex)
9. [Astronacci (Gema Goeyardi): konsep yang bisa ditemukan](#9-astronacci-gema-goeyardi)
10. [Daftar istilah dan artinya](#10-daftar-istilah)
11. [Catatan dan langkah berikutnya](#11-catatan-dan-langkah-berikutnya)

---

## 1. Cara membaca peta ini

**Penamaan segmen.** Banyak file berisi lebih dari satu video. `AC_crypto_57 §3` berarti video ke-3 di dalam file `AC_crypto_57.txt`.

**Label status:**

| Label | Artinya |
|---|---|
| **UTUH** | Video lengkap dari awal sampai akhir. |
| **TERPOTONG-AWAL** / **TERPOTONG-AKHIR** | Bagian awal atau akhir rekaman hilang. Kalau hanya salam pembuka yang hilang, ditulis "awal terpotong sedikit (isi utuh)". |
| **DOBEL** | Isinya sama dengan file/segmen lain. Rekamannya sama, hanya hasil transkripnya sedikit berbeda. Cukup baca satu, yaitu yang diberi tanda ⭐. |
| **SAMBUNGAN** | Lanjutan langsung dari file lain, atau file lain melanjutkannya. |
| **KOMPILASI** | Satu file berisi banyak video yang urutannya acak. |
| **POTONGAN** | Cuplikan pendek dari rekaman yang lebih panjang. |
| **HILANG** | Video/modul yang disebut dalam kelas, tetapi tidak ada di folder ini. |

**Tingkat kesulitan:** 🟢 dasar · 🟡 menengah · 🔴 lanjutan.

**Soal kualitas teks.** Semua file adalah transkrip otomatis: tanpa titik-koma, banyak salah dengar. Contoh: "week off" maksudnya *Wyckoff*, "do teori" maksudnya *Dow Theory*, "Beat over" maksudnya *bid–offer*, "all testing / self testing" maksudnya nama pengajar *Alvesting*. Daftar lengkapnya ada di [bagian 10](#103-kamus-salah-dengar-transkrip).

---

## 2. Gambaran besar: isi folder dalam 1 menit

| Pasar | Sumber / mentor | File | Isi utama | Kondisi |
|---|---|---|---|---|
| **Crypto** | **Akademi Crypto**. Pengajar: Timothy Ronald (pendiri), Kalimasada (investasi), Alvesting/"AFS" (teknikal), dan seorang analis yang membawakan live *market update* (namanya tidak disebut). | `AC_crypto_1` – `AC_crypto_62` (62 file, sekitar 176 video, ±164 unik) | Investasi, riset naratif & fundamental, teknikal lengkap (Dow, SMC, Wyckoff, Fibonacci, harmonic, indikator, order flow), psikologi, on-chain/DEX | Banyak **kompilasi** dan **dobel** |
| **Saham** | **Remora** (Ko Hengki). Ada kelas Remora Academy dan live komunitas Remora Traders. | `Remora_saham_1` – `16` | "Analisa transaksi"/bandarmologi: broker summary, antrean bid–offer, perilaku ritel vs pemain besar. Juga teknikal dasar dan cara berpikir probabilitas. | Live panjang, beberapa potongan & dobel |
| **Saham** | **Saham Master Class** batch 8, Ko Andri (Andre Hakim) | `AndreHakim_saham_1` – `5` | Investasi saham: fundamental, "market maker baik", money management, mental | Rapi (4 hari + 1 hari kopdar) |
| **Forex** | 3 sumber lepas, tidak saling terkait | `forex_1` – `3` | Scalping EURUSD M1 (FXcopet, 2012), support/resistance di emas, kursus Ichimoku (bahasa Inggris) | `forex_3` urutannya acak |
| *Bukan trading* | Kelas jualan "Sekolah Jalanan" (Timothy Ronald) | `AC_crypto_12` – `19` | Teknik menjual, motivasi | Tidak perlu untuk bot |

> Fakta kecil: di [AC_crypto_5](mentah/AC_crypto_5.txt#L300-L310) analis Akademi Crypto berkata urusan saham ia "serahkan ke ahlinya, Hengki, Andri". Jadi ketiga kelas Anda (crypto, Remora, Andre Hakim) berasal dari satu lingkaran mentor yang sama.

---

## 3. Masalah kualitas transkrip

### 3.1 File/segmen DOBEL (cukup baca yang ⭐)

| Materi | Salinan yang ada |
|---|---|
| DEX Trading Tutorial modul 1 | ⭐ [AC_crypto_7](mentah/AC_crypto_7.txt) = [AC_crypto_38 §1](mentah/AC_crypto_38.txt#L1-L368) = [AC_crypto_61 §11](mentah/AC_crypto_61.txt#L1663-L2052) |
| DEX Trading Tutorial modul 2 | ⭐ [AC_crypto_9](mentah/AC_crypto_9.txt) = [AC_crypto_59 §7](mentah/AC_crypto_59.txt#L1360-L1544) = [AC_crypto_62 §9](mentah/AC_crypto_62.txt#L2902-L3093) |
| DEX Trading Tutorial modul 3 | ⭐ [AC_crypto_8](mentah/AC_crypto_8.txt) = [AC_crypto_59 §6](mentah/AC_crypto_59.txt#L954-L1359) = [AC_crypto_59 §11](mentah/AC_crypto_59.txt#L1964-L2359). Video ini bahkan muncul dua kali di file yang sama. |
| DEX Trading Tutorial modul 4 | ⭐ [AC_crypto_10](mentah/AC_crypto_10.txt) = [AC_crypto_38 §2](mentah/AC_crypto_38.txt#L369-L609) = [AC_crypto_57 §11](mentah/AC_crypto_57.txt#L3273-L3540) |
| DEX Trading Tutorial modul 5 | ⭐ [AC_crypto_11](mentah/AC_crypto_11.txt) = [AC_crypto_41](mentah/AC_crypto_41.txt) (seluruh file) = [AC_crypto_58 §6](mentah/AC_crypto_58.txt#L1222-L1419) |
| Crypto Investing Tools modul 1 | ⭐ [AC_crypto_52 §1](mentah/AC_crypto_52.txt#L1-L254) = [AC_crypto_52 §2](mentah/AC_crypto_52.txt#L255-L513), terulang di file yang sama |
| Cara membeli altcoin | ⭐ [AC_crypto_62 §15](mentah/AC_crypto_62.txt#L4002-L4587). Bagian akhirnya terulang sebagai potongan di [AC_crypto_25 §3](mentah/AC_crypto_25.txt#L453-L642). |
| Live perdana Remora Traders | ⭐ [Remora_saham_14](mentah/Remora_saham_14.txt) = [Remora_saham_1](mentah/Remora_saham_1.txt) + [Remora_saham_2](mentah/Remora_saham_2.txt). File 1 dan 2 adalah belahan dari rekaman yang sama. |
| Potongan live darurat Remora | [Remora_saham_5](mentah/Remora_saham_5.txt) seluruh isinya sudah ada di ⭐ [Remora_saham_3](mentah/Remora_saham_3.txt) |

Ringkasnya: **[AC_crypto_38](mentah/AC_crypto_38.txt) dan [AC_crypto_41](mentah/AC_crypto_41.txt) seluruhnya dobel**, jadi boleh dilewati. Begitu juga [Remora_saham_1](mentah/Remora_saham_1.txt), [Remora_saham_2](mentah/Remora_saham_2.txt), dan [Remora_saham_5](mentah/Remora_saham_5.txt).

**"Versi kembar" (bukan dobel persis).** Kursus *Narrative Research* direkam dua kali oleh pengajar berbeda, Kalimasada dan Alvesting. Isinya mirip tetapi kalimatnya berbeda. Detailnya di [5.C](#c-riset-naratif-dua-versi).

### 3.2 File KOMPILASI (satu file berisi banyak video acak)

| File | Jumlah video di dalamnya |
|---|---|
| [AC_crypto_57](mentah/AC_crypto_57.txt) | 12 |
| [AC_crypto_58](mentah/AC_crypto_58.txt) | 16 |
| [AC_crypto_59](mentah/AC_crypto_59.txt) | 17 |
| [AC_crypto_60](mentah/AC_crypto_60.txt) | 17 |
| [AC_crypto_61](mentah/AC_crypto_61.txt) | 18 |
| [AC_crypto_62](mentah/AC_crypto_62.txt) | 15 |
| AC_crypto_20, 22, 23, 24, 25, 26, 27, 29, 34, 38, 40, 44, 52, 53, 54 | 2–5 video per file |
| [forex_3](mentah/forex_3.txt) | 11 pelajaran Ichimoku, urutan acak |
| [forex_1](mentah/forex_1.txt) | Sekitar 20 sesi harian, urutannya **sudah benar** |

Semua video di dalam kompilasi sudah dipecah dan ditaruh di topiknya masing-masing pada bagian 5–7.

### 3.3 TERPOTONG

| File | Yang hilang |
|---|---|
| [AC_crypto_1](mentah/AC_crypto_1.txt), [AC_crypto_4](mentah/AC_crypto_4.txt) | Awal **dan** akhir. Keduanya potongan dari live. |
| [AC_crypto_2](mentah/AC_crypto_2.txt), [AC_crypto_3](mentah/AC_crypto_3.txt), [AC_crypto_5](mentah/AC_crypto_5.txt) | Awal. Potongan live. |
| [AC_crypto_16](mentah/AC_crypto_16.txt) | Awal |
| [AC_crypto_33](mentah/AC_crypto_33.txt) | Awal: bagian pembukaan Timothy Ronald |
| [AC_crypto_57 §1](mentah/AC_crypto_57.txt#L1-L600) | Akhir: modul Altcoin Scalping 5 berhenti di tengah kalimat |
| [AC_crypto_60 §11](mentah/AC_crypto_60.txt#L2734-L2823) | Akhir, sedikit |
| [AC_crypto_25 §3](mentah/AC_crypto_25.txt#L453-L642) | Hanya potongan akhir sebuah video |
| [Remora_saham_9](mentah/Remora_saham_9.txt) | Awal |
| [Remora_saham_13](mentah/Remora_saham_13.txt) | Awal dan akhir. Rekaman berhenti sebelum sesi screening. |
| [Remora_saham_16](mentah/Remora_saham_16.txt) | Akhir: berhenti di tengah hitungan |
| [Remora_saham_3](mentah/Remora_saham_3.txt), [4](mentah/Remora_saham_4.txt), [5](mentah/Remora_saham_5.txt), [6](mentah/Remora_saham_6.txt), [7](mentah/Remora_saham_7.txt) | Semuanya potongan dari satu live. Lihat 3.4. |
| [AndreHakim_saham_1](mentah/AndreHakim_saham_1.txt) | Awal |
| [AndreHakim_saham_5](mentah/AndreHakim_saham_5.txt) | Akhir |

**Hanya salam pembukanya yang terpotong, isinya utuh:** AC_crypto_12, 17, 43, 44 §1–2, 45, 57 §4–5, 58 §1, 58 §8, 59 §3, 59 §16–17, 60 §2, 60 §5, 60 §8–9, 60 §15, 61 §7–8, 62 §4, 62 §6, 62 §13–14.

### 3.4 SAMBUNGAN

- **Remora_saham_1 → Remora_saham_2.** File 2 dimulai tepat di kalimat terakhir file 1. Versi utuhnya ada di Remora_saham_14.
- **Remora_saham_3 → Remora_saham_4.** Sekitar 130 kata pertama file 4 sama dengan akhir file 3, lalu file 4 berlanjut ke penutup live.
- **Remora_saham_6 → Remora_saham_3.** Pertanyaan tentang "algo asing" di akhir file 6 dijawab di awal file 3.
- **Remora_saham_7 → Remora_saham_5.** File 7 berhenti di "...mayoritas di", lalu file 5 dimulai dengan "sab..." (maksudnya saham PSAB, terpotong di tengah kata).
- **Kelas berurutan per hari:** Andre Hakim (hari 1–5) dan Remora Academy. Lihat [bagian 6](#6-peta-saham).
- **forex_1:** sesi live trading harian yang saling menyambung (2 Agustus – September 2012).

### 3.5 HILANG (disebut ada, tetapi tidak ada di folder)

- **Crypto:**
  - Fibonacci Secret modul 4
  - Order Flow modul 4
  - Dow Theory modul 4
  - Investing Principles prinsip 6 dan 7
  - Portfolio Management modul 1–4 (hanya modul 5 yang ada)
  - Video "Apa itu Bitcoin & cara membeli Bitcoin"
  - Narrative Research versi Kalimasada modul 4–5 (versi Alvesting lengkap)
  - Kelas jualan: modul "mentalitas seorang sales"
- **Saham:** Remora Academy hari 1
- **Forex:** forex_2 adalah "video ke-2" dari sebuah seri. Video 1 dan 3 tidak ada.

---

## 4. Jalur belajar yang disarankan

Urutan ini disusun untuk orang awam yang tujuannya **membuat bot forex**. Isinya diambil dari ketiga pasar. Penjelasan tiap file ada di bagian 5–7.

**Tahap 0: Pola pikir & menjaga modal (wajib, sebelum menyentuh grafik)**

1. [AC_crypto_21](mentah/AC_crypto_21.txt): trading bukan judi; cari untung yang sebanding risikonya.
2. [Money Management (AC_crypto_62 §3)](mentah/AC_crypto_62.txt#L1039-L1798), lalu [Mind Management (AC_crypto_32)](mentah/AC_crypto_32.txt).
3. Seri [Crypto Money Psychology 1–7](#e-psikologi--manajemen-uang): bias-bias yang membuat trader rugi.
4. [AndreHakim_saham_2](mentah/AndreHakim_saham_2.txt): mental saat harga turun.

**Tahap 1: Dasar membaca grafik**

5. [Technical Research by AFS 1–5](#f1-technical-research-by-afs-modul-gratis-fondasi): **fondasi paling penting**. Urutannya tren → area → pola → pemicu → entry/exit.
6. [Dow Theory](#f2-dow-theory): tren itu apa.
7. [forex_2](mentah/forex_2.txt): support/resistance & supply/demand, dengan contoh di emas (XAUUSD).
8. [Remora_saham_11](mentah/Remora_saham_11.txt): prinsip teknikal dasar, harga & volume.

**Tahap 2: Alat bantu harga**

9. [Fibonacci Secret](#f4-fibonacci-secret)
10. [Kamus Pattern Crypto (pola grafik)](#f3-kamus-pattern-crypto-kpk)
11. [Technical Indicators](#f8-technical-indicators-cti)

**Tahap 3: Konsep "uang besar"**

12. [Smart Money Concept](#f6-smart-money-concept-smc)
13. [Wyckoff](#f7-wyckoff-ditulis-week-off)
14. [Harmonic Trading + Elliott Wave](#f5-harmonic-trading-termasuk-elliott-wave)
15. [Order Flow](#f9-order-flow). Opsional untuk forex; alasannya ada di bagian 8.

**Tahap 4: Eksekusi & gaya trading**

16. [Altcoin Scalping 101](#f10-altcoin-scalping-101): konsep scalping.
17. [forex_1](mentah/forex_1.txt): contoh sistem scalping yang aturannya jelas, sehingga cocok sebagai contoh "aturan yang bisa dijadikan bot".
18. [forex_3: kursus Ichimoku](#73-forex_3--kursus-ichimoku-bahasa-inggris), diikuti dalam urutan logisnya.

**Tahap 5: Waktu (timing)**

19. forex_3 bagian [Teori Harga](mentah/forex_3.txt#L2844-L3270) dan [Teori Waktu](mentah/forex_3.txt#L713-L1184).
20. [Astronacci](#9-astronacci-gema-goeyardi).

**Tahap 6: Melihat mentor menerapkan ilmunya**

21. [Live market update Akademi Crypto (AC_crypto_1–5)](#h-live-market-update-analis-akademi-crypto)
22. Live Remora (opsional): contoh cara berpikir probabilitas dan kesabaran.

---

## 5. Peta CRYPTO — Akademi Crypto

### A. Pengenalan & pola pikir (Timothy Ronald)

| # | File | Isi (bahasa sederhana) | Level | Status |
|---|---|---|---|---|
| 1 | [AC_crypto_31](mentah/AC_crypto_31.txt) | Pembuka Akademi Crypto. Kenapa Bitcoin lahir (inflasi, contoh Argentina) dan siapa Satoshi. Jenis-jenis crypto, termasuk "store of value". Risiko sistemik (contoh FTX) vs risiko satu koin. Cara menyusun portofolio agresif/moderat/konservatif dan *rebalancing*. Big/mid/small cap. Cara memakai CoinMarketCap. Pesan utamanya: "follow the smart money". | 🟢 | UTUH |
| 2 | [AC_crypto_21](mentah/AC_crypto_21.txt) | Mindset crypto: jangan bermental judi, jangan *all-in*, jangan pakai *leverage*. Cari *risk-adjusted return*. Crypto dan saham sekarang saling berkorelasi. Siklus pasar dilihat dari beberapa *timeframe*. "Attention economy". Pegang aset pemenang, hindari jebakan ritel. | 🟢 | UTUH |
| 3 | [AC_crypto_51](mentah/AC_crypto_51.txt) | "Bitcoin bukan skema Ponzi": definisi Ponzi, uang fiat diibaratkan permainan kursi musik, efek jaringan, tanda tangan digital, cara menilai *store of value*, skenario siklus, dan strategi portofolio pribadi 2023. | 🟢 | UTUH |
| 4 | [AC_crypto_33](mentah/AC_crypto_33.txt) | Rekaman webinar promosi. Timothy memperkenalkan Alvesting (AFS). Isinya: jadilah yang pertama di sebuah narasi, *risk:reward* 1:3, bahaya *binary option*, jangan menumpuk indikator, ciri token dengan "bandar baik", lalu ajakan menjadi member. | 🟢 | TERPOTONG-AWAL |

### B. Investasi crypto (Kalimasada)

#### B1. Crypto Investing Guide, dasar sekali (8 modul)

| # | File | Isi | Level |
|---|---|---|---|
| 1 | [AC_crypto_53 §1](mentah/AC_crypto_53.txt#L1-L248) | Bisakah kaya tanpa investasi? Nilai uang terus tergerus inflasi. | 🟢 |
| 2 | [AC_crypto_26 §1](mentah/AC_crypto_26.txt#L1-L138) | Efek kupu-kupu: biaya peluang (*opportunity cost*) dari setiap pilihan. | 🟢 |
| 3 | [AC_crypto_28](mentah/AC_crypto_28.txt) | "Men lie, women lie, numbers don't": bandingkan hasil membuka usaha dengan memarkir uang di aset. | 🟢 |
| 4 | [AC_crypto_26 §2](mentah/AC_crypto_26.txt#L139-L271) | Mau mulai dari mana? Pertama, punya Bitcoin dulu. | 🟢 |
| 5 | [AC_crypto_53 §5](mentah/AC_crypto_53.txt#L611-L752) | Investor vs "bajing loncat" (orang yang lompat-lompat koin). | 🟢 |
| 6 | [AC_crypto_53 §2](mentah/AC_crypto_53.txt#L249-L405) | Cara membeli crypto: di CEX (bursa terpusat) atau DEX (bursa terdesentralisasi). | 🟢 |
| 7 | [AC_crypto_53 §3](mentah/AC_crypto_53.txt#L406-L553) | Tempat menyimpan crypto (wallet). | 🟢 |
| 8 | [AC_crypto_53 §4](mentah/AC_crypto_53.txt#L554-L610) | Siap menjadi investor crypto: regulasi masih minim, jadi harus siap menanggung risiko. | 🟢 |

#### B2. Crypto Investing Principles (7 prinsip, hanya 5 yang ada)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_48](mentah/AC_crypto_48.txt) | Keyakinan: pahami betul apa yang dibeli ("seperti memilih jodoh"). |
| 2 | [AC_crypto_20 §1](mentah/AC_crypto_20.txt#L1-L396) | Keberanian ("scared money makes no money"). |
| 3 | [AC_crypto_20 §2](mentah/AC_crypto_20.txt#L397-L795) | Keterbukaan: jadi oportunis, ikuti ke mana likuiditas mengalir. |
| 4 | [AC_crypto_25 §1](mentah/AC_crypto_25.txt#L1-L272) | Kedisiplinan. |
| 5 | [AC_crypto_25 §2](mentah/AC_crypto_25.txt#L273-L452) | Kesabaran ("sabar pangkal kaya"; tidak ada yang bisa menebak waktu dengan sempurna). |
| 6–7 | — | **HILANG** |

#### B3. Crypto Investing Strategy (7 strategi)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_22 §1](mentah/AC_crypto_22.txt#L1-L283) | **Bajing loncat**: pindah-pindah koin mengikuti rotasi sektor. |
| 2 | [AC_crypto_27 §1](mentah/AC_crypto_27.txt#L1-L242) | **Serigala–domba** (*greater fool theory*): beli lebih awal daripada "domba" yang datang terlambat. |
| 3 | [AC_crypto_49](mentah/AC_crypto_49.txt) | **Moon bag**: setelah naik, tarik kembali modal awal dan biarkan sisanya "terbang" gratis. |
| 4 | [AC_crypto_22 §2](mentah/AC_crypto_22.txt#L284-L413) | **Gulung-gulung**: semua profit diputar lagi (*compounding* 100%). Pengajarnya sendiri menyebut strategi ini sangat berbahaya. |
| 5 | [AC_crypto_27 §2](mentah/AC_crypto_27.txt#L243-L447) | **Tebar jala**: sebar uang ke banyak koin. |
| 6 | [AC_crypto_27 §3](mentah/AC_crypto_27.txt#L448-L594) | **Terkonsentrasi**: fokus ke 1–2 aset besar (BTC, ETH). |
| 7 | [AC_crypto_27 §4](mentah/AC_crypto_27.txt#L595-L711) | **Cicilan**: beli dan jual bertahap (*multiple entry/exit*). |

#### B4. Crypto Investing Tools (5 modul)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_52 §1](mentah/AC_crypto_52.txt#L1-L254) (§2 = DOBEL) | Situs data dasar crypto. |
| 2 | [AC_crypto_30](mentah/AC_crypto_30.txt) | *Portfolio tracker*: alat pemantau untung-rugi. |
| 3 | [AC_crypto_23 §1](mentah/AC_crypto_23.txt#L1-L180) | Wallet & *self-custody*. Keamanan adalah nomor satu. |
| 4 | [AC_crypto_23 §2](mentah/AC_crypto_23.txt#L181-L311) | Alat kuantitatif / data *on-chain* (misalnya Glassnode). |
| 5 | [AC_crypto_52 §3](mentah/AC_crypto_52.txt#L514-L665) | Alat fundamental blockchain: "laporan keuangan" sebuah proyek crypto. |

#### B5. Crypto Investing Alpha (7 modul)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_29 §1](mentah/AC_crypto_29.txt#L1-L270) | **Elevator concept**: uang mengalir bergiliran dari big cap ke mid cap lalu ke small cap. |
| 2 | [AC_crypto_24 §1](mentah/AC_crypto_24.txt#L1-L149) | **Pagi–siang–malam**: rotasi yang sama, tetapi di dalam satu narasi. |
| 3 | [AC_crypto_50](mentah/AC_crypto_50.txt) | **Wallet tracker**: mencontek dompet "pintar" yang aktivitasnya terlihat di blockchain. |
| 4 | [AC_crypto_24 §2](mentah/AC_crypto_24.txt#L150-L347) | Sentimen *fear & greed* (takut vs serakah). |
| 5 | [AC_crypto_24 §3](mentah/AC_crypto_24.txt#L348-L443) | Model *stock-to-flow* Bitcoin. |
| 6 | [AC_crypto_29 §2](mentah/AC_crypto_29.txt#L271-L433) | Memeriksa *smart contract* dalam 5 langkah untuk mendeteksi token penipuan. |
| 7 | [AC_crypto_29 §3](mentah/AC_crypto_29.txt#L434-L553) | Memanfaatkan AI untuk mengalahkan pasar. |

#### B6. Praktik membeli & trading spot

| File | Isi | Status |
|---|---|---|
| [AC_crypto_62 §15](mentah/AC_crypto_62.txt#L4002-L4587) | Cara membeli altcoin (Kalimasada). | UTUH. Video sebelumnya, "cara beli Bitcoin", **HILANG**. |
| [AC_crypto_62 §2](mentah/AC_crypto_62.txt#L411-L1038) | Tutorial trading spot (Alvesting): bedanya pasar spot dan derivatif, lalu praktik order. | UTUH |

#### B7. Portofolio

| File | Isi |
|---|---|
| [AC_crypto_37](mentah/AC_crypto_37.txt) | Alokasi portofolio versi Kalimasada: apa itu portofolio, tujuan keuangan, jangka waktu. |
| [AC_crypto_60 §7](mentah/AC_crypto_60.txt#L1767-L2098) | Topik yang sama, versi Alvesting. |
| [AC_crypto_6](mentah/AC_crypto_6.txt) | Portfolio Management modul 5 (modul terakhir): 70% Bitcoin, 30% untuk "dimainkan" (15% altcoin, 15% meme coin). Modul 1–4 **HILANG**. |

### C. Riset naratif (dua versi)

*Riset naratif* artinya mencari sektor/tema yang sedang atau akan diburu "uang besar".

**Versi Alvesting (lengkap):**

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_60 §6](mentah/AC_crypto_60.txt#L1360-L1766) | Pengantar riset naratif. |
| 2 | [AC_crypto_58 §9](mentah/AC_crypto_58.txt#L2426-L2824) | Cara menjadi yang pertama di setiap narasi. |
| 3 | [AC_crypto_60 §7](mentah/AC_crypto_60.txt#L1767-L2098) | Alokasi portofolio. |
| 4 | [AC_crypto_62 §4](mentah/AC_crypto_62.txt#L1799-L2245) | Narasi apa yang mungkin besar bulan depan. |
| 5 | [AC_crypto_58 §8](mentah/AC_crypto_58.txt#L2089-L2425) | Contoh kasus: narasi *spatial computing* (Q1 2024). |

**Versi Kalimasada (3 dari 5):**

1. [AC_crypto_62 §1](mentah/AC_crypto_62.txt#L1-L410): pengantar.
2. [AC_crypto_55](mentah/AC_crypto_55.txt): jadi yang pertama dan menjadi kontrarian sejati.
3. [AC_crypto_37](mentah/AC_crypto_37.txt): alokasi portofolio.

### D. Riset fundamental (Alvesting)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_59 §15](mentah/AC_crypto_59.txt#L3150-L3400) | Ada 3 jenis riset: naratif, teknikal, fundamental. Menurut pengajar, di crypto fundamental justru yang "paling tidak penting". |
| 2 | [AC_crypto_61 §17](mentah/AC_crypto_61.txt#L3275-L3583) | Faktor-faktor dalam riset fundamental. |
| 3 | [AC_crypto_61 §18](mentah/AC_crypto_61.txt#L3584-L3894) | *Tokenomics* (5 komponennya) dan nilai intrinsik proyek. |

### E. Psikologi & manajemen uang

| # | File | Isi | Level |
|---|---|---|---|
| — | [AC_crypto_62 §3](mentah/AC_crypto_62.txt#L1039-L1798) | **Money management**: cara memandang dan mengelola uang trading. | 🟢 |
| — | [AC_crypto_32](mentah/AC_crypto_32.txt) | **Mind management**: mengelola pikiran. Lanjutan dari money management. | 🟢 |
| 1 | [AC_crypto_58 §1](mentah/AC_crypto_58.txt#L1-L289) | Money Psychology 1: psikologi adalah kunci keberhasilan; pengantar bias. | 🟢 |
| 2 | [AC_crypto_59 §3](mentah/AC_crypto_59.txt#L421-L680) | 2: bukti ilmiah (riset Lo & Repin 2002 tentang emosi trader). | 🟡 |
| 3 | [AC_crypto_60 §17](mentah/AC_crypto_60.txt#L3858-L4070) | 3: mekanisme otak yang memunculkan bias. | 🟡 |
| 4 | [AC_crypto_61 §7](mentah/AC_crypto_61.txt#L977-L1191) | 4: teori perilaku dari para pakar. | 🟡 |
| 5 | [AC_crypto_60 §16](mentah/AC_crypto_60.txt#L3656-L3857) | 5: *overconfidence* (terlalu percaya diri). | 🟢 |
| 6 | [AC_crypto_60 §15](mentah/AC_crypto_60.txt#L3478-L3655) | 6: *herding* (ikut-ikutan orang banyak). | 🟢 |
| 7 | [AC_crypto_61 §8](mentah/AC_crypto_61.txt#L1192-L1324) | 7: *loss aversion* (terlalu takut rugi). | 🟢 |
| — | [AC_crypto_46](mentah/AC_crypto_46.txt) | Persiapan mental sebelum scalping: risiko 1% per transaksi, jangan menyalahkan diri, trading adalah "permainan angka". | 🟢 |

### F. Teknikal (Alvesting / AFS)

#### F1. Technical Research by AFS (modul gratis, fondasi)

| # | File | Isi | Level |
|---|---|---|---|
| 1 | [AC_crypto_35](mentah/AC_crypto_35.txt) | **Analisa tren**: candlestick, mulai dari *timeframe* besar, struktur naik/turun (HH/HL/LH/LL), *moving average*, membandingkan banyak koin sekaligus. | 🟢 |
| 2 | [AC_crypto_58 §7](mentah/AC_crypto_58.txt#L1420-L2088) | **Analisa area**: zona support/resistance. | 🟢 |
| 3 | [AC_crypto_57 §2](mentah/AC_crypto_57.txt#L601-L1383) | **Analisa pola** (*pattern*). | 🟡 |
| 4 | [AC_crypto_57 §3](mentah/AC_crypto_57.txt#L1384-L1873) | **Analisa pemicu** (*trigger*): tanda untuk mulai masuk. | 🟡 |
| 5 | [AC_crypto_59 §14](mentah/AC_crypto_59.txt#L2640-L3149) | **Analisa entry & exit**: menggabungkan keempat tahap sebelumnya. | 🟡 |

#### F2. Dow Theory

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_60 §5](mentah/AC_crypto_60.txt#L1122-L1359) | Sejarah dan 6 prinsip Dow Theory. |
| 2 | [AC_crypto_47](mentah/AC_crypto_47.txt) | Konsep tren: tren yang signifikan harus didukung volume. |
| 3 | [AC_crypto_62 §14](mentah/AC_crypto_62.txt#L3887-L4001) | Tren lanjutan & durasi tren. |
| 4 | — | **HILANG** |
| 5 | [AC_crypto_57 §5](mentah/AC_crypto_57.txt#L2207-L2410) | Fase-fase pasar menurut Dow. |

#### F3. Kamus Pattern Crypto (KPK)

| # | File | Pola |
|---|---|---|
| 1 | [AC_crypto_59 §8](mentah/AC_crypto_59.txt#L1545-L1684) | Apa itu *pattern* (pola grafik). |
| 2 | [AC_crypto_57 §6](mentah/AC_crypto_57.txt#L2411-L2620) | Pola ABCD. |
| 3 | [AC_crypto_62 §5](mentah/AC_crypto_62.txt#L2246-L2481) | Bat pattern. |
| 4 | [AC_crypto_60 §2](mentah/AC_crypto_60.txt#L347-L579) | Gartley pattern. |
| 5 | [AC_crypto_43](mentah/AC_crypto_43.txt) | Crab pattern. |
| 6 | [AC_crypto_59 §9](mentah/AC_crypto_59.txt#L1685-L1804) | Diamond pattern. |
| 7 | [AC_crypto_60 §3](mentah/AC_crypto_60.txt#L580-L839) | Broadening pattern. |
| 8 | [AC_crypto_58 §5](mentah/AC_crypto_58.txt#L1043-L1221) | Andrews Pitchfork. |
| 9 | [AC_crypto_61 §6](mentah/AC_crypto_61.txt#L852-L976) | Linear Regression Channel. |
| 10 | [AC_crypto_57 §7](mentah/AC_crypto_57.txt#L2621-L2712) | Rectangle channel. |

#### F4. Fibonacci Secret

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_59 §4](mentah/AC_crypto_59.txt#L681-L823) | Apa itu deret Fibonacci. |
| 2 | [AC_crypto_58 §14](mentah/AC_crypto_58.txt#L3644-L3763) | "Keajaiban" Fibonacci di alam dan kehidupan. |
| 3 | [AC_crypto_58 §15](mentah/AC_crypto_58.txt#L3764-L3878) | *Golden ratio* (rasio emas). |
| 4 | — | **HILANG** |
| 5 | [AC_crypto_60 §1](mentah/AC_crypto_60.txt#L1-L346) | **Fibonacci retracement** untuk trading & investasi. |
| 6 | [AC_crypto_58 §13](mentah/AC_crypto_58.txt#L3476-L3643) | Harmonic support (dari ekstensi Fibonacci). |
| 7 | [AC_crypto_59 §5](mentah/AC_crypto_59.txt#L824-L953) | Harmonic resistance, dengan target 1.618 / 2.618 / 3.618. |
| 8 | [AC_crypto_62 §7](mentah/AC_crypto_62.txt#L2625-L2790) | *Trend-based Fibonacci extension*. |
| 9 | [AC_crypto_42](mentah/AC_crypto_42.txt) | Fibonacci channel. |
| 10 | [AC_crypto_56](mentah/AC_crypto_56.txt) | Rangkuman & pendalaman. |

#### F5. Harmonic Trading (termasuk Elliott Wave)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_58 §12](mentah/AC_crypto_58.txt#L3319-L3473) | Pengantar harmonic trading. |
| 2 | [AC_crypto_60 §10](mentah/AC_crypto_60.txt#L2543-L2733) | Tahapan menerapkannya. |
| 3 | [AC_crypto_62 §11](mentah/AC_crypto_62.txt#L3308-L3459) | Peran Fibonacci dalam harmonic. |
| 4 | [AC_crypto_62 §10](mentah/AC_crypto_62.txt#L3094-L3307) | **Elliott Wave**. |
| 5 | [AC_crypto_54 §1](mentah/AC_crypto_54.txt#L1-L161) | Elliott Wave + Fibonacci. |
| 6 | [AC_crypto_61 §4](mentah/AC_crypto_61.txt#L618-L732) | Dasar pola & rasio harmonic. |
| 7 | [AC_crypto_54 §2](mentah/AC_crypto_54.txt#L162-L322) | Harmonic head & shoulders, dengan contoh BTC. |
| 8 | [AC_crypto_61 §5](mentah/AC_crypto_61.txt#L733-L851) | Shark pattern (juga Butterfly). |
| 9 | [AC_crypto_62 §12](mentah/AC_crypto_62.txt#L3460-L3588) | *Entry trigger*. |
| 10 | [AC_crypto_60 §11](mentah/AC_crypto_60.txt#L2734-L2823) | Rangkuman. TERPOTONG-AKHIR, sedikit. |

#### F6. Smart Money Concept (SMC)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_61 §2](mentah/AC_crypto_61.txt#L283-L436) | Pengantar: apa itu *smart money*. |
| 2 | [AC_crypto_61 §1](mentah/AC_crypto_61.txt#L1-L282) | Fokus SMC adalah likuiditas. |
| 3 | [AC_crypto_34 §1](mentah/AC_crypto_34.txt#L1-L451) | Likuiditas 1: BSL & SSL (kumpulan stop loss di atas/bawah harga). |
| 4 | [AC_crypto_34 §2](mentah/AC_crypto_34.txt#L452-L824) | Likuiditas 2. |
| 5 | [AC_crypto_58 §4](mentah/AC_crypto_58.txt#L810-L1042) | Likuiditas 3: pola-pola likuiditas. |
| 6 | [AC_crypto_36](mentah/AC_crypto_36.txt) | *Market structure*: *break of structure*, *stop hunt*. |
| 7 | [AC_crypto_58 §3](mentah/AC_crypto_58.txt#L597-L809) | *Change of character* (CHoCH). |
| 8 | [AC_crypto_58 §2](mentah/AC_crypto_58.txt#L290-L596) | *Order block*. |
| 9 | [AC_crypto_59 §1](mentah/AC_crypto_59.txt#L1-L195) | Momentum (*pace & rhythm*). |
| 10 | [AC_crypto_59 §2](mentah/AC_crypto_59.txt#L196-L420) | Penerapan: cara pengajar memakai SMC. |

#### F7. Wyckoff (ditulis "week off")

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_60 §13](mentah/AC_crypto_60.txt#L3105-L3330) | Pengantar, dibawakan Kalimasada. |
| 2 | [AC_crypto_40 §1](mentah/AC_crypto_40.txt#L1-L281) | 3 hukum & prinsip Wyckoff. |
| 3 | [AC_crypto_60 §12](mentah/AC_crypto_60.txt#L2824-L3104) | Siklus pasar: akumulasi → naik → distribusi → turun. |
| 4 | [AC_crypto_40 §2](mentah/AC_crypto_40.txt#L282-L441) | Contoh fase-fase itu di crypto. |
| 5 | [AC_crypto_57 §12](mentah/AC_crypto_57.txt#L3541-L3713) | *Supply & demand*. |
| 6 | [AC_crypto_61 §9](mentah/AC_crypto_61.txt#L1325-L1511) | Analisa volume. |
| 7 | [AC_crypto_61 §10](mentah/AC_crypto_61.txt#L1512-L1662) | Pola price action ala Wyckoff. |
| 8 | [AC_crypto_59 §10](mentah/AC_crypto_59.txt#L1805-L1963) | Fase A & B. |
| 9 | [AC_crypto_60 §14](mentah/AC_crypto_60.txt#L3331-L3477) | Fase C, D, E. |
| 10 | [AC_crypto_62 §8](mentah/AC_crypto_62.txt#L2791-L2901) | Penerapan di pasar crypto. |

#### F8. Technical Indicators (CTI)

| # | File | Indikator |
|---|---|---|
| 1 | [AC_crypto_61 §12](mentah/AC_crypto_61.txt#L2053-L2292) | Pengantar: indikator itu apa. |
| 2 | [AC_crypto_44 §1](mentah/AC_crypto_44.txt#L1-L299) | Pivot points. |
| 3 | [AC_crypto_44 §2](mentah/AC_crypto_44.txt#L300-L489) | Keltner Channel. |
| 4 | [AC_crypto_59 §16](mentah/AC_crypto_59.txt#L3401-L3555) | Parabolic SAR. |
| 5 | [AC_crypto_61 §13](mentah/AC_crypto_61.txt#L2293-L2514) | Renko chart. |
| 6 | [AC_crypto_61 §14](mentah/AC_crypto_61.txt#L2515-L2646) | KST (*Know Sure Thing*). |
| 7 | [AC_crypto_59 §17](mentah/AC_crypto_59.txt#L3556-L3718) | Donchian Channel (transkrip menulisnya "dimension channels"). |
| 8 | [AC_crypto_62 §6](mentah/AC_crypto_62.txt#L2482-L2624) | Chaikin Money Flow (CMF). |
| 9 | [AC_crypto_44 §3](mentah/AC_crypto_44.txt#L490-L714) | Ichimoku Cloud. |
| 10 | [AC_crypto_58 §11](mentah/AC_crypto_58.txt#L3223-L3318) | Volume Profile Fixed Range (VPFR). |

#### F9. Order Flow

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_61 §3](mentah/AC_crypto_61.txt#L437-L617) | Apa itu *order flow trading*. |
| 2 | [AC_crypto_60 §4](mentah/AC_crypto_60.txt#L840-L1121) | Dasar order flow: terpusat vs terdesentralisasi, sisi *bid* & *ask*. |
| 3 | [AC_crypto_39](mentah/AC_crypto_39.txt) | *Footprint chart*. |
| 4 | — | **HILANG** |
| 5 | [AC_crypto_57 §8](mentah/AC_crypto_57.txt#L2713-L2993) | HVN (*high volume node*) & *delta*. |
| 6 | [AC_crypto_59 §12](mentah/AC_crypto_59.txt#L2360-L2492) | *Volume cluster*. |
| 7 | [AC_crypto_59 §13](mentah/AC_crypto_59.txt#L2493-L2639) | *Unfinished business* & *cumulative delta*. |
| 8 | [AC_crypto_57 §9](mentah/AC_crypto_57.txt#L2994-L3138) | Aplikasi ATAS. |
| 9 | [AC_crypto_57 §10](mentah/AC_crypto_57.txt#L3139-L3272) | Indikator order flow di ATAS. |
| 10 | [AC_crypto_58 §16](mentah/AC_crypto_58.txt#L3879-L3946) | *Heatmap*: melihat permintaan asli dan menghindari order palsu. |

#### F10. Altcoin Scalping 101

| # | File | Isi | Status |
|---|---|---|---|
| 1 | [AC_crypto_61 §15](mentah/AC_crypto_61.txt#L2647-L2920) | Apa itu altcoin. | UTUH |
| 2 | [AC_crypto_58 §10](mentah/AC_crypto_58.txt#L2825-L3220) | Dasar teknik scalping. | UTUH |
| 3/4 | [AC_crypto_46](mentah/AC_crypto_46.txt) dan [AC_crypto_62 §13](mentah/AC_crypto_62.txt#L3589-L3886) | Persiapan mental dan persiapan teknikal sebelum scalping. Nomor modulnya tidak disebut. | UTUH |
| 5 | [AC_crypto_57 §1](mentah/AC_crypto_57.txt#L1-L600) | *Screening* altcoin: price action, korelasi dengan BTC, volume. | TERPOTONG-AKHIR |

### G. On-chain & DEX

#### G1. On-chain Trading (Alvesting)

| # | File | Isi |
|---|---|---|
| 1 | [AC_crypto_61 §16](mentah/AC_crypto_61.txt#L2921-L3274) | Apa itu *on-chain trading*. |
| 2 | [AC_crypto_45](mentah/AC_crypto_45.txt) | DEX: spot (Uniswap dll.) vs derivatif (dYdX, GMX). |
| 3 | [AC_crypto_57 §4](mentah/AC_crypto_57.txt#L1874-L2206) | Wallet. |
| 4 | [AC_crypto_60 §9](mentah/AC_crypto_60.txt#L2349-L2542) | Alat pendukung. |
| 5 | [AC_crypto_60 §8](mentah/AC_crypto_60.txt#L2099-L2348) | Kesalahan yang harus dihindari. |

#### G2. DEX Trading Tutorial (Kalimasada). Tiap modul ada 3 salinan, lihat 3.1.

| # | File ⭐ | Isi |
|---|---|---|
| 1 | [AC_crypto_7](mentah/AC_crypto_7.txt) | Apa itu CEX & DEX dan apa saja yang dibutuhkan. |
| 2 | [AC_crypto_9](mentah/AC_crypto_9.txt) | Perbedaan struktur CEX vs DEX. |
| 3 | [AC_crypto_8](mentah/AC_crypto_8.txt) | Praktik di jaringan Ethereum. |
| 4 | [AC_crypto_10](mentah/AC_crypto_10.txt) | Praktik di jaringan Solana. |
| 5 | [AC_crypto_11](mentah/AC_crypto_11.txt) | Tips lanjutan: mencari token, dominasi wallet, keluar bertahap. Pesannya: meme coin itu hiburan saja. |

### H. Live market update (analis Akademi Crypto)

Ini potongan-potongan live, kemungkinan sekitar akhir 2025–2026 berdasarkan harga BTC yang disebut. Nama pembicara tidak disebut. Isinya penting karena memperlihatkan **cara mentor crypto Anda membaca pasar saat ini**. Urutannya hanya perkiraan dari harga yang disebut.

| File | Isi | Status |
|---|---|---|
| [AC_crypto_2](mentah/AC_crypto_2.txt) | BTC di *range high*. Stochastic sudah *cross*, jadi disebut "grey area": beli dekat resistance membuat stop loss sulit ditempatkan. Posisi long di sekitar 88 ribu. | TERPOTONG-AWAL |
| [AC_crypto_3](mentah/AC_crypto_3.txt) | Komentar narasi (ICO, prediction market, RWA, meme launchpad). Kesimpulannya: pasar stagnan, jaga modal. | TERPOTONG-AWAL |
| [AC_crypto_1](mentah/AC_crypto_1.txt) | "Super cycle terjadi, tapi bukan di crypto" (emas dan perak yang naik). BTC di "grey zone", lebih berani beli di 80 ribu. Cara main token baru: tunggu turun dan membentuk *base*, lalu masuk bertahap dengan batas cut loss. | TERPOTONG awal & akhir |
| [AC_crypto_4](mentah/AC_crypto_4.txt) | Siklus 4 tahun ("beli setahun sebelum halving, jual setahun setelahnya"). BTC turun 52% dari puncak. *Golden pocket* Fibonacci di bekas ATH. Rebalancing ke emas dan cash. | TERPOTONG awal & akhir |
| [AC_crypto_5](mentah/AC_crypto_5.txt) | Area 50 ribu untuk pembelian besar; rencana portofolio 70% BTC. Fear & greed di titik ekstrem. Pelajaran siklus ini: "only Bitcoin you can trust". Urusan saham diserahkan ke Hengki & Andri. | TERPOTONG-AWAL |

### I. Bukan trading: kelas jualan "Sekolah Jalanan" (Timothy Ronald)

Tidak dibutuhkan untuk bot. Dicatat agar tidak membingungkan. Urutan perkiraan:

1. [AC_crypto_18](mentah/AC_crypto_18.txt): pengenalan kelas.
2. [AC_crypto_12](mentah/AC_crypto_12.txt): motivasi, menghapus *limiting belief*.
3. [AC_crypto_13](mentah/AC_crypto_13.txt): *sales funnel*.
4. [AC_crypto_15](mentah/AC_crypto_15.txt): prospecting & follow up.
5. [AC_crypto_14](mentah/AC_crypto_14.txt): tipe-tipe penjual.
6. [AC_crypto_16](mentah/AC_crypto_16.txt): psikologi penjualan & nada bicara. TERPOTONG-AWAL.
7. [AC_crypto_19](mentah/AC_crypto_19.txt): membangun *rapport*.
8. [AC_crypto_17](mentah/AC_crypto_17.txt): menangani keberatan pembeli.

Modul "mentalitas seorang sales" **HILANG**.

---

## 6. Peta SAHAM

### 6.1 Remora — Ko Hengki

**Inti ajarannya: "analisa transaksi"** (bandarmologi). Bukan sekadar membaca grafik, tetapi melihat **siapa** yang membeli dan menjual: kode broker di *broker summary*, cara antrean *bid–offer* dipasang, apakah ritel sedang panik atau serakah. Pegangannya: berpikir **probabilitas, bukan kemungkinan**.

**Kelas Remora Academy** (urutan dari petunjuk di dalam transkrip):

| Hari | File | Isi | Level | Status |
|---|---|---|---|---|
| 1 | — | — | — | **HILANG** |
| 2 | [Remora_saham_11](mentah/Remora_saham_11.txt) | Prinsip teknikal dasar: harga & volume, tren primer/sekunder/minor, kesalahan umum (terlalu banyak indikator membuat bingung dan subjektif), probabilitas vs posibilitas. Contoh menghitung lot di saham emas. | 🟢 | UTUH |
| 3 | [Remora_saham_10](mentah/Remora_saham_10.txt) | Review harga & volume. Empat alat: teknikal, platform, broker summary, bid–offer. Mengenali broker ritel vs "imposter". *Buy on breakout* vs *buy on weakness*. | 🟡 | UTUH |
| 4 | [Remora_saham_9](mentah/Remora_saham_9.txt) | Support yang "sengaja digambar" bandar, ARB, membaca bid–offer, broker XC/XL. Laporan kepemilikan ≥5% (KSEI), data SID, NeoBDM. | 🟡 | TERPOTONG-AWAL |
| 5 (perkiraan) | [Remora_saham_15](mentah/Remora_saham_15.txt) | Analisa transaksi: membaca *flow*, siapa "imposter", *split order*, frekuensi, distribusi. Ditutup dengan "materi lanjut besok". | 🔴 | UTUH, tetapi transkripnya sangat berantakan |
| Terakhir | [Remora_saham_8](mentah/Remora_saham_8.txt) | "Last day": skenario *takeover*, prinsip-prinsip dasar, akumulasi 4 minggu di NeoBDM, bid–offer & "algo asing", contoh-contoh saham. | 🔴 | UTUH |

**Live komunitas:**

| File | Isi | Status |
|---|---|---|
| ⭐ [Remora_saham_14](mentah/Remora_saham_14.txt) | Live perdana Remora Traders. Tanya-jawab soal ukuran posisi dan pembagian investasi/swing/trading. Contoh broker XC/XL. Lima alat probabilitasnya: teknikal, broker summary (menghitung ritel), bid–offer, kepentingan pemilik, C-level. | UTUH. File 1 + 2 = DOBEL dari file ini. |
| [Remora_saham_12](mentah/Remora_saham_12.txt) | Live *ask me anything*. Kasus PANI/CBPK; saham bisa ATH karena dibeli institusi, bukan ritel. | UTUH |
| [Remora_saham_13](mentah/Remora_saham_13.txt) | Tanya-jawab: tidak percaya hoki/feng shui; pola bid "pemain besar" vs offer ritel. | TERPOTONG awal & akhir |
| [Remora_saham_16](mentah/Remora_saham_16.txt) | Studi kasus IPO (SUPA): menghitung barang dari prospektus (lot IPO × harga), pindah barang antarbroker, melacak siapa penjualnya. | TERPOTONG-AKHIR |

**Live darurat (sekitar akhir Agustus 2025: demo DPR, kekhawatiran saham PSAB disuspensi).** Rekaman ini terpecah jadi beberapa potongan yang saling tumpang-tindih. Urutan perkiraan: **7 → 5** dan **6 → 3 → 4**.

| File | Isi | Status |
|---|---|---|
| [Remora_saham_7](mentah/Remora_saham_7.txt) | Komitmen mentor; cara mengumpulkan saham (jumlah lot diacak); asing jarang *panic selling*; PSAB/BRMS. | POTONGAN, berlanjut ke file 5 |
| [Remora_saham_5](mentah/Remora_saham_5.txt) | 145 kata. | POTONGAN, DOBEL dengan isi file 3 |
| [Remora_saham_6](mentah/Remora_saham_6.txt) | Mengevaluasi kinerja dengan membandingkan ke daftar *top gainer/loser*. | POTONGAN |
| [Remora_saham_3](mentah/Remora_saham_3.txt) | Cara mengenali "algo asing" (order langsung menempel dalam milidetik). Proses analisa BSBK (saham Rp50 yang "dibangunkan"). Broker "imposter". *Moon stock* BKSL. Rencana membuat alat analisa bid–offer. | POTONGAN |
| [Remora_saham_4](mentah/Remora_saham_4.txt) | Penutup live: komposisi portofolio, "prepare for the worst". | SAMBUNGAN dari file 3 |

### 6.2 Andre Hakim — Ko Andri, "Saham Master Class" batch 8

**Gaya:** investasi jangka menengah–panjang. Mencari saham *multibagger* (naik berlipat-lipat), terutama milik konglomerat yang punya "market maker baik", sambil menjaga mental dan manajemen uang. Kelasnya 4 hari, ditambah hari ke-5 kopdar.

| Hari | File | Isi | Level | Status |
|---|---|---|---|---|
| 1 | [AndreHakim_saham_4](mentah/AndreHakim_saham_4.txt) | Perkenalan, struktur kelas, dasar saham (saham diterbitkan untuk menggalang dana), ajakan "rewire your brain". | 🟢 | UTUH |
| 2 | [AndreHakim_saham_2](mentah/AndreHakim_saham_2.txt) | Mindset & psikologi (transkrip menulis "mindset dan teknologi"): cara tidak panik saat turun, kuat menahan (*hold*) lama, "stamina", *proper temperament*. Menurutnya *day trading* = judi. | 🟢 | UTUH |
| 3 | [AndreHakim_saham_3](mentah/AndreHakim_saham_3.txt) | Memilih saham: fundamental (PER, PBV, dividen), market maker baik (targetnya masuk MSCI/indeks), *corporate action*. Broker summary disebutnya "ilmu jalanan". Teknikal hanya untuk saham *big cap*. Antre bid untuk scalping, porsi investasi vs trading, jam ramai bursa, DCA reksa dana. | 🟡 | UTUH |
| 4 | [AndreHakim_saham_1](mentah/AndreHakim_saham_1.txt) | Money management: target ≥20% per tahun, rumus 72, *dividend payout ratio*, berani *cut loss*, contoh portofolio pribadi. "Hari terakhir" materi. | 🟡 | TERPOTONG-AWAL |
| 5 | [AndreHakim_saham_5](mentah/AndreHakim_saham_5.txt) | Kopdar/makan bersama: perkenalan peserta, tanya-jawab saham properti/batu bara. | 🟢 | TERPOTONG-AKHIR |

---

## 7. Peta FOREX

Ketiga file forex berasal dari sumber yang **berbeda** dan tidak saling terkait.

### 7.1 [forex_2](mentah/forex_2.txt) — Support/Resistance & Supply/Demand di emas

Level: 🟢. Ditujukan untuk pemula, dengan contoh di XAUUSD (emas):

- **Support/resistance** = area tempat harga memantul ≥2 kali.
- Ia juga menjelaskan *supply & demand*, tetapi lebih suka SnR karena SnD "menunggunya lama".
- Ikuti tren (klaimnya: peluang menang ±70%).
- Pola "N" dengan konsolidasi sempit; konsolidasi yang terlalu lebar cenderung *fake out*.
- Perhatikan bentuk *body* candle saat ditutup.
- Backtest memakai *tool* Traders Family.

Ini "video ke-2". **Video 1 & 3 HILANG.**

### 7.2 [forex_1](mentah/forex_1.txt) — Tutorial scalping FXcopet (2012)

Level: 🟡.

| Bagian | Isi |
|---|---|
| [L1–330](mentah/forex_1.txt#L1-L330) | Pengantar: sejarah FXcopet, cerita pendirinya bangkrut, cara memilih broker (regulasi, spread, kecepatan eksekusi, leverage, margin call), gambaran strategi. |
| [L331–3245](mentah/forex_1.txt#L331-L3245) | Sekitar 20 sesi live trading harian (2 Agustus – September 2012), EURUSD timeframe 1 menit. |
| [L3245–3450](mentah/forex_1.txt#L3245-L3450) | **Kesimpulan aturan** (lihat di bawah). |

**Aturannya** (sangat mudah dijadikan bot):

- Pair EURUSD, timeframe M1 (1 menit), terutama di sesi Eropa.
- Cari dua garis horizontal: merah di atas, aqua di bawah, jaraknya **≤15 pip**.
- Harga menembus garis atas → buy. Menembus garis bawah → sell.
- Take profit minimal 10 pip, atau tutup manual di akhir sesi Eropa (17.00–18.00 WIB).
- Kalau harga berbalik: tutup posisi, lalu buka arah sebaliknya dengan target **2× kerugian** untuk "recover".
- Sinyal muncul sekitar 3 kali per minggu.

⚠️ **Catatan:** teknik "recover" (membalik posisi untuk menutup rugi) berisiko tinggi kalau tidak dibatasi. Data juga dari 2012, ketika kondisi pasar dan spread berbeda. Wajib di-backtest ulang.

### 7.3 [forex_3](mentah/forex_3.txt) — Kursus Ichimoku (bahasa Inggris)

Level: 🔴. Kursus "Ichimoku King" oleh Rafał Zuchowicz (London). **KOMPILASI dengan urutan acak**: pengantarnya justru ada di tengah file. Urutan logisnya:

| # | Baris | Pelajaran |
|---|---|---|
| 1 | [L1185–1547](mentah/forex_3.txt#L1185-L1547) | Pengantar kursus; sejarah Goichi Hosoda (pencipta Ichimoku) dan buku-buku aslinya. |
| 2 | [L3271–3398](mentah/forex_3.txt#L3271-L3398) | Memasang indikator Ichimoku dan setting-nya. |
| 3 | [L1948–2438](mentah/forex_3.txt#L1948-L2438) | Tenkan-sen (garis cepat, 9 periode). |
| 4 | [L3399–3522](mentah/forex_3.txt#L3399-L3522) | Kijun-sen (garis 26 periode). |
| 5 | [L3523–3685](mentah/forex_3.txt#L3523-L3685) | Kumo / awan (Senkou Span A & B). |
| 6 | [L2439–2843](mentah/forex_3.txt#L2439-L2843) | Chikou Span (garis tertinggal). |
| 7 | [L1548–1947](mentah/forex_3.txt#L1548-L1947) | Teori gelombang: gelombang I, V, N, P, Y, S. |
| 8 | [L2844–3270](mentah/forex_3.txt#L2844-L3270) | Teori harga: target V, N, E, NT. |
| 9 | [L713–1184](mentah/forex_3.txt#L713-L1184) | **Teori waktu**: angka Hosoda 9, 17, 26 dan turunannya (33, 42, 65, 76, 129, …), diuji di DAX 5 menit. |
| 10 | [L1–712](mentah/forex_3.txt#L1-L712) | Praktik live di USD/TRY, dua bagian: [L1–535](mentah/forex_3.txt#L1-L535) dan "48 jam kemudian" [L536–712](mentah/forex_3.txt#L536-L712). |

---

## 8. Dari kelas saham & crypto ke bot forex

Menurut Anda cara risetnya sama untuk semua pasar. Untuk **membaca grafik dan mengelola risiko, itu benar**: grafik di semua pasar digerakkan perilaku manusia yang sama, yaitu takut dan serakah. Tetapi ada alat yang **khusus** pasar tertentu dan tidak bisa dipakai di forex. Rinciannya:

| Konsep | Dari kelas | Bisa dipakai di forex? | Catatan untuk bot |
|---|---|---|---|
| Struktur pasar (HH/HL/LH/LL, BOS, CHoCH), Dow Theory | AC Technical Research, Dow, SMC | ✅ Ya | Mudah dijadikan aturan: deteksi *swing high/low* otomatis. |
| Support/resistance, supply/demand | AC, forex_2, Remora hari 2 | ✅ Ya | Zona dari *swing*/pivot. |
| Fibonacci retracement/extension, *golden pocket* | AC Fibonacci Secret, live AC_crypto_4 | ✅ Ya | Mudah dihitung. |
| Pola harmonic, Elliott Wave, pola grafik | AC Harmonic, KPK | ⚠️ Ya, tetapi sulit diotomatisasi | Perlu toleransi rasio dan banyak sinyal palsu. Cocok jadi tahap lanjut. |
| Likuiditas / *stop hunt* / *order block* (SMC) | AC Smart Money | ✅ Ya, sangat populer di forex | Definisinya harus dibuat tegas dan terukur. |
| Wyckoff | AC | ⚠️ Sebagian | Volume di forex hanya *tick volume* (lihat baris order flow). |
| Indikator (MA/EMA, Ichimoku, Keltner, Donchian, Parabolic SAR, pivot, stochastic) | AC CTI, live AC, forex_3 | ✅ Ya | **Paling mudah dikodekan.** |
| Volume profile, CMF, order flow, footprint, heatmap | AC Order Flow | ⚠️ Terbatas | Forex spot tidak punya bursa pusat, jadi volume dari broker hanya *tick volume*. Alternatifnya data *futures* CME (mis. 6E untuk EURUSD, GC untuk emas). |
| Money management: risiko 1%/transaksi, RR ≥1:2, ukuran posisi | AC Money Management, Andre hari 4, Remora | ✅ **WAJIB** | Inti dari bot yang tidak cepat habis modal. |
| Psikologi & bias | AC Money Psychology | ✅ Ya | Untuk bot: alasan memakai aturan tetap. Untuk Anda: jangan mematikan bot hanya karena rugi beberapa kali berturut-turut. |
| Sentimen *fear & greed* | AC Alpha | ⚠️ Analognya | Di forex: laporan COT dan data posisi ritel dari broker. |
| Riset naratif | AC Narrative | ⚠️ Analognya | Di forex: tema makro seperti suku bunga bank sentral, inflasi, NFP. |
| Siklus 4 tahun, halving, stock-to-flow | AC | ❌ Tidak | Khas Bitcoin. |
| On-chain, wallet tracker, tokenomics, DEX, smart contract | AC | ❌ Tidak | Khas crypto. |
| Bandarmologi: broker summary, kode broker, bid–offer, SID, KSEI, "imposter" | Remora, Andre | ❌ Tidak langsung | Forex tidak punya data kode broker publik. **Prinsipnya** (ikuti uang besar, waspada saat ritel ramai) tetap berguna. |
| Valuasi saham (PER, PBV, dividen), MSCI | Andre | ❌ Tidak | Khas saham. |
| Jam sesi (Asia/Eropa/AS), jadwal berita | forex_1, Astronacci | ✅ Khas forex | Filter jam trading. |
| Teori waktu (Ichimoku, Fibonacci time, fase bulan) | forex_3, Astronacci | 🧪 Bisa diuji | Lihat bagian 9. |

**Kesimpulan:**

- Kerangka bot pertama paling masuk akal memakai urutan **Technical Research by AFS** (tren → area → pola → pemicu → entry/exit) plus aturan **money management**, ditambah filter sesi forex.
- Mentor crypto Anda kebanyakan bermain *swing*/investasi di timeframe harian–mingguan. Jadi bot yang memakai timeframe **H4/D1** lebih cocok dengan gaya mereka. Timeframe itu juga lebih tahan terhadap *noise* dan biaya spread dibanding timeframe menit.
- Semua mentor Anda mengulang pesan yang sama: **backtest dulu sebelum memakai uang sungguhan.** Ini juga berlaku untuk bot.

---

## 9. Astronacci (Gema Goeyardi)

Videonya hilang, dan materi kelas lengkapnya (CAT Institute, A-Shop) berbayar, jadi tidak tersedia publik. Berikut yang **bisa saya temukan** dari sumber publik: makalah ilmiah karya Gema sendiri, blog resmi astronacci.com, dan transkrip video YouTube resmi Astronacci.

### 9.1 Konsep dasarnya

1. **Analisa "4 dimensi":** makroekonomi, fundamental, teknikal, dan **waktu** (astrologi). Teknikal menjawab "**di harga berapa**", astrologi menjawab "**kapan**". Analis mereka sendiri menyebut astrologi "level 2" dan teknikal "level 1": kuasai teknikal dulu.
2. **Fase bulan** (paling sering dipakai): *New Moon* (bulan baru, Matahari–Bulan berimpit 0°) dan *Full Moon* (purnama, berseberangan 180°). Keduanya dianggap kandidat **titik balik** harga dalam ±1–2 hari, bisa puncak atau lembah. **Selalu dikonfirmasi** dengan teknikal: support/resistance, Fibonacci, gap, EMA21. Menurut analis mereka, faktor ini paling banyak diriset di IHSG dan **emas**; di saham AS hasilnya "fifty-fifty".
3. **Faktor astro lain:**
   - Deklinasi bulan.
   - Aspek planet: sudut antardua planet dilihat dari bumi, yaitu 0° konjungsi, 60° sextile, 90° square, 120° trine, 180° oposisi.
   - *Ingress*: planet pindah zodiak.
   - *Retrograde*: Merkurius ±24 hari, 3–4× setahun. Dipakai sebagai **penanda waktu** pasar yang rawan *sideways* dan *false breakout*, **bukan** sinyal beli/jual.
   - Siklus "Sun in Capricorn" untuk emas.
4. **Fibonacci waktu:** ukur jarak waktu antar-*swing* (puncak ke puncak, lembah ke lembah), lalu proyeksikan ke depan dengan angka Fibonacci (13, 21, 34, 55, 89, 144, 233, …). Tanggal tempat **≥3 proyeksi bertumpuk** dianggap kandidat kuat.
5. **"Astronacci"** = tanggal peristiwa astro yang **juga** jatuh di tumpukan proyeksi Fibonacci waktu.
6. **Definisi titik balik** di makalahnya adalah pola 5 candle: puncak didahului 2 *high* yang makin tinggi dan diikuti 2 *high* yang makin rendah; lembah sebaliknya. Ini mirip indikator "fractal".
7. **Teknik harga yang sering mereka ajarkan:**
   - Fibonacci retracement 23.6/38.2/50/61.8/78.6% dan ekstensi. Setiap pasar punya rasio "favorit" sendiri (misalnya 1.618 vs 2.618) yang harus dicari lewat backtest ±5 tahun.
   - Price action & candlestick: engulfing, pin bar, hammer, shooting star.
   - **Koreksi ABC di emas, timeframe H4**: masuk di akhir gelombang C.
   - Stop loss ditaruh di luar area retracement.

### 9.2 Seberapa kuat buktinya?

- Di makalah Gema dkk. (2021), dengan data IHSG & emas 2008–2017:
  - Peluang sebuah hari menjadi titik balik **tanpa metode apa pun**: ±8–9%.
  - Dengan **Fibonacci waktu saja**: ±42–43%.
  - **Astronacci + fase bulan**: 64% di IHSG (**7 dari 11 kejadian**) dan 54% di emas (7 dari 13).
- **Catatan jujur:**
  - Sampelnya sangat kecil.
  - Diuji pada data yang sama dengan data yang dipakai merumuskan metodenya.
  - Penulisnya adalah pemilik metode itu sendiri.
  - Beberapa angka di tabelnya tidak konsisten.
  - Klaim "70–80%" atau "75%" di video/blog tidak disertai data.
  - Saya tidak menemukan uji independen dari pihak lain.
  - Secara ilmiah, pengaruh langsung planet ke harga belum terbukti. Pihak Astronacci sendiri berargumen pengaruhnya "tidak langsung, lewat psikologi".
- Jadi perlakukan Astronacci sebagai **hipotesis yang perlu diuji**, bukan kepastian.

### 9.3 Cara memakainya di bot (bisa diuji secara objektif)

- Tanggal fase bulan, posisi planet, dan retrograde **bisa dihitung otomatis** dengan pustaka astronomi Python (misalnya `skyfield` atau `ephem`). Tidak perlu situs pihak ketiga.
- *Swing* 5-candle dan tumpukan Fibonacci waktu juga **bisa dihitung otomatis**.
- Lalu uji di EURUSD/XAUUSD: apakah tanggal-tanggal itu **lebih sering** menjadi titik balik dibanding hari biasa? Kalau tidak lebih baik dari acak, buang. Kalau lebih baik, pakai sebagai **filter waktu tambahan** di atas analisa utama.
- Kerabat terdekat Astronacci yang **sudah ada** di materi Anda adalah **teori waktu Ichimoku** di [forex_3 L713–1184](mentah/forex_3.txt#L713-L1184).

**Saran:** sesuai keinginan Anda, jadikan analisa dari kelas **crypto & saham** sebagai mesin utama bot. Konsep Astronacci menjadi **filter opsional** yang harus lolos backtest dulu.

### 9.4 Sumber

- Goeyardi, G. M., Ghozali, I., & Hady, H. (2021). *Financial Analysis Method Based On Astrology, Fibonacci, And Astronacci To Find A Date Of Direction Inversion…* Turkish Journal of Computer and Mathematics Education 12(4). [PDF](https://scispace.com/pdf/financial-analysis-method-based-on-astrology-fibonacci-and-2bqr3lari5.pdf) · versi jurnal IJEBR: [IDEAS/RePEc](https://ideas.repec.org/a/ids/ijecbr/v22y2021i2-3p290-310.html)
- Blog Astronacci: [Belajar Trading Astronacci](https://astronacci.com/blog/read/belajar-trading-astronacci-konsep-dasar-strategi) · [Time Cycle Trading](https://astronacci.com/blog/read/time-cycle-trading-untuk-siklus-pasar-dan-struktur-waktu) · [Mercury Retrograde sebagai penanda waktu](https://astronacci.com/blog/read/memahami-mercury-retrograde-sebagai-penanda-waktu-dalam-market)
- Video YouTube Astronacci: [Astrology kok dipake buat trading? (moon phase)](https://www.youtube.com/watch?v=hHhogj1JGms) · [Jurus A-B-C di Gold](https://www.youtube.com/watch?v=joEApBiyCOM)
- Berita: [IDX Channel, Okt 2025: "Time Trading" Astronacci](https://www.idxchannel.com/market-news/pendekatan-time-trading-makin-diterima-astronacci-siap-ekspansi-ke-kawasan-regional/all)

---

## 10. Daftar istilah

Penjelasan dibuat sesederhana mungkin. Istilah disusun per kelompok.

### 10.1 Istilah umum trading & risiko

| Istilah | Arti sederhana |
|---|---|
| **Trading** | Membeli lalu menjual dalam waktu relatif singkat untuk mengambil selisih harga. |
| **Investasi / investing** | Membeli aset untuk disimpan lama karena yakin nilainya tumbuh. |
| **Scalping** | Trading super cepat (detik sampai menit) dengan target untung kecil tapi sering. |
| **Day trading** | Posisi dibuka dan ditutup di hari yang sama. |
| **Swing trading** | Menahan posisi beberapa hari sampai minggu, mengikuti "ayunan" harga. |
| **Long / buy** | Bertaruh harga naik. |
| **Short / sell** | Bertaruh harga turun (untung kalau harga turun). |
| **Posisi** | Transaksi yang sedang terbuka. |
| **Entry** | Titik masuk (saat membuka posisi). |
| **Exit** | Titik keluar (saat menutup posisi). |
| **TP (take profit)** | Batas harga untuk mengambil untung secara otomatis. |
| **SL (stop loss)** | Batas harga untuk memotong rugi secara otomatis. |
| **CL (cut loss)** | Menutup posisi yang rugi, biasanya manual. |
| **Floating profit/loss** | Untung/rugi yang belum direalisasi karena posisi masih terbuka. |
| **Risk–reward (RR)** | Perbandingan risiko dan target. RR 1:3 artinya mempertaruhkan 1 untuk mengincar 3. |
| **Win rate** | Persentase transaksi yang untung. |
| **Money management / position sizing** | Aturan berapa banyak uang yang dipakai per transaksi, misalnya risiko maksimal 1% modal. |
| **Drawdown** | Penurunan modal dari titik tertingginya. |
| **Backtest** | Menguji strategi di data harga masa lalu sebelum dipakai dengan uang sungguhan. |
| **Trading plan** | Rencana tertulis: kapan masuk, keluar, dan seberapa besar. |
| **Leverage** | "Pinjaman" dari broker untuk memperbesar posisi. Untung dan rugi ikut membesar. |
| **Margin call (MC)** | Modal habis/menipis sehingga posisi ditutup paksa oleh broker. |
| **Compounding (gulung-gulung)** | Untung diputar lagi sehingga modal tumbuh berbunga. |
| **Rumus 72** | Kira-kira lama uang berlipat dua = 72 ÷ persen return per tahun. |
| **DCA (dollar cost averaging)** | Membeli rutin dalam jumlah kecil supaya dapat harga rata-rata. |
| **Lump sum** | Membeli sekaligus. |
| **Rebalancing** | Mengembalikan porsi portofolio ke rencana awal, misalnya kembali ke 70/30. |
| **Diversifikasi** | Menyebar uang ke beberapa aset supaya risikonya tidak menumpuk. |
| **Portofolio** | Kumpulan aset yang dimiliki. |
| **Bull market / bullish** | Pasar sedang naik / pandangan naik. |
| **Bear market / bearish** | Pasar sedang turun / pandangan turun. |
| **Sideways / konsolidasi / range** | Harga bergerak mendatar di satu rentang. |
| **ATH (all time high)** | Harga tertinggi sepanjang sejarah. |
| **Pucuk** | Harga di puncak. "Beli di pucuk" artinya membeli di harga tertinggi. |
| **Nyangkut** | Terjebak rugi karena membeli di harga tinggi. |
| **Cuan** | Untung. |
| **FOMO** | Takut ketinggalan, sehingga membeli karena ikut-ikutan. |
| **Fear & greed** | Dua emosi penggerak pasar: takut dan serakah. |
| **Smart money** | "Uang pintar": dana besar dari institusi atau pemain berpengalaman. |
| **Ritel** | Investor/trader perorangan bermodal kecil. |
| **Likuiditas (liquidity)** | Banyaknya uang/transaksi di suatu pasar. Pasar likuid mudah dibeli-jual tanpa harga melompat. |
| **Probabilitas vs posibilitas** | Probabilitas = seberapa *mungkin* sesuatu terjadi (dihitung). Posibilitas = *bisa saja* terjadi. Ko Hengki menekankan berpikir dengan probabilitas. |

### 10.2 Istilah analisa teknikal (dipakai di semua pasar)

| Istilah | Arti sederhana |
|---|---|
| **Chart / grafik** | Gambar pergerakan harga dari waktu ke waktu. |
| **Candlestick (candle)** | "Batang lilin" yang menunjukkan harga buka, tutup, tertinggi, dan terendah dalam satu periode. |
| **Timeframe (TF)** | Lamanya satu candle: M1 = 1 menit, H1 = 1 jam, H4 = 4 jam, D1 = harian, W = mingguan. |
| **Body / wick (ekor)** | Badan candle (dari harga buka ke tutup) / garis tipis di atas atau bawahnya. |
| **Engulfing, hammer, pin bar, doji, shooting star** | Bentuk-bentuk candle yang sering dianggap tanda pembalikan arah. |
| **Price action (PA)** | Membaca gerak harga murni tanpa banyak indikator. |
| **Tren (uptrend/downtrend)** | Arah umum harga: naik atau turun. |
| **HH / HL / LH / LL** | *Higher High / Higher Low* (tanda tren naik); *Lower High / Lower Low* (tanda tren turun). |
| **Swing high / swing low** | Titik puncak / lembah kecil pada grafik. |
| **Market structure** | Susunan puncak dan lembah yang menunjukkan tren. |
| **Support** | "Lantai": area tempat harga cenderung berhenti turun. |
| **Resistance** | "Atap": area tempat harga cenderung berhenti naik. |
| **SnR / SnD** | Support & Resistance / Supply & Demand. |
| **Supply / demand zone** | Area tempat banyak penjual / pembeli menunggu. |
| **Breakout** | Harga menembus support/resistance. |
| **Fake out / false breakout** | Tembusan palsu: harga lalu kembali lagi. |
| **Retest** | Harga kembali menyentuh level yang baru ditembus untuk "mengetes". |
| **Pullback / koreksi / retracement** | Turun/naik sementara melawan tren utama. |
| **Reversal / titik balik / turning point** | Pembalikan arah tren. |
| **Gap** | Lompatan harga yang menyisakan "lubang" di grafik. |
| **Volume** | Jumlah yang diperdagangkan. Di forex biasanya hanya *tick volume* (jumlah perubahan harga). |
| **Multi-timeframe** | Melihat timeframe besar untuk arah, timeframe kecil untuk titik masuk. |
| **Indikator** | Rumus dari data harga/volume yang digambar di grafik untuk membantu analisa. |
| **MA / EMA (moving average)** | Rata-rata harga N periode. EMA lebih cepat bereaksi. Contoh: EMA21, MA50. |
| **Stochastic / RSI** | Indikator "osilator" untuk melihat apakah harga sudah terlalu tinggi/rendah. |
| **Pivot points** | Level support/resistance otomatis dari harga periode sebelumnya. |
| **Keltner / Donchian Channel** | Pita di atas dan bawah harga untuk melihat volatilitas dan *breakout*. |
| **Parabolic SAR** | Titik-titik di atas/bawah harga untuk mengikuti tren dan menaruh stop. |
| **Renko** | Grafik berbentuk bata yang mengabaikan waktu, hanya mencatat pergerakan harga tertentu. |
| **KST (Know Sure Thing)** | Indikator momentum gabungan dari beberapa *rate of change*. |
| **CMF (Chaikin Money Flow)** | Indikator arah aliran uang (masuk/keluar). |
| **Volume profile / VPFR** | Histogram volume per level harga, untuk melihat harga mana yang paling ramai. |
| **Ichimoku** | Sistem indikator Jepang. **Tenkan-sen** = garis cepat (9). **Kijun-sen** = garis sedang (26). **Senkou Span A/B** membentuk **Kumo** (awan) yang menjadi zona support/resistance. **Chikou Span** = harga digeser 26 periode ke belakang. |
| **Dow Theory** | Teori klasik: pasar bergerak dalam tren (primer, sekunder, harian) yang harus dikonfirmasi volume. |
| **Elliott Wave** | Teori gelombang: tren naik terdiri dari 5 gelombang, koreksinya 3 gelombang (A-B-C). |
| **Koreksi ABC** | Pola koreksi 3 langkah. Astronacci mengajarkan masuk di akhir gelombang C. |
| **Wyckoff** | Teori siklus "bandar": akumulasi → markup (naik) → distribusi → markdown (turun), dibagi fase A–E. |
| **Akumulasi / distribusi** | Pemain besar diam-diam mengumpulkan / melepas barang. |
| **Spring / upthrust** | Tembusan palsu ke bawah / ke atas dalam pola Wyckoff. |
| **Fibonacci** | Deret 1, 1, 2, 3, 5, 8, 13, 21, … yang rasionya (0.382, 0.5, 0.618, 1.618, …) dipakai untuk menebak area pantulan dan target. |
| **Fibonacci retracement** | Level koreksi (23.6/38.2/50/61.8/78.6%). |
| **Fibonacci extension** | Level target lanjutan (1.272/1.618/2.618/…). |
| **Golden ratio / golden pocket** | 1.618 / area 0.618–0.65, dianggap level pantulan terkuat. |
| **Fibonacci channel / trend-based extension** | Variasi alat Fibonacci untuk saluran dan target. |
| **Harmonic support/resistance** | Area beli/jual dari ekstensi Fibonacci (istilah dari kelas AC). |
| **Harmonic pattern** | Pola harga dengan rasio Fibonacci tertentu: **ABCD, Gartley, Bat, Crab, Butterfly, Shark**. Titik akhirnya disebut **PRZ** (*potential reversal zone*). |
| **Head & shoulders, double top/bottom, triangle, wedge, diamond, broadening, rectangle** | Nama-nama pola grafik klasik. |
| **Andrews Pitchfork** | Alat tiga garis sejajar ("garpu") untuk memperkirakan saluran harga. |
| **Linear Regression Channel (LRC)** | Saluran harga dari garis regresi (garis rata-rata lurus). |
| **Smart Money Concept (SMC)** | Cara membaca jejak pemain besar lewat likuiditas. |
| **Liquidity / BSL / SSL** | Tumpukan stop loss di atas puncak (*buy-side liquidity*) / di bawah lembah (*sell-side liquidity*). |
| **Stop hunt / liquidity grab** | Harga sengaja "menyapu" stop loss lalu berbalik. |
| **BOS (break of structure)** | Struktur tren ditembus searah tren: tren berlanjut. |
| **CHoCH (change of character)** | Struktur ditembus berlawanan arah: tanda awal tren berubah. |
| **Order block (OB)** | Candle/area terakhir sebelum gerakan besar, tempat order besar diduga berada. |
| **Order flow** | Membaca aliran order beli/jual secara langsung (bukan hanya harga). |
| **Bid / ask (offer)** | Harga yang diminta pembeli / ditawarkan penjual. |
| **Order book** | Daftar antrean order beli dan jual. |
| **Footprint chart** | Grafik yang menampilkan volume beli & jual di setiap level harga dalam satu candle. |
| **Delta / cumulative delta** | Selisih volume beli agresif dan jual agresif / jumlah kumulatifnya. |
| **HVN / LVN** | Level harga dengan volume tinggi / rendah. |
| **Volume cluster** | Area tempat volume menumpuk. |
| **Unfinished business (auction)** | Level yang "belum tuntas" diperdagangkan dan cenderung dikunjungi lagi. |
| **Heatmap** | Peta warna antrean order besar di order book. |
| **ATAS** | Aplikasi khusus untuk analisa order flow. |
| **Momentum (pace & rhythm)** | Kecepatan dan irama pergerakan harga. |
| **Screening** | Menyaring daftar aset untuk memilih yang layak ditradingkan. |
| **Fractal 5 candle** | Puncak/lembah yang diapit 2 candle di kiri dan 2 di kanan. Dipakai Astronacci sebagai definisi titik balik. |

### 10.3 Kamus "salah dengar" transkrip

| Tertulis di transkrip | Maksud sebenarnya |
|---|---|
| week off, pick of, week of trading | **Wyckoff** |
| do teori, doteri, dot teori, blue theory | **Dow Theory** |
| all testing, self testing, of testing, all fasting, alvesti, avesting, investing (sebagai nama) | **Alvesting** (pengajar teknikal AC, juga disebut "AFS") |
| kali masada, kalimah sada, kalim asada | **Kalimasada** (pengajar investasi AC) |
| akademi akan crypto, akad crypto, Karim crypto | **Akademi Crypto** |
| Beat over, Beat nya, nge Beat | **Bid–offer**, antre di sisi *bid* |
| bandar molek | **Bandarmologi** |
| broksum, broker summer | **Broker summary** |
| VIP channels, flip channels | **Fibonacci channels** |
| dimension channels | **Donchian channels** |
| parabolic sap | **Parabolic SAR** |
| checking money flow | **Chaikin Money Flow** |
| kelner channel | **Keltner Channel** |
| no sorting / kst | **KST (Know Sure Thing)** |
| garlic / garply pattern | **Gartley pattern** |
| bad pattern | **Bat pattern** |
| brodening | **Broadening** |
| Andrew state / Andrews pitchfork | **Andrews Pitchfork** |
| sharp pattern | **Shark pattern** |
| elit wave | **Elliott Wave** |
| hit map | **Heatmap** |
| atas | **ATAS** (aplikasi order flow) |
| ima, ama | **EMA / MA** |
| cek / cex, decks | **CEX / DEX** |
| tgi, tggi | **TGE** (*token generation event*, saat token baru diluncurkan) |
| MSI, mci, mcci | **MSCI** (indeks global) |
| munfess, monkeys, mun cycle | **Moon phase / moon cycle** (dalam video Astronacci) |
| strategi komputer, copet, cometer, sepeda, separator, joker | **Strategi "copet"** (scalping FXcopet) di forex_1 |
| hosoda, Chico, kumo | **Goichi Hosoda**, **Chikou**, **Kumo** (Ichimoku) |
| mindset dan teknologi | **Mindset dan psikologi** (AndreHakim_saham_2) |
| lemoora / remote akademi | **Remora Academy** |

### 10.4 Istilah crypto

| Istilah | Arti sederhana |
|---|---|
| **Bitcoin (BTC)** | Crypto pertama dan terbesar. Dianggap "emas digital" (*store of value*). |
| **Altcoin** | Semua crypto selain Bitcoin. |
| **Meme coin** | Koin "lelucon" yang harganya digerakkan tren/viral. Sangat berisiko. |
| **Stablecoin** | Koin yang nilainya dipatok ke dolar (misalnya USDT). |
| **Market cap (kapitalisasi pasar)** | Harga × jumlah koin beredar. Big/mid/small cap = besar/sedang/kecil. |
| **Store of value** | Aset untuk menyimpan nilai jangka panjang. |
| **Halving** | Peristiwa ±4 tahun sekali ketika hadiah penambang Bitcoin dipotong setengah. Dasar "siklus 4 tahun". |
| **Siklus 4 tahun** | Pola naik-turun Bitcoin mengikuti halving. Rumus di kelas: beli setahun sebelum halving, jual setahun sesudahnya. |
| **Stock-to-flow** | Model harga Bitcoin berdasarkan kelangkaan (stok dibanding produksi baru). |
| **Altcoin season** | Masa ketika altcoin naik lebih kencang daripada Bitcoin. |
| **Narasi / sektor** | Tema yang sedang diburu pasar: AI, RWA, meme, DePIN, dan sebagainya. |
| **RWA** | *Real World Assets*: aset dunia nyata yang dijadikan token. |
| **Tokenomics** | "Ekonomi" sebuah token: jumlah, pembagian, jadwal rilis, kegunaan. |
| **Nilai intrinsik** | Nilai "sebenarnya" menurut fundamental. |
| **CEX** | *Centralized exchange*, bursa terpusat seperti Indodax, Tokocrypto, Binance. |
| **DEX** | *Decentralized exchange*, bursa langsung di blockchain tanpa perantara (Uniswap, PancakeSwap). |
| **Spot / derivatif / futures** | Spot = beli asetnya langsung. Derivatif/futures = kontrak taruhan harga, bisa pakai leverage. |
| **Perp DEX / prop DEX** | DEX untuk kontrak *perpetual* (futures tanpa jatuh tempo). |
| **Wallet / dompet** | Aplikasi penyimpan crypto (misalnya MetaMask). |
| **Self-custody** | Menyimpan aset sendiri, bukan di bursa. |
| **Seed phrase** | 12/24 kata kunci untuk memulihkan wallet. Jangan pernah dibagikan. |
| **On-chain** | Terjadi/tercatat langsung di blockchain dan bisa dilihat siapa saja. |
| **Wallet tracker** | Memantau dompet orang lain (misalnya dompet "pintar") untuk dicontek. |
| **Smart contract** | Program otomatis di blockchain. Bisa dicek untuk mendeteksi token penipuan. |
| **Rug pull** | Pengembang kabur membawa dana. |
| **Liquidity pool / AMM** | Kolam dana di DEX yang menggantikan order book. |
| **Gas fee** | Biaya transaksi di blockchain. |
| **Launchpad / ICO / TGE** | Tempat/acara peluncuran token baru. |
| **Airdrop** | Pembagian token gratis. |
| **Moon bag** | Sisa koin yang dibiarkan "terbang" setelah modal ditarik. |
| **Relief bounce** | Pantulan naik sementara setelah turun tajam. |
| **Range high / range low** | Batas atas / bawah rentang harga. |
| **Grey area / grey zone** | Area yang tidak jelas arahnya; lebih baik tidak masuk. |
| **Base** | Area dasar tempat harga berhenti turun dan "membangun pondasi". |
| **Liquidity grab** | Harga sengaja menyapu stop loss. |

### 10.5 Istilah saham Indonesia

| Istilah | Arti sederhana |
|---|---|
| **IHSG / JCI** | Indeks Harga Saham Gabungan: "rata-rata" seluruh saham di Bursa Efek Indonesia. |
| **Emiten** | Perusahaan yang sahamnya diperdagangkan di bursa. |
| **Lot** | Satuan beli saham di Indonesia: 1 lot = 100 lembar. |
| **Tick** | Satuan kenaikan harga terkecil. |
| **Bid / offer** | Antrean beli / antrean jual. |
| **HAKA / HAKI** | *Hajar kanan* (langsung beli di harga offer) / *hajar kiri* (langsung jual di harga bid). |
| **ARA / ARB** | Auto Reject Atas / Bawah: batas naik/turun maksimal harian. |
| **Broker summary (broksum)** | Ringkasan broker mana yang membeli dan menjual suatu saham. |
| **Kode broker (XC, XL, CC, YP, PD, dll.)** | Kode sekuritas. Ada yang identik dengan ritel (misalnya aplikasi populer), ada yang dengan pemain besar. |
| **Bandar / bandarmologi** | Pemain besar penggerak saham / ilmu membaca jejak mereka. |
| **"Imposter"** | Istilah Ko Hengki untuk pemain besar yang "menyamar" memakai broker ritel. |
| **Algo asing** | Robot trading dana asing. Ordernya langsung menempel dalam milidetik. |
| **Market maker (MM)** | Pihak yang menjaga likuiditas atau mengatur harga sebuah saham. |
| **Akumulasi / distribusi (akum / disti)** | Mengumpulkan / membuang barang secara bertahap. |
| **Gorengan** | Saham yang dinaikkan secara tidak wajar, biasanya tidak likuid. |
| **Saham gocap** | Saham di harga Rp50 (harga terendah papan reguler). |
| **FCA** | *Full Call Auction*: papan pemantauan khusus yang perdagangannya lewat lelang berkala. |
| **Suspend** | Perdagangan saham dihentikan sementara oleh bursa. |
| **Free float** | Porsi saham yang dimiliki publik dan bisa diperdagangkan. |
| **SID** | Single Investor Identification: jumlah investor pemegang suatu saham. |
| **KSEI / laporan kepemilikan ≥5%** | Data pemegang saham besar yang wajib dilaporkan. |
| **NeoBDM** | Platform data bandarmologi (akumulasi/distribusi per broker). |
| **MSCI** | Indeks global. Saham yang masuk biasanya dibeli dana asing. |
| **IPO / prospektus** | Penawaran saham perdana / dokumen resminya. |
| **Corporate action** | Aksi perusahaan: dividen, *rights issue*, *private placement*, *stock split*, dsb. |
| **Rights issue / private placement (PP)** | Penerbitan saham baru untuk pemegang lama / untuk pihak tertentu. |
| **Takeover / backdoor listing** | Pengambilalihan perusahaan / masuk bursa lewat membeli perusahaan yang sudah tercatat. |
| **PER (P/E)** | Harga dibagi laba per saham: "berapa tahun balik modal dari laba". |
| **PBV** | Harga dibagi nilai buku per saham. |
| **Dividen / dividend payout ratio / dividend yield** | Bagian laba yang dibagikan / persentase laba yang dibagi / dividen dibanding harga saham. |
| **Blue chip / big cap** | Saham perusahaan besar dan mapan. |
| **Multibagger** | Saham yang naik berlipat-lipat. |
| **Moon stock** | Istilah Ko Hengki untuk saham pilihan yang potensinya naik sangat tinggi. |
| **Serok** | Membeli saat harga turun. |
| **Buy on breakout / buy on weakness** | Membeli saat menembus resistance / membeli saat sedang turun. |
| **Reksa dana** | Wadah dana bersama yang dikelola manajer investasi. |

### 10.6 Istilah forex

| Istilah | Arti sederhana |
|---|---|
| **Forex (FX)** | Pasar jual-beli mata uang. Buka 24 jam, Senin–Jumat. |
| **Pair** | Pasangan mata uang, misalnya EURUSD (euro terhadap dolar AS). |
| **XAUUSD** | Emas dalam dolar AS. Diperdagangkan seperti pair forex. |
| **Pip / poin** | Satuan pergerakan terkecil yang lazim. Di EURUSD 1 pip = 0.0001. Di forex_1 disebut "poin". |
| **Spread** | Selisih harga beli dan jual: biaya tersembunyi dari broker. |
| **Lot (forex)** | Ukuran posisi. 1 lot standar = 100.000 unit; mini = 10.000; mikro = 1.000. |
| **Swap / rollover** | Biaya/bunga untuk posisi yang ditahan melewati hari. |
| **Broker** | Perusahaan perantara tempat membuka akun trading. Pilih yang **teregulasi**. |
| **MetaTrader 4/5 (MT4/MT5)** | Aplikasi trading forex paling umum. Bisa menjalankan bot (*Expert Advisor*). |
| **Expert Advisor (EA) / robot / bot** | Program yang membuka-tutup posisi secara otomatis. |
| **Pending order (buy stop / sell stop / limit)** | Order yang menunggu harga tertentu tersentuh dulu. |
| **Sesi Asia / Eropa / Amerika** | Jam ramai pasar per wilayah. Sesi Eropa kira-kira sore–malam WIB. |
| **NFP** | *Non-Farm Payrolls*: data tenaga kerja AS, rilis bulanan, membuat harga bergejolak. |
| **COT report** | Laporan posisi para pelaku besar di pasar futures AS, untuk membaca sentimen. |
| **Tick volume** | "Volume" versi broker forex: jumlah perubahan harga, bukan jumlah uang. |

### 10.7 Istilah psikologi trading

| Istilah | Arti sederhana |
|---|---|
| **Bias kognitif** | "Jebakan" cara berpikir yang membuat keputusan tidak rasional. |
| **Overconfidence** | Terlalu percaya diri, merasa pasti benar. |
| **Herding** | Ikut-ikutan orang banyak. |
| **Loss aversion** | Rasa sakit karena rugi terasa lebih besar daripada senang karena untung, sehingga enggan cut loss. |
| **Greater fool theory** | "Akan selalu ada orang yang lebih bodoh yang mau membeli lebih mahal." |
| **Opportunity cost** | Keuntungan yang hilang karena memilih opsi lain. |
| **Limiting belief** | Keyakinan yang membatasi diri, seperti "saya tidak bakat". |
| **Hopium** | Harapan berlebihan yang tidak realistis. |
| **Kontrarian** | Mengambil posisi berlawanan dengan mayoritas. |

### 10.8 Istilah Astronacci / astrologi finansial

| Istilah | Arti sederhana |
|---|---|
| **Astrologi finansial** | Mengaitkan posisi benda langit dengan siklus pasar. Belum terbukti ilmiah. |
| **Time trading / time cycle** | Fokus pada **kapan** harga berbalik, bukan hanya di harga berapa. |
| **New Moon / Full Moon** | Bulan baru (Matahari–Bulan berimpit) / purnama (berseberangan). Dianggap kandidat titik balik. |
| **Moon declination** | Posisi bulan di utara/selatan garis khatulistiwa langit. |
| **Aspek planet** | Sudut antardua planet dilihat dari bumi: **konjungsi** 0°, **sextile** 60°, **square** 90°, **trine** 120°, **oposisi** 180°. |
| **Ingress** | Planet berpindah ke rasi zodiak berikutnya. |
| **Retrograde** | Planet *tampak* berjalan mundur dari bumi. Mercury Retrograde dipakai sebagai "penanda waktu rawan". |
| **Fibonacci time projection** | Memproyeksikan tanggal ke depan memakai angka Fibonacci dari jarak antar-*swing*. |
| **Angka Hosoda** | Angka waktu Ichimoku (9, 17, 26, …). Mirip konsep Fibonacci waktu. |

---

## 11. Catatan dan langkah berikutnya

- **File asli tidak diubah.** Pemilahan per pasar & topik dilakukan **di dokumen ini**, tidak dengan memindahkan atau memecah file. Kalau Anda mau, saya bisa membuat **salinan terpilah** (satu file per video/modul di folder baru, misalnya `materi/terpilah/`) atau **indeks CSV/JSON** yang nantinya bisa dibaca bot. File di `mentah/` tetap utuh.
- **Yang bisa membantu kalau Anda punya:**
  1. Akses ulang atau catatan kelas Astronacci (misalnya hubungi Astronacci untuk akses ulang kelas yang dibeli). Unggah ke `materi/mentah/`, lalu saya petakan.
  2. Modul-modul yang ditandai **HILANG** di bagian 3.5.
- **Tahap bot nanti:** kita perlu memilih platform eksekusi (misalnya MetaTrader 5, OANDA, atau cTrader), akun **demo**, dan sumber data historis untuk backtest. Itu dibahas saat mulai membangun bot.
