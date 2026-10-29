# 07 · FILTER WAKTU (opsional)

Halaman ini berisi dua kelompok konsep **waktu**:

1. **Astronacci** (Gema Goeyardi), dari [PETA bagian 9](../materi/PETA.md#9-astronacci-gema-goeyardi). Videonya tidak ada di folder Anda; isinya dirangkum PETA dari makalah Gema dkk., blog resmi, dan video YouTube resmi Astronacci (daftar sumber di [PETA 9.4](../materi/PETA.md#94-sumber)).
2. **Teori waktu Hosoda** (Ichimoku), dari kursus Rafał di [forex_3](../materi/mentah/forex_3.txt#L713-L1184). Ini "kerabat terdekat" Astronacci yang ada di materi Anda ([PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif)).

## Status: opsional, default MATI

- Semua filter di halaman ini **mati secara default**. Mesin utama bot tetap setup dari kelas kripto, saham, dan forex.
- Filter waktu **tidak pernah** menjadi sinyal masuk sendiri. Astronacci sendiri: teknikal menjawab "**di harga berapa**", waktu menjawab "**kapan**"; teknikal adalah "level 1", astrologi "level 2" ([PETA 9.1 butir 1](../materi/PETA.md#91-konsep-dasarnya)).
- **Efek pada bot (Q-38):**

  | Tahap | Fase bulan, Fibonacci waktu, tanggal Astronacci (WKT-01 – 03) | Angka waktu Hosoda (WKT-05) | Mercury retrograde (WKT-04) |
  |---|---|---|---|
  | **Sebelum lolos uji** | Hanya **dicatat** di log setiap transaksi; keputusan bot tidak berubah | Sama | Sama |
  | **Kalau lolos uji** | Di tanggal kandidat, hanya **setup pembalikan** yang boleh masuk | Dipakai untuk **waktu ambil untung** | Kalau terbukti setup breakout lebih sering gagal saat retrograde: **setup breakout dimatikan** selama retrograde (Q-41) |

- Dasar efek "kalau lolos" dari sumbernya sendiri: Astronacci memakai tanggal kandidat sebagai **titik balik** yang dikonfirmasi teknikal; Rafał mengambil untung saat **target waktu bertepatan dengan target harga**.

### Setup mana yang dihitung "pembalikan" dan "breakout"

*Usulan saya; hanya dipakai kalau filter lolos uji. Silakan diubah.*

| Kelompok | Setup |
|---|---|
| **Pembalikan** | AFS-03 (double/triple top-bottom), AFS-06 (stop hunt), AFS-07 (CHoCH), AFS-09 (pembalikan Dow), AFS-10 (ABCD), AFS-13B (pantulan Keltner), AFS-15 (PSAR), AFS-16 mode pantulan, AFS-17 (KST), AFS-18 versi divergensi, AFS-21 (Renko reversal) |
| **Breakout** | AFS-03 versi konfirmasi (tembus neckline), AFS-09, AFS-18 versi breakout, AFS-20 mode breakout, KMS-02, HKI-01 *buy on breakout*, PLN-01 |

Filter fase bulan dan Fibonacci waktu hanya berlaku untuk setup dengan **entry di H4 ke atas** (Q-39), karena jendela harian kurang berarti untuk timeframe kecil.

### Seberapa kuat buktinya (dari PETA 9.2)

| Metode | Peluang suatu hari menjadi titik balik | Data |
|---|---|---|
| Tanpa metode apa pun | ±8–9% | IHSG & emas 2008–2017 |
| Fibonacci waktu saja | ±42–43% | sama |
| Astronacci + fase bulan | 64% IHSG (**7 dari 11**), 54% emas (**7 dari 13**) | sama |

Catatan dari PETA: sampelnya sangat kecil, diuji pada data yang sama dengan data yang dipakai merumuskan metodenya, penulisnya pemilik metode, beberapa angka di tabelnya tidak konsisten, klaim "70–80%" di video/blog tanpa data, dan tidak ditemukan uji independen. Jadi ini **hipotesis yang harus diuji**, bukan kepastian ([PETA 9.2](../materi/PETA.md#92-seberapa-kuat-buktinya)).

---

## Definisi bersama: titik balik

Dipakai oleh WKT-02, WKT-03, WKT-05, dan untuk mengukur hasil uji.

- Bot memakai **swing fractal 2–2** ([D-01](00-aturan-global.md#d-01--swing-high-dan-swing-low)), seperti semua swing lain di rulebook (Q-12, Q-40): puncak = *high* lebih tinggi dari 2 candle sebelumnya dan 2 candle sesudahnya; lembah sebaliknya.
- Titik balik baru **pasti** setelah 2 candle sesudahnya selesai.
- Makalah Gema dkk. memakai versi yang sedikit lebih ketat: *high* naik **dua kali berturut-turut** sebelum puncak, lalu turun dua kali berturut-turut sesudahnya ([PETA 9.1 butir 6](../materi/PETA.md#91-konsep-dasarnya); makalah hlm. 1586). Untuk perbandingan dengan angka di makalah, titik balik versi makalah juga bisa dihitung dan dicatat.

---

## WKT-01 · Fase bulan (New Moon / Full Moon)

| | |
|---|---|
| Sumber | [PETA 9.1 butir 2](../materi/PETA.md#91-konsep-dasarnya) |
| Pasar | Paling banyak diriset di IHSG dan **emas**; di saham AS hasilnya "fifty-fifty". Bot menguji **XAUUSD, EURUSD, BTC, ETH** (Q-39) |
| Status | ⚪ 🟢 (siap diuji) |

**Aturan:**

1. Hitung tanggal **New Moon** (Matahari–Bulan berimpit 0°) dan **Full Moon** (berseberangan 180°).
2. Hari dalam jendela **±1 hari** atau **±2 hari** dari tanggal itu = **kandidat titik balik**: bisa puncak, bisa lembah. Kedua jendela **diuji** (Q-39).
3. Kandidat ini **wajib dikonfirmasi teknikal**: support/resistance, Fibonacci, gap, EMA21. Di bot, konfirmasinya adalah setup pembalikan yang memberi sinyal di tanggal itu.
4. Hanya untuk setup dengan **entry di H4 ke atas** (Q-39).

Tanggal fase bulan bisa dihitung otomatis dengan pustaka astronomi Python (misalnya `skyfield` atau `ephem`), tanpa situs pihak ketiga ([PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif)).

---

## WKT-02 · Tumpukan proyeksi Fibonacci waktu

| | |
|---|---|
| Sumber | [PETA 9.1 butir 4](../materi/PETA.md#91-konsep-dasarnya); makalah Gema dkk. 2021 ([PETA 9.4](../materi/PETA.md#94-sumber)) |
| Status | ⚪ 🟢 (siap diuji) |

**Aturan (Q-40):**

1. **Titik balik** dari **D1**, fractal 2–2. Pakai **semua** titik balik dalam **233 candle D1 terakhir** (233 = angka Fibonacci terbesar yang dipakai).
2. **Proyeksi ke depan.** Makalah Gema dkk. (versi TURCOMAT 12(4), hlm. 1583–1595) **tidak menjelaskan** cara menghitung proyeksinya; ia hanya mengelompokkan hari menjadi "proyeksi kurang dari 3" dan "lebih dari 3". Jadi dua cara diuji:
   - **(a)** Dari **tiap** titik balik, hitung maju **13, 21, 34, 55, 89, 144, 233** candle.
   - **(b)** Untuk tiap pasangan titik balik sejenis yang berurutan (puncak ke puncak, lembah ke lembah; [PETA 9.1 butir 4](../materi/PETA.md#91-konsep-dasarnya)), ukur jaraknya, lalu proyeksikan dari titik yang lebih baru dengan kelipatan **0,382; 0,618; 1; 1,618; 2,618** × jarak itu.
3. **Toleransi:** proyeksi yang jatuh **±1 hari** dari suatu tanggal dihitung bertumpuk di tanggal itu.
4. **Kandidat titik balik kuat** = tanggal dengan **≥3 proyeksi** bertumpuk (PETA). Makalah menulis "lebih dari 3" untuk kelompok ini dan "kurang dari 3" untuk kelompok lain, jadi angka 3 sendiri tidak tegas → diuji **≥3** dan **≥4**.

---

## WKT-03 · Tanggal "Astronacci"

| | |
|---|---|
| Sumber | [PETA 9.1 butir 5](../materi/PETA.md#91-konsep-dasarnya) |
| Status | ⚪ 🟢 (siap diuji) |

**Aturan:** tanggal "Astronacci" = tanggal di jendela fase bulan (WKT-01) yang **juga** jatuh di tumpukan proyeksi Fibonacci waktu (WKT-02). Ini kombinasi yang menghasilkan angka 64%/54% di makalah Gema. Semua pilihan uji WKT-01 dan WKT-02 ikut berlaku.

---

## WKT-04 · Mercury retrograde sebagai penanda waktu rawan

| | |
|---|---|
| Sumber | [PETA 9.1 butir 3](../materi/PETA.md#91-konsep-dasarnya) |
| Status | ⚪ 🟢 (siap diuji) |

**Aturan:** Merkurius *retrograde* (±24 hari, 3–4 kali setahun) dipakai Astronacci sebagai **penanda waktu** pasar yang rawan **sideways** dan **false breakout**. Menurut Astronacci sendiri ini **bukan** sinyal beli/jual. Tanggal retrograde bisa dihitung dengan pustaka astronomi.

**Cara uji dan efeknya (Q-41):**

1. Sebelum lolos uji: hanya **dicatat** apakah sebuah transaksi dibuka saat retrograde.
2. Bandingkan persentase gagal (kena SL) **setup breakout** (daftar di atas) saat retrograde dan di luar retrograde, di data pemilihan ([G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian)).
3. Kalau terbukti lebih sering gagal saat retrograde: **setup breakout dimatikan** selama retrograde. Kalau tidak: tetap hanya dicatat.

---

## Faktor astro lain (tidak dijadikan aturan)

PETA juga menyebut **deklinasi bulan**, **aspek planet** (0° konjungsi, 60° sextile, 90° square, 120° trine, 180° oposisi), **ingress** (planet pindah zodiak), dan siklus "**Sun in Capricorn**" untuk emas ([PETA 9.1 butir 3](../materi/PETA.md#91-konsep-dasarnya)). Tidak ada rincian cara pakainya (jendela waktu, arah, konfirmasi), jadi **tidak dijadikan aturan**. Kalau WKT-01 sampai WKT-03 lolos uji, faktor-faktor ini bisa diuji dengan cara yang sama.

## Teknik harga Astronacci (sudah tercakup di setup lain)

PETA 9.1 butir 7 menyebut teknik harga yang sering diajarkan Astronacci: Fibonacci retracement & ekstensi, *price action* (engulfing, pin bar, hammer, shooting star), koreksi ABC di emas H4 (masuk di akhir gelombang C), dan SL di luar area retracement. Semuanya sudah tercakup di [AFS-04](01-alvesting-akademi-crypto.md#afs-04--pantulan-golden-pocket-fibonacci), [AFS-01](01-alvesting-akademi-crypto.md#afs-01--technical-research-5-tahap-versi-swing), dan [AFS-24](01-alvesting-akademi-crypto.md#afs-24--elliott-wave).

Satu prinsip yang berguna untuk bot: **setiap pasar punya rasio Fibonacci "favorit" sendiri** (misalnya 1,618 vs 2,618) yang harus dicari lewat **backtest ±5 tahun** ([PETA 9.1 butir 7](../materi/PETA.md#91-konsep-dasarnya)). Di rulebook ini, pemilihan target AFS-04 sudah diatur oleh RR minimum (Q-08); prinsip ini dicatat untuk versi berikutnya.

---

## WKT-05 · Angka waktu Hosoda (Ichimoku)

| | |
|---|---|
| Sumber | [forex_3 L713–L1184](../materi/mentah/forex_3.txt#L713-L1184), dipakai di praktik live [forex_3 L151–L300](../materi/mentah/forex_3.txt#L151-L300) |
| Pasar | Semua (contoh: DAX M5, minyak, AUD/CHF, USD/JPY, USD/TRY) |
| Status | ⚪ 🟢 (siap diuji) |

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

1. Beri nomor **1** pada candle awal tren atau titik balik. Di bot: swing D-01 di timeframe entry (Q-12).
2. Waspadai **reaksi atau pembalikan** saat hitungan mencapai 26, 33, 42, 51, 65, 76, dan seterusnya. Berlaku di timeframe apa pun ([forex_3 L895–L955](../materi/mentah/forex_3.txt#L895-L955)).
3. **Keseimbangan waktu:** gerakan berikutnya sering sama panjang waktunya dengan gerakan sebelumnya (contoh 26 = 26 = 26; 13 = 13) ([forex_3 L1013–L1095](../materi/mentah/forex_3.txt#L1013-L1095)). Di praktik: turun 25 candle + koreksi 18 candle = 42 (angka Hosoda), lalu proyeksi waktu CD = AB, = BC, atau = ABC ([forex_3 L151–L300](../materi/mentah/forex_3.txt#L151-L300)).
4. **Gabungkan dengan target harga** ([ICH-04](06-mentor-forex.md#ich-04--target-harga-hosoda-untuk-tp)). Ambil untung terutama saat target waktu bertepatan dengan target harga ([forex_3 L3194–L3250](../materi/mentah/forex_3.txt#L3194-L3250), [forex_3 L611–L660](../materi/mentah/forex_3.txt#L611-L660)).

Rafał juga menyarankan memeriksa apakah pasar pilihan Anda bereaksi pada angka-angka ini, atau pada angka lain ([forex_3 L1170–L1184](../materi/mentah/forex_3.txt#L1170-L1184)). Jadi angka ini pun harus diuji per instrumen.

**Efek kalau lolos uji (Q-38: waktu ambil untung):** posisi ICH-01 – ICH-03 **ditutup** saat hitungan candle sejak titik awal mencapai angka Hosoda **dan** harga berada di zona salah satu target ICH-04 (target ± 0,5 × ATR(14)), walaupun TP-nya belum tersentuh. *(Terjemahan saya dari "ambil untung saat target waktu bertepatan dengan target harga".)*

---

## Cara menguji sebelum dipakai

Diambil dari [PETA 9.3](../materi/PETA.md#93-cara-memakainya-di-bot-bisa-diuji-secara-objektif), dirinci menjadi langkah:

1. **Hitung tanggal-tanggal kandidat** untuk periode historis: fase bulan dan retrograde (pustaka astronomi), tumpukan Fibonacci waktu (WKT-02), dan hitungan Hosoda (WKT-05).
2. **Tandai titik balik sebenarnya** di data harga dengan definisi di atas.
3. **Bandingkan:** apakah tanggal kandidat **lebih sering** menjadi titik balik dibanding hari biasa (patokan dasar ±8–9% di makalah Gema)?
4. **Uji di data yang berbeda** dari data yang dipakai untuk mengatur parameter (supaya tidak mengulang kelemahan makalah Gema), dan pastikan jumlah kejadiannya cukup banyak. Pembagian datanya sama dengan [G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian) (Q-42): pilihan uji (jendela ±1/±2 hari, cara a/b, ambang ≥3/≥4) ditentukan di data penyusunan dan pemilihan, lalu dikunci dan dicek **sekali** di data uji akhir.
5. **Kalau di data uji akhir tidak lebih baik dari acak → buang.** Kalau lebih baik → boleh dinyalakan dengan efek di tabel atas (Q-38). *(Memakai data uji akhir untuk filter waktu adalah penerapan saya atas Q-42.)*
6. Instrumen yang diuji: **XAUUSD, EURUSD, BTC, ETH** (Q-39).
