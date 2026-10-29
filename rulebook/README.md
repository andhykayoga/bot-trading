# RULEBOOK STRATEGI BOT (forex & kripto)

Rulebook ini menerjemahkan isi kelas ke dalam **aturan yang bisa dikodekan**. Sumbernya adalah peta [`materi/PETA.md`](../materi/PETA.md) dan transkrip di [`materi/mentah/`](../materi/mentah/). Setiap aturan diberi tautan ke file dan **nomor baris** transkrip tempat mentor mengatakannya, jadi bisa dicek sendiri.

**Prinsip penyusunan:**

1. **Mesin utama** diambil dari kelas **kripto** (Akademi Crypto) dan **saham** (Remora, Andre Hakim), ditambah materi **forex** (Pola N dan Ichimoku Rafał).
2. Bot hanya untuk **forex dan kripto**: **EURUSD, XAUUSD, BTC, ETH** (Q-02). **Tahap sekarang hanya forex**; kripto ditambahkan nanti, di akun terpisah dengan batasnya sendiri (Q-49, Q-50). Bagian yang **hanya berlaku di saham** (broker summary, antrean bid–offer, SID/KSEI, ARA/ARB, PER/PBV, MSCI, dan lain-lain) **tidak dijadikan aturan**. Daftarnya ada di [08-tidak-dijadikan-aturan.md](08-tidak-dijadikan-aturan.md).
3. Konsep **Astronacci** (PETA bagian 9) masuk sebagai **filter waktu opsional**, default **mati**, di [07-filter-waktu.md](07-filter-waktu.md).
4. **Bagian yang ambigu tidak ditebak.** Kalau mentor tidak menyebut angka atau definisinya, aturan itu ditandai 🟡 dan diberi nomor pertanyaan **Q-xx** di [09-pertanyaan-untuk-anda.md](09-pertanyaan-untuk-anda.md). **Jawaban Anda** disimpan di [10-jawaban.md](10-jawaban.md) dan sudah diterapkan. Kalau saya harus mengisi detail teknis kecil sendiri, tempatnya ditandai "usulan saya" atau "terjemahan saya".
5. Angka "uji dulu" menjadi **parameter backtest** dengan nilai awal dari Anda, diuji hanya di sekitar nilai itu, dan varian dipilih dari data yang tidak dipakai saat menyusun strategi ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)).

---

## Daftar isi

| File | Isi |
|---|---|
| [00-aturan-global.md](00-aturan-global.md) | Aturan yang berlaku untuk **semua setup**: risiko per transaksi, stop loss, RR, batas transaksi & posisi, berita, rem darurat, leverage, cara menguji parameter. Juga **definisi bersama** (swing, zona, retest, candle, volume, dll.) dan daftar **perbedaan pendapat antar-mentor** beserta keputusan Anda. |
| [01-alvesting-akademi-crypto.md](01-alvesting-akademi-crypto.md) | **Alvesting (AFS)**, pengajar teknikal Akademi Crypto: Technical Research 5 tahap, scalping, Smart Money Concept, Fibonacci, Dow Theory, pola, indikator, order flow, filter. |
| [02-kalimasada-akademi-crypto.md](02-kalimasada-akademi-crypto.md) | **Kalimasada**: Wyckoff dan VSA. Modul investasi spot kripto ditunda. |
| [03-analis-live-akademi-crypto.md](03-analis-live-akademi-crypto.md) | **Analis live market update** Akademi Crypto: filter "grey area". Siklus halving dan token baru (TGE) ditunda. |
| [04-ko-hengki-remora.md](04-ko-hengki-remora.md) | **Ko Hengki (Remora)**: hanya prinsip harga & volume serta tren yang berlaku umum. Bandarmologi tidak dipakai. |
| [05-ko-andri-andre-hakim.md](05-ko-andri-andre-hakim.md) | **Ko Andri (Andre Hakim)**: prinsip manajemen posisi yang berlaku umum. Valuasi saham tidak dipakai. |
| [06-mentor-forex.md](06-mentor-forex.md) | Dua sumber forex: **Pola N** di emas (forex_2) dan **Ichimoku** Rafał Zuchowicz (forex_3). FXcopet tidak dipakai. |
| [07-filter-waktu.md](07-filter-waktu.md) | **Filter waktu opsional**: Astronacci (fase bulan, Fibonacci waktu, retrograde) dan angka waktu Hosoda (Ichimoku). |
| [08-tidak-dijadikan-aturan.md](08-tidak-dijadikan-aturan.md) | Materi yang sengaja **tidak** dijadikan aturan atau **ditunda**, beserta alasannya. Termasuk arsip FXcopet. |
| [09-pertanyaan-untuk-anda.md](09-pertanyaan-untuk-anda.md) | Semua pertanyaan, Q-01 – Q-51. Semuanya sudah dijawab. |
| [10-jawaban.md](10-jawaban.md) | **Jawaban Anda** untuk Q-01 – Q-51, dengan tautan ke tempat penerapannya. |

