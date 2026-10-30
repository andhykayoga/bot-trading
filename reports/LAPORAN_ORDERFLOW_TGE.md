# Laporan: order flow dan token baru (TGE)

Ditulis 29 Oktober 2026. Aturan diuji persis seperti yang dikunci lebih dulu di `reports/RENCANA_ORDERFLOW_TGE.md` (di-commit sebelum hasil dihitung). Bagian yang tidak dijelaskan mentor saya lengkapi dari riset dan pemberitaan, dengan sumber yang dicantumkan.

## Ringkasan

| Modul | Hasil | Artinya |
|---|---|---|
| Order flow AFS-22D: candle berlawanan dengan delta di zona | belum bisa dinilai: semua varian rugi 83–99% di data penyusunan | jangan dipakai |
| Order flow AFS-22F: delta sebagai filter 4 setup | 1 dari 4 lolos tipis (+0,3% dalam ±2 tahun); di periode lain filter justru menurunkan hasil | tidak ada keunggulan nyata |
| Token baru LIVE-02 (24 token) | tidak lolos: rata-rata -3,5%, median -1,9% per token | aturan mentor tidak menghasilkan untung |

Temuan terpenting justru dari pembandingnya. Token baru di Binance 2023–2025 dibuka rata-rata di 4,8× harga yang dibayar investor terakhir (median). Kalau dibeli saat listing dan ditahan setahun, 20 dari 24 token turun, dengan median -88%. "Lantai" valuasi investor juga tidak menahan harga: 18 dari 24 token pernah jatuh di bawah lantai dalam dua tahun.

## A. Order flow (AFS-22, Alvesting)

### Yang saya lengkapi dari riset

Mentor hanya menjelaskan cara membaca delta, tanpa entry, SL, dan TP. Dua penelitian yang saya pakai:

