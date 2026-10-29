# 00 · ATURAN GLOBAL (berlaku untuk semua setup)

Aturan di halaman ini **mengalahkan** aturan setup. Kalau sebuah setup memberi sinyal tetapi melanggar aturan global, sinyal itu **dibatalkan**.

Hampir semua aturan di sini disepakati lebih dari satu mentor. Kalau mentor berbeda pendapat, perbedaannya ditulis terang-terangan di [bagian akhir](#perbedaan-pendapat-antar-mentor) dan diubah menjadi pertanyaan untuk Anda.

---

## G-01 · Risiko per transaksi maksimal 1%

**Aturan:** kerugian maksimal **satu** transaksi, jika kena stop loss, adalah **1%** dari modal. Ukuran posisi (lot/kontrak) **dihitung dari** jarak stop loss, bukan sebaliknya.

```
ukuran_posisi = (modal × risiko%) ÷ (jarak entry–SL × nilai per unit)
```

| Mentor | Yang dikatakan | Sumber |
|---|---|---|
| Kalimasada | Risk per trade idealnya 1% dari total portofolio: "100 kesempatan untuk salah". | [AC_crypto_62 L1599–L1648](../materi/mentah/AC_crypto_62.txt#L1599-L1648) |
| Kalimasada | 1% **dari porsi trading** (30% portofolio), bukan dari total. | [AC_crypto_6 L96–L115](../materi/mentah/AC_crypto_6.txt#L96-L115) |
| Alvesting | Scalping: 0,5%–1%. Maksimal 2%, jangan sampai 10%. | [AC_crypto_58 L3055–L3104](../materi/mentah/AC_crypto_58.txt#L3055-L3104), [AC_crypto_62 L3669–L3688](../materi/mentah/AC_crypto_62.txt#L3669-L3688) |
| Alvesting | Harmonic: 0,5%–1%. | [AC_crypto_60 L2613–L2632](../materi/mentah/AC_crypto_60.txt#L2613-L2632) |
| Mentor forex_2 | "Haram hukumnya jika risikonya di atas 1%." Lot dihitung dengan kalkulator risiko. | [forex_2 L1040–L1089](../materi/mentah/forex_2.txt#L1040-L1089) |
| FXcopet | Contoh: 0,02 lot untuk modal $115. | [forex_1 L381–L390](../materi/mentah/forex_1.txt#L381-L390) |

**Belum jelas:** 1% dari apa, dan apakah scalping memakai 0,5% → **Q-01**.

---

## G-02 · Stop loss wajib, di titik "analisa saya salah"

**Aturan:**

1. **Setiap** posisi punya stop loss sejak dibuka.
2. Long: SL **di bawah** swing low / support / area beli. Short: SL **di atas** swing high / resistance / area jual.
3. SL diberi **jarak tambahan** dari level tersebut, karena harga sering menembus sebentar untuk menyapu stop loss (*liquidity grab*). Jarak tambahan diukur dengan **ATR**. Di kripto, ATR dipakai dalam **persen**; di forex dan komoditas dalam satuan harga (pip).
4. SL **tidak boleh dimatikan, dijauhkan, atau "ditunggu dulu siapa tahu mantul"**.

| Sumber | Isi |
|---|---|
| [AC_crypto_59 L2740–L2819](../materi/mentah/AC_crypto_59.txt#L2740-L2819) | SL long di bawah swing low, SL short di atas swing high. |
| [AC_crypto_59 L2819–L2859](../materi/mentah/AC_crypto_59.txt#L2819-L2859) | Jarak SL pakai ATR. Kripto: ATR dalam % (contoh BTC 3,36%). Forex: satuan harga. |
| [AC_crypto_33 L1090–L1129](../materi/mentah/AC_crypto_33.txt#L1090-L1129) | Jarak SL di bawah support diukur pakai ATR karena sering ada *liquidity grab*. |
| [AC_crypto_62 L1669–L1708](../materi/mentah/AC_crypto_62.txt#L1669-L1708) | Contoh kesalahan: mematikan SL lalu menambah posisi, akhirnya habis. |

**Belum jelas:** periode dan kelipatan ATR, dan apakah SL dihitung dari level swing atau dari harga entry → **Q-11**. Cara bot mengenali swing high/low → **Q-12**.

---

## G-03 · Perbandingan untung:rugi (RR) tidak boleh di bawah 1:1

**Aturan:** setup dengan target lebih kecil dari risikonya **tidak diambil**. Mentor menyebut RR negatif (contoh 1:0,8, seperti *binary option*) sebagai judi.

| Mentor | RR yang disebut | Sumber |
|---|---|---|
| Alvesting | Di bawah 1:1 = judi. Contoh sehat 1:3 dan 1:5. | [AC_crypto_59 L2870–L2969](../materi/mentah/AC_crypto_59.txt#L2870-L2969), [AC_crypto_33 L755–L799](../materi/mentah/AC_crypto_33.txt#L755-L799) |
| Alvesting | Scalping: harus lebih dari 1:1 karena biaya; target 1:2–1:3. | [AC_crypto_58 L3113–L3134](../materi/mentah/AC_crypto_58.txt#L3113-L3134) |
| Alvesting | SMC: minimal 1:2 untuk jangka pendek, lebih dari 1:3 untuk swing. | [AC_crypto_58 L730–L739](../materi/mentah/AC_crypto_58.txt#L730-L739) |
| Alvesting | "Selalu 1:2 atau 1:3, jangan 1:1 atau 1:0,8." | [AC_crypto_60 L467–L480](../materi/mentah/AC_crypto_60.txt#L467-L480) |
| Kalimasada | Contoh 1:3. | [AC_crypto_62 L1739–L1778](../materi/mentah/AC_crypto_62.txt#L1739-L1778) |
| Mentor forex_2 | 1:1,5 atau 1:2. | [forex_2 L1940–L1959](../materi/mentah/forex_2.txt#L1940-L1959) |

**Belum jelas:** RR minimum yang dipakai bot → **Q-07**. Sampai dijawab, setiap setup memakai RR dari mentornya sendiri.

---

## G-04 · Dilarang average down

**Aturan:** posisi yang sedang rugi **tidak boleh ditambah**. Kalau kena SL, posisi ditutup.

- Kalimasada: "nggak pernah average down", dengan contoh akun habis karena terus menambah posisi ([AC_crypto_62 L1665–L1718](../materi/mentah/AC_crypto_62.txt#L1665-L1718)).
- Ko Andri: posisi **trading** yang turun harus di-*cut loss*. Average down hanya untuk **investasi** ([AndreHakim_saham_1 L700–L729](../materi/mentah/AndreHakim_saham_1.txt#L700-L729), [AndreHakim_saham_3 L810–L819](../materi/mentah/AndreHakim_saham_3.txt#L810-L819)).

Pembelian bertahap yang **direncanakan sejak awal** (misalnya cicilan 5× di modul investasi spot) bukan average down, karena jumlah dan levelnya sudah ditentukan sebelum masuk. Lihat [KMS-I3](02-kalimasada-akademi-crypto.md#kms-i3--cicilan-5-kali-masuk-dan-5-kali-keluar).

---

## G-05 · Dilarang hedging

**Aturan:** tidak boleh membuka long dan short **bersamaan** pada aset yang sama untuk "menahan" kerugian ([AC_crypto_62 L1715–L1738](../materi/mentah/AC_crypto_62.txt#L1715-L1738)).

Catatan: Alvesting mengajarkan scalper boleh punya **bias dua arah**, yaitu long lalu short di hari yang sama ([AC_crypto_62 L3609–L3668](../materi/mentah/AC_crypto_62.txt#L3609-L3668)). Itu berurutan, bukan bersamaan, jadi tidak melanggar G-05.

---

## G-06 · Dilarang revenge trading

**Aturan:** setelah rugi, **ukuran posisi berikutnya tidak boleh dinaikkan** untuk "balik modal". Setelah untung juga tidak boleh langsung menggandakan ukuran.

- Kalimasada: setelah kehilangan 30%, menaruh risiko 50% "pasti benar" lalu habis ([AC_crypto_62 L1695–L1714](../materi/mentah/AC_crypto_62.txt#L1695-L1714)).
- Alvesting: revenge trading biasanya ukurannya lebih besar dan setup-nya tidak siap ([AC_crypto_46 L291–L328](../materi/mentah/AC_crypto_46.txt#L291-L328)).
- FXcopet: tidak ada trader sukses yang serakah dengan lot dibesarkan ([forex_1 L3385–L3404](../materi/mentah/forex_1.txt#L3385-L3404)).

⚠️ **Bertabrakan** dengan teknik "recover" FXcopet (membalik posisi untuk menutup rugi). Lihat **Q-32**.

---

## G-07 · Rencana tidak diubah di tengah jalan

**Aturan:** setelah posisi terbuka, bot **tidak** mengubah arah, menutup lebih awal, atau memindah TP/SL di luar aturan setup. Prinsipnya *set and forget*.

- Alvesting: jangan sering cek PnL; jangan ubah plan long menjadi short di tengah jalan ([AC_crypto_46 L241–L290](../materi/mentah/AC_crypto_46.txt#L241-L290)); patuh pada trading plan ([AC_crypto_59 L1625–L1644](../materi/mentah/AC_crypto_59.txt#L1625-L1644)).
- Mentor forex_2: *set and forget*, nyalakan alarm, biarkan TP/SL bekerja ([forex_2 L2060–L2089](../materi/mentah/forex_2.txt#L2060-L2089)).

Pengecualian **hanya** jika setup sendiri punya aturan keluar lebih awal. Contoh: Alvesting memakai CHoCH berlawanan arah untuk mengamankan sebagian profit ([AC_crypto_58 L645–L669](../materi/mentah/AC_crypto_58.txt#L645-L669)).

---

## G-08 · Jangan overtrading

**Aturan:** jumlah transaksi dibatasi. Angkanya berbeda antar-mentor:

| Mentor | Batas | Sumber |
|---|---|---|
| Alvesting | 3–5 transaksi sehari sudah banyak. Lebih dari itu overtrading. Contoh "orang kantoran": ±1 transaksi sehari. | [AC_crypto_58 L3175–L3194](../materi/mentah/AC_crypto_58.txt#L3175-L3194), [AC_crypto_59 L3010–L3029](../materi/mentah/AC_crypto_59.txt#L3010-L3029) |
| Alvesting | Jangan sampai 10–20 kali sehari. | [AC_crypto_62 L3669–L3678](../materi/mentah/AC_crypto_62.txt#L3669-L3678) |
| FXcopet | Maksimal 2 transaksi sehari. Kalau sudah kena TP sekali, berhenti hari itu. | [forex_1 L645–L659](../materi/mentah/forex_1.txt#L645-L659) |
| Ko Andri | Scalping/trading hanya kalau ada momentum. Jangan dipaksa. | [AndreHakim_saham_3 L820–L839](../materi/mentah/AndreHakim_saham_3.txt#L820-L839) |
| Analis live | Saat pasar sulit: kurangi frekuensi, naikkan keyakinan. | [AC_crypto_1 L281–L330](../materi/mentah/AC_crypto_1.txt#L281-L330) |

**Belum jelas:** angka untuk bot → **Q-06**.

---

## G-09 · Hanya instrumen yang likuid

**Aturan:** bot hanya bertransaksi di aset yang **paling ramai diperdagangkan**.

- Alvesting: pilih aset dengan volume tertinggi di exchange, karena analisanya lebih "real" ([AC_crypto_35 L335–L359](../materi/mentah/AC_crypto_35.txt#L335-L359), [AC_crypto_57 L81–L129](../materi/mentah/AC_crypto_57.txt#L81-L129)).
- Alvesting: SMC hanya relevan untuk aset likuid besar (BTC, ETH, BNB). Untuk meme coin "100% tidak relevan" ([AC_crypto_61 L91–L129](../materi/mentah/AC_crypto_61.txt#L91-L129)).
- Kalimasada: Wyckoff diterapkan di aset besar seperti BTC dan ETH ([AC_crypto_62 L2795–L2809](../materi/mentah/AC_crypto_62.txt#L2795-L2809)).
- Ko Andri: analisa teknikal hanya berlaku di aset besar dengan likuiditas tinggi; aset kecil mudah "digambar" ([AndreHakim_saham_3 L1050–L1139](../materi/mentah/AndreHakim_saham_3.txt#L1050-L1139)). Scalping hanya di aset yang ramai ([AndreHakim_saham_3 L850–L860](../materi/mentah/AndreHakim_saham_3.txt#L850-L860)).

**Belum jelas:** daftar pair dan koin → **Q-02**.

---

## G-10 · Tren dibaca dari timeframe besar

**Aturan:** arah (bias) diambil dari timeframe yang lebih besar. Timeframe kecil hanya untuk mencari titik masuk. Timeframe besar dianggap lebih valid dan lebih sedikit *noise*.

| Gaya | Tren | Pola / area | Pemicu | Sumber |
|---|---|---|---|---|
| Swing (Alvesting) | D1 | H4 | M15 | [AC_crypto_35 L250–L279](../materi/mentah/AC_crypto_35.txt#L250-L279) |
| Scalping (Alvesting) | H1 | M15 | M5 | [AC_crypto_62 L3709–L3728](../materi/mentah/AC_crypto_62.txt#L3709-L3728) |
| SMC (Alvesting) | H4 | — | M15 | [AC_crypto_34 L461–L529](../materi/mentah/AC_crypto_34.txt#L461-L529) |
| Ichimoku (Rafał) | W1 & D1 | — | H4 | [forex_3 L1–L240](../materi/mentah/forex_3.txt#L1-L240) |

Alvesting juga melarang trading di M1 atau timeframe detik ([AC_crypto_35 L230–L249](../materi/mentah/AC_crypto_35.txt#L230-L249)). FXcopet justru memakai M1. Lihat [FXC-01](06-mentor-forex.md#fxc-01--tembus-garis-merahaqua-eurusd-m1).

---

## G-11 · Satu indikator per kategori

**Aturan:** indikator dibagi tiga kategori: **tren** (MA, Bollinger, Supertrend, Ichimoku, dll.), **osilator** (RSI, Stochastic, MACD, KST, dll.), dan **volume** (OBV, CMF, volume profile, dll.). Satu setup memakai **paling banyak satu indikator dari tiap kategori**, karena indikator sejenis sering saling bertentangan.

- [AC_crypto_61 L2203–L2252](../materi/mentah/AC_crypto_61.txt#L2203-L2252): kesalahan memakai EMA + Bollinger + Supertrend sekaligus.
- [AC_crypto_33 L1020–L1089](../materi/mentah/AC_crypto_33.txt#L1020-L1089): pilih satu dari tiap kategori, lalu pakai terus dengan konsisten.
- Ko Hengki: indikator yang berbeda memberi sinyal berbeda, akhirnya trader jadi subjektif ([Remora_saham_11 L3930–L3959](../materi/mentah/Remora_saham_11.txt#L3930-L3959)).

Indikator juga hanya **pelengkap**, bukan alat utama. Urutannya: tren → area → pola → pemicu ([AC_crypto_57 L1844–L1873](../materi/mentah/AC_crypto_57.txt#L1844-L1873)).

---

## G-12 · Exit ditentukan sebelum entry

**Aturan:** bot tidak membuka posisi sebelum SL dan TP-nya bisa dihitung. Menurut Alvesting, exit "sama pentingnya" dengan entry ([AC_crypto_35 L108–L149](../materi/mentah/AC_crypto_35.txt#L108-L149), [AC_crypto_58 L1495–L1519](../materi/mentah/AC_crypto_58.txt#L1495-L1519), [AC_crypto_59 L2650–L2689](../materi/mentah/AC_crypto_59.txt#L2650-L2689)).

---

## G-13 · Berita besar (forex)

**Aturan:** di forex, **jangan membuka posisi** saat ada rilis berita berdampak besar, misalnya NFP.

- FXcopet tidak berani trading saat NFP; menunggu harga stabil dulu ([forex_1 L545–L579](../materi/mentah/forex_1.txt#L545-L579), [forex_1 L841–L850](../materi/mentah/forex_1.txt#L841-L850)).
- Mentor forex_2: berita hanya "mempercepat TP atau SL". Kalau mau aman, jangan trading saat berita ([forex_2 L2185–L2209](../materi/mentah/forex_2.txt#L2185-L2209)).

**Belum jelas:** berapa menit sebelum/sesudah berita, dan apakah berlaku juga untuk kripto → **Q-15**.

---

## G-14 · Backtest dulu, dan nilai hasilnya dengan data

**Aturan:**

1. Setiap setup **wajib di-backtest** sebelum memakai uang sungguhan. Semua mentor mengulang pesan ini (contoh: [AC_crypto_59 L410–L420](../materi/mentah/AC_crypto_59.txt#L410-L420), [AC_crypto_56 L141–L150](../materi/mentah/AC_crypto_56.txt#L141-L150)).
2. Panjang data minimum menurut mentor forex_2: **H1 minimal 2 tahun**; D1 bisa 15–20 tahun ([forex_2 L1110–L1139](../materi/mentah/forex_2.txt#L1110-L1139), [forex_2 L1400–L1409](../materi/mentah/forex_2.txt#L1400-L1409)).
3. Catat minimal: jumlah transaksi, persentase menang, rugi beruntun terpanjang, untung beruntun terpanjang, pip/persen per bulan ([forex_2 L1410–L1449](../materi/mentah/forex_2.txt#L1410-L1449)).

**Patokan harapan** dari mentor, supaya hasil backtest tidak dinilai salah:

- Algoritma "smart money" terbaik disebut akurasinya sekitar 40%. Akurasi 50% ke atas sudah bagus, asal RR-nya sehat ([AC_crypto_59 L2690–L2709](../materi/mentah/AC_crypto_59.txt#L2690-L2709), [AC_crypto_62 L1599–L1612](../materi/mentah/AC_crypto_62.txt#L1599-L1612)).
- Ko Hengki: peluang menang 55% sudah cukup ([Remora_saham_11 L4040–L4059](../materi/mentah/Remora_saham_11.txt#L4040-L4059)).
- Rugi 5 kali berturut-turut itu wajar menurut data backtest Pola N ([forex_2 L1425–L1449](../materi/mentah/forex_2.txt#L1425-L1449)). Jadi **bot tidak dimatikan hanya karena beberapa kali rugi beruntun** selama masih dalam batas hasil backtest.
- Ko Andri memakai target kinerja **minimal 20% per tahun** sebagai patokan ([AndreHakim_saham_1 L1430–L1459](../materi/mentah/AndreHakim_saham_1.txt#L1430-L1459)).

---

## G-15 · Rem darurat (belum ada di materi)

Tidak ada mentor yang menyebut batas rugi harian, mingguan, atau batas *drawdown* untuk menghentikan trading. Yang ada hanya prinsip 1% per transaksi dan "100 nyawa". Aturan ini **sengaja dikosongkan** sampai Anda menjawab **Q-05**.

---

## Perbedaan pendapat antar-mentor

Hal-hal berikut **tidak saya pilihkan**, karena mentor Anda sendiri berbeda pendapat. Semuanya menjadi pertanyaan di [09](09-pertanyaan-untuk-anda.md).

| # | Topik | Pendapat A | Pendapat B | Pertanyaan |
|---|---|---|---|---|
| 1 | Dasar 1% risiko | 1% dari **total** portofolio (Kalimasada, [AC_crypto_62](../materi/mentah/AC_crypto_62.txt#L1609-L1618)) | 1% dari **porsi trading** 30% (Kalimasada, [AC_crypto_6](../materi/mentah/AC_crypto_6.txt#L96-L115)) | Q-01 |
| 2 | RR minimum | 1:1,5 (forex_2) | 1:2 sampai 1:3 (Alvesting) | Q-07 |
| 3 | Ambil untung bertahap & titik impas (BE) | **Tidak boleh**: tanpa TP1/TP2, tanpa BE, karena "merusak psikologi" ([forex_2 L1360–L1379](../materi/mentah/forex_2.txt#L1360-L1379)) | **Boleh**: TP1/TP2/TP3 ([AC_crypto_62 L3749–L3768](../materi/mentah/AC_crypto_62.txt#L3749-L3768)); ambil 50–90% lalu BE ([forex_3 L661–L705](../materi/mentah/forex_3.txt#L661-L705)) | Q-08 |
| 4 | Kapan masuk saat breakout | **Antisipasi**: masuk di dalam pola sebelum tembus, "jangan kejar breakout" (Alvesting, [AC_crypto_57 L831–L850](../materi/mentah/AC_crypto_57.txt#L831-L850)) | **Konfirmasi**: masuk saat/ setelah harga tembus atau *close* di luar level (FXcopet, Pola N, Dow Theory) | Q-09 |
| 5 | Leverage | Jangan pakai leverage (Timothy, [AC_crypto_21 L11–L20](../materi/mentah/AC_crypto_21.txt#L11-L20)) | Derivatif boleh untuk porsi 30% bagi yang agresif (Kalimasada, [AC_crypto_62 L1339–L1368](../materi/mentah/AC_crypto_62.txt#L1339-L1368)) | Q-04 |
| 6 | Frekuensi | ±1 sehari / maks 2 sehari | 3–5 sehari | Q-06 |
| 7 | Timeframe Fibonacci | Paling valid di W1/MN; M1–M5 itu "judi berlogika" ([AC_crypto_56 L41–L80](../materi/mentah/AC_crypto_56.txt#L41-L80)) | Pola ABCD dan Gartley justru "paling works" di M15/H1 ([AC_crypto_57 L2600–L2609](../materi/mentah/AC_crypto_57.txt#L2600-L2609), [AC_crypto_60 L367–L386](../materi/mentah/AC_crypto_60.txt#L367-L386)) | per setup |
| 8 | Tren vs pola | Tren dulu, pola hanya konfirmasi ([AC_crypto_57 L1341–L1380](../materi/mentah/AC_crypto_57.txt#L1341-L1380)) | Harmonic: "pattern means everything", pola lebih dulu daripada tren ([AC_crypto_60 L2743–L2762](../materi/mentah/AC_crypto_60.txt#L2743-L2762)) | per setup |
| 9 | Menutup rugi | Teknik "recover": balik arah, target 2× kerugian (FXcopet) | Larangan revenge trading (Kalimasada, Alvesting) | Q-32 |
| 10 | Jarak SL dengan ATR | SL = entry − 1×ATR% ([AC_crypto_59 L2829–L2848](../materi/mentah/AC_crypto_59.txt#L2829-L2848)) | SL = di bawah support, jaraknya diukur ATR ([AC_crypto_33 L1090–L1099](../materi/mentah/AC_crypto_33.txt#L1090-L1099)) | Q-11 |
| 11 | Jual di siklus halving | Jual setahun setelah halving ([AC_crypto_4 L420–L435](../materi/mentah/AC_crypto_4.txt#L420-L435)) | Puncak ±500 hari setelah halving ([AC_crypto_3 L51–L55](../materi/mentah/AC_crypto_3.txt#L51-L55)) | Q-27 |
