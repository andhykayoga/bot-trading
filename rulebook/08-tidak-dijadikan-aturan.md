# 08 · MATERI YANG TIDAK DIJADIKAN ATURAN

Supaya jelas apa yang sengaja ditinggalkan dan kenapa.

## A. Hanya berlaku di saham (sesuai permintaan Anda)

| Materi | Mentor | Alasan |
|---|---|---|
| Broker summary, kode broker (XC, XL, CC, YP, PD, dll.), "imposter", akumulasi per broker (NeoBDM) | Ko Hengki, Ko Andri | Forex dan kripto tidak punya data kode broker publik. |
| Antrean bid–offer, HAKA/HAKI, "algo asing", antre bid di jam tertentu | Ko Hengki, Ko Andri | Mekanisme antrean bursa saham Indonesia. Analog terdekat di kripto adalah *order flow* ([AFS-22](01-alvesting-akademi-crypto.md#afs-22--sinyal-order-flow)). |
| SID, laporan kepemilikan ≥5% (KSEI), free float, prospektus IPO | Ko Hengki | Data khusus emiten saham. |
| ARA/ARB, FCA, suspensi, saham gocap | Ko Hengki | Aturan khusus Bursa Efek Indonesia. |
| PER, PBV, dividen, *dividend payout ratio*, valuasi | Ko Andri | Valuasi perusahaan. |
| *Market maker* "baik", target masuk MSCI/indeks, aksi korporasi (*rights issue*, *private placement*, *stock split*, *takeover*) | Ko Andri, Ko Hengki | Khas saham. |
| *Moon stock* (saham pilihan dari analisa bandar) | Ko Hengki | Seluruhnya bergantung pada analisa transaksi broker. |

Prinsip umumnya ("ikuti uang besar", "waspada kalau ritel ramai") tetap terwakili lewat setup SMC, Wyckoff, dan filter volume.

## B. Khas kripto, tetapi bukan aturan trading yang bisa diotomasi

| Materi | Alasan |
|---|---|
| Riset naratif (mencari sektor/tema yang akan naik) | Butuh penilaian berita dan tren sosial. |
| Riset fundamental & tokenomics | Butuh penilaian proyek; bukan sinyal harga. |
| On-chain, wallet tracker, DEX, smart contract, keamanan wallet | Bukan bagian dari bot trading di exchange. |
| Elevator concept, pagi–siang–malam, bajing loncat, serigala–domba, tebar jala, terkonsentrasi | Strategi investasi rotasi sektor; aturannya tidak dalam bentuk angka. Yang berbentuk angka sudah masuk [KMS-I1–I4](02-kalimasada-akademi-crypto.md#b-modul-investasi-spot-kripto-ditunda). |
| *Stock-to-flow* | Model valuasi BTC, bukan aturan trading. |
| Gulung-gulung (*compounding* 100%) | Pengajarnya sendiri menyebut sangat berbahaya. |

## C. Pandangan pasar sesaat

Pandangan harga di live market update (BTC "lebih berani beli di 80 ribu", "50 ribu area bagus", target emas, prediksi ETH, dll.) **tidak** dijadikan aturan, karena hanya berlaku pada waktu rekaman. Cara berpikirnya diambil di [03](03-analis-live-akademi-crypto.md).

## D. Psikologi & mental

Seri Money Psychology, Mind Management, dan kelas mental Ko Andri tidak menjadi aturan bot secara langsung. Isinya diterjemahkan menjadi aturan **disiplin** yang memang cocok untuk bot:

- Aturan tetap, tidak berubah karena emosi → G-07.
- Tidak menaikkan ukuran setelah rugi → G-06.
- Tidak mematikan bot hanya karena beberapa kali rugi beruntun → G-14.

## E. Sulit diotomasi (disimpan, ditandai 🔴)

Sudah tercantum di masing-masing file: Elliott Wave (AFS-24), Andrews Pitchfork (AFS-25), momentum akselerasi/deselerasi (AFS-F3), titik A-B-C-D dan "tiga lini masa" Dow, *liquidity pattern* SMC, Wyckoff spring/UTAD (KMS-01), teori gelombang Hosoda.

## F. Bukan trading

Kelas jualan "Sekolah Jalanan" ([AC_crypto_12–19](../materi/PETA.md#i-bukan-trading-kelas-jualan-sekolah-jalanan-timothy-ronald)).

## G. FXcopet (forex_1): tidak dipakai

**Alasan (keputusan Anda, Q-31):** bukan dari mentor utama Anda, dan indikatornya tidak diketahui. File indikator "copet"/"kompas" tidak ada di repo, dan cara indikator itu menggambar garis merah/aqua serta setting TMA-nya tidak dijelaskan di video.

Karena FXcopet di-skip, pertanyaan teknik "recover" (Q-32) dan jam tutup (Q-33) tidak relevan lagi. Aturan setup-nya disimpan di bawah hanya sebagai **arsip**, supaya tidak perlu dicari ulang dari transkrip. Bot **tidak** memakainya.

### FXC-01 · Tembus garis merah/aqua, EURUSD M1 (arsip)

| | |
|---|---|
| Sumber | Aturan akhir: [forex_1 L3295–L3450](../materi/mentah/forex_1.txt#L3295-L3450); sesi live: [forex_1 L331–L3245](../materi/mentah/forex_1.txt#L331-L3245) |
| Pasar | F — hanya EURUSD |
| Timeframe | M1 saja ("nggak perlu lihat timeframe lain") ([forex_1 L3305–L3314](../materi/mentah/forex_1.txt#L3305-L3314)) |
| Status | Tidak dipakai |

**Alat:** indikator "copet" milik FXcopet: garis horizontal otomatis **merah** (atas) dan **aqua** (bawah) sebagai batas sideways ([forex_1 L731–L790](../materi/mentah/forex_1.txt#L731-L790), [forex_1 L811–L830](../materi/mentah/forex_1.txt#L811-L830)), plus **TMA** (*Triangular Moving Average*) dengan pita ([forex_1 L299–L310](../materi/mentah/forex_1.txt#L299-L310), [forex_1 L431–L445](../materi/mentah/forex_1.txt#L431-L445)).

**Ringkasan aturan dari mentor:**

- **Syarat:** garis merah dan aqua sudah terbentuk ([forex_1 L1011–L1029](../materi/mentah/forex_1.txt#L1011-L1029)); jaraknya maksimal 15 pip ([forex_1 L3355–L3374](../materi/mentah/forex_1.txt#L3355-L3374)); sesi Eropa, atau sesi Asia kalau sesi Eropa tidak ada sinyal ([forex_1 L3435–L3444](../materi/mentah/forex_1.txt#L3435-L3444)); tidak ada berita besar ([forex_1 L545–L579](../materi/mentah/forex_1.txt#L545-L579)); buy di area pita bawah TMA, sell di pita atas ([forex_1 L1101–L1115](../materi/mentah/forex_1.txt#L1101-L1115)).
- **Entry:** tembus garis merah ke atas → buy; tembus garis aqua ke bawah → sell ([forex_1 L3314–L3334](../materi/mentah/forex_1.txt#L3314-L3334)).
- **TP:** minimal 10 pip ([forex_1 L3334–L3350](../materi/mentah/forex_1.txt#L3334-L3350)), atau garis horizontal berikutnya dikurangi spread ([forex_1 L611–L620](../materi/mentah/forex_1.txt#L611-L620)), atau tutup manual di "penutupan sesi Eropa, jam 5.00 sampai 6.00 WIB" ([forex_1 L3350–L3364](../materi/mentah/forex_1.txt#L3350-L3364)).
- **SL:** garis horizontal berlawanan ± spread ([forex_1 L391–L400](../materi/mentah/forex_1.txt#L391-L400), [forex_1 L695–L705](../materi/mentah/forex_1.txt#L695-L705)).
- **Frekuensi:** maksimal 2 transaksi sehari; berhenti setelah sekali TP ([forex_1 L645–L659](../materi/mentah/forex_1.txt#L645-L659)).
- **Teknik "recover":** setelah kena SL, buka arah sebaliknya dengan target 2× kerugian ([forex_1 L3405–L3430](../materi/mentah/forex_1.txt#L3405-L3430)). Bertentangan dengan larangan revenge trading ([G-06](00-aturan-global.md#g-06--dilarang-revenge-trading)), tanpa SL, dan mirip martingale.
- **Catatan:** data dari 2012; klaim hasil "hampir 70%" tanpa data tingkat menang ([forex_1 L3255–L3265](../materi/mentah/forex_1.txt#L3255-L3265)).

## H. Ditunda di versi pertama (sesuai jawaban Anda)

Materi berikut tetap ada di file masing-masing dengan label ⏸, tetapi **tidak dipakai** bot versi pertama.

| Materi | Alasan | Jawaban |
|---|---|---|
| Pola harmonic XABCD ([AFS-11](01-alvesting-akademi-crypto.md#afs-11--pola-harmonic-xabcd)) | Hanya ABCD dan double/triple top-bottom yang dipakai. | Q-23 |
| Pola grafik klasik selain double/triple top-bottom ([AFS-23](01-alvesting-akademi-crypto.md#afs-23--pola-grafik-klasik)) | Sama. | Q-23 |
| Screening altcoin & korelasi BTC ([AFS-F1](01-alvesting-akademi-crypto.md#afs-f1--screening-altcoin--korelasi-btc)) | Hanya BTC dan ETH. | Q-25 |
| Modul investasi spot Kalimasada ([KMS-I1–I4](02-kalimasada-akademi-crypto.md#b-modul-investasi-spot-kripto-ditunda)) | Versi pertama hanya trading. | Q-29 |
| Siklus halving ([LIVE-01](03-analis-live-akademi-crypto.md#live-01--siklus-halving-bitcoin-spot-jangka-panjang)) | Bot tidak mengelola investasi jangka panjang. | Q-27 |
| Token baru / TGE ([LIVE-02](03-analis-live-akademi-crypto.md#live-02--token-baru-tge-30-saat-listing-70-di-base)) | Tidak dipakai. | Q-30 |
| Trailing stop 5–10% ([AND-02](05-ko-andri-andre-hakim.md#and-02--trailing-stop-510)) | Untuk investor yang tidak memantau pasar; bot selalu punya SL/TP sendiri. | Q-37 |
| Futures kripto | Baru dipertimbangkan setelah lolos demo, lewat exchange berizin OJK. | Q-03 |
| Data volume bursa berjangka CME untuk forex | Tick volume dipakai dulu. | Q-14 |
