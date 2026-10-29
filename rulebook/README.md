# RULEBOOK STRATEGI BOT (forex & kripto)

Rulebook ini menerjemahkan isi kelas ke dalam **aturan yang bisa dikodekan**. Sumbernya adalah peta [`materi/PETA.md`](../materi/PETA.md) dan transkrip di [`materi/mentah/`](../materi/mentah/). Setiap aturan diberi tautan ke file dan **nomor baris** transkrip tempat mentor mengatakannya, jadi bisa dicek sendiri.

**Prinsip penyusunan:**

1. **Mesin utama** diambil dari kelas **kripto** (Akademi Crypto) dan **saham** (Remora, Andre Hakim), ditambah materi **forex**.
2. Bot hanya untuk **forex dan kripto**. Bagian yang **hanya berlaku di saham** (broker summary, antrean bid–offer, SID/KSEI, ARA/ARB, PER/PBV, MSCI, dan lain-lain) **tidak dijadikan aturan**. Daftarnya ada di [08-tidak-dijadikan-aturan.md](08-tidak-dijadikan-aturan.md).
3. Konsep **Astronacci** (PETA bagian 9) masuk sebagai **filter waktu opsional**, default **mati**, di [07-filter-waktu.md](07-filter-waktu.md).
4. **Bagian yang ambigu tidak ditebak.** Kalau mentor tidak menyebut angka atau definisinya, aturan itu ditandai 🟡 dan diberi nomor pertanyaan **Q-xx**. Semua pertanyaan ada di [09-pertanyaan-untuk-anda.md](09-pertanyaan-untuk-anda.md), ditulis dengan bahasa awam.

---

## Daftar isi

| File | Isi |
|---|---|
| [00-aturan-global.md](00-aturan-global.md) | Aturan yang berlaku untuk **semua setup**: risiko per transaksi, stop loss wajib, larangan average down, hedging, revenge trading, filter instrumen, dan lain-lain. Juga daftar **perbedaan pendapat antar-mentor**. |
| [01-alvesting-akademi-crypto.md](01-alvesting-akademi-crypto.md) | **Alvesting (AFS)**, pengajar teknikal Akademi Crypto: Technical Research 5 tahap, scalping, Smart Money Concept, Fibonacci, Dow Theory, pola harmonic & kamus pola, indikator, order flow, screening altcoin. |
| [02-kalimasada-akademi-crypto.md](02-kalimasada-akademi-crypto.md) | **Kalimasada**: money management, Wyckoff, modul investasi spot kripto (alokasi, moon bag, cicilan, fear & greed). |
| [03-analis-live-akademi-crypto.md](03-analis-live-akademi-crypto.md) | **Analis live market update** Akademi Crypto: filter "grey area", siklus halving Bitcoin, cara main token baru (TGE). |
| [04-ko-hengki-remora.md](04-ko-hengki-remora.md) | **Ko Hengki (Remora)**: hanya prinsip harga & volume serta tren yang berlaku umum. Bandarmologi tidak dipakai. |
| [05-ko-andri-andre-hakim.md](05-ko-andri-andre-hakim.md) | **Ko Andri (Andre Hakim)**: prinsip manajemen posisi yang berlaku umum. Valuasi saham tidak dipakai. |
| [06-mentor-forex.md](06-mentor-forex.md) | Tiga sumber forex: **FXcopet** (scalping EURUSD M1), **Pola N** di emas (forex_2), **Ichimoku** Rafał Zuchowicz (forex_3). |
| [07-filter-waktu.md](07-filter-waktu.md) | **Filter waktu opsional**: Astronacci (fase bulan, Fibonacci waktu, retrograde) dan angka waktu Hosoda (Ichimoku). |
| [08-tidak-dijadikan-aturan.md](08-tidak-dijadikan-aturan.md) | Materi yang sengaja **tidak** dijadikan aturan, beserta alasannya. |
| [09-pertanyaan-untuk-anda.md](09-pertanyaan-untuk-anda.md) | **Semua pertanyaan** untuk Anda, dari yang paling menentukan. |

---

## Cara membaca

### Label status setiap setup

