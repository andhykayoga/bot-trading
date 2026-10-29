# 00 · ATURAN GLOBAL (berlaku untuk semua setup)

Aturan di halaman ini **mengalahkan** aturan setup. Kalau sebuah setup memberi sinyal tetapi melanggar aturan global, sinyal itu **dibatalkan**.

Isinya berasal dari dua sumber: **kata mentor** (dengan tautan ke transkrip) dan **jawaban Anda** di [10-jawaban.md](10-jawaban.md) (ditandai "Q-xx"). Kalau mentor berbeda pendapat, keputusannya dicatat di [bagian akhir](#perbedaan-pendapat-antar-mentor).

## Daftar isi

| Bagian | Isi |
|---|---|
| [G-01](#g-01--risiko-per-transaksi-maksimal-1) – [G-06](#g-06--dilarang-revenge-trading) | Risiko 1% (scalping 0,5%), SL wajib, RR minimum, tanpa average down, tanpa hedging, tanpa revenge trading |
| [G-07](#g-07--rencana-tidak-diubah-di-tengah-jalan) – [G-13](#g-13--berita-besar) | Set and forget, batas frekuensi & posisi, instrumen, timeframe, indikator, exit, berita |
| [G-14](#g-14--backtest-dulu-dan-nilai-hasilnya-dengan-data) – [G-17](#g-17--parameter-uji-dan-pemilihan-varian) | Backtest, rem darurat, jenis akun & leverage, cara menguji parameter & memilih varian |
| [Definisi bersama (D-01 – D-11)](#definisi-bersama) | Swing, struktur, ATR, zona, retest, candle, volume, osilator, angka persen di forex, konvensi eksekusi, label scalping |
| [Perbedaan pendapat antar-mentor](#perbedaan-pendapat-antar-mentor) | Daftar perbedaan dan keputusan Anda |

---

## G-01 · Risiko per transaksi maksimal 1%

**Aturan:**

1. Kerugian maksimal **satu** transaksi, jika kena stop loss, adalah **1% dari saldo akun bot**. Akun bot hanya berisi uang trading (Q-01).
2. Posisi berlabel **scalping** ([D-11](#d-11--label-posisi-scalping-atau-trading)): **0,5%**. Ini batas bawah Alvesting, karena scalping lebih sering bertransaksi dan biayanya lebih besar (Q-01).
3. Ukuran posisi (lot/kontrak) **dihitung dari** jarak stop loss, bukan sebaliknya:

   ```
   ukuran_posisi = (saldo × risiko%) ÷ (jarak entry–SL × nilai per unit)
   ```

4. Kalau ukuran itu melanggar batas [G-08](#g-08--jangan-overtrading) (risiko terbuka total 3%) atau [G-16](#g-16--jenis-akun-dan-leverage) (spot 1×, forex total 10× saldo), ukurannya **dipotong** sampai muat. Risiko boleh lebih kecil dari 1%, tidak boleh lebih besar. Kalau setelah dipotong ukurannya di bawah ukuran minimum broker/exchange, posisi **tidak dibuka**. *(Cara menangani batas ini adalah usulan saya, bukan kata mentor.)*

| Mentor | Yang dikatakan | Sumber |
|---|---|---|
| Kalimasada | Risk per trade idealnya 1% dari total portofolio: "100 kesempatan untuk salah". | [AC_crypto_62 L1599–L1648](../materi/mentah/AC_crypto_62.txt#L1599-L1648) |
| Kalimasada | 1% **dari porsi trading** (30% portofolio), bukan dari total. | [AC_crypto_6 L96–L115](../materi/mentah/AC_crypto_6.txt#L96-L115) |
| Alvesting | Scalping: 0,5%–1%. Maksimal 2%, jangan sampai 10%. | [AC_crypto_58 L3055–L3104](../materi/mentah/AC_crypto_58.txt#L3055-L3104), [AC_crypto_62 L3669–L3688](../materi/mentah/AC_crypto_62.txt#L3669-L3688) |
| Alvesting | Harmonic: 0,5%–1%. | [AC_crypto_60 L2613–L2632](../materi/mentah/AC_crypto_60.txt#L2613-L2632) |
| Mentor forex_2 | "Haram hukumnya jika risikonya di atas 1%." Lot dihitung dengan kalkulator risiko. | [forex_2 L1040–L1089](../materi/mentah/forex_2.txt#L1040-L1089) |

---

## G-02 · Stop loss wajib, di titik "analisa saya salah"

**Aturan:**

1. **Setiap** posisi punya stop loss sejak dibuka.
2. Letak dasar: long **di bawah** swing low / support / area beli; short **di atas** swing high / resistance / area jual. Kalau setup menyebut level lain (Kumo, Kijun, garis P, pita channel, dan sejenisnya), level itu yang dipakai.
3. SL diberi **jarak tambahan** dari level tersebut, karena harga sering menembus sebentar untuk menyapu stop loss (*liquidity grab*). Besarnya **1 × ATR(14)** dari timeframe tempat level itu berada (Q-11):

   ```
   long : SL = level − 1 × ATR(14)
   short: SL = level + 1 × ATR(14)
   ```

   Pembanding di backtest: **0,5×** dan **1,5×** ATR ([G-17](#g-17--parameter-uji-dan-pemilihan-varian)). Swing dikenali dengan [D-01](#d-01--swing-high-dan-swing-low); ATR dijelaskan di [D-03](#d-03--atr).
4. **Pengecualian:** [PLN-01](06-mentor-forex.md#pln-01--pola-n-impuls--koreksi-sempit--tembus) memakai SL tepat di ujung wick koreksi, sesuai mentornya dan Q-34.
5. Kalau SL ini membuat RR di bawah minimum (G-03), **jangan masuk**. SL **tidak boleh diperkecil** supaya RR terlihat bagus (Q-11).
6. SL **tidak boleh dimatikan, dijauhkan, atau "ditunggu dulu siapa tahu mantul"**.

| Sumber | Isi |
|---|---|
| [AC_crypto_59 L2740–L2819](../materi/mentah/AC_crypto_59.txt#L2740-L2819) | SL long di bawah swing low, SL short di atas swing high. |
| [AC_crypto_59 L2819–L2859](../materi/mentah/AC_crypto_59.txt#L2819-L2859) | Jarak SL pakai ATR. Kripto: ATR dalam % (contoh BTC 3,36%). Forex: satuan harga. |
| [AC_crypto_33 L1090–L1129](../materi/mentah/AC_crypto_33.txt#L1090-L1129) | Jarak SL di bawah support diukur pakai ATR karena sering ada *liquidity grab*. |
| [AC_crypto_62 L1669–L1708](../materi/mentah/AC_crypto_62.txt#L1669-L1708) | Contoh kesalahan: mematikan SL lalu menambah posisi, akhirnya habis. |

---

## G-03 · RR minimum 1:1,5

**Aturan:**

1. Setiap setup memakai RR minimum dari mentornya sendiri, tetapi **tidak pernah di bawah 1:1,5** (Q-07). RR minimum tiap setup tertulis di kartunya.
2. **Setup yang mentornya tidak menyebut target:** TP = entry ± RR × jarak entry–SL, dengan

   | Timeframe entry | RR |
   |---|---|
   | H1 ke bawah | **1:2** |
   | H4 ke atas | **1:3** |

   Patokannya Alvesting: minimal 1:2 untuk jangka pendek, lebih dari 1:3 untuk swing ([AC_crypto_58 L730–L739](../materi/mentah/AC_crypto_58.txt#L730-L739)). Berlaku untuk AFS-05, AFS-09, AFS-10, AFS-14, AFS-15, AFS-17, AFS-18, AFS-19 (long), KMS-02, dan HKI-01.
3. **Setup yang mentornya memberi beberapa target** (TP1/TP2/TP3, level ekstensi Fibonacci, R1–R3, target Hosoda, dan sejenisnya): bot memakai **satu TP**, yaitu target **terdekat** yang RR-nya memenuhi minimum. Kalau tidak ada yang memenuhi, **jangan masuk** (Q-08).
4. **Pengecualian Smart Money** (AFS-06 – AFS-08): TP = likuiditas terdekat di sisi lawan. Kalau RR ke sana kurang dari minimum, jangan masuk; bot tidak mencari target yang lebih jauh (Q-20).
5. Satu TP, satu SL, *set and forget* (Q-08). Varian "50% ditutup di TP1, sisanya SL ke titik impas" hanya diuji sebagai **pembanding**, dan hanya di setup Alvesting dan Ichimoku ([G-17](#g-17--parameter-uji-dan-pemilihan-varian)).

Yang dikatakan mentor (semua sepakat: di bawah 1:1 = judi, seperti *binary option*):

| Mentor | RR yang disebut | Sumber |
|---|---|---|
| Alvesting | Di bawah 1:1 = judi. Contoh sehat 1:3 dan 1:5. | [AC_crypto_59 L2870–L2969](../materi/mentah/AC_crypto_59.txt#L2870-L2969), [AC_crypto_33 L755–L799](../materi/mentah/AC_crypto_33.txt#L755-L799) |
| Alvesting | Scalping: harus lebih dari 1:1 karena biaya; target 1:2–1:3. | [AC_crypto_58 L3113–L3134](../materi/mentah/AC_crypto_58.txt#L3113-L3134) |
| Alvesting | SMC: minimal 1:2 untuk jangka pendek, lebih dari 1:3 untuk swing. | [AC_crypto_58 L730–L739](../materi/mentah/AC_crypto_58.txt#L730-L739) |
| Alvesting | "Selalu 1:2 atau 1:3, jangan 1:1 atau 1:0,8." | [AC_crypto_60 L467–L480](../materi/mentah/AC_crypto_60.txt#L467-L480) |
| Kalimasada | Contoh 1:3. | [AC_crypto_62 L1739–L1778](../materi/mentah/AC_crypto_62.txt#L1739-L1778) |
| Mentor forex_2 | 1:1,5 atau 1:2. | [forex_2 L1940–L1959](../materi/mentah/forex_2.txt#L1940-L1959) |

---

## G-04 · Dilarang average down

**Aturan:** posisi yang sedang rugi **tidak boleh ditambah**. Kalau kena SL, posisi ditutup.

- Kalimasada: "nggak pernah average down", dengan contoh akun habis karena terus menambah posisi ([AC_crypto_62 L1665–L1718](../materi/mentah/AC_crypto_62.txt#L1665-L1718)).
- Ko Andri: posisi **trading** yang turun harus di-*cut loss*. Average down hanya untuk **investasi** ([AndreHakim_saham_1 L700–L729](../materi/mentah/AndreHakim_saham_1.txt#L700-L729), [AndreHakim_saham_3 L810–L819](../materi/mentah/AndreHakim_saham_3.txt#L810-L819)).

Menambah posisi yang **sedang untung** (*pyramiding*, contoh di ICH-03) juga tidak dipakai di versi pertama, karena [G-08](#g-08--jangan-overtrading) membatasi 1 posisi per instrumen.

---

## G-05 · Dilarang hedging

**Aturan:** tidak boleh membuka long dan short **bersamaan** pada aset yang sama untuk "menahan" kerugian ([AC_crypto_62 L1715–L1738](../materi/mentah/AC_crypto_62.txt#L1715-L1738)).

Catatan: Alvesting mengajarkan scalper boleh punya **bias dua arah**, yaitu long lalu short di hari yang sama ([AC_crypto_62 L3609–L3668](../materi/mentah/AC_crypto_62.txt#L3609-L3668)). Itu berurutan, bukan bersamaan, jadi tidak melanggar G-05.

---

## G-06 · Dilarang revenge trading

**Aturan:** setelah rugi, **ukuran posisi berikutnya tidak boleh dinaikkan** untuk "balik modal". Setelah untung juga tidak boleh langsung menggandakan ukuran. Ukuran selalu mengikuti G-01.

- Kalimasada: setelah kehilangan 30%, menaruh risiko 50% "pasti benar" lalu habis ([AC_crypto_62 L1695–L1714](../materi/mentah/AC_crypto_62.txt#L1695-L1714)).
- Alvesting: revenge trading biasanya ukurannya lebih besar dan setup-nya tidak siap ([AC_crypto_46 L291–L328](../materi/mentah/AC_crypto_46.txt#L291-L328)).

---

## G-07 · Rencana tidak diubah di tengah jalan

**Aturan:** setelah posisi terbuka, bot **tidak** mengubah arah, menutup lebih awal, atau memindah TP/SL di luar aturan. Prinsipnya *set and forget*.

- Alvesting: jangan sering cek PnL; jangan ubah plan long menjadi short di tengah jalan ([AC_crypto_46 L241–L290](../materi/mentah/AC_crypto_46.txt#L241-L290)); patuh pada trading plan ([AC_crypto_59 L1625–L1644](../materi/mentah/AC_crypto_59.txt#L1625-L1644)).
- Mentor forex_2: *set and forget*, nyalakan alarm, biarkan TP/SL bekerja ([forex_2 L2060–L2089](../materi/mentah/forex_2.txt#L2060-L2089)).

**Pengecualian** (hanya ini):

1. Posisi **scalping** ditutup setelah **3 jam** walaupun belum kena TP/SL (Q-19). Pembanding di backtest: 24 jam.
2. Posisi **scalping** ditutup **sebelum berita besar** ([G-13](#g-13--berita-besar)).
3. [HKI-01](04-ko-hengki-remora.md#hki-01--ikuti-tren-sekunder--minor-keluar-saat-struktur-patah) keluar saat struktur patah, sesuai mentornya.
4. Rem darurat [G-15](#g-15--rem-darurat).

Alvesting juga memakai CHoCH berlawanan arah untuk mengamankan sebagian profit ([AC_crypto_58 L645–L669](../materi/mentah/AC_crypto_58.txt#L645-L669)). Ini **tidak dipakai** di versi pertama, karena Anda memilih satu TP dan satu SL (Q-08).

---

## G-08 · Jangan overtrading

**Aturan (Q-06):**

1. Maksimal **3 transaksi baru per hari**, semua instrumen digabung. Di bawah batas itu, frekuensi mengikuti mentor masing-masing setup.
2. Maksimal **1 posisi per instrumen** dan **3 posisi bersamaan**. **BTC dan ETH yang searah dihitung satu posisi**, karena geraknya sangat mirip.
3. **Total risiko terbuka** (jumlah kerugian kalau semua posisi kena SL) maksimal **3%**.
4. Kalau dua setup memberi sinyal di instrumen yang sama, yang **lebih dulu** terpicu yang dipakai. Sinyal lain diabaikan selama posisi itu masih terbuka. *(Usulan saya, konsekuensi dari butir 2.)*

Kapan "hari" dimulai → [Q-44](09-pertanyaan-untuk-anda.md#q-44--hari-dan-rugi-dihitung-bagaimana).

Yang dikatakan mentor:

| Mentor | Batas | Sumber |
|---|---|---|
| Alvesting | 3–5 transaksi sehari sudah banyak. Lebih dari itu overtrading. Contoh "orang kantoran": ±1 transaksi sehari. | [AC_crypto_58 L3175–L3194](../materi/mentah/AC_crypto_58.txt#L3175-L3194), [AC_crypto_59 L3010–L3029](../materi/mentah/AC_crypto_59.txt#L3010-L3029) |
| Alvesting | Jangan sampai 10–20 kali sehari. | [AC_crypto_62 L3669–L3678](../materi/mentah/AC_crypto_62.txt#L3669-L3678) |
| Ko Andri | Scalping/trading hanya kalau ada momentum. Jangan dipaksa. | [AndreHakim_saham_3 L820–L839](../materi/mentah/AndreHakim_saham_3.txt#L820-L839) |
| Analis live | Saat pasar sulit: kurangi frekuensi, naikkan keyakinan. | [AC_crypto_1 L281–L330](../materi/mentah/AC_crypto_1.txt#L281-L330) |

---

## G-09 · Hanya instrumen yang likuid

**Aturan:** bot hanya bertransaksi di aset yang **paling ramai diperdagangkan**. Untuk versi pertama (Q-02):

| Pasar | Instrumen |
|---|---|
| Forex & emas (**F**) | **EURUSD**, **XAUUSD** |
| Kripto (**K**) | **BTC**, **ETH** |

Pair contoh Ichimoku Rafał (AUD/CHF, USD/JPY, USD/TRY) tidak dipakai dulu; USD/TRY tidak likuid (Q-02). Altcoin tidak dipakai di versi pertama (Q-25).

Dasar dari mentor:

- Alvesting: pilih aset dengan volume tertinggi di exchange, karena analisanya lebih "real" ([AC_crypto_35 L335–L359](../materi/mentah/AC_crypto_35.txt#L335-L359), [AC_crypto_57 L81–L129](../materi/mentah/AC_crypto_57.txt#L81-L129)).
- Alvesting: SMC hanya relevan untuk aset likuid besar (BTC, ETH, BNB). Untuk meme coin "100% tidak relevan" ([AC_crypto_61 L91–L129](../materi/mentah/AC_crypto_61.txt#L91-L129)).
- Kalimasada: Wyckoff diterapkan di aset besar seperti BTC dan ETH ([AC_crypto_62 L2795–L2809](../materi/mentah/AC_crypto_62.txt#L2795-L2809)).
- Ko Andri: analisa teknikal hanya berlaku di aset besar dengan likuiditas tinggi; aset kecil mudah "digambar" ([AndreHakim_saham_3 L1050–L1139](../materi/mentah/AndreHakim_saham_3.txt#L1050-L1139)). Scalping hanya di aset yang ramai ([AndreHakim_saham_3 L850–L860](../materi/mentah/AndreHakim_saham_3.txt#L850-L860)).

---

## G-10 · Tren dibaca dari timeframe besar

**Aturan:** arah (bias) diambil dari timeframe yang lebih besar. Timeframe kecil hanya untuk mencari titik masuk. Timeframe besar dianggap lebih valid dan lebih sedikit *noise*.

| Gaya | Tren | Pola / area | Pemicu | Sumber |
|---|---|---|---|---|
| Swing (Alvesting) | D1 | H4 | M15 | [AC_crypto_35 L250–L279](../materi/mentah/AC_crypto_35.txt#L250-L279) |
| Scalping (Alvesting) | H1 | M15 | M5 | [AC_crypto_62 L3709–L3728](../materi/mentah/AC_crypto_62.txt#L3709-L3728) |
| SMC (Alvesting) | H4 | — | M15 | [AC_crypto_34 L461–L529](../materi/mentah/AC_crypto_34.txt#L461-L529) |
| Ichimoku (Rafał) | W1 & D1 | — | H4 | [forex_3 L1–L240](../materi/mentah/forex_3.txt#L1-L240) |
| Ko Hengki | sekunder **D1**, minor **H4** | — | — | Q-12, berdasarkan [AC_crypto_60 L1270–L1277](../materi/mentah/AC_crypto_60.txt#L1270-L1277) |

Alvesting juga melarang trading di M1 atau timeframe detik ([AC_crypto_35 L230–L249](../materi/mentah/AC_crypto_35.txt#L230-L249)). Timeframe terkecil di rulebook ini adalah M5.

---

## G-11 · Satu indikator per kategori

**Aturan:** indikator dibagi tiga kategori: **tren** (MA, Bollinger, Supertrend, Ichimoku, dll.), **osilator** (RSI, Stochastic, MACD, KST, dll.), dan **volume** (OBV, CMF, volume profile, dll.). Satu setup memakai **paling banyak satu indikator dari tiap kategori**, karena indikator sejenis sering saling bertentangan.

- [AC_crypto_61 L2203–L2252](../materi/mentah/AC_crypto_61.txt#L2203-L2252): kesalahan memakai EMA + Bollinger + Supertrend sekaligus.
- [AC_crypto_33 L1020–L1089](../materi/mentah/AC_crypto_33.txt#L1020-L1089): pilih satu dari tiap kategori, lalu pakai terus dengan konsisten.
- Ko Hengki: indikator yang berbeda memberi sinyal berbeda, akhirnya trader jadi subjektif ([Remora_saham_11 L3930–L3959](../materi/mentah/Remora_saham_11.txt#L3930-L3959)).

Indikator juga hanya **pelengkap**, bukan alat utama. Urutannya: tren → area → pola → pemicu ([AC_crypto_57 L1844–L1873](../materi/mentah/AC_crypto_57.txt#L1844-L1873)).

---

## G-12 · Exit ditentukan sebelum entry

**Aturan:** bot tidak membuka posisi sebelum SL dan TP-nya bisa dihitung, dan keduanya dikirim **bersamaan** dengan order entry. Menurut Alvesting, exit "sama pentingnya" dengan entry ([AC_crypto_35 L108–L149](../materi/mentah/AC_crypto_35.txt#L108-L149), [AC_crypto_58 L1495–L1519](../materi/mentah/AC_crypto_58.txt#L1495-L1519), [AC_crypto_59 L2650–L2689](../materi/mentah/AC_crypto_59.txt#L2650-L2689)).

---

## G-13 · Berita besar

**Aturan (Q-15):**

1. **Jendela larangan:** dari **30 menit sebelum** sampai **30 menit sesudah** rilis berita. Tidak ada posisi baru di jendela ini.
2. **Berita yang dihitung:** kategori **"high impact"** di kalender ekonomi untuk mata uang instrumen itu.

   | Instrumen | Mata uang yang diperhatikan | Minimal |
   |---|---|---|
   | EURUSD | USD, EUR | NFP, CPI AS, keputusan suku bunga Fed (FOMC), keputusan suku bunga ECB |
   | XAUUSD | USD | NFP, CPI AS, FOMC |
   | BTC, ETH | — | **hanya** FOMC, CPI AS, NFP |

3. **Posisi yang sudah terbuka:**
   - Posisi trading/swing **dibiarkan** dengan SL terpasang. Mentor forex_2: berita hanya mempercepat TP atau SL ([forex_2 L2193–L2194](../materi/mentah/forex_2.txt#L2193-L2194)).
   - Posisi **scalping ditutup** sebelum rilis, yaitu saat jendela larangan dimulai. *(Saat penutupan ini adalah tafsiran saya atas "ditutup sebelum berita".)*
4. Kripto ikut karena sekarang bergerak bersama pasar saham AS. Timothy: "Nasdaq turun, crypto pasti turun" ([AC_crypto_21 L243–L249](../materi/mentah/AC_crypto_21.txt#L243-L249)).

Dasar dari mentor forex_2: berita hanya "mempercepat TP atau SL"; kalau mau aman, jangan trading saat berita ([forex_2 L2185–L2209](../materi/mentah/forex_2.txt#L2185-L2209)).

Kebutuhan data: jadwal kalender ekonomi historis (untuk backtest) dan terkini (untuk live).

---

## G-14 · Backtest dulu, dan nilai hasilnya dengan data

**Aturan:**

1. Setiap setup **wajib di-backtest** sebelum memakai uang sungguhan. Semua mentor mengulang pesan ini (contoh: [AC_crypto_59 L410–L420](../materi/mentah/AC_crypto_59.txt#L410-L420), [AC_crypto_56 L141–L150](../materi/mentah/AC_crypto_56.txt#L141-L150)). Setelah backtest, uji di **akun demo** dulu (Q-03).
2. Panjang data minimum menurut mentor forex_2: **H1 minimal 2 tahun**; D1 bisa 15–20 tahun ([forex_2 L1110–L1139](../materi/mentah/forex_2.txt#L1110-L1139), [forex_2 L1400–L1409](../materi/mentah/forex_2.txt#L1400-L1409)). Panjang ini untuk **data penyusunan**; data pemilihan ([G-17](#g-17--parameter-uji-dan-pemilihan-varian)) ditambahkan di luar itu.
3. Catat minimal: jumlah transaksi, persentase menang, rugi beruntun terpanjang, untung beruntun terpanjang, pip/persen per bulan ([forex_2 L1410–L1449](../materi/mentah/forex_2.txt#L1410-L1449)), dan drawdown terburuk (dipakai [G-15](#g-15--rem-darurat)).
4. Kripto di-backtest **long dan short**, walaupun akun sungguhan versi pertama hanya spot (Q-03).

**Patokan harapan** dari mentor, supaya hasil backtest tidak dinilai salah:

- Algoritma "smart money" terbaik disebut akurasinya sekitar 40%. Akurasi 50% ke atas sudah bagus, asal RR-nya sehat ([AC_crypto_59 L2690–L2709](../materi/mentah/AC_crypto_59.txt#L2690-L2709), [AC_crypto_62 L1599–L1612](../materi/mentah/AC_crypto_62.txt#L1599-L1612)).
- Ko Hengki: peluang menang 55% sudah cukup ([Remora_saham_11 L4040–L4059](../materi/mentah/Remora_saham_11.txt#L4040-L4059)).
- Rugi 5 kali berturut-turut itu wajar menurut data backtest Pola N ([forex_2 L1425–L1449](../materi/mentah/forex_2.txt#L1425-L1449)). Jadi **bot tidak dimatikan hanya karena beberapa kali rugi beruntun**, selama masih di dalam batas [G-15](#g-15--rem-darurat).
- Ko Andri memakai target kinerja **minimal 20% per tahun** sebagai patokan ([AndreHakim_saham_1 L1430–L1459](../materi/mentah/AndreHakim_saham_1.txt#L1430-L1459)).

---

## G-15 · Rem darurat

Tidak ada mentor yang menyebut batas ini. Angkanya dari Anda (Q-05).

| Kejadian | Tindakan |
|---|---|
| Rugi **hari ini** mencapai **3%** | Tidak membuka posisi baru sampai besok. |
| Rugi **minggu ini** mencapai **6%** | Tidak membuka posisi baru sampai minggu depan. |
| Saldo turun dari titik tertingginya melewati **batas drawdown** | **Berhenti total** sampai Anda memeriksa. |
| Kejadian teknis aneh: posisi **tanpa SL**, **order dobel**, atau **koneksi putus lama** | **Berhenti total** sampai Anda memeriksa. |

**Batas drawdown** = yang **lebih kecil** antara **15%** dan **1,5 × drawdown terburuk di backtest**. Contoh: drawdown terburuk backtest 8% → 1,5 × 8% = 12% → batasnya 12%.

**Belum jelas** → [Q-44](09-pertanyaan-untuk-anda.md#q-44--hari-dan-rugi-dihitung-bagaimana): "hari" dan "minggu" mulai jam berapa, rugi dihitung termasuk posisi yang masih terbuka atau tidak, apa yang terjadi pada posisi terbuka saat berhenti total, dan berapa lama "koneksi putus lama".

---

## G-16 · Jenis akun dan leverage

**Aturan (Q-03, Q-04):**

| Pasar | Akun versi pertama | Leverage |
|---|---|---|
| Kripto | **Spot saja** | **1×** |
| Kripto (nanti) | Futures, **setelah lolos demo**, lewat exchange **berizin OJK** yang menyediakan API | maksimal **2×** |
| Forex & emas | Akun broker; leverage akun boleh, karena hanya memengaruhi jaminan | **total nilai semua posisi terbuka maksimal 10× saldo** |

Akibatnya:

1. Di akun kripto sungguhan versi pertama, sinyal **short** tidak dieksekusi. Di backtest, short tetap diuji supaya nilainya ketahuan ([G-14](#g-14--backtest-dulu-dan-nilai-hasilnya-dengan-data)). Short di backtest dihitung seperti futures tanpa leverage (1×), termasuk biaya *funding* kalau datanya ada.
2. Di spot, ukuran posisi tidak bisa lebih besar dari saldo yang tersedia. Kalau G-01 meminta lebih, ukuran dipotong (G-01 butir 4).

Patokan dari Anda: ESMA membatasi trader ritel **30×** untuk pair mayor, **20×** untuk emas, dan **2×** untuk kripto.

---

## G-17 · Parameter uji dan pemilihan varian

**Instruksi Anda:** angka "uji dulu" menjadi parameter backtest dengan **nilai awal** dari Anda, diuji **hanya di sekitar** nilai itu supaya tidak overfitting, dan varian **dipilih dari hasil di data yang tidak dipakai saat menyusun strategi**.

**Cara menjalankannya:**

1. **Data dibagi menurut waktu**, tidak diacak:
   - **Data penyusunan** (bagian yang lebih lama): untuk menulis dan memeriksa kode, dan menjalankan semua nilai/varian.
   - **Data pemilihan** (bagian terbaru): tidak dilihat sampai kode selesai. Nilai parameter dan varian **dipilih dari hasil di sini**.

   Berapa bagian yang disisihkan → [Q-42](09-pertanyaan-untuk-anda.md#q-42--data-mana-yang-disisihkan-untuk-memilih-varian). Ukuran "hasil lebih baik" → [Q-43](09-pertanyaan-untuk-anda.md#q-43--hasil-lebih-baik-diukur-dengan-apa).
2. **Rentang uji.** Kalau Anda menulis rentang, rentang itu yang dipakai. Kalau hanya nilai awal, yang diuji adalah **0,5×, 1×, dan 1,5×** nilai awal. Pola ini diambil dari rentang yang Anda tulis sendiri (Q-11: 0,5–1,5× ATR; Q-20: 10–30 candle untuk nilai 20; Q-28: 0,5–1,5×). Hitungan candle dibulatkan.
3. **Satu parameter diubah sekali**; parameter lain tetap di nilai awal. Ini membatasi jumlah kombinasi, supaya hasilnya tidak kebetulan cocok dengan data.
4. Kalau hasil terbaik jatuh di ujung rentang, rentang **tidak diperlebar**.
5. Karena pilihan diambil dari data pemilihan, angka hasilnya cenderung sedikit terlalu bagus. Pemeriksaan terakhir sebelum uang sungguhan adalah **akun demo** (Q-03).

### Daftar parameter uji

| Parameter | Dipakai di | Nilai awal | Nilai yang diuji | Dasar |
|---|---|---|---|---|
| Jarak tambahan SL | semua setup (G-02) | 1 × ATR(14) | 0,5× · 1× · 1,5× | Q-11 |
| Faktor k persen→ATR (forex) | AFS-04, AFS-09 di forex (D-09) | k = persen ÷ ATR% BTC | 0,5k · k · 1,5k | Q-10 |
| Pantulan varian konfirmasi | AFS-04 | — | 3% · 4% · 5% (rentang mentor) | mentor, Q-09 |
| Selisih maksimal puncak double/triple | AFS-03 | 0,5 × ATR(14) | 0,25× · 0,5× · 0,75× | Q-23 |
| Stop hunt: tembus minimal | AFS-06 | 0,1 × ATR(14) | 0,05× · 0,1× · 0,15× | Q-20 |
| Stop hunt: close kembali ke range dalam | AFS-06 | 3 candle | 2 · 3 · 4 | Q-20 |
| Order limit OB/FVG batal setelah | AFS-06 (b), AFS-08 | 20 candle M15 | 10 · 20 · 30 | Q-20 |
| Retest: waktu tunggu maksimal | semua retest (D-05) | 10 candle | 5 · 10 · 15 | Q-20 |
| Grey area: jarak ke resistance | LIVE-F1 | 1 × ATR(14) | 0,5× · 1× · 1,5× | Q-28 |
| Pola N: jumlah candle koreksi maksimal | PLN-01 | 3 | 2 · 3 · 4 | Q-34 |
| Pola N: kedalaman koreksi maksimal | PLN-01 | 50% impuls | 25% · 50% · 75% | Q-34 |
| Fase bulan: jendela | WKT-01 | ±1 hari | ±1 · ±2 hari | Q-39 |
| Fibonacci waktu: jumlah proyeksi yang bertumpuk | WKT-02 | ≥3 | ≥3 · ≥4 | PETA, makalah Gema |

### Daftar varian pembanding

| Setup | Default | Pembanding | Dasar |
|---|---|---|---|
| AFS-01, AFS-02 | minimal 4 dari 5 poin (poin 1, 2, 4 wajib) | 5 dari 5 | Q-18 |
| AFS-03, AFS-04 | versi konfirmasi | versi antisipasi | Q-09 |
| Setup Alvesting & Ichimoku yang punya beberapa target | satu TP | 50% di TP1, sisanya SL ke titik impas | Q-08 |
| Posisi scalping | ditutup setelah 3 jam | ditutup setelah 24 jam | Q-19 |
| AFS-06 | (a) masuk saat candle BMS close | (b) limit order di OB/FVG — **setara**, keduanya diuji | Q-20 |
| AFS-12 | SL di bawah P | SL di bawah S1 — **setara**, keduanya diuji | Q-22 |
| AFS-13 | AFS-13A (mode tren) | AFS-13B (mode pantulan) — diuji terpisah; di live hanya satu yang aktif per instrumen | Q-24 |
| AFS-19 | POC minggu lalu (chart H1) | POC bulan lalu (chart H4/D1) — **setara** | Q-24 |
| ICH-01 – ICH-03 | SL di balik Kijun + ATR | SL di balik swing terakhir + ATR | Q-35 |
| PLN-01 | entry mulai 18.00 WIB | tanpa batas jam | Q-34 |
| HKI-01 | *buy on weakness* | *buy on breakout* — **setara**, keduanya sah menurut Ko Hengki | Q-09 |
| Semua aturan volume di forex | tick volume | aturan volume dimatikan | Q-14 |
| WKT-02 | cara (a): hitungan Fibonacci dari titik balik | cara (b): kelipatan Fibonacci dari jarak antar-titik balik — **setara** | Q-40 |

---

## Definisi bersama

Definisi di bawah dipakai oleh semua setup, supaya istilah yang sama selalu berarti hal yang sama.

### D-01 · Swing high dan swing low

Dari Q-12 (fractal 2 kiri, 2 kanan):

- **Swing high** = candle yang *high*-nya **lebih tinggi** dari *high* 2 candle sebelumnya **dan** 2 candle sesudahnya.
- **Swing low** = candle yang *low*-nya **lebih rendah** dari *low* 2 candle sebelumnya **dan** 2 candle sesudahnya.
- Swing baru **diakui setelah 2 candle sesudahnya close**. Backtest tidak boleh memakai swing sebelum waktu itu.
- Dipakai untuk **semua** swing: SL (G-02), struktur (D-02), level support/resistance (D-04), titik ABCD (AFS-10), impuls Fibonacci (AFS-04), divergensi (AFS-18), titik A/B/C target Hosoda (ICH-04), awal hitungan waktu Hosoda (WKT-05), dan titik balik di filter waktu (07).

### D-02 · Struktur dan tren

- **Bullish** = minimal **2 higher high** dan **2 higher low** berturut-turut (dari swing D-01). Sebuah higher low tetap sah selama low sebelumnya tidak ditembus ([AC_crypto_35 L370–L429](../materi/mentah/AC_crypto_35.txt#L370-L429)).
- **Bearish** = minimal 2 lower high dan 2 lower low ([AC_crypto_35 L425–L469](../materi/mentah/AC_crypto_35.txt#L425-L469)).
- **Sideways** = bukan bullish dan bukan bearish.
- **BOS / BMS** = candle **close** melewati swing high (atau swing low) terakhir. Wick saja tidak dihitung ([AC_crypto_36 L41–L59](../materi/mentah/AC_crypto_36.txt#L41-L59)).
- **CHoCH** = dalam struktur bullish, candle close di bawah higher low terakhir (berbalik bearish); cerminannya untuk bearish.
- **Tingkatan tren:** primer & sekunder dibaca di MN/W1/D1; minor untuk jangka pendek ([AC_crypto_60 L1270–L1277](../materi/mentah/AC_crypto_60.txt#L1270-L1277)). Untuk Ko Hengki: sekunder = **D1**, minor = **H4** (Q-12).

### D-03 · ATR

- **ATR(14)** dengan rumus bawaan TradingView (rata-rata Wilder).
- Selalu diambil dari **timeframe level/swing yang bersangkutan** (Q-11, Q-17).
- **ATR%** = ATR ÷ harga close × 100. Dipakai di D-09.

### D-04 · Zona support dan resistance

- **Level horizontal** = harga swing high/low (D-01) di timeframe area setup.
- **Zona** = level **± 0,5 × ATR(14)** dari timeframe level itu, jadi tebalnya 1 ATR (Q-17). Contoh mentor: zona 10.000–9.700 (±3%) untuk BTC, kira-kira 1 ATR ([AC_crypto_58 L1695–L1696](../materi/mentah/AC_crypto_58.txt#L1695-L1696)).
- "Harga di zona" = range candle (high–low) menyentuh zona.

### D-05 · Retest

- Setelah sebuah level ditembus (candle **close** di luarnya), **retest** = harga **kembali masuk zona** level itu (D-04) dalam maksimal **10 candle** (nilai awal; diuji 5 · 10 · 15). Lewat dari itu, setup **batal** (Q-20).
- Q-20 butir 4 menjawab retest untuk CHoCH. Definisi yang sama dipakai untuk **semua** setup yang menyebut retest (AFS-07, AFS-13A, AFS-14, AFS-16, AFS-20, KMS-02), supaya konsisten.

### D-06 · Candle

Definisi baku dari pustaka **TA-Lib** (Q-16):

| Istilah mentor | Arah | Fungsi TA-Lib |
|---|---|---|
| *Hammer* | long | `CDLHAMMER` |
| *Inverted hammer* | long | `CDLINVERTEDHAMMER` |
| *Bullish engulfing* | long | `CDLENGULFING` = +100 |
| *Hanging man* | short | `CDLHANGINGMAN` |
| *Shooting star* | short | `CDLSHOOTINGSTAR` |
| *Bearish engulfing* | short | `CDLENGULFING` = −100 |

Ukuran candle (Q-16, Q-26):

| Istilah | Definisi |
|---|---|
| Candle **kuat** | badan (jarak open–close) **≥ 70%** dari panjang candle (high − low) |
| Candle **besar** | panjang (high − low) **di atas** rata-rata panjang 20 candle terakhir |
| Candle **kecil** | panjang **di bawah** rata-rata panjang 20 candle terakhir |

### D-07 · Volume

- Volume **naik/tinggi** = volume candle **di atas rata-rata 20 candle** terakhir. **Turun/rendah** = di bawahnya (Q-26).
- **Kripto:** volume dari exchange sumber data harga.
- **Forex & emas:** **tick volume** dari sumber data yang sama dengan harga, hanya untuk perbandingan relatif (Q-14). Data bursa berjangka CME tidak dipakai di versi pertama.
- Di backtest forex, setiap aturan volume diuji dua cara: memakai tick volume, dan aturan volume **dimatikan**. Yang dipakai adalah yang hasilnya lebih baik di data pemilihan (G-17). Kalau aturan volume dimatikan, setup yang **seluruhnya** bergantung volume (AFS-18 CMF, AFS-19 POC) tidak dijalankan di forex; filter volume (AFS-F2, KMS-F1, HKI-F1, HKI-F2) dianggap selalu lolos.

### D-08 · Osilator

- **Stochastic:** jenuh beli **di atas 80**, jenuh jual **di bawah 20** (bawaan TradingView) (Q-13). Setting Alvesting: **5,3,3**.
- **RSI(14):** jenuh beli **di atas 70**, jenuh jual **di bawah 30** (Q-13).
- "Silang naik di area jenuh jual" = garis %K memotong %D ke atas saat %K masih di bawah 20. Cerminannya untuk jenuh beli. *(Rincian persilangan ini usulan saya.)*

### D-09 · Angka persen kripto di forex

Dari Q-10:

- **Kripto (BTC, ETH):** angka persen dari mentor dipakai apa adanya.
- **Forex & emas:** angka persen diganti dengan **k × ATR(14) harian** instrumen itu, dengan

  ```
  k = persen mentor ÷ rata-rata ATR%(14) harian BTC selama periode data penyusunan
  ```

- **Contoh hitungan:** kalau rata-rata ATR% harian BTC = 3,36% (angka contoh mentor, [AC_crypto_59 L2841](../materi/mentah/AC_crypto_59.txt#L2841)), maka untuk aturan 3%: k = 3 ÷ 3,36 ≈ 0,89. Kalau ATR harian EURUSD 70 pip, ambangnya 0,89 × 70 ≈ 62 pip.
- Backtest hanya menguji **0,5k, k, 1,5k** (G-17).
- Dipakai di: [AFS-09](01-alvesting-akademi-crypto.md#afs-09--validasi-tembus-3-dow-theory) (3%) dan [AFS-04](01-alvesting-akademi-crypto.md#afs-04--pantulan-golden-pocket-fibonacci) varian konfirmasi (3–5%).

### D-10 · Konvensi eksekusi

*Ini usulan saya untuk hal teknis yang tidak dibahas mentor. Silakan diubah.*

1. Semua sinyal dihitung dari candle yang **sudah close**.
2. "Masuk saat candle X close" → order pasar. Di backtest diisi di harga **open candle berikutnya**.
3. "Masuk di zona" (D-04) → order limit di **tepi zona yang pertama disentuh** harga (long: tepi atas zona support; short: tepi bawah zona resistance).
4. "Masuk di garis" (P, EMA, Kijun, Kumo, pita channel) → order limit **tepat di garis** itu.
5. TP di zona → tepi zona yang **pertama dicapai** harga (long: tepi bawah zona resistance). TP di garis → tepat di garis.
6. Biaya (spread, komisi, swap/*funding*) selalu dihitung di backtest.
7. Kalau dalam satu candle SL dan TP sama-sama tersentuh, backtest menganggap **SL** yang kena lebih dulu.

### D-11 · Label posisi: scalping atau trading

Dari Ko Andri ([AND-G1](05-ko-andri-andre-hakim.md#and-g1--tentukan-jenis-posisi-sejak-awal-posisi-trading-yang-rugi-di-cut-loss)): setiap posisi diberi label sejak dibuka, dan label tidak berubah.

| | Scalping | Trading |
|---|---|---|
| Risiko (G-01) | **0,5%** | **1%** |
| Batas waktu (G-07) | ditutup setelah **3 jam** (pembanding 24 jam) | tidak ada |
| Saat berita besar (G-13) | ditutup sebelum rilis | dibiarkan dengan SL |

- **Scalping:** [AFS-02](01-alvesting-akademi-crypto.md#afs-02--technical-research-5-tahap-versi-scalping).
- **Belum pasti:** AFS-03, AFS-12, AFS-20 → [Q-45](09-pertanyaan-untuk-anda.md#q-45--setup-mana-yang-dihitung-scalping).
- **Trading:** semua setup lain.

---

## Perbedaan pendapat antar-mentor

Mentor Anda berbeda pendapat soal hal-hal berikut. Keputusannya dari jawaban Anda di [10](10-jawaban.md).

| # | Topik | Pendapat A | Pendapat B | Keputusan |
|---|---|---|---|---|
| 1 | Dasar 1% risiko | 1% dari **total** portofolio (Kalimasada, [AC_crypto_62](../materi/mentah/AC_crypto_62.txt#L1609-L1618)) | 1% dari **porsi trading** 30% (Kalimasada, [AC_crypto_6](../materi/mentah/AC_crypto_6.txt#L96-L115)) | 1% dari saldo akun bot yang hanya berisi uang trading; scalping 0,5% (Q-01) |
| 2 | RR minimum | 1:1,5 (forex_2) | 1:2 sampai 1:3 (Alvesting) | Ikut mentor per setup, tidak pernah di bawah 1:1,5 (Q-07) |
| 3 | Ambil untung bertahap & titik impas (BE) | **Tidak boleh**: tanpa TP1/TP2, tanpa BE, karena "merusak psikologi" ([forex_2 L1360–L1379](../materi/mentah/forex_2.txt#L1360-L1379)) | **Boleh**: TP1/TP2/TP3 ([AC_crypto_62 L3749–L3768](../materi/mentah/AC_crypto_62.txt#L3749-L3768)); ambil 50–90% lalu BE ([forex_3 L661–L705](../materi/mentah/forex_3.txt#L661-L705)) | Satu TP, satu SL; versi bertahap hanya pembanding (Q-08) |
| 4 | Kapan masuk saat breakout | **Antisipasi**: masuk di dalam pola sebelum tembus, "jangan kejar breakout" (Alvesting, [AC_crypto_57 L831–L850](../materi/mentah/AC_crypto_57.txt#L831-L850)) | **Konfirmasi**: masuk saat/setelah harga tembus atau *close* di luar level (Pola N, Dow Theory) | Ikut mentor per setup; AFS-03 & AFS-04 default konfirmasi (Q-09) |
| 5 | Leverage | Jangan pakai leverage (Timothy, [AC_crypto_21 L11–L20](../materi/mentah/AC_crypto_21.txt#L11-L20)) | Derivatif boleh untuk porsi 30% bagi yang agresif (Kalimasada, [AC_crypto_62 L1339–L1368](../materi/mentah/AC_crypto_62.txt#L1339-L1368)) | Kripto spot 1×; forex total ≤10× saldo; futures kripto nanti ≤2× (Q-04) |
| 6 | Frekuensi | ±1 sehari (Alvesting, "orang kantoran") | 3–5 sehari (Alvesting, scalping) | Maksimal 3 transaksi baru per hari, semua instrumen (Q-06) |
| 7 | Timeframe Fibonacci | Paling valid di W1/MN; M1–M5 itu "judi berlogika" ([AC_crypto_56 L41–L80](../materi/mentah/AC_crypto_56.txt#L41-L80)) | Pola ABCD dan Gartley justru "paling works" di M15/H1 ([AC_crypto_57 L2600–L2609](../materi/mentah/AC_crypto_57.txt#L2600-L2609), [AC_crypto_60 L367–L386](../materi/mentah/AC_crypto_60.txt#L367-L386)) | Per setup: AFS-04 di D1/W1, AFS-10 di M15/H1 |
| 8 | Tren vs pola | Tren dulu, pola hanya konfirmasi ([AC_crypto_57 L1341–L1380](../materi/mentah/AC_crypto_57.txt#L1341-L1380)) | Harmonic: "pattern means everything", pola lebih dulu daripada tren ([AC_crypto_60 L2743–L2762](../materi/mentah/AC_crypto_60.txt#L2743-L2762)) | Harmonic ditunda (Q-23); tren dulu |
| 9 | Jarak SL dengan ATR | SL = entry − 1×ATR% ([AC_crypto_59 L2829–L2848](../materi/mentah/AC_crypto_59.txt#L2829-L2848)) | SL = di bawah support, jaraknya diukur ATR ([AC_crypto_33 L1090–L1099](../materi/mentah/AC_crypto_33.txt#L1090-L1099)) | SL = swing ± 1×ATR(14) (Q-11) |
| 10 | Jual di siklus halving | Jual setahun setelah halving ([AC_crypto_4 L420–L435](../materi/mentah/AC_crypto_4.txt#L420-L435)) | Puncak ±500 hari setelah halving ([AC_crypto_3 L51–L55](../materi/mentah/AC_crypto_3.txt#L51-L55)) | Tidak dipakai di versi pertama (Q-27) |