---

## Cara membaca

### Label status setiap setup

| Label | Artinya |
|---|---|
| 🟢 **Siap dikodekan** | Semua syarat dan angka sudah ada (dari mentor atau jawaban Anda). Angka yang masih harus diuji sudah punya nilai awal. |
| 🟡 **Butuh jawaban** | Logikanya jelas, tetapi ada hal yang belum ditentukan. Lihat nomor **Q-xx**. |
| 🔴 **Sulit diotomasi** | Sangat bergantung pada "mata" trader, atau butuh data yang tidak tersedia. Disimpan sebagai referensi. |
| ⏸ **Ditunda** | Tidak dipakai di bot versi pertama, sesuai jawaban Anda. |
| ⚪ **Filter / konteks** | Bukan sinyal masuk, melainkan penyaring: "boleh/tidak boleh trading sekarang". Ditulis bersama label siap/belumnya, misalnya ⚪ 🟢. |

### Label pasar

| Label | Artinya |
|---|---|
| **K** | Berlaku untuk kripto (BTC, ETH). |
| **F** | Berlaku untuk forex (EURUSD dan emas XAUUSD). |
| **K\*** / **F\*** | Berlaku, **tetapi angkanya disesuaikan**: angka persen dari kelas kripto diubah ke kelipatan ATR di forex ([D-09](00-aturan-global.md#d-09--angka-persen-kripto-di-forex)), dan volume forex memakai tick volume ([D-07](00-aturan-global.md#d-07--volume)). |

### Format setiap setup

Setiap setup ditulis dengan urutan yang sama, supaya mudah diubah menjadi kode:

- **Kartu ringkas**: sumber, pasar, timeframe, arah, label (scalping/trading), RR minimum, status.
- **Syarat**: semua harus terpenuhi, berurutan.
- **Entry**: kapan dan bagaimana order dipasang.
- **Stop loss (SL)** dan **take profit (TP)**.
- **Batal / jangan masuk jika**.
- **Belum jelas**: hal yang belum ditentukan, dengan nomor pertanyaannya.

Istilah teknis dijelaskan di [PETA bagian 10](../materi/PETA.md#10-daftar-istilah).

---

## Urutan kerja bot (alur keputusan)

Semua setup dipasang di dalam alur yang sama. Urutan ini diambil dari cara para mentor sendiri bekerja: tren → area → pola → pemicu → entry/exit ([AC_crypto_57 L1854–1873](../materi/mentah/AC_crypto_57.txt#L1854-L1873)).

```
1. Aturan global (00)        → boleh trading sekarang? (rem darurat G-15, jendela berita G-13,
                                instrumen G-09, batas transaksi & posisi G-08)
2. Filter pasar (⚪)          → "grey area", volume, VSA
3. Setup (🟢)                 → syarat terpenuhi? hitung entry, SL, TP; RR cukup? (G-03)
4. Ukuran posisi (G-01)       → dari jarak SL: 1% (scalping 0,5%), dipotong kalau melewati batas G-08/G-16
5. Filter waktu (07, opsional) → hanya dicatat sampai lolos uji
6. Kelola posisi              → TP/SL sesuai setup, tanpa intervensi (G-07); scalping ditutup setelah 3 jam
```

---

## Indeks semua setup

### Akademi Crypto — Alvesting (AFS) → [01](01-alvesting-akademi-crypto.md)

| ID | Setup | Pasar | TF | Status |
|---|---|---|---|---|
| AFS-01 | Technical Research 5 tahap, versi swing | K, F | D1 / H4 / M15 | 🟢 |
| AFS-02 | Technical Research 5 tahap, versi scalping | K, F | H1 / M15 / M5 | 🟢 |
| AFS-03 | Double/triple top-bottom + tembus neckline (scalping) | K, F | M15 | 🟢 |
| AFS-04 | Pantulan Fibonacci *golden pocket* 0,5–0,618 | K, F\* | D1 / W1 | 🟢 |
| AFS-05 | *Money magnet* EMA 13 & 21 | K, F | H1 / H4 / D1 (diuji) | 🟢 |
| AFS-06 | Stop hunt + break of structure (inti SMC) | K, F | H4 / M15 | 🟢 |
| AFS-07 | Change of character (CHoCH) + retest | K, F | H4 / M15 | 🟢 |
| AFS-08 | Revisit fair value gap setelah BOS | K, F | H4 / M15 | 🟢 |
| AFS-09 | Validasi tembus 3% Dow Theory (MA21) | K, F\* | D1 | 🟢 |
| AFS-10 | Pola ABCD | K, F | M15 / H1 | 🟢 |
| AFS-11 | Pola harmonic XABCD (Gartley, Bat, Crab, Butterfly, Shark) | K, F | H1–D1 | ⏸ |
| AFS-12 | Pivot point: entry di garis P (scalping di M5/M15, trading di H1) | K, F | H1 / M15 / M5 | 🟢 |
| AFS-13A | Keltner Channel (EMA20, ATR10, ×2), mode tren | K, F | H1 / H4 / D1 (diuji) | 🟢 |
| AFS-13B | Keltner Channel, mode pantulan | K, F | H1 / H4 / D1 (diuji) | 🟢 |
| AFS-14 | Ichimoku "di atas/bawah semua garis" | K, F | D1 | 🟢 |
| AFS-15 | Parabolic SAR titik ke-2 | K, F | H1 / H4 | 🟢 |
| AFS-16 | Donchian Channel (pantulan & silang tengah) | K, F | H1 / H4 / D1 (diuji) | 🟢 |
| AFS-17 | KST silang di garis nol | K, F | D1 | 🟢 |
| AFS-18 | Konfirmasi Chaikin Money Flow | K, F\* | H4 / D1 | 🟢 |
| AFS-19 | Pantulan POC (volume profile) | K, F\* | H1 / H4 / D1 | 🟢 |
| AFS-20 | Linear Regression Channel | K, F | H4 | 🟢 |
| AFS-21 | Renko reversal | K, F | D1 | 🟢 |
| AFS-22 | Order flow: divergensi delta, stacked imbalance, unfinished auction | K | — | ⏸ |
| AFS-23 | Pola grafik klasik selain double/triple top-bottom | K, F | H4 / D1 | ⏸ |
| AFS-24 | Elliott Wave (masuk di gelombang 2 & 4) | K, F | D1 | 🔴 |
| AFS-25 | Andrews Pitchfork | K, F | D1 | 🔴 |
| AFS-F1 | Filter screening altcoin & korelasi BTC | K | — | ⏸ |
| AFS-F2 | Filter konfirmasi volume untuk breakout | K, F\* | — | ⚪ 🟢 |
| AFS-F3 | Filter momentum (akselerasi/deselerasi) | K, F | — | ⚪ 🔴 |

### Akademi Crypto — Kalimasada (KMS) → [02](02-kalimasada-akademi-crypto.md)

| ID | Setup | Pasar | Status |
|---|---|---|---|
| KMS-01 | Wyckoff spring / UTAD + reclaim | K (BTC, ETH) | 🔴 |
| KMS-02 | Wyckoff breakout range + retest (JAC/LPS, LPSY), D1 | K, F\* | 🟢 |
| KMS-F1 | Filter VSA (volume vs ukuran candle) | K, F\* | ⚪ 🟢 |
| KMS-I1 – I4 | Modul investasi spot (alokasi, moon bag, cicilan, Fear & Greed) | K (spot) | ⏸ |

### Akademi Crypto — Analis live (LIVE) → [03](03-analis-live-akademi-crypto.md)

| ID | Setup | Pasar | Status |
|---|---|---|---|
| LIVE-F1 | Filter "grey area" (dekat resistance + stochastic sudah silang turun) | K, F | ⚪ 🟢 |
| LIVE-01 | Siklus halving Bitcoin (spot jangka panjang) | K (BTC) | ⏸ |
| LIVE-02 | Token baru / TGE (30% saat listing, 70% di *base*) | K (spot) | ⏸ |

### Saham → hanya prinsip umum → [04](04-ko-hengki-remora.md), [05](05-ko-andri-andre-hakim.md)

| ID | Aturan | Pasar | Status |
|---|---|---|---|
| HKI-F1 | "Naik bervolume, koreksi tanpa volume" | K, F\* | ⚪ 🟢 |
| HKI-F2 | Breakout pola harus bervolume | K, F\* | ⚪ 🟢 |
| HKI-01 | Ikuti tren sekunder (D1) & minor (H4), keluar saat struktur patah | K, F | 🟢 |
| AND-G1 | Tentukan jenis posisi sejak awal; trading rugi → cut loss | K, F | 🟢 |
| AND-G2 | Hanya aset besar & likuid; trading hanya saat ada momentum | K, F | ⚪ |
| AND-02 | Trailing stop 5–10% | K (spot) | ⏸ |

### Forex → [06](06-mentor-forex.md)

| ID | Setup | Pasar | TF | Status |
|---|---|---|---|---|
| PLN-01 | Pola N: impuls → koreksi sempit → tembus, stop order | F | H1 | 🟢 |
| ICH-01 | Ichimoku Hosoda: tren penuh (harga, Tenkan–Kijun, Kumo, Chikou) | F, K | W1 & D1 / H4 | 🟢 |
| ICH-02 | Ichimoku: retest Kijun | F, K | D1 / H4 | 🟢 |
| ICH-03 | Ichimoku: pullback ke Tenkan dalam tren kuat | F, K | D1 | 🟢 |
| ICH-04 | Target harga Hosoda (V, N, E, NT) untuk TP | F, K | semua | 🟢 |

FXcopet (FXC-01) tidak dipakai; arsipnya di [08 · bagian G](08-tidak-dijadikan-aturan.md#g-fxcopet-forex_1-tidak-dipakai).

### Filter waktu (opsional) → [07](07-filter-waktu.md)

| ID | Filter | Status |
|---|---|---|
| WKT-01 | Fase bulan (New Moon / Full Moon) | ⚪ 🟢 siap diuji |
| WKT-02 | Tumpukan proyeksi Fibonacci waktu | ⚪ 🟢 siap diuji |
| WKT-03 | Tanggal "Astronacci" (fase bulan ∩ Fibonacci waktu) | ⚪ 🟢 siap diuji |
| WKT-04 | Mercury retrograde sebagai penanda waktu rawan | ⚪ 🟢 siap diuji |
| WKT-05 | Angka waktu Hosoda (9, 17, 26, 33, 42, …) | ⚪ 🟢 siap diuji |

Semua filter waktu hanya **dicatat** sampai lolos uji (Q-38).

---

## Rekomendasi urutan pengembangan

Ini **saran**, bukan aturan dari mentor. Alasannya: mulai dari setup yang aturannya paling lengkap, paling sering diulang mentor, dan paling mudah diuji.

1. **Pasang aturan global dulu** ([00](00-aturan-global.md)): risiko 1% / 0,5%, SL swing ± 1 ATR, RR minimum, batas transaksi & posisi, rem darurat, jendela berita, dan definisi bersama D-01 – D-12. Ini dipakai semua setup.
2. **Setup pertama yang layak dicoba** (semuanya 🟢):
   - **ICH-01 – ICH-04** Ichimoku Rafał dan **AFS-14** Ichimoku Alvesting. Rumusnya baku, setting jelas (9/26/52), satu perhitungan Ichimoku dipakai bersama.
   - **PLN-01** Pola N. Aturannya rinci, mentor punya data backtest sendiri (≈67% menang, RR 1:1,5–1:2).
   - **AFS-06** Stop hunt + BOS. Diulang berkali-kali sebagai "kombinasi paling ampuh".
   - **AFS-04** Golden pocket, **AFS-09** Dow 3%, **AFS-17** KST — semuanya timeframe besar.
3. **Setup 🟢 lainnya** (AFS-01/02, AFS-03, AFS-05, AFS-12, AFS-13A/B, AFS-16, AFS-20, KMS-02) menyusul. Beberapa di antaranya punya banyak varian atau timeframe yang diuji, jadi jumlah percobaannya lebih besar (G-17).
4. **Setup 🔴 dan ⏸** disimpan untuk versi berikutnya.
5. **Filter waktu** hanya dicatat dulu, dan baru boleh mengubah keputusan **setelah** lolos uji statistik (lihat [07](07-filter-waktu.md#cara-menguji-sebelum-dipakai)).

## Pertanyaan yang masih terbuka

Tidak ada. Semua pertanyaan (Q-01 – Q-51) sudah dijawab di [10-jawaban.md](10-jawaban.md). Tidak ada setup yang berstatus 🟡.