| Label | Artinya |
|---|---|
| 🟢 **Siap dikodekan** | Semua syarat dan angka disebut mentor. Programmer bisa langsung menulis kodenya. |
| 🟡 **Butuh jawaban** | Logikanya jelas, tetapi ada angka/definisi yang tidak disebut mentor. Lihat nomor **Q-xx**. |
| 🔴 **Sulit diotomasi** | Sangat bergantung pada "mata" trader, atau butuh data yang tidak tersedia. Disimpan sebagai referensi, **tidak disarankan** untuk bot versi pertama. |
| ⚪ **Filter / konteks** | Bukan sinyal masuk, melainkan penyaring: "boleh/tidak boleh trading sekarang". |

### Label pasar

| Label | Artinya |
|---|---|
| **K** | Berlaku untuk kripto. |
| **F** | Berlaku untuk forex (termasuk emas XAUUSD). |
| **K\*** / **F\*** | Berlaku, **tetapi angkanya harus disesuaikan** (contoh: aturan "tembus 3%" dari kelas kripto terlalu besar untuk forex). Lihat Q-10. |

### Format setiap setup

Setiap setup ditulis dengan urutan yang sama, supaya mudah diubah menjadi kode:

- **Kartu ringkas**: mentor, sumber, pasar, timeframe, arah, status.
- **Syarat**: semua harus terpenuhi, berurutan.
- **Entry**: kapan dan bagaimana order dipasang.
- **Stop loss (SL)** dan **take profit (TP)**.
- **Batal / jangan masuk jika**.
- **Belum jelas**: hal yang tidak disebut mentor, dengan nomor pertanyaannya.

