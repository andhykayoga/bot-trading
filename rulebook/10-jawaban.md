# 10 · JAWABAN ANDA

Jawaban Anda untuk [09-pertanyaan-untuk-anda.md](09-pertanyaan-untuk-anda.md). Isinya disimpan sesuai yang Anda tulis; hanya formatnya yang dirapikan. Di bawah setiap jawaban ada baris **→ Diterapkan di**, yaitu tempat jawaban itu mengubah rulebook.

**Instruksi umum dari Anda:**

> Terapkan ke rulebook: ubah 🟡 jadi 🟢 sesuai jawaban, dan simpan jawaban ini di rulebook/10-jawaban.md. Jawaban "uji dulu" jadikan parameter backtest dengan nilai awal yang saya tulis, dan uji hanya di sekitar nilai itu supaya tidak overfitting. Pilih varian berdasarkan hasil di data yang tidak dipakai saat menyusun strategi.

Cara instruksi ini dijalankan ada di [G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian). Pertanyaan baru yang muncul saat menerapkan jawaban ada di [09 · Bagian 8](09-pertanyaan-untuk-anda.md#bagian-8--pertanyaan-lanjutan).

---

## Bagian 1 — Wajib

### [Q-01](09-pertanyaan-untuk-anda.md#q-01--risiko-per-transaksi-1-dari-apa) · Risiko per transaksi

A. 1% dari saldo akun bot; akun bot hanya berisi uang trading. Scalping 0,5% (batas bawah Alvesting, karena transaksinya lebih sering dan biayanya lebih besar).

→ Diterapkan di: [G-01](00-aturan-global.md#g-01--risiko-per-transaksi-maksimal-1), [D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading).

### [Q-02](09-pertanyaan-untuk-anda.md#q-02--pair-dan-koin-apa-saja) · Instrumen

EURUSD, XAUUSD, BTC, ETH. Pair contoh Ichimoku Rafał tidak dipakai dulu (USD/TRY tidak likuid).

→ Diterapkan di: [G-09](00-aturan-global.md#g-09--hanya-instrumen-yang-likuid).

### [Q-03](09-pertanyaan-untuk-anda.md#q-03--kripto-spot-futures-atau-keduanya) · Spot atau futures

Di backtest, kripto diuji long dan short supaya ketahuan nilai setup short. Di akun sungguhan versi pertama: A, spot saja. Futures baru dipertimbangkan setelah lolos demo, lewat exchange berizin OJK yang menyediakan API.

→ Diterapkan di: [G-16](00-aturan-global.md#g-16--jenis-akun-dan-leverage).

### [Q-04](09-pertanyaan-untuk-anda.md#q-04--leverage-maksimum) · Leverage

Kripto 1× (spot). Forex/emas: leverage akun dari broker boleh, karena hanya memengaruhi jaminan, tetapi total nilai semua posisi terbuka maksimal 10× saldo. Kalau nanti futures kripto dipakai: maksimal 2×. Patokan: ESMA membatasi trader ritel 30× untuk pair mayor, 20× untuk emas, dan 2× untuk kripto.

→ Diterapkan di: [G-16](00-aturan-global.md#g-16--jenis-akun-dan-leverage).

### [Q-05](09-pertanyaan-untuk-anda.md#q-05--rem-darurat) · Rem darurat

A, ya.

- Rugi hari ini 3% → berhenti sampai besok.
- Rugi minggu ini 6% → berhenti sampai minggu depan.
- Saldo turun dari puncak lebih dari 15% atau lebih dari 1,5× drawdown terburuk di backtest (pakai yang lebih kecil) → berhenti total sampai saya periksa.
- Berhenti total juga kalau ada kejadian teknis aneh: posisi tanpa SL, order dobel, atau koneksi putus lama.

→ Diterapkan di: [G-15](00-aturan-global.md#g-15--rem-darurat). Pertanyaan lanjutan: [Q-44](09-pertanyaan-untuk-anda.md#q-44--hari-dan-rugi-dihitung-bagaimana).

### [Q-06](09-pertanyaan-untuk-anda.md#q-06--berapa-transaksi-per-hari-dan-berapa-posisi-sekaligus) · Frekuensi dan posisi bersamaan

1. D, ikut mentor per setup, dengan batas total 3 transaksi baru per hari untuk semua instrumen.
2. Maksimal 1 posisi per instrumen dan 3 posisi bersamaan. BTC dan ETH searah dihitung satu posisi karena geraknya sangat mirip. Total risiko terbuka maksimal 3%.

→ Diterapkan di: [G-08](00-aturan-global.md#g-08--jangan-overtrading).

### [Q-07](09-pertanyaan-untuk-anda.md#q-07--perbandingan-untungrugi-rr-minimum) · RR minimum

D, ikut mentor per setup, dengan batas bawah 1:1,5 untuk semua setup. Untuk setup tanpa target (AFS-05, AFS-09, AFS-15, AFS-17, KMS-02): 1:2 kalau entry di H1 ke bawah, 1:3 kalau entry di H4/D1. Ini patokan Alvesting: minimal 1:2 untuk jangka pendek, lebih dari 1:3 untuk swing ([AC_crypto_58 L730–L739](../materi/mentah/AC_crypto_58.txt#L730-L739)).

→ Diterapkan di: [G-03](00-aturan-global.md#g-03--rr-minimum-115) dan kartu setiap setup. Aturan "setup tanpa target" juga dipakai untuk setup lain yang mentornya tidak menyebut target: AFS-10, AFS-14, AFS-18, AFS-19 (long), HKI-01.

### [Q-08](09-pertanyaan-untuk-anda.md#q-08--ambil-untung-bertahap-dan-titik-impas) · TP bertahap dan titik impas

A untuk versi pertama: satu TP, satu SL.

- Kalau mentor memberi beberapa target (TP1/TP2/TP3), TP = target terdekat yang memenuhi RR minimum Q-07. Kalau tidak ada yang memenuhi, jangan masuk.
- Varian "50% ditutup di TP1, sisanya SL ke titik impas" diuji sebagai pembanding, hanya di setup Alvesting dan Ichimoku (mentornya memakai TP bertahap).

→ Diterapkan di: [G-03](00-aturan-global.md#g-03--rr-minimum-115), [G-17](00-aturan-global.md#g-17--parameter-uji-dan-pemilihan-varian).

### [Q-09](09-pertanyaan-untuk-anda.md#q-09--masuk-sebelum-atau-sesudah-harga-menembus) · Antisipasi atau konfirmasi

C, ikut mentor masing-masing setup. Untuk setup yang punya dua versi (AFS-03, AFS-04), default-nya versi konfirmasi (candle close di luar level). Versi antisipasi diuji sebagai pembanding.

→ Diterapkan di: [AFS-03](01-alvesting-akademi-crypto.md#afs-03--double-topbottom--tembus-neckline), [AFS-04](01-alvesting-akademi-crypto.md#afs-04--pantulan-golden-pocket-fibonacci), [HKI-01](04-ko-hengki-remora.md#hki-01--ikuti-tren-sekunder--minor-keluar-saat-struktur-patah).

### [Q-10](09-pertanyaan-untuk-anda.md#q-10--angka-persen-dari-kelas-kripto-dipakai-di-forex) · Angka persen di forex

A. Di kripto, persen dari mentor tetap dipakai. Di forex, persen diubah jadi kelipatan ATR(14) harian dengan patokan BTC: k = persen mentor ÷ rata-rata ATR% harian BTC di periode backtest. Lalu pakai k × ATR harian pair forex. Contoh mentor sendiri: ATR BTC 3,36% ([AC_crypto_59 L2841](../materi/mentah/AC_crypto_59.txt#L2841)). Backtest hanya menguji di sekitar nilai k itu.

→ Diterapkan di: [D-09](00-aturan-global.md#d-09--angka-persen-kripto-di-forex).

---

## Bagian 2 — Aturan teknis umum

### [Q-11](09-pertanyaan-untuk-anda.md#q-11--seberapa-jauh-stop-loss-dari-titik-analisa-salah) · Jarak stop loss

A. SL = swing low − 1 × ATR(14); untuk short, swing high + 1 × ATR(14). ATR diambil dari timeframe tempat swing itu.

- Patokannya contoh mentor: SL BTC sekitar 1 ATR (3,36%) dari titik masuk di support ([AC_crypto_59 L2835–L2849](../materi/mentah/AC_crypto_59.txt#L2835-L2849)).
- Kalau SL ini membuat RR di bawah minimum, jangan masuk; SL tidak boleh diperkecil.
- Pembanding yang boleh diuji: 0,5× dan 1,5× ATR.

→ Diterapkan di: [G-02](00-aturan-global.md#g-02--stop-loss-wajib-di-titik-analisa-saya-salah).

### [Q-12](09-pertanyaan-untuk-anda.md#q-12--bagaimana-bot-mengenali-puncak-dan-lembah) · Puncak dan lembah

A, fractal 2 candle kiri dan 2 kanan untuk semua swing.

- Tren sekunder Ko Hengki = D1, tren minor = H4. Dasarnya: Alvesting bilang tren primer & sekunder dibaca di MN/W1/D1, sedangkan minor untuk jangka pendek ([AC_crypto_60 L1270–L1277](../materi/mentah/AC_crypto_60.txt#L1270-L1277)).
- Titik awal hitungan Hosoda dan titik A/B/C di ICH-04: ya, pakai definisi swing yang sama.

→ Diterapkan di: [D-01](00-aturan-global.md#d-01--swing-high-dan-swing-low), [D-02](00-aturan-global.md#d-02--struktur-dan-tren).

### [Q-13](09-pertanyaan-untuk-anda.md#q-13--jenuh-beli-dan-jenuh-jual-di-angka-berapa) · Jenuh beli / jenuh jual

A. Stochastic 80/20 (bawaan TradingView), RSI 70/30.

→ Diterapkan di: [D-08](00-aturan-global.md#d-08--osilator).

### [Q-14](09-pertanyaan-untuk-anda.md#q-14--volume-di-forex) · Volume di forex

A. Tick volume dari sumber data yang sama dengan harga, hanya untuk perbandingan relatif (naik/turun dibanding rata-rata). Di backtest forex, bandingkan dengan C (aturan volume dimatikan) dan pakai yang hasilnya lebih baik. B tidak dipakai di versi pertama.

→ Diterapkan di: [D-07](00-aturan-global.md#d-07--volume).

### [Q-15](09-pertanyaan-untuk-anda.md#q-15--jadwal-berita) · Jadwal berita

1. 30 menit sebelum dan 30 menit sesudah berita.
2. Berita kategori "high impact" di kalender ekonomi untuk mata uang pair itu (XAUUSD ikut USD). Minimal NFP, CPI AS, serta keputusan suku bunga Fed (FOMC) dan ECB.
3. Posisi swing dibiarkan dengan SL terpasang. Mentor forex_2: berita hanya mempercepat TP/SL ([forex_2 L2193–L2194](../materi/mentah/forex_2.txt#L2193-L2194)). Posisi scalping ditutup sebelum berita.
4. Kripto ikut aturan ini, tetapi hanya untuk FOMC, CPI AS, dan NFP. Timothy: sekarang "Nasdaq turun, crypto pasti turun" ([AC_crypto_21 L243–L249](../materi/mentah/AC_crypto_21.txt#L243-L249)).

→ Diterapkan di: [G-13](00-aturan-global.md#g-13--berita-besar).

### [Q-16](09-pertanyaan-untuk-anda.md#q-16--definisi-candle-pemicu) · Candle pemicu

A. Pakai definisi baku dari pustaka TA-Lib (CDLHAMMER, CDLENGULFING, CDLSHOOTINGSTAR, dan seterusnya). "Candle kuat" = badan minimal 70% dari panjang candle (high−low).

→ Diterapkan di: [D-06](00-aturan-global.md#d-06--candle).

### [Q-17](09-pertanyaan-untuk-anda.md#q-17--seberapa-tebal-zona-supportresistance) · Tebal zona

A. Zona = level ± 0,5 × ATR(14), jadi tebal totalnya 1 ATR, di timeframe level itu. Ukuran ini setara contoh mentor: zona 10.000–9.700 (sekitar 3%) untuk BTC, kira-kira 1 ATR BTC ([AC_crypto_58 L1695–L1696](../materi/mentah/AC_crypto_58.txt#L1695-L1696)).

→ Diterapkan di: [D-04](00-aturan-global.md#d-04--zona-support-dan-resistance).

---

## Bagian 3 — Setup Alvesting

### [Q-18](09-pertanyaan-untuk-anda.md#q-18--afs-01-berapa-poin-minimal) · AFS-01: poin minimal

B. Minimal 4 poin, dengan poin 1, 2, dan 4 wajib. Versi 5 dari 5 diuji sebagai pembanding.

→ Diterapkan di: [AFS-01](01-alvesting-akademi-crypto.md#afs-01--technical-research-5-tahap-versi-swing). Pertanyaan lanjutan: [Q-46](09-pertanyaan-untuk-anda.md#q-46--afs-01-indikator-untuk-poin-5).

### [Q-19](09-pertanyaan-untuk-anda.md#q-19--batas-waktu-posisi-scalping) · Batas waktu scalping

A. Posisi scalping ditutup setelah 3 jam. Kata mentor: "kalau scalping itu maksimal tiga jam" ([AC_crypto_58 L3053](../materi/mentah/AC_crypto_58.txt#L3053)). B (24 jam) diuji sebagai pembanding.

→ Diterapkan di: [D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading), [AFS-02](01-alvesting-akademi-crypto.md#afs-02--technical-research-5-tahap-versi-scalping). Pertanyaan lanjutan: [Q-45](09-pertanyaan-untuk-anda.md#q-45--setup-mana-yang-dihitung-scalping).

### [Q-20](09-pertanyaan-untuk-anda.md#q-20--smart-money-kapan-masuk-di-mana-keluar) · Smart Money

1. Uji dua cara, keduanya dari mentor:
   - (a) Masuk saat candle BMS close ("keep it simple", [AC_crypto_59 L351–L370](../materi/mentah/AC_crypto_59.txt#L351-L370)).
   - (b) Limit order di OB/FVG setelah BOS ("perfect combo", [AC_crypto_59 L385–L400](../materi/mentah/AC_crypto_59.txt#L385-L400)). Order (b) batal kalau tidak terisi dalam 20 candle M15 (uji dulu 10–30) atau kalau harga sudah menyentuh target.
2. TP ke likuiditas terdekat di sisi lawan: PDH/PDL, PWH/PWL, atau swing high/low. Masuk hanya kalau RR ke sana memenuhi minimum Q-07.
3. Uji dulu. Nilai awal: harga menembus high/low acuan minimal 0,1 × ATR(14), lalu close kembali di dalam range dalam 3 candle atau kurang.
4. Uji dulu. Nilai awal: harga kembali masuk zona level yang ditembus (lebar zona dari Q-17), ditunggu maksimal 10 candle.

→ Diterapkan di: [AFS-06](01-alvesting-akademi-crypto.md#afs-06--stop-hunt--break-of-structure), [AFS-07](01-alvesting-akademi-crypto.md#afs-07--change-of-character-choch--retest), [AFS-08](01-alvesting-akademi-crypto.md#afs-08--revisit-order-block--fair-value-gap), [D-05](00-aturan-global.md#d-05--retest).

### [Q-21](09-pertanyaan-untuk-anda.md#q-21--definisi-order-block--fvg) · Definisi FVG

A. FVG 3 candle: bullish kalau low candle sekarang di atas high 2 candle sebelumnya; bearish kebalikannya. Begitulah cara kerja indikator FVG LuxAlgo yang dipakai mentor. Celah yang terlalu kecil dibanding volatilitas diabaikan, seperti setting threshold "Auto" di LuxAlgo.

→ Diterapkan di: [AFS-08](01-alvesting-akademi-crypto.md#afs-08--revisit-order-block--fair-value-gap).

### [Q-22](09-pertanyaan-untuk-anda.md#q-22--pivot-point) · Pivot point

1. Ikut bawaan TradingView sesuai pesan mentor "settingnya default aja" ([AC_crypto_44 L60–L90](../materi/mentah/AC_crypto_44.txt#L60-L90)). Dengan Pivots Timeframe "Auto", chart M5/M15 memakai pivot harian, chart H1 memakai pivot mingguan.
2. Uji kedua versi SL, karena keduanya dari mentor.

→ Diterapkan di: [AFS-12](01-alvesting-akademi-crypto.md#afs-12--pivot-point-entry-di-garis-p).

### [Q-23](09-pertanyaan-untuk-anda.md#q-23--pola-grafik-dan-pola-harmonic) · Pola grafik dan harmonic

B. Hanya ABCD dan double/triple top-bottom. Pola harmonic XABCD dan pola grafik lain ditunda.

- ABCD: C = 0,382–0,886 × AB, sesuai angka transkrip dan sama dengan versi longgar di buku.
- D = proyeksi BC dengan pasangan resiprok: C 0,618 → D 1,618; C 0,786 → D 1,27 (rentang 1,13–2,618). Angka "1,232" di transkrip dianggap salah dengar.
- Double/triple top: batas selisih puncak diuji dulu, nilai awal maksimal 0,5 × ATR(14).

→ Diterapkan di: [AFS-03](01-alvesting-akademi-crypto.md#afs-03--double-topbottom--tembus-neckline), [AFS-10](01-alvesting-akademi-crypto.md#afs-10--pola-abcd), [AFS-11](01-alvesting-akademi-crypto.md#afs-11--pola-harmonic-xabcd), [AFS-23](01-alvesting-akademi-crypto.md#afs-23--pola-grafik-klasik).

### [Q-24](09-pertanyaan-untuk-anda.md#q-24--setting-indikator-yang-rancu) · Setting indikator

- Keltner: EMA, yaitu bawaan TradingView yang dipakai mentor (panjang 20, ATR 10, pengali 2; persis angka yang ia sebut di [AC_crypto_44 L362–L365](../materi/mentah/AC_crypto_44.txt#L362-L365)). Mode tren dan mode pantulan dijadikan dua setup terpisah dan diuji sendiri-sendiri. Di live, hanya satu yang aktif per instrumen.
- Donchian: cara mentor (pantulan & silang garis tengah), panjang bawaan TradingView 20. Mode breakout tidak dipakai.
- Linear Regression Channel: bawaan TradingView, 100 candle, deviasi 2.
- Renko: ukuran bata dari ATR(14), cara bawaan TradingView.
- POC: uji dulu dua rentang: minggu lalu (untuk H1) dan bulan lalu (untuk H4/D1).

→ Diterapkan di: [AFS-13](01-alvesting-akademi-crypto.md#afs-13--keltner-channel), [AFS-16](01-alvesting-akademi-crypto.md#afs-16--donchian-channel), [AFS-19](01-alvesting-akademi-crypto.md#afs-19--pantulan-poc-volume-profile), [AFS-20](01-alvesting-akademi-crypto.md#afs-20--linear-regression-channel), [AFS-21](01-alvesting-akademi-crypto.md#afs-21--renko-reversal). Pertanyaan lanjutan (timeframe): [Q-47](09-pertanyaan-untuk-anda.md#q-47--timeframe-dan-cara-masuk-yang-belum-disebut).

### [Q-25](09-pertanyaan-untuk-anda.md#q-25--altcoin) · Altcoin

Tidak di versi pertama; hanya BTC dan ETH.

→ Diterapkan di: [AFS-F1](01-alvesting-akademi-crypto.md#afs-f1--screening-altcoin--korelasi-btc) (ditunda).

---

## Bagian 4 — Kalimasada & analis live

### [Q-26](09-pertanyaan-untuk-anda.md#q-26--seberapa-besar-yang-disebut-volume-naik) · Volume naik, candle besar

A. Volume "naik/tinggi" = di atas rata-rata 20 candle terakhir. Candle "besar" = range (high−low) di atas rata-rata 20 candle; "kecil" = di bawahnya.

→ Diterapkan di: [D-06](00-aturan-global.md#d-06--candle), [D-07](00-aturan-global.md#d-07--volume).

### [Q-27](09-pertanyaan-untuk-anda.md#q-27--siklus-halving-jual-kapan) · Siklus halving

D. Bot tidak mengelola investasi jangka panjang di versi pertama.

→ Diterapkan di: [LIVE-01](03-analis-live-akademi-crypto.md#live-01--siklus-halving-bitcoin-spot-jangka-panjang) (ditunda).

### [Q-28](09-pertanyaan-untuk-anda.md#q-28--grey-area-seberapa-dekat-dengan-resistance) · Grey area

A. Dalam 1 × ATR(14) dari resistance, di timeframe resistance itu (contoh mentor di D1). Uji dulu 0,5–1,5×.

→ Diterapkan di: [LIVE-F1](03-analis-live-akademi-crypto.md#live-f1--filter-grey-area).

### [Q-29](09-pertanyaan-untuk-anda.md#q-29--modul-investasi-spot-kripto) · Modul investasi spot

Tidak. Versi pertama hanya trading; modul investasi spot dilewati.

→ Diterapkan di: [02 · bagian B](02-kalimasada-akademi-crypto.md#b-modul-investasi-spot-kripto-ditunda) (ditunda).

### [Q-30](09-pertanyaan-untuk-anda.md#q-30--token-baru-tge) · Token baru (TGE)

B, tidak.

→ Diterapkan di: [LIVE-02](03-analis-live-akademi-crypto.md#live-02--token-baru-tge-30-saat-listing-70-di-base) (ditunda).

---

## Bagian 5 — Forex

### [Q-31](09-pertanyaan-untuk-anda.md#q-31--indikator-fxcopet) · FXcopet

**Jawaban akhir (revisi):** skip FXcopet sepenuhnya. FXC-01 dihapus dari rulebook dan dipindahkan ke [08-tidak-dijadikan-aturan.md](08-tidak-dijadikan-aturan.md#g-fxcopet-forex_1-tidak-dipakai), karena bukan dari mentor utama Anda dan indikatornya tidak diketahui.

Jawaban awal (diganti oleh revisi di atas): "B, tunda FXcopet. File indikatornya tidak ada di repo, dan setting TMA tidak disebut di transkrip. Kalau nanti saya upload file indikatornya ke materi/indikator/, setup ini dibuka lagi."

→ Diterapkan di: [06](06-mentor-forex.md) (FXcopet dihapus), [08 · bagian G](08-tidak-dijadikan-aturan.md#g-fxcopet-forex_1-tidak-dipakai), dan semua rujukan FXcopet di [00](00-aturan-global.md).

### [Q-32](09-pertanyaan-untuk-anda.md#q-32--teknik-recover-fxcopet) · Teknik "recover"

**Tidak relevan** karena FXcopet di-skip (Q-31).

Jawaban awal: "A, jangan dipakai. Teknik ini melanggar G-06, tidak punya SL, dan cara kerjanya mirip martingale."

### [Q-33](09-pertanyaan-untuk-anda.md#q-33--jam-tutup-fxcopet) · Jam tutup FXcopet

**Tidak relevan** karena FXcopet di-skip (Q-31).

Jawaban awal: "Kemungkinan besar A (pagi, sekitar penutupan sesi Amerika). Mentor selalu menyebut jam dalam format 24 jam: 12.32, 15.53, 11.04, 8.44 WIB (forex_1 L1900, L2038, L2328, L2152). Ia juga bilang tren sesi Eropa bisa berlanjut 'sampai penutupan sesi Amerika' (forex_1 L2966)."

### [Q-34](09-pertanyaan-untuk-anda.md#q-34--pola-n-angka-angka-yang-belum-disebut) · Pola N

1. Uji dulu. Nilai awal: koreksi maksimal 3 candle dan tidak lebih dalam dari 50% impuls. Mentor sendiri memakai 50% candle impuls untuk varian limit order ([forex_2 L848–L850](../materi/mentah/forex_2.txt#L848-L850)).
2. Badan minimal 70% dari panjang candle (sama dengan Q-16).
3. Ya. SL di ujung wick candle sebelum candle breakout, yaitu ujung koreksi ([forex_2 L1911–L1928](../materi/mentah/forex_2.txt#L1911-L1928)).
4. H1, karena itu timeframe backtest mentor ([forex_2 L1119–L1129](../materi/mentah/forex_2.txt#L1119-L1129)). Entry hanya mulai 18.00 WIB, sesuai pesan "trading malam hari aja di atas 6.00 sore" ([forex_2 L2206](../materi/mentah/forex_2.txt#L2206)). Versi tanpa batas jam diuji sebagai pembanding.

→ Diterapkan di: [PLN-01](06-mentor-forex.md#pln-01--pola-n-impuls--koreksi-sempit--tembus).

### [Q-35](09-pertanyaan-untuk-anda.md#q-35--ichimoku-di-mana-stop-loss) · Stop loss Ichimoku

A. Di balik Kijun, ditambah jarak ATR dari Q-11. Rafał: close di bawah Kijun = tanda bahaya ([forex_3 L3475–L3490](../materi/mentah/forex_3.txt#L3475-L3490)). C diuji sebagai pembanding.

→ Diterapkan di: [ICH-01](06-mentor-forex.md#ich-01--tren-penuh-harga-tenkankijun-kumo-chikou), [ICH-02](06-mentor-forex.md#ich-02--retest-kijun), [ICH-03](06-mentor-forex.md#ich-03--pullback-ke-tenkan-dalam-tren-kuat).

### [Q-36](09-pertanyaan-untuk-anda.md#q-36--ichimoku-chikou-digeser-26-atau-25) · Pergeseran Chikou

A. Geser 25 candle (candle sekarang dihitung sebagai 1), untuk Chikou maupun Kumo, sesuai koreksi Rafał ([forex_3 L2449–L2570](../materi/mentah/forex_3.txt#L2449-L2570), [forex_3 L2809–L2835](../materi/mentah/forex_3.txt#L2809-L2835)).

→ Diterapkan di: [06 · bagian B](06-mentor-forex.md#b-ichimoku--rafał-zuchowicz-forex_3) dan [AFS-14](01-alvesting-akademi-crypto.md#afs-14--ichimoku-di-atasbawah-semua-garis) (bot memakai satu perhitungan Ichimoku yang sama).

---

## Bagian 6 — Saham

### [Q-37](09-pertanyaan-untuk-anda.md#q-37--trailing-stop-ko-andri) · Trailing stop

A, tidak. Trailing stop itu untuk investor yang tidak memantau pasar; bot selalu punya SL/TP sendiri.

→ Diterapkan di: [AND-02](05-ko-andri-andre-hakim.md#and-02--trailing-stop-510) (tidak dipakai).

---

## Bagian 7 — Filter waktu

### [Q-38](09-pertanyaan-untuk-anda.md#q-38--apa-efek-filter-waktu-pada-bot) · Efek filter waktu

Sebelum lolos uji: C, hanya dicatat. Kalau lolos:

- Fase bulan, Fibonacci waktu, dan tanggal Astronacci → B, hanya setup pembalikan di tanggal kandidat. Astronacci sendiri memakai tanggal itu sebagai kandidat titik balik yang dikonfirmasi teknikal.
- Angka Hosoda → D. Rafał mengambil untung saat target waktu bertepatan dengan target harga.
- Mercury retrograde → lihat Q-41.

→ Diterapkan di: [07](07-filter-waktu.md#status-opsional-default-mati).

### [Q-39](09-pertanyaan-untuk-anda.md#q-39--fase-bulan) · Fase bulan

1. Uji keduanya: ±1 hari dan ±2 hari.
2. XAUUSD, EURUSD, BTC, ETH.
3. Hanya untuk setup dengan entry di H4 ke atas.

→ Diterapkan di: [WKT-01](07-filter-waktu.md#wkt-01--fase-bulan-new-moon--full-moon).

### [Q-40](09-pertanyaan-untuk-anda.md#q-40--fibonacci-waktu) · Fibonacci waktu

1. D1, titik balik fractal 2–2 (Q-12). Pakai semua titik balik dalam 233 candle D1 terakhir, karena 233 adalah angka Fibonacci terbesar yang dipakai.
2. Toleransi ±1 hari.
3. Ikuti cara di makalah Gema dkk. 2021 (PETA 9.4). Kalau makalahnya tidak tegas, uji dua cara:
   - (a) Hitungan Fibonacci 13, 21, 34, … candle, langsung dari tiap titik balik.
   - (b) Kelipatan Fibonacci (0,382; 0,618; 1; 1,618; 2,618) dari jarak antar-titik balik.

**Catatan penerapan:** makalahnya sudah saya periksa (versi TURCOMAT 12(4), hlm. 1583–1595). Makalah itu **tidak menjelaskan** cara menghitung proyeksi Fibonacci waktu; ia hanya mengelompokkan hari menjadi "proyeksi kurang dari 3" dan "lebih dari 3". Jadi kedua cara (a) dan (b) diuji.

→ Diterapkan di: [WKT-02](07-filter-waktu.md#wkt-02--tumpukan-proyeksi-fibonacci-waktu).

### [Q-41](09-pertanyaan-untuk-anda.md#q-41--mercury-retrograde) · Mercury retrograde

Sebelum lolos uji: C. Kalau terbukti setup breakout lebih sering gagal saat retrograde: A, setup breakout dimatikan selama retrograde.

→ Diterapkan di: [WKT-04](07-filter-waktu.md#wkt-04--mercury-retrograde-sebagai-penanda-waktu-rawan).