- [Cont, Kukanov & Stoikov (2014)](https://arxiv.org/abs/1011.6402): ketidakseimbangan beli-jual agresif menjelaskan gerak harga **pada saat yang sama**, bukan ke depan.
- [Kim & Hansen (2026)](https://arxiv.org/abs/2607.09426), data perpetual Binance 2021–2024: ketidakseimbangan di awal tiap 15 menit memang meramal arah 4–12 jam ke depan, tetapi besarnya ±0,5 bp, kira-kira sepersepuluh biaya transaksi. Penulisnya sendiri menyebut ini bukan strategi yang berdiri sendiri.

Karena itu delta saya pakai sebagai **konfirmasi** di titik yang sudah punya alasan (zona support/resistance, atau sinyal setup tren/breakout yang sudah ada), di timeframe H1/H4. Data: candle 1 jam spot Binance BTC & ETH 2017–2026 beserta volume beli taker. Data footprint per level harga tidak dipakai karena ukurannya puluhan GB per bulan, jadi imbalance 300%, stacked imbalance, dan HVN tidak diuji.

### AFS-22D · candle merah + delta positif di support (dan kebalikannya di resistance)

Masuk di open candle berikutnya, SL di luar ujung candle sinyal ± sl_atr × ATR, TP 2R. Pemilihan memakai aturan G-17 yang sama dengan setup lain.

| Timeframe | sl_atr | Transaksi penyusunan | Hasil penyusunan | Transaksi pemilihan | Hasil pemilihan |
|---|---|---|---|---|---|
| H1 | 1,0 | 3968 | -98,6% | 1210 | -80,3% |
| H4 | 1,0 | 1174 | -86,7% | 379 | -13,2% |
| H4 | 0,5 | 1976 | -94,2% | 600 | -44,2% |
| H4 | 1,5 | 749 | -82,6% | 261 | +5,0% |

Status: **belum bisa dinilai**, karena tidak ada varian yang untung di data penyusunan. Semua varian rugi 83–99% di 2017–2023. Satu varian (H4, sl_atr 1,5) untung +5% di data pemilihan, tetapi setelah rugi 83% di data sebelumnya; itu kebetulan, bukan pola. Uji akhir tidak dijalankan.

### AFS-22F · delta sebagai filter setup yang sudah ada

Long hanya kalau delta candle sinyal positif, short hanya kalau negatif. Parameter setup tidak diubah.

| Setup | Penyusunan (tanpa → dengan) | Pemilihan (tanpa → dengan) | Uji akhir (transaksi) | Syarat lolos |
|---|---|---|---|---|
| AFS-16T (Supertrend tren) | +72,3% → +71,1% | +33,4% → +28,6% | -12,8% (51) → -16,1% (51) | tidak lolos |
| AFS-18 (breakout) | +40,1% → +25,4% | +17,6% → +9,9% | -4,8% (28) → -1,0% (36) | tidak lolos |
| AFS-20B (breakout) | +43,7% → +23,4% | +6,8% → +8,3% | -22,0% (27) → -15,5% (27) | tidak lolos |
| HKI-01-H4 (tren Ko Hengki) | +46,1% → +44,1% | +15,1% → +10,6% | -1,4% (40) → +0,3% (37) | lolos (tipis) |

Satu dari empat lolos secara teknis: HKI-01-H4 berubah dari −1,4% menjadi +0,3% di uji akhir. Tetapi:

- +0,3% dalam hampir dua tahun itu praktis impas, jauh di bawah bunga deposito.
- Di data penyusunan dan pemilihan, filter delta justru **menurunkan** hasil di hampir semua setup (termasuk HKI-01-H4: 46,1% → 44,1% dan 15,1% → 10,6%). Kalau delta benar-benar membantu, hasilnya harus naik di semua periode, bukan hanya di satu periode.
- Dengan empat percobaan, satu yang lolos tipis sangat mungkin kebetulan.

**Kesimpulan order flow:** delta candle (versi yang bisa diuji dari data publik) tidak memberi keunggulan yang bisa dipakai, sejalan dengan riset di atas: informasinya sudah langsung tercermin di harga.

## B. Token baru / TGE (LIVE-02)

### Aturan yang diuji

Dari mentor: tunggu listing spot; **lantai** = valuasi investor terakhir ÷ jumlah token; masuk 30% di harga listing, 70% di base dekat lantai; cut loss di bawah lantai; target dari FDV. Yang saya lengkapi (dikunci di `reports/RENCANA_ORDERFLOW_TGE.md` sebelum hasil dihitung): harga listing = close hari pertama di Binance; base = harga ≤ 50% harga listing, ≤ 1,3 × lantai, dan tidak mencetak low baru selama 14 hari; cut loss di close < 0,833 × lantai; target di close ≥ 3,33 × lantai; maksimal 730 hari; biaya 0,2% per transaksi.

### Data valuasi (dikumpulkan dari pemberitaan, tiap angka ada sumbernya)

Dari 175 pasangan USDT yang mulai diperdagangkan di Binance antara Januari 2023 dan Juni 2025, hanya **24 token** yang valuasi putaran investornya bisa diverifikasi dari berita (The Block, TechCrunch, Fortune, Decrypt, laporan Arrakis); daftar dan sumbernya di `bot/research/tge_valuasi.csv`. 33 proyek lain sudah saya cari tetapi valuasinya tidak diumumkan atau hanya dari satu sumber yang lemah: ZK, MOVE, ETHFI, DYM, ALT, TNSR, AEVO, JTO, CYBER, ARKM, ID, USUAL, VANA, BABY, SOPH, SAHARA, PARTI, HYPER, BB, PORTAL, PIXEL, HUMA, RESOLV, MAV, LISTA, KERNEL, GPS, SIGN, KAITO, RED, WCT, NTRN, NFP. Sisanya kebanyakan bukan TGE (token lama yang baru masuk Binance, stablecoin, ganti nama) atau koin meme/komunitas tanpa investor. Beberapa token TGE lain tidak sempat dicari (mis. EDU, XAI, AI, ACE, BANANA, GUN, HOME, NEWT, HAEDAL).

Untuk token yang jumlahnya terus bertambah (inflasi, tanpa batas maksimum), saya pakai jumlah token saat TGE, karena itu dasar harga yang dibayar investor. Tanda * = putaran sesudahnya tidak mengumumkan valuasi, jadi yang dipakai valuasi terakhir yang diketahui.

### Hasil per token

| Token | Listing | Valuasi | Lantai ($) | Harga listing ($) | Listing ÷ lantai | Beli base | Keluar | Hasil aturan | Beli-tahan 365 hari | BTC 365 hari |
|---|---|---|---|---|---|---|---|---|---|---|
| [ARB](https://www.theblock.co/post/116148) | 2023-03-23 | $1,2 M | 0,120 | 1,32 | 11,0× | – | target (2023-03-25) | -1% | +21% | +125% |
| [SUI](https://www.theblock.co/post/168532/mysten-labs-sui-blockchain-fundraise-ftx-ventures) | 2023-05-03 | $2 M | 0,200 | 1,40 | 7,0× | – | target (2023-05-05) | -2% | -20% | +103% |
| [WLD](https://decrypt.co/142308/sam-altman-worldcoin-115-million-blockchain-capital)* | 2023-07-24 | $3 M | 0,300 | 2,16 | 7,2× | – | target (2023-07-26) | +1% | +0% | +125% |
| [SEI](https://techcrunch.com/2023/04/11/trading-focused-blockchain-sei-raises-30m-bringing-valuation-up-to-800m/) | 2023-08-15 | $800 jt | 0,0800 | 0,179 | 2,2× | – | target (2023-11-29) | +17% | +57% | +101% |
| [TIA](https://www.theblock.co/post/177841) | 2023-10-31 | $1 M | 1,00 | 2,28 | 2,3× | – | target (2023-11-12) | +22% | +108% | +108% |
| [MANTA](https://techcrunch.com/2023/07/19/team-behind-crypto-privacy-protocol-manta-network-is-now-valued-at-500m/) | 2024-01-18 | $500 jt | 0,500 | 2,17 | 4,3× | – | target (2024-01-20) | +2% | -62% | +151% |
| [STRK](https://www.theblock.co/post/148672/starkware-raises-series-d-funding-8-billion-valuation) | 2024-02-20 | $8 M | 0,800 | 1,97 | 2,5× | 2024-06-15 | cut loss (2024-06-29) | -41% | -89% | +85% |
| [ENA](https://www.coincarp.com/fundraising/ethena-strategic/) | 2024-04-02 | $300 jt | 0,0200 | 0,775 | 38,8× | – | target (2024-04-04) | +14% | -57% | +26% |
| [W](https://fortune.com/crypto/2023/11/29/wormhole-raises-225-million-2-5-billion-valuation-jump-crypto-split) | 2024-04-03 | $2,5 M | 0,250 | 1,31 | 5,2× | – | target (2024-04-05) | -5% | -93% | +26% |
| [SAGA](https://www.theblock.co/post/147770)* | 2024-04-09 | $130 jt | 0,130 | 6,56 | 50,4× | – | target (2024-04-11) | -2% | -96% | +19% |
| [OMNI](https://icodrops.com/omni-network) | 2024-04-17 | $150 jt | 1,50 | 27,14 | 18,1× | – | target (2024-04-19) | -2% | -93% | +38% |
| [REZ](https://forklog.com/en/renzo-raises-3-2-million-in-seed-funding-valued-at-25-million/)* | 2024-04-30 | $25 jt | 0,0025 | 0,160 | 64,0× | – | target (2024-05-02) | -1% | -91% | +55% |
| [IO](https://www.theblockcrypto.com/post/280665/solana-depin-io-net-1-billion-token-valuation-funding) | 2024-06-11 | $1 M | 1,25 | 4,17 | 3,3× | – | target (2024-06-13) | +11% | -81% | +61% |
| [ZRO](https://www.theblock.co/post/224762/layerzero-series-b) | 2024-06-20 | $3 M | 3,00 | 3,43 | 1,1× | – | cut loss (2025-02-25) | -8% | -50% | +59% |
| [EIGEN](https://www.theblock.co/post/278575/andreessen-horowitz-invests-100-million-in-restaking-project-eigenlayer-bloomberg)* | 2024-10-01 | $500 jt | 0,299 | 4,01 | 13,4× | – | target (2024-10-03) | -6% | -62% | +95% |
| [SCR](https://www.theblock.co/post/217340/ethereum-scaling-scroll-50-million-funding-round-1-8-billion-valuation) | 2024-10-11 | $1,8 M | 1,80 | 1,13 | 0,6× | – | cut loss (2024-10-13) | +1% | -85% | +77% |
| [ME](https://techcrunch.com/2022/06/21/magic-eden-raises-130m-hitting-unicorn-status-at-1-6b-valuation/) | 2024-12-10 | $1,6 M | 1,60 | 5,67 | 3,5× | – | target (2024-12-12) | -1% | -95% | -5% |
| [SOLV](https://app.dealroom.co/news/feed/solv-protocol-raises-11m-funding) | 2025-01-17 | $200 jt | 0,0207 | 0,130 | 6,3× | – | target (2025-01-19) | -6% | -90% | -9% |
| [BERA](https://arrakis.finance/blog/lessons-from-h1-2025-top-token-launches) | 2025-02-06 | $1 M | 2,00 | 8,72 | 4,4× | – | target (2025-02-08) | -4% | -94% | -27% |
| [LAYER](https://arrakis.finance/blog/lessons-from-h1-2025-top-token-launches) | 2025-02-11 | $80 jt | 0,0800 | 1,05 | 13,2× | – | target (2025-02-13) | -2% | -92% | -30% |
| [SHELL](https://www.theblock.co/post/285072/web3-ai-platform-myshell-funding)* | 2025-02-27 | $57 jt | 0,0570 | 0,598 | 10,5× | – | target (2025-03-01) | -6% | -95% | -22% |
| [NIL](https://arrakis.finance/blog/lessons-from-h1-2025-top-token-launches) | 2025-03-24 | $400 jt | 0,400 | 0,727 | 1,8× | 2025-05-04 | cut loss (2025-06-15) | -21% | -95% | -20% |
| [INIT](https://www.theblock.co/post/318547/initia-cobie-echo-funding-token-valuation) | 2025-04-24 | $250 jt | 0,250 | 0,755 | 3,0× | – | target (2025-04-26) | +3% | -88% | -18% |
| [SXT](https://arrakis.finance/blog/lessons-from-h1-2025-top-token-launches) | 2025-05-08 | $300 jt | 0,0600 | 0,145 | 2,4× | 2025-06-18 | cut loss (2025-11-04) | -44% | -90% | -23% |

### Ringkasan

| Sampel | Token | Rata-rata | Median | Untung | Rata-rata beli-tahan 365 hari | Median beli-tahan 365 hari | Rata-rata BTC 365 hari | Syarat lolos |
|---|---|---|---|---|---|---|---|---|
| Semua | 24 | -3,5% | -1,9% | 8/24 | -59,7% | -88,2% | +45,8% | tidak lolos |
| Hanya valuasi putaran terakhir (tambahan) | 19 | -3,7% | -1,6% | 7/19 | -57,3% | -87,7% | +43,6% | tidak lolos |

Cara keluar: 19 token target, 5 token cut loss.

### Cara membaca hasilnya

- **16 dari 24 token** sudah listing di atas target (3,33 × lantai). Aturan langsung menjual porsi 30% di hari kedua, jadi hasilnya kecil, antara -6% dan +14%. 3 token lain (SEI, TIA, INIT) naik ke target sesudahnya (+17%, +22%, +3%).
- Hanya **3 token** yang turun cukup dalam sehingga porsi 70% dibeli di "base dekat lantai" (STRK, SXT, NIL). Semuanya lalu kena cut loss (-41%, -44%, -21%) karena harga terus turun menembus lantai.
- *(Tambahan, bukan syarat lolos)* Kalau token yang listing di atas target dilewati saja (tidak dibeli sama sekali), rata-rata per token tetap negatif: -3,0%.
- **Lantai bukan support.** 18 dari 24 token pernah di bawah lantai, dan 17 berada di bawah lantai pada hari ke-730 (atau di data terakhir kalau belum genap dua tahun). Valuasi investor bukan harga yang dijaga siapa pun; investor awal justru sering menjual setelah token mereka terbuka.
- **Pembanding beli saat listing, tahan 365 hari:** rata-rata -60%, median -88%; hanya ARB, SEI, TIA, WLD yang naik. BTC di tanggal yang sama rata-rata +46%. Jadi aturan mentor jauh lebih baik daripada membeli saat listing, terutama karena aturan itu membuat Anda hampir selalu cepat keluar atau tidak masuk sama sekali.

### Catatan kejujuran

- Sampel 24 token hanya sedikit di atas syarat minimum 20. Valuasi yang diberitakan kebanyakan milik proyek besar dan terkenal; token kecil bisa berperilaku lain.
- Sebagian valuasi berasal dari sumber anonim atau agregator (SCR, TIA, ENA, SOLV, OMNI). Valuasi perusahaan juga tidak selalu sama dengan valuasi token. Hasil hanya-valuasi-putaran-terakhir ditampilkan terpisah di atas dan kesimpulannya sama.
- Harga listing = close hari pertama. Candle pertama Binance kadang dimulai dari harga yang tidak bisa didapat (misalnya OMNI dibuka $1 lalu ditutup $27), jadi open hari pertama tidak dipakai.
- Token yang sudah dihapus dari Binance ikut dicari. OMNI masuk sampel; NTRN dan NFP tidak punya valuasi yang bisa diverifikasi.

## Apa artinya untuk Anda

- **Order flow:** untuk BTC/ETH di H1/H4, informasi delta candle sudah tercermin di harga. Tidak perlu membeli alat footprint/order flow untuk tujuan ini.
- **Token baru:** bagian aturan mentor yang berguna adalah bagian **menahan diri**: jangan beli di pre-market atau saat listing kalau harga sudah berkali-kali lipat valuasi investor. Bagian "beli di base dekat lantai" tidak terbukti, karena lantai tidak menahan harga.
- Ini sejalan dengan laporan sebelumnya: yang terbukti tetap aturan sederhana di BTC/ETH (filter tren SMA 200, trailing stop) dan rencana investasi di `reports/RENCANA_UNTUNG.md`.
- **Valuasi Ko Andri dan bandarmologi Ko Hengki** menunggu data saham. Panduannya ada di `reports/PANDUAN_DATA_STOCKBIT.md`.

## Cara mengulang

```bash
python -m bot.data.download orderflow tge
python scripts/run_orderflow_tge.py --orderflow --tge
python scripts/run_orderflow_tge.py
```
