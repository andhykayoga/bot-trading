# 07 · FILTER WAKTU (opsional)

Halaman ini berisi dua kelompok konsep **waktu**:

1. **Astronacci** (Gema Goeyardi), dari [PETA bagian 9](../materi/PETA.md#9-astronacci-gema-goeyardi). Videonya tidak ada di folder Anda; isinya dirangkum PETA dari makalah Gema dkk., blog resmi, dan video YouTube resmi Astronacci (daftar sumber di [PETA 9.4](../materi/PETA.md#94-sumber)).
2. **Teori waktu Hosoda** (Ichimoku), dari kursus Rafał di [forex_3](../materi/mentah/forex_3.txt#L713-L1184). Ini "kerabat terdekat" Astronacci yang ada di materi Anda ([PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif)).

## Status: opsional, default MATI

- Semua filter di halaman ini **mati secara default**. Mesin utama bot tetap setup dari kelas kripto, saham, dan forex.
- Filter hanya boleh dinyalakan **setelah lolos uji** (lihat [cara menguji](#cara-menguji-sebelum-dipakai)).
- Filter waktu **tidak pernah** menjadi sinyal masuk sendiri. Astronacci sendiri: teknikal menjawab "**di harga berapa**", waktu menjawab "**kapan**"; teknikal adalah "level 1", astrologi "level 2" ([PETA 9.1 butir 1](../materi/PETA.md#91-konsep-dasarnya)).
- Bagaimana filter memengaruhi keputusan bot (memblokir, mengizinkan, atau hanya mencatat) **belum ditentukan** → **Q-38**.

### Seberapa kuat buktinya (dari PETA 9.2)

| Metode | Peluang suatu hari menjadi titik balik | Data |
|---|---|---|
| Tanpa metode apa pun | ±8–9% | IHSG & emas 2008–2017 |
| Fibonacci waktu saja | ±42–43% | sama |
| Astronacci + fase bulan | 64% IHSG (**7 dari 11**), 54% emas (**7 dari 13**) | sama |

Catatan dari PETA: sampelnya sangat kecil, diuji pada data yang sama dengan data yang dipakai merumuskan metodenya, penulisnya pemilik metode, beberapa angka di tabelnya tidak konsisten, klaim "70–80%" di video/blog tanpa data, dan tidak ditemukan uji independen. Jadi ini **hipotesis yang harus diuji**, bukan kepastian ([PETA 9.2](../materi/PETA.md#92-seberapa-kuat-buktinya)).

---

## Definisi bersama: titik balik (swing) 5 candle

Dipakai oleh WKT-02, WKT-03, dan untuk mengukur hasil uji.

- **Puncak** = candle yang *high*-nya lebih tinggi daripada 2 candle sebelumnya **dan** 2 candle sesudahnya.
- **Lembah** = candle yang *low*-nya lebih rendah daripada 2 candle sebelumnya **dan** 2 candle sesudahnya.

Ini definisi dari makalah Gema dkk. dan mirip indikator *fractal* ([PETA 9.1 butir 6](../materi/PETA.md#91-konsep-dasarnya)). Konsekuensinya: titik balik baru **pasti** setelah 2 candle sesudahnya selesai.

---

## WKT-01 · Fase bulan (New Moon / Full Moon)

| | |
|---|---|
| Sumber | [PETA 9.1 butir 2](../materi/PETA.md#91-konsep-dasarnya) |
| Pasar | Paling banyak diriset di IHSG dan **emas**; di saham AS hasilnya "fifty-fifty" |
| Status | ⚪ 🟡 |

**Aturan:**

1. Hitung tanggal **New Moon** (Matahari–Bulan berimpit 0°) dan **Full Moon** (berseberangan 180°).
2. Hari dalam jendela **±1–2 hari** dari tanggal itu = **kandidat titik balik**: bisa puncak, bisa lembah.
3. Kandidat ini **wajib dikonfirmasi teknikal**: support/resistance, Fibonacci, gap, EMA21.

Tanggal fase bulan bisa dihitung otomatis dengan pustaka astronomi Python (misalnya `skyfield` atau `ephem`), tanpa situs pihak ketiga ([PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif)).

**Belum jelas** → **Q-39**: jendela ±1 atau ±2 hari? Instrumen mana yang diuji? Berlaku untuk setup timeframe berapa?

---

## WKT-02 · Tumpukan proyeksi Fibonacci waktu

| | |
|---|---|
| Sumber | [PETA 9.1 butir 4](../materi/PETA.md#91-konsep-dasarnya) |
| Status | ⚪ 🟡 |

**Aturan:**

1. Ukur **jarak waktu** antar-titik balik: puncak ke puncak, lembah ke lembah.
2. Proyeksikan ke depan dengan angka Fibonacci: **13, 21, 34, 55, 89, 144, 233, …** (dalam jumlah candle/hari).
3. Tanggal tempat **≥3 proyeksi bertumpuk** = kandidat titik balik yang kuat.

**Belum jelas** → **Q-40**:

- Titik balik yang dipakai diambil dari timeframe apa (D1?) dan berapa titik ke belakang?
- Seberapa dekat proyeksi harus jatuh supaya dihitung "bertumpuk" (hari yang sama, atau ±1 hari)?
- Angka Fibonacci dipakai sebagai kelipatan jarak antar-titik, atau sebagai jumlah hari langsung dari titik balik? PETA menyebut "proyeksikan ke depan dengan angka Fibonacci" tanpa merinci.

---

## WKT-03 · Tanggal "Astronacci"

| | |
|---|---|
| Sumber | [PETA 9.1 butir 5](../materi/PETA.md#91-konsep-dasarnya) |
| Status | ⚪ 🟡 |

**Aturan:** tanggal "Astronacci" = tanggal peristiwa astro (terutama fase bulan, WKT-01) yang **juga** jatuh di tumpukan proyeksi Fibonacci waktu (WKT-02). Ini kombinasi yang menghasilkan angka 64%/54% di makalah Gema.

**Belum jelas:** sama dengan WKT-01 dan WKT-02 (Q-39, Q-40).

---

## WKT-04 · Mercury retrograde sebagai penanda waktu rawan

| | |
|---|---|
| Sumber | [PETA 9.1 butir 3](../materi/PETA.md#91-konsep-dasarnya) |
| Status | ⚪ 🟡 |

**Aturan:** Merkurius *retrograde* (±24 hari, 3–4 kali setahun) dipakai Astronacci sebagai **penanda waktu** pasar yang rawan **sideways** dan **false breakout**. Menurut Astronacci sendiri ini **bukan** sinyal beli/jual.

Tanggal retrograde juga bisa dihitung dengan pustaka astronomi.

**Belum jelas** → **Q-41**: saat retrograde, apa yang dilakukan bot? (contoh pilihan: setup breakout dimatikan, ukuran posisi dikecilkan, atau hanya dicatat).

---

## Faktor astro lain (tidak dijadikan aturan)

PETA juga menyebut **deklinasi bulan**, **aspek planet** (0° konjungsi, 60° sextile, 90° square, 120° trine, 180° oposisi), **ingress** (planet pindah zodiak), dan siklus "**Sun in Capricorn**" untuk emas ([PETA 9.1 butir 3](../materi/PETA.md#91-konsep-dasarnya)). Tidak ada rincian cara pakainya (jendela waktu, arah, konfirmasi), jadi **tidak dijadikan aturan**. Kalau WKT-01 sampai WKT-03 lolos uji, faktor-faktor ini bisa diuji dengan cara yang sama.

## Teknik harga Astronacci (sudah tercakup di setup lain)

PETA 9.1 butir 7 menyebut teknik harga yang sering diajarkan Astronacci: Fibonacci retracement & ekstensi, *price action* (engulfing, pin bar, hammer, shooting star), koreksi ABC di emas H4 (masuk di akhir gelombang C), dan SL di luar area retracement. Semuanya sudah tercakup di [AFS-04](01-alvesting-akademi-crypto.md#afs-04--pantulan-golden-pocket-fibonacci), [AFS-01](01-alvesting-akademi-crypto.md#afs-01--technical-research-5-tahap-versi-swing), dan [AFS-24](01-alvesting-akademi-crypto.md#afs-24--elliott-wave).

Satu prinsip yang berguna untuk bot: **setiap pasar punya rasio Fibonacci "favorit" sendiri** (misalnya 1,618 vs 2,618) yang harus dicari lewat **backtest ±5 tahun** ([PETA 9.1 butir 7](../materi/PETA.md#91-konsep-dasarnya)). Ini bisa dipakai saat mengatur parameter AFS-04 per instrumen.

---

## WKT-05 · Angka waktu Hosoda (Ichimoku)

| | |
|---|---|
| Sumber | [forex_3 L713–L1184](../materi/mentah/forex_3.txt#L713-L1184), dipakai di praktik live [forex_3 L151–L300](../materi/mentah/forex_3.txt#L151-L300) |
| Pasar | Semua (contoh: DAX M5, minyak, AUD/CHF, USD/JPY, USD/TRY) |
| Status | ⚪ 🟡 |

**Angka dasar:** **9, 17, 26**. Angka turunan dibentuk dengan menjumlahkan angka dasar lalu **mengurangi candle yang dihitung dua kali** (candle puncak/lembah ikut dihitung di dua gerakan) ([forex_3 L733–L800](../materi/mentah/forex_3.txt#L733-L800)):

| Angka | Asal (menurut Rafał) |
|---|---|
| 17 | 9 + 9 − 1 |
| 26 | 17 + 9 |
| 33 | 17 + 17 − 1 |
| 42 | 26 + 17 − 1 |
| 51 | 26 + 26 − 1 |
| 65 | 33 + 33 − 1 |
| **76** | 3 × 26 − 2 — **sering menjadi titik balik total** |
| 83 | 42 + 42 − 1 (Rafał mengucapkan "eighty two", tetapi hitungannya 83) |
| 97 | 3 × 33 − 2 |
| 101 | 51 + 51 − 1 |
| 129 | 65 + 65 − 1 |

Sumber tabel: [forex_3 L800–L875](../materi/mentah/forex_3.txt#L800-L875).

**Cara pakai menurut Rafał:**

1. Beri nomor **1** pada candle awal tren atau titik balik.
2. Waspadai **reaksi atau pembalikan** saat hitungan mencapai 26, 33, 42, 51, 65, 76, dan seterusnya. Berlaku di timeframe apa pun ([forex_3 L895–L955](../materi/mentah/forex_3.txt#L895-L955)).
3. **Keseimbangan waktu:** gerakan berikutnya sering sama panjang waktunya dengan gerakan sebelumnya (contoh 26 = 26 = 26; 13 = 13) ([forex_3 L1013–L1095](../materi/mentah/forex_3.txt#L1013-L1095)). Di praktik: turun 25 candle + koreksi 18 candle = 42 (angka Hosoda), lalu proyeksi waktu CD = AB, = BC, atau = ABC ([forex_3 L151–L300](../materi/mentah/forex_3.txt#L151-L300)).
4. **Gabungkan dengan target harga** ([ICH-04](06-mentor-forex.md#ich-04--target-harga-hosoda-untuk-tp)). Ambil untung terutama saat target waktu bertepatan dengan target harga ([forex_3 L3194–L3250](../materi/mentah/forex_3.txt#L3194-L3250), [forex_3 L611–L660](../materi/mentah/forex_3.txt#L611-L660)).

Rafał juga menyarankan memeriksa apakah pasar pilihan Anda bereaksi pada angka-angka ini, atau pada angka lain ([forex_3 L1170–L1184](../materi/mentah/forex_3.txt#L1170-L1184)). Jadi angka ini pun harus diuji per instrumen.

**Belum jelas:** dipakai untuk apa di bot (filter masuk, pengatur waktu TP, atau hanya catatan) → **Q-38**. Titik awal hitungan → **Q-12**.

---

## Cara menguji sebelum dipakai

Diambil dari [PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif), dirinci menjadi langkah:

1. **Hitung tanggal-tanggal kandidat** untuk periode historis: fase bulan dan retrograde (pustaka astronomi), tumpukan Fibonacci waktu (WKT-02), dan hitungan Hosoda (WKT-05).
2. **Tandai titik balik sebenarnya** di data harga dengan definisi 5 candle di atas.
3. **Bandingkan:** apakah tanggal kandidat **lebih sering** menjadi titik balik dibanding hari biasa (patokan dasar ±8–9% di makalah Gema)?
4. **Uji di data yang berbeda** dari data yang dipakai untuk mengatur parameter (supaya tidak mengulang kelemahan makalah Gema), dan pastikan jumlah kejadiannya cukup banyak.
5. **Kalau tidak lebih baik dari acak → buang.** Kalau lebih baik → boleh dinyalakan sebagai filter tambahan sesuai jawaban Q-38.
6. Instrumen yang disarankan PETA untuk diuji: **EURUSD** dan **XAUUSD**; tambahkan instrumen kripto jika bot juga trading kripto.
