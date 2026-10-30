# Panduan: sinyal masuk ke Telegram

Tiap pagi 07.15 WIB, GitHub menjalankan `scripts/sinyal_harian.py` (jadwal di `.github/workflows/sinyal-harian.yml`)
lalu mengirim pesan ke Telegram Anda. Gratis, tidak perlu komputer Anda menyala.

**Isi pesan: semua bertanda skor 0–100** (cara menghitungnya di [`SKOR_STRATEGI.md`](SKOR_STRATEGI.md)), supaya Anda
yang memilih:

| Sinyal | Skor | Kapan |
|---|---|---|
| Trailing stop 10% BTC/ETH | 100 | jual saat turun 10% dari puncak, beli lagi saat tembus tertinggi 20 hari |
| Trailing stop 5% BTC/ETH | 100 | sama, dengan jarak 5% (lebih sering) |
| Rata-rata 200 hari BTC/ETH | 100 | pegang selama harga di atas rata-rata 200 hari |
| Cicil 5× RSI mingguan BTC/ETH | 87 | tiap Senin: beli 1/5 kalau RSI mingguan di bawah 30, jual 1/5 kalau di atas 70 |
| IPO: pesan, lalu jual di hari pertama | 100 | saat masa pemesanan dibuka dan saat hari listing |
| Info ganti pengendali (backdoor) | 49 | saat ada pengumuman BEI; di uji tidak lebih baik dari IHSG |

Pilih **satu** aturan kripto dan ikuti terus. Papan skor di tiap pesan menunjukkan posisi semua aturan dan seberapa
jauh dari sinyal berikutnya.

**Kapan pesan masuk:** ada sinyal di atas, tiap Senin (laporan mingguan dan ringkasan jurnal), atau bot gagal
mengambil data. Hari lain tidak ada pesan, artinya tidak ada yang perlu dilakukan.

**Jurnal otomatis:** tiap sinyal dicatat di `jurnal/sinyal.csv` di GitHub. Di bawah pesan ada tombol **✅** (saya
jalankan) dan **❌** (saya lewati); jawaban Anda dicatat paling lambat jam 07.15 atau 19.15 berikutnya. Tekan dalam 24
jam. Untuk menilai jurnal: minta saya menjalankan `scripts/nilai_jurnal.py`, atau jalankan sendiri. Di bawah 30
transaksi selesai, hasilnya belum bisa disimpulkan (aturan trailing stop memberi ±25 sinyal setahun untuk BTC+ETH).

## Pasang sekali (±10 menit)

**1. Buat bot Telegram**

1. Di Telegram, cari **@BotFather** (centang biru), tekan Start.
2. Ketik `/newbot`, beri nama (misalnya `Sinyal Andhyka`), lalu username yang berakhiran `bot`
   (misalnya `sinyal_andhyka_bot`).
3. BotFather membalas dengan **token** (bentuknya seperti `123456789:AAH...`). Simpan, jangan dibagikan ke siapa pun,
   termasuk di chat ini.
4. Buka bot baru Anda (klik tautan dari BotFather) dan tekan **Start**. Bot tidak bisa mengirim pesan sebelum Anda
   menekan Start.

**2. Cari chat id Anda**

Cari **@userinfobot** di Telegram, tekan Start. Ia membalas angka `Id` (misalnya `123456789`). Itu chat id Anda.

**3. Simpan keduanya di GitHub**

1. Buka github.com/andhykayoga/bot-trading → **Settings** → **Secrets and variables** → **Actions**.
2. **New repository secret**: nama `TELEGRAM_BOT_TOKEN`, isi token dari langkah 1.
3. **New repository secret** lagi: nama `TELEGRAM_CHAT_ID`, isi angka dari langkah 2.

**4. Gabungkan ke branch utama**

Jadwal otomatis GitHub hanya berjalan dari branch utama (`main`). Kode ini ada di branch
`claude/confident-newton-sa3u9i`, jadi perlu digabung sekali lewat *pull request* (tinggal klik **Merge**).

**5. Coba kirim**

Repo → tab **Actions** → **Sinyal harian ke Telegram** → **Run workflow** → **Run**. Dalam 1–2 menit pesan contoh
masuk ke Telegram. Kalau tidak masuk, buka hasil run di tab yang sama; pesan galatnya tertulis di sana.

## Aplikasi untuk eksekusi

**Kripto** (pilih yang terdaftar di OJK; cek daftar terbaru di situs OJK):

| Aplikasi | Catatan |
|---|---|
| Indodax | Exchange terbesar di Indonesia; ada stop-limit order. |
| Tokocrypto | Grup Binance; pasangan BTC/USDT dan ETH/USDT. |
| Pintu | Paling sederhana untuk pemula. |
| Pluang | Ada order Stop dan Stop-Limit di mode Pro. |

Belum ada satu pun aplikasi kripto berizin OJK di atas yang terbukti punya order **trailing stop** otomatis.
Binance, KuCoin, dan MEXC punya, tetapi tidak berizin di Indonesia. **Itu tidak masalah**, karena:

- Aturan yang diuji memakai **harga penutupan harian**. Trailing stop di aplikasi memakai harga detik itu, jadi bisa
  terpicu oleh turun sesaat lalu naik lagi. Hasilnya beda dengan yang diuji.
- Aturan ini juga punya sinyal **beli lagi**, dan tidak ada aplikasi yang bisa melakukannya otomatis.

Jadi cukup ikuti pesan Telegram: saat ada JUAL, jual ke USDT dengan *market order*; saat ada BELI, beli dengan
USDT. Bot yang menghitung trailing stop-nya tiap pagi.

**Saham** (untuk ikut e-IPO): Stockbit, Ajaib, IPOT, dan Bions punya menu e-IPO. Ajaib dan M-Stock (Mirae) juga punya
order trailing stop untuk saham, tetapi belum ada aturan beli saham yang lolos uji, jadi fitur itu belum dibutuhkan.
