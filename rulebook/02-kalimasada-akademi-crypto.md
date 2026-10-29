# 02 · KALIMASADA — Akademi Crypto

Kalimasada mengajar investasi, money management, dan Wyckoff. Aturan money management-nya sudah masuk ke [aturan global](00-aturan-global.md) (G-01, G-04, G-05, G-06). Halaman ini berisi sisanya:

- [A. Wyckoff](#a-wyckoff) — untuk trading, khusus aset besar (BTC, ETH).
- [B. Modul investasi spot kripto](#b-modul-investasi-spot-kripto-ditunda) — **ditunda**: versi pertama hanya trading (Q-29).

---

## A. Wyckoff

**Prinsip dasar** ([AC_crypto_60 L3105–L3330](../materi/mentah/AC_crypto_60.txt#L3105-L3330), [AC_crypto_40 L1–L281](../materi/mentah/AC_crypto_40.txt#L1-L281)):

- Elemen wajib hanya dua: **harga** dan **volume**. Tanpa volume, Wyckoff tidak bisa dipakai ([AC_crypto_60 L3265–L3314](../materi/mentah/AC_crypto_60.txt#L3265-L3314)).
- Tiga hukum:
  1. **Permintaan & penawaran**: volume beli naik + harga naik = bullish; volume jual naik + harga turun = bearish ([AC_crypto_40 L61–L179](../materi/mentah/AC_crypto_40.txt#L61-L179)).
  2. **Sebab–akibat**: konsolidasi panjang (akumulasi/distribusi) adalah "sebab"; tren sesudahnya adalah "akibat" ([AC_crypto_40 L175–L209](../materi/mentah/AC_crypto_40.txt#L175-L209)).
  3. **Usaha–hasil**: volume tinggi tetapi harga tidak bergerak = kelelahan, tanda pembalikan. Volume rendah tetapi harga bergerak jauh = tren kuat ([AC_crypto_40 L209–L279](../materi/mentah/AC_crypto_40.txt#L209-L279)).
- Hanya diterapkan di aset besar seperti BTC dan ETH ([AC_crypto_62 L2791–L2809](../materi/mentah/AC_crypto_62.txt#L2791-L2809)).

**Empat fase pasar** ([AC_crypto_60 L2824–L3104](../materi/mentah/AC_crypto_60.txt#L2824-L3104)):

| Fase | Ciri dari mentor |
|---|---|
| **Akumulasi** | Range sempit (contoh BTC 10–20%), volume kecil; volume naik setiap harga mendekati support; ada **spring** (tembus low lalu balik cepat ke dalam range). |
| **Markup** | Breakout ke atas range + higher high/higher low + volume naik. |
| **Distribusi** | Range sempit di atas (setelah naik 200–300%), volume jual tinggi dekat resistance; ada **upthrust** (tembus atas palsu lalu balik ke range). |
| **Markdown** | Breakdown dari range + lower high/lower low + volume jual naik. |

**Lima tahap Wyckoff** (A–E) ([AC_crypto_59 L1805–L1963](../materi/mentah/AC_crypto_59.txt#L1805-L1963), [AC_crypto_60 L3331–L3477](../materi/mentah/AC_crypto_60.txt#L3331-L3477)):

| Tahap | Akumulasi | Distribusi | Tindakan menurut mentor |
|---|---|---|---|
| A | *Preliminary support*, *last selling impulse*, *automatic reaction*, *secondary test* | *Preliminary supply*, *last buying impulse*, *automatic reaction*, *secondary test* | **Ambil untung** posisi lama |
| B | ST-SOW, UA (berlangsung lebih lama) | mSOW, UT | **Tunggu**, jangan trading |
| C | **Spring** | **UTAD** | **Tempat masuk terbaik** |
| D | JAC (lompat keluar range) + **LPS** (retest) | *Fall through the ice* + **LPSY** (retest) | Harga **selalu retest** dulu |
| E | SOS + LPS (HH/HL) | SOW + LPSY (LH/LL) | Tren sudah berjalan |

### KMS-01 · Wyckoff spring / UTAD + reclaim

| | |
|---|---|
| Sumber | [AC_crypto_40 L281–L340](../materi/mentah/AC_crypto_40.txt#L281-L340), [AC_crypto_60 L3331–L3390](../materi/mentah/AC_crypto_60.txt#L3331-L3390), [AC_crypto_62 L2791–L2901](../materi/mentah/AC_crypto_62.txt#L2791-L2901) |
| Pasar | K (BTC, ETH) |
| Arah | Long setelah spring, short setelah UTAD |
| Status | 🔴 |

**Long (spring):**

1. Ada range akumulasi yang panjang setelah tren turun.
2. Harga **menembus support range** (spring / *shake out*).
3. Harga kembali ke dalam range (*reclaim* / *return to origin*).
4. **Entry agresif** saat spring terjadi; **entry yang lebih baik** setelah *reclaim*, karena kalau ternyata bukan spring harga akan terus turun ([AC_crypto_40 L321–L340](../materi/mentah/AC_crypto_40.txt#L321-L340)).
5. Konfirmasi dengan **VSA**: volume naik tetapi candle mengecil (keraguan) ([AC_crypto_62 L2821–L2880](../materi/mentah/AC_crypto_62.txt#L2821-L2880)).

**Short (UTAD):** cerminannya di range distribusi ([AC_crypto_62 L2801–L2849](../materi/mentah/AC_crypto_62.txt#L2801-L2849)).

**Kenapa 🔴:** mengenali tahap A–E butuh "mata"; mentor sendiri bilang Wyckoff lebih sulit dan butuh banyak latihan ([AC_crypto_60 L3465–L3477](../materi/mentah/AC_crypto_60.txt#L3465-L3477)). SL dan TP juga tidak disebut. Logikanya mirip [AFS-06](01-alvesting-akademi-crypto.md#afs-06--stop-hunt--break-of-structure) (stop hunt + BOS), yang lebih mudah dikodekan.

---

### KMS-02 · Wyckoff breakout range + retest

| | |
|---|---|
| Sumber | [AC_crypto_40 L360–L441](../materi/mentah/AC_crypto_40.txt#L360-L441), [AC_crypto_60 L3385–L3440](../materi/mentah/AC_crypto_60.txt#L3385-L3440) |
| Pasar | K (BTC, ETH) |
| Arah | Long (markup), short (markdown) |
| Label | Trading |
| RR minimum | TP tetap: 1:2 (entry H1 ke bawah) / 1:3 (H4 ke atas) (Q-07) |
| Status | 🟡 (tinggal Q-48) |

**Long (markup):**

1. Ada range konsolidasi yang lama (fase akumulasi). Ukuran range → [Q-48](09-pertanyaan-untuk-anda.md#q-48--wyckoff-kms-02-range-seperti-apa).
2. Candle **close di atas** range **dengan volume naik**, yaitu volume di atas rata-rata 20 candle ([D-07](00-aturan-global.md#d-07--volume), Q-26). Kalau volume belum mendukung: *wait and see*, supaya tidak kena *false breakout* ([AC_crypto_40 L381–L399](../materi/mentah/AC_crypto_40.txt#L381-L399)).
3. Tunggu **retest** batas atas range (LPS) — menurut mentor harga selalu retest dulu ([AC_crypto_60 L3401–L3420](../materi/mentah/AC_crypto_60.txt#L3401-L3420)). Retest mengikuti [D-05](00-aturan-global.md#d-05--retest): harga masuk zona batas range dalam maksimal 10 candle.
4. → Long: order limit di tepi atas zona itu.

**Short (markdown):** close di bawah range distribusi dengan volume jual naik → retest (LPSY) → short ([AC_crypto_40 L421–L431](../materi/mentah/AC_crypto_40.txt#L421-L431), [AC_crypto_60 L3420–L3430](../materi/mentah/AC_crypto_60.txt#L3420-L3430)).

**SL:** mentor tidak menyebut → di titik invalidasi (G-02): long = swing low terakhir di dalam range − 1 × ATR(14); short = swing high terakhir + 1 × ATR(14).

**TP:** mentor tidak menyebut → TP tetap 1:2 atau 1:3 sesuai timeframe entry (Q-07).

**Belum jelas** → [Q-48](09-pertanyaan-untuk-anda.md#q-48--wyckoff-kms-02-range-seperti-apa): timeframe, berapa lama minimal range, dan selebar apa maksimalnya.

---

### KMS-F1 · Filter VSA (volume vs ukuran candle)

| | |
|---|---|
| Sumber | [AC_crypto_61 L1325–L1505](../materi/mentah/AC_crypto_61.txt#L1325-L1505) |
| Pasar | K, F\* |
| Status | ⚪ 🟢 |

Tabel ringkas dari mentor ([AC_crypto_61 L1365–L1390](../materi/mentah/AC_crypto_61.txt#L1365-L1390)):

| Volume | Ukuran candle | Arti |
|---|---|---|
| Tinggi / naik | Besar | **Lanjut** searah tren |
| Rendah / turun | Kecil | **Lanjut** (koreksi sehat) |
| Rendah / turun | Besar | **Potensi pembalikan** |
| Tinggi / naik | Kecil | **Potensi pembalikan** |

Kegunaan untuk bot: (1) menyaring sinyal pembalikan (hanya diambil kalau VSA juga menunjukkan potensi pembalikan); (2) menyaring breakout (lihat [AFS-F2](01-alvesting-akademi-crypto.md#afs-f2--konfirmasi-volume-untuk-breakout)).

Pola penyerapan (*absorption*): beli agresif beruntun tetapi muncul wick atas = diserap penjual limit; jual agresif beruntun tetapi muncul wick bawah = diserap pembeli limit ([AC_crypto_57 L3665–L3705](../materi/mentah/AC_crypto_57.txt#L3665-L3705)).

**Ukuran untuk bot (Q-26):** volume tinggi/naik = di atas rata-rata 20 candle; rendah/turun = di bawahnya ([D-07](00-aturan-global.md#d-07--volume)). Candle besar = panjang (high − low) di atas rata-rata 20 candle; kecil = di bawahnya ([D-06](00-aturan-global.md#d-06--candle)). Di forex memakai tick volume, dibandingkan dengan versi tanpa filter ini (Q-14).

---

## B. Modul investasi spot kripto (ditunda)

Bagian ini berasal dari kelas **investasi**, bukan trading. **Tidak dipakai di versi pertama**: Anda memilih bot hanya untuk trading (Q-29). Isinya disimpan untuk versi berikutnya; semua setup di bagian ini berstatus ⏸.

### KMS-I1 · Alokasi portofolio 70/15/15

| | |
|---|---|
| Sumber | [AC_crypto_6 L1–L192](../materi/mentah/AC_crypto_6.txt#L1-L192), [AC_crypto_62 L1329–L1558](../materi/mentah/AC_crypto_62.txt#L1329-L1558) |
| Pasar | K (spot) |
| Status | ⏸ ditunda (Q-29) |

**Aturan dari mentor:**

1. **70% BTC** (dibeli sekaligus atau dicicil bulanan), **30% untuk "dimainkan"**: 15% altcoin + 15% meme coin. Lakukan *rebalancing* kembali ke porsi ini ([AC_crypto_6 L76–L95](../materi/mentah/AC_crypto_6.txt#L76-L95), [AC_crypto_6 L176–L185](../materi/mentah/AC_crypto_6.txt#L176-L185)).
2. Versi lain: **pasif** = 100% spot BTC + ETH; **agresif** = 70% spot, 30% derivatif ([AC_crypto_62 L1339–L1428](../materi/mentah/AC_crypto_62.txt#L1339-L1428)).
3. Di porsi spot: **maksimal 10% per koin** ("10 slot") ([AC_crypto_62 L1469–L1488](../materi/mentah/AC_crypto_62.txt#L1469-L1488)).
4. Satu koin pun **dibeli bertahap**, contoh 4 × 25% ([AC_crypto_62 L1488–L1528](../materi/mentah/AC_crypto_62.txt#L1488-L1528)).
5. **30% selalu cair** (cash/stablecoin) untuk membeli saat harga jatuh ([AC_crypto_62 L1528–L1558](../materi/mentah/AC_crypto_62.txt#L1528-L1558)).
6. Meme coin: "tebar jala", **1% per posisi** dari porsi tersebut ([AC_crypto_6 L126–L175](../materi/mentah/AC_crypto_6.txt#L126-L175)).

**Catatan untuk nanti:** angka 2 dan 5 tidak sama dengan angka 1 (70/30 vs 70/30 + 30% cair). Kalau modul ini dibuka, kombinasinya perlu dipilih.

---

### KMS-I2 · Moon bag

| | |
|---|---|
| Sumber | [AC_crypto_49](../materi/mentah/AC_crypto_49.txt) |
| Pasar | K (spot) |
| Status | ⏸ ditunda (Q-29) |

**Aturan:** ketika sebuah aset spot **naik 100% (2×)**, **jual 50%**. Uang yang keluar sama dengan modal awal, jadi sisanya menjadi "moon bag" gratis yang dibiarkan berjalan. Modal yang sudah bebas boleh diputar ke aset lain ([AC_crypto_49 L141–L189](../materi/mentah/AC_crypto_49.txt#L141-L189)).

Mentor menyebut strategi ini cocok untuk: mengejar *top gainer*, ikut *pump and dump*, dan saat kondisi pasar buruk ([AC_crypto_49 L91–L140](../materi/mentah/AC_crypto_49.txt#L91-L140)). Analis live juga memakainya: "double pun mungkin saya moon bag" ([AC_crypto_1 L641–L660](../materi/mentah/AC_crypto_1.txt#L641-L660)).

---

### KMS-I3 · Cicilan 5 kali masuk dan 5 kali keluar

| | |
|---|---|
| Sumber | [AC_crypto_27 L595–L711](../materi/mentah/AC_crypto_27.txt#L595-L711) |
| Pasar | K (spot) |
| Timeframe | W1 (juga MN dan D1 untuk tren). **Bukan** H4/M15 ([AC_crypto_27 L655–L665](../materi/mentah/AC_crypto_27.txt#L655-L665)) |
| Status | ⏸ ditunda (Q-29) |

**Aturan:**

1. Modal untuk satu aset dibagi menjadi **5 kali masuk** ([AC_crypto_27 L645–L654](../materi/mentah/AC_crypto_27.txt#L645-L654)).
2. **Masuk bertahap** saat osilator (RSI atau Stochastic) W1 di area **jenuh jual**.
3. **Keluar bertahap** (5 kali) saat osilator W1 di area **jenuh beli** / fase distribusi ([AC_crypto_27 L660–L700](../materi/mentah/AC_crypto_27.txt#L660-L700)).
4. Bisa digabung dengan moon bag ([AC_crypto_27 L700–L711](../materi/mentah/AC_crypto_27.txt#L700-L711)).

**Catatan untuk nanti:** jarak antar-cicilan (setiap candle W1? setiap turun X%?) tidak disebut mentor. Level jenuh beli/jual sudah ada di [D-08](00-aturan-global.md#d-08--osilator).

---

### KMS-I4 · Fear & Greed Index

| | |
|---|---|
| Sumber | [AC_crypto_24 L150–L347](../materi/mentah/AC_crypto_24.txt#L150-L347); dipakai juga oleh analis live ([AC_crypto_5 L141–L160](../materi/mentah/AC_crypto_5.txt#L141-L160)) |
| Pasar | K (spot) |
| Status | ⏸ ditunda (Q-29) |

**Aturan:** indeks 0–100. **Extreme fear** = potensi dasar → saat untuk membeli. Contoh mentor: angka 26 di awal 2023, dan angka sangat rendah di 2019. **Extreme greed** = tanda koreksi → saat untuk menjual. Kondisi ekstrem bisa bertahan berbulan-bulan ([AC_crypto_24 L260–L310](../materi/mentah/AC_crypto_24.txt#L260-L310)).

Tanda puncak lain menurut mentor (tidak bisa diukur bot): semua orang membicarakan kripto, muncul prediksi harga yang tidak masuk akal ([AC_crypto_24 L210–L259](../materi/mentah/AC_crypto_24.txt#L210-L259)).

**Catatan untuk nanti:** ambang angka "extreme" tidak dibakukan mentor.
