# 04 · KO HENGKI — Remora

Inti ajaran Ko Hengki adalah **analisa transaksi** (bandarmologi): kode broker, broker summary, antrean bid–offer, data SID/KSEI, "imposter", "algo asing". Semua itu **khas pasar saham Indonesia** dan datanya tidak ada di forex maupun kripto, jadi **tidak dijadikan aturan** (lihat [08](08-tidak-dijadikan-aturan.md)).

Yang diambil hanya bagian yang ia sebut sebagai **dasar teknikal**, yaitu **harga & volume** dan cara memakai tren. Ia sendiri bilang bisa trading tanpa candlestick dan tanpa bandarmologi, tetapi **tidak bisa tanpa harga dan volume** ([Remora_saham_11 L1610–L1625](../materi/mentah/Remora_saham_11.txt#L1610-L1625)).

---

## HKI-F1 · "Naik bervolume, koreksi tanpa volume"

| | |
|---|---|
| Sumber | [Remora_saham_11 L3870–L3899](../materi/mentah/Remora_saham_11.txt#L3870-L3899), [Remora_saham_11 L3960–L3999](../materi/mentah/Remora_saham_11.txt#L3960-L3999) |
| Pasar | K, F\* |
| Status | ⚪ 🟡 |

**Aturan:** tren naik dianggap **sehat** kalau:

1. Saat harga naik, volume ikut naik.
2. Saat harga koreksi, volume mengecil.

Pola ini menandakan pemain besar belum menjual. Ikuti arahnya: koreksi yang sehat adalah kesempatan masuk. Kalau harga terus gagal menembus suatu level dan volumenya hilang, perhatikan; begitu volume muncul lagi dan menembus, lanjut ([Remora_saham_11 L3970–L3999](../materi/mentah/Remora_saham_11.txt#L3970-L3999)).

Ini sejalan dengan VSA Kalimasada ([KMS-F1](02-kalimasada-akademi-crypto.md#kms-f1--filter-vsa-volume-vs-ukuran-candle)).

**Belum jelas:** ukuran "volume naik/mengecil" → **Q-26**; volume forex → **Q-14**.

---

## HKI-F2 · Breakout pola harus bervolume

| | |
|---|---|
| Sumber | [Remora_saham_11 L3680–L3699](../materi/mentah/Remora_saham_11.txt#L3680-L3699) |
| Pasar | K, F\* |
| Status | ⚪ 🟡 |

**Aturan:** pola seperti *cup*, *sideways breakout*, *bottoming rebound*, double bottom **harus tembus dengan volume**. "Kalau break-nya nggak dengan volume, kalian jangan pakai."

Sama dengan [AFS-F2](01-alvesting-akademi-crypto.md#afs-f2--konfirmasi-volume-untuk-breakout) dan prinsip Dow Theory.

---

## HKI-01 · Ikuti tren sekunder & minor, keluar saat struktur patah

| | |
|---|---|
| Sumber | [Remora_saham_11 L1975–L2109](../materi/mentah/Remora_saham_11.txt#L1975-L2109) |
| Pasar | K, F |
| Status | 🟡 |

**Aturan:**

1. Hanya main aset yang sedang **naik** (*uptrend*).
2. Untuk dana yang belum besar, pakai **tren sekunder dan minor**, bukan tren mayor (sulit ditahan) ([Remora_saham_11 L2005–L2020](../materi/mentah/Remora_saham_11.txt#L2005-L2020)).
3. Ko Hengki memakai **dua akun terpisah**: satu untuk tren sekunder (dikumpulkan dan ditahan, "bonus tahunan"), satu untuk tren minor (diambil cepat setiap naik, "gajian") ([Remora_saham_11 L2075–L2100](../materi/mentah/Remora_saham_11.txt#L2075-L2100)).
4. **Keluar** saat tren patah (*break of structure*) ([Remora_saham_11 L1995–L2005](../materi/mentah/Remora_saham_11.txt#L1995-L2005)).

**Dua gaya masuk** — keduanya sah, soal karakter ([Remora_saham_10 L2530–L2545](../materi/mentah/Remora_saham_10.txt#L2530-L2545)):

| Gaya | Kelebihan | Kekurangan |
|---|---|---|
| **Buy on weakness** (beli saat koreksi ke support) | Lebih pasti, ruang untung lebih besar | Harus menunggu |
| **Buy on breakout** | Tidak perlu menunggu, cepat | Ruang lebih sedikit, lebih volatil |

**Checklist entry** yang ia sebut: support + volume + pola + RR. Kalau tembus sedikit di bawah support, *cut* ([Remora_saham_11 L3985–L3999](../materi/mentah/Remora_saham_11.txt#L3985-L3999), [Remora_saham_11 L4090–L4095](../materi/mentah/Remora_saham_11.txt#L4090-L4095)).

**Belum jelas:**

- Batas tren mayor/sekunder/minor dalam timeframe tidak disebut → **Q-12**. Gaya masuk mana yang dipakai bot → **Q-09**.
- Besar *cut loss*: Ko Hengki bilang tergantung karakter masing-masing (3%? 5%?) ([Remora_saham_14 L2040–L2049](../materi/mentah/Remora_saham_14.txt#L2040-L2049)) → mengikuti G-01/G-02.

---

## Catatan lain dari Ko Hengki (konteks, bukan aturan)

- **Breakdown palsu vs asli.** Menembus support pelan-pelan lalu naik lagi = bukan breakdown. Breakdown yang asli cepat dan kasar, sering melompat jauh dari angka psikologis ([Remora_saham_14 L2585–L2645](../materi/mentah/Remora_saham_14.txt#L2585-L2645)). Juga: support yang jebol **tanpa volume** sering justru jebakan/akumulasi ([Remora_saham_11 L3750–L3850](../materi/mentah/Remora_saham_11.txt#L3750-L3850)). Ia mengaitkannya dengan perilaku pemain besar di saham Indonesia. Logika serupa di kripto/forex adalah *stop hunt* ([AFS-06](01-alvesting-akademi-crypto.md#afs-06--stop-hunt--break-of-structure)) dan *spring* ([KMS-01](02-kalimasada-akademi-crypto.md#kms-01--wyckoff-spring--utad--reclaim)).
- **Probabilitas, bukan kemungkinan.** Dengan harga–volume, support/resistance, dan pola, peluang menang di atas 50% (±55%) sudah cukup. Jangan main 50:50 ([Remora_saham_11 L1490–L1509](../materi/mentah/Remora_saham_11.txt#L1490-L1509), [Remora_saham_11 L4040–L4059](../materi/mentah/Remora_saham_11.txt#L4040-L4059)).
- **Terlalu banyak indikator** membuat bingung dan subjektif (sudah masuk G-11).
- **Candlestick** hanya ±10% bobot analisanya ([Remora_saham_11 L1600–L1609](../materi/mentah/Remora_saham_11.txt#L1600-L1609)).