Istilah teknis dijelaskan di [PETA bagian 10](../materi/PETA.md#10-daftar-istilah).

---

## Urutan kerja bot (alur keputusan)

Semua setup dipasang di dalam alur yang sama. Urutan ini diambil dari cara para mentor sendiri bekerja: tren → area → pola → pemicu → entry/exit ([AC_crypto_57 L1854–1873](../materi/mentah/AC_crypto_57.txt#L1854-L1873)).

```
1. Aturan global (00)        → boleh trading hari ini? (batas risiko, berita, sesi, instrumen likuid)
2. Filter pasar (⚪)          → misal: korelasi BTC untuk altcoin, "grey area", volume
3. Setup (🟢/🟡)              → syarat terpenuhi? hitung entry, SL, TP
4. Ukuran posisi (G-01)       → lot/kontrak dihitung dari jarak SL dan risiko per transaksi
5. Filter waktu (07, opsional) → hanya jika diaktifkan dan sudah lolos backtest
6. Kelola posisi              → TP/SL sesuai setup, tanpa intervensi manual (G-12)
```

---

## Indeks semua setup

### Akademi Crypto — Alvesting (AFS) → [01](01-alvesting-akademi-crypto.md)

| ID | Setup | Pasar | TF | Status |
|---|---|---|---|---|
| AFS-01 | Technical Research 5 tahap, versi swing | K, F | D1 / H4 / M15 | 🟡 |
| AFS-02 | Technical Research 5 tahap, versi scalping | K, F | H1 / M15 / M5 | 🟡 |
| AFS-03 | Double top/bottom + tembus neckline (contoh scalping) | K, F | M15 | 🟡 |
| AFS-04 | Pantulan Fibonacci *golden pocket* 0,5–0,618 | K, F\* | W1 / D1 | 🟡 |
| AFS-05 | *Money magnet* EMA 13 & 21 | K, F | — | 🟡 |
| AFS-06 | Stop hunt + break of structure (inti SMC) | K, F | H4 / M15 | 🟡 |
| AFS-07 | Change of character (CHoCH) + retest | K, F | H4 / M15 | 🟡 |
| AFS-08 | Revisit order block / fair value gap setelah BOS | K, F | H4 / M15 | 🟡 |
| AFS-09 | Validasi tembus 3% Dow Theory (MA21 / trendline) | K, F\* | D1 | 🟡 |
| AFS-10 | Pola ABCD | K, F | M15 / H1 | 🟡 |
| AFS-11 | Pola harmonic XABCD (Gartley, Bat, Crab, Butterfly, Shark) | K, F | H1–D1 | 🔴 |
| AFS-12 | Pivot point: entry di garis P | K, F | H1 / M15 / M5 | 🟡 |
| AFS-13 | Keltner Channel (SMA20, ATR10, ×2) | K, F | — | 🟡 |
| AFS-14 | Ichimoku "di atas/bawah semua garis" | K, F | D1 | 🟢 |
| AFS-15 | Parabolic SAR titik ke-2 | K, F | H1 / H4 | 🟡 |
| AFS-16 | Donchian Channel | K, F | — | 🟡 |
| AFS-17 | KST silang di garis nol | K, F | D1 | 🟢 |
| AFS-18 | Konfirmasi Chaikin Money Flow | K, F\* | H4 / D1 | 🟡 |
| AFS-19 | Pantulan POC (volume profile) | K, F\* | H1+ | 🟡 |
| AFS-20 | Linear Regression Channel (intraday) | K, F | intraday | 🟡 |
| AFS-21 | Renko reversal | K, F | D1 | 🟡 |
| AFS-22 | Order flow: divergensi delta, stacked imbalance, unfinished auction | K | — | 🟡 |
| AFS-23 | Pola grafik klasik (pennant, triangle, flag, H&S, wedge, broadening, diamond, rectangle) | K, F | H4 / D1 | 🔴 |
| AFS-24 | Elliott Wave (masuk di gelombang 2 & 4) | K, F | D1 | 🔴 |
| AFS-25 | Andrews Pitchfork | K, F | D1 | 🔴 |
| AFS-F1 | Filter screening altcoin & korelasi BTC | K | — | ⚪ |
| AFS-F2 | Filter konfirmasi volume untuk breakout | K, F\* | — | ⚪ |
| AFS-F3 | Filter momentum (akselerasi/deselerasi) | K, F | — | ⚪ 🔴 |

### Akademi Crypto — Kalimasada (KMS) → [02](02-kalimasada-akademi-crypto.md)

| ID | Setup | Pasar | Status |
|---|---|---|---|
| KMS-01 | Wyckoff spring / UTAD + reclaim | K (BTC, ETH) | 🔴 |
| KMS-02 | Wyckoff breakout range + retest (JAC/LPS, LPSY) | K (BTC, ETH) | 🟡 |
| KMS-F1 | Filter VSA (volume vs ukuran candle) | K, F\* | ⚪ 🟡 |
| KMS-I1 | Alokasi portofolio spot 70/15/15 | K (spot) | 🟡 |
| KMS-I2 | Moon bag (jual 50% saat naik 2×) | K (spot) | 🟢 |
| KMS-I3 | Cicilan 5× masuk/keluar (mean reversion W1) | K (spot) | 🟡 |
| KMS-I4 | Fear & Greed Index | K (spot) | ⚪ 🟡 |

### Akademi Crypto — Analis live (LIVE) → [03](03-analis-live-akademi-crypto.md)

| ID | Setup | Pasar | Status |
|---|---|---|---|
| LIVE-F1 | Filter "grey area" (dekat resistance + stochastic sudah silang turun) | K, F | ⚪ 🟡 |
| LIVE-01 | Siklus halving Bitcoin (spot jangka panjang) | K (BTC) | 🟡 |
| LIVE-02 | Token baru / TGE (30% saat listing, 70% di *base*) | K (spot) | 🔴 |

### Saham → hanya prinsip umum → [04](04-ko-hengki-remora.md), [05](05-ko-andri-andre-hakim.md)

| ID | Aturan | Pasar | Status |
|---|---|---|---|
| HKI-F1 | "Naik bervolume, koreksi tanpa volume" | K, F\* | ⚪ 🟡 |
| HKI-F2 | Breakout pola harus bervolume | K, F\* | ⚪ 🟡 |
| HKI-01 | Ikuti tren sekunder & minor, keluar saat struktur patah | K, F | 🟡 |
| AND-G1 | Tentukan jenis posisi sejak awal; trading rugi → cut loss | K, F | 🟢 |
| AND-G2 | Hanya aset besar & likuid; trading hanya saat ada momentum | K, F | ⚪ |
| AND-02 | Trailing stop 5–10% | K (spot) | 🟡 |

### Forex → [06](06-mentor-forex.md)

| ID | Setup | Pasar | TF | Status |
|---|---|---|---|---|
| FXC-01 | FXcopet: tembus garis merah/aqua, range ≤15 pip | F (EURUSD) | M1 | 🔴 |
| PLN-01 | Pola N: impuls → koreksi sempit → tembus, stop order | F (XAUUSD) | H1 | 🟡 |
| ICH-01 | Ichimoku Hosoda: tren penuh (harga, Tenkan–Kijun, Kumo, Chikou) | F, K | D1 / H4 | 🟡 |
| ICH-02 | Ichimoku: retest Kijun | F, K | D1 / H4 | 🟡 |
| ICH-03 | Ichimoku: pullback ke Tenkan dalam tren kuat | F, K | D1 | 🟡 |
| ICH-04 | Target harga Hosoda (V, N, E, NT) untuk TP | F, K | semua | 🟢 |

### Filter waktu (opsional) → [07](07-filter-waktu.md)

| ID | Filter | Status |
|---|---|---|
| WKT-01 | Fase bulan (New Moon / Full Moon) | ⚪ 🟡 |
| WKT-02 | Tumpukan proyeksi Fibonacci waktu | ⚪ 🟡 |
| WKT-03 | Tanggal "Astronacci" (fase bulan ∩ Fibonacci waktu) | ⚪ 🟡 |
| WKT-04 | Mercury retrograde sebagai penanda waktu rawan | ⚪ 🟡 |
| WKT-05 | Angka waktu Hosoda (9, 17, 26, 33, 42, …) | ⚪ 🟡 |

---

## Rekomendasi urutan pengembangan

Ini **saran**, bukan aturan dari mentor. Alasannya: mulai dari setup yang paling jelas aturannya, paling sering diulang mentor, dan paling mudah diuji.

1. **Pasang aturan global dulu** ([00](00-aturan-global.md)): risiko per transaksi, SL wajib, tanpa average down. Semua mentor sepakat soal ini.
2. **Setup pertama yang layak dicoba** (aturannya paling lengkap):
   - **AFS-14** Ichimoku "semua garis" dan **ICH-01** Ichimoku Hosoda. Rumusnya baku, setting jelas (9/26/52).
   - **AFS-17** KST silang nol (D1).
   - **AFS-12** Pivot point dan **AFS-13** Keltner. Rumus baku, tinggal Q-22 dan Q-24.
   - **PLN-01** Pola N. Aturannya rinci, mentor punya data backtest sendiri (≈67% menang, RR 1:1,5–1:2).
   - **AFS-06** Stop hunt + BOS (SMC). Diulang berkali-kali sebagai "kombinasi paling ampuh", tetapi butuh jawaban Q-20 dulu.
3. **Setup 🔴** (harmonic, Elliott, pola grafik klasik, FXcopet) disimpan untuk tahap lanjut.
4. **Filter waktu Astronacci** baru dinyalakan **setelah** lolos uji statistik (lihat [07](07-filter-waktu.md#cara-menguji-sebelum-dipakai)).

## Pertanyaan yang paling menentukan

Sebelum menulis kode, sepuluh pertanyaan ini paling berpengaruh. Detailnya di [09](09-pertanyaan-untuk-anda.md):

- **Q-01** Risiko per transaksi: 1% dari apa?
- **Q-02** Pair dan koin apa saja yang boleh ditradingkan?
- **Q-03** Kripto: spot, futures, atau keduanya?
- **Q-04** Leverage maksimum.
- **Q-05** Rem darurat (batas rugi harian/mingguan)?
- **Q-06** Maksimal transaksi per hari dan posisi terbuka bersamaan.
- **Q-07** Perbandingan untung:rugi (RR) minimum.
- **Q-08** Boleh ambil untung bertahap dan geser SL ke titik impas?
- **Q-09** Masuk sebelum atau sesudah breakout?
- **Q-10** Angka persen dari kelas kripto: bagaimana menerapkannya di forex?
