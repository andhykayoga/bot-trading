# 05 · KO ANDRI — Andre Hakim (Saham Master Class)

Ko Andri adalah investor jangka menengah–panjang. Sebagian besar kelasnya membahas memilih saham (PER, PBV, dividen, *market maker*, MSCI, aksi korporasi) dan mental investor. Semua itu **khas saham** dan **tidak dijadikan aturan** (lihat [08](08-tidak-dijadikan-aturan.md)).

Yang diambil adalah prinsip manajemen posisinya, karena berlaku di pasar mana pun.

---

## AND-G1 · Tentukan jenis posisi sejak awal; posisi trading yang rugi di-cut loss

| | |
|---|---|
| Sumber | [AndreHakim_saham_3 L770–L819](../materi/mentah/AndreHakim_saham_3.txt#L770-L819), [AndreHakim_saham_1 L700–L729](../materi/mentah/AndreHakim_saham_1.txt#L700-L729) |
| Pasar | K, F |
| Status | 🟢 |

**Aturan:**

1. Setiap posisi diberi **label sejak dibuka**: scalping (menit–jam), trading (hari–bulan), atau investasi (bulan–tahun).
2. **Scalping & trading yang rugi → cut loss.** Hanya posisi **investasi** yang boleh di-*average down*.
3. Labelnya tidak boleh berubah di tengah jalan: posisi trading yang rugi tidak boleh "diubah jadi investasi".

Untuk bot: semua setup yang dipakai di versi pertama berlabel **scalping** atau **trading** ([D-11](00-aturan-global.md#d-11--label-posisi-scalping-atau-trading)). Label **investasi** hanya untuk modul investasi spot ([KMS-I1–I4](02-kalimasada-akademi-crypto.md#b-modul-investasi-spot-kripto-ditunda), [LIVE-01](03-analis-live-akademi-crypto.md#live-01--siklus-halving-bitcoin-spot-jangka-panjang)), yang ditunda (Q-29). Jadi di versi pertama tidak ada posisi yang boleh di-*average down* (G-04).

---

## AND-G2 · Hanya aset besar & likuid, dan hanya saat ada momentum

| | |
|---|---|
| Sumber | [AndreHakim_saham_3 L820–L860](../materi/mentah/AndreHakim_saham_3.txt#L820-L860), [AndreHakim_saham_3 L1050–L1139](../materi/mentah/AndreHakim_saham_3.txt#L1050-L1139) |
| Pasar | K, F |
| Status | ⚪ (sudah masuk G-08 dan G-09) |

- Analisa teknikal hanya berlaku di aset besar dengan likuiditas tinggi, yang naiknya "organik". Di aset kecil, grafiknya mudah "digambar" pemain besar untuk menipu trader teknikal.
- Scalping hanya di aset yang ramai; di aset sepi akan rugi.
- Ko Andri sendiri scalping/trading **tidak setiap hari**, hanya saat ada momentum: "jangan dipaksa, jangan overtrade".
- Keputusan TP dan cut loss harus berdasarkan fakta, bukan perasaan ([AndreHakim_saham_1 L1030–L1050](../materi/mentah/AndreHakim_saham_1.txt#L1030-L1050)).

---

## AND-02 · Trailing stop 5–10%

| | |
|---|---|
| Sumber | [AndreHakim_saham_1 L690–L705](../materi/mentah/AndreHakim_saham_1.txt#L690-L705) |
| Pasar | K (spot), asalnya saham |
| Status | ⏸ tidak dipakai (Q-37) |

**Aturan dari mentor:** bagi yang tidak memantau pasar sepanjang hari, pasang **trailing stop 5% sampai 10%**. Kalau harga naik, stop ikut naik; kalau harga turun sejauh itu, posisi otomatis terjual.

**Kenapa tidak dipakai (Q-37):** trailing stop itu untuk investor yang tidak memantau pasar; bot selalu punya SL dan TP sendiri.

---

## AND-03 · Patokan kinerja

| | |
|---|---|
| Sumber | [AndreHakim_saham_1 L1430–L1459](../materi/mentah/AndreHakim_saham_1.txt#L1430-L1459), [AndreHakim_saham_1 L2388–L2442](../materi/mentah/AndreHakim_saham_1.txt#L2388-L2442) |
| Status | ⚪ (dipakai sebagai alat evaluasi, lihat G-14) |

- Target kinerja **minimal 20% per tahun**.
- Untung hanya boleh ditarik kalau kinerja di atas 20%, sebagai disiplin.

Untuk bot: angka 20%/tahun bisa dipakai sebagai salah satu patokan lulus/tidaknya hasil backtest, **selain** batas risiko (G-01) dan rugi beruntun yang wajar (G-14).
