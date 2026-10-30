"""Uji saham backdoor / ganti pengendali (reports/RENCANA_IPO_BACKDOOR.md bagian B).

Beli di penutupan hari bursa pertama setelah publik tahu siapa pengendali barunya, tahan 250 (dan 500) hari bursa,
dibanding IHSG. Daftar peristiwa di bot/research/backdoor_peristiwa.csv (dari berita, dibekukan sebelum harga diunduh).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from bot.research import ipo

ROOT = Path(__file__).resolve().parents[2]
PERISTIWA = ROOT / "bot" / "research" / "backdoor_peristiwa.csv"
HARGA = ROOT / "data" / "backdoor" / "harga"
MULAI, AKHIR = pd.Timestamp("2023-08-01"), pd.Timestamp("2025-10-29")   # arsip BEI baru mulai Agustus 2023
BATAS_KOHORT = pd.Timestamp("2024-10-01")


PENGUMUMAN = ROOT / "data" / "backdoor" / "pengumuman"
LAMPIRAN = ROOT / "data" / "backdoor" / "lampiran"
KATA = r"pengendali|pengambilalihan|pengambil alihan|tender wajib|tender sukarela|negosiasi"
BUKAN = (r"tidak (?:menyebabkan|mengubah|mengakibatkan)(?: adanya)?(?: perubahan)? pengendali|pasar negosiasi"
         r"|perkara hukum|waran")


def kandidat() -> pd.DataFrame:
    """Pengumuman BEI yang judulnya menyinggung ganti pengendali, tanpa yang jelas bukan (lihat BUKAN)."""
    d = pd.concat([pd.read_parquet(f) for f in sorted(PENGUMUMAN.glob("*.parquet"))], ignore_index=True)
    d["tanggal"] = pd.to_datetime(d.tanggal)
    j = d.judul.str.replace(r"\s+", " ", regex=True)
    d = d[j.str.contains(KATA, case=False) & ~j.str.contains(BUKAN, case=False) & (d.kode.str.len() == 4)]
    return d.drop_duplicates(["kode", "judul", "tanggal"]).sort_values(["kode", "tanggal"]).reset_index(drop=True)


def teks_lampiran(lampiran_json: str) -> str:
    """Unduh lampiran PDF pengumuman (lewat idx.id) dan ubah ke teks; disimpan supaya tidak diunduh ulang."""
    import json
    import subprocess
    import urllib.request
    LAMPIRAN.mkdir(parents=True, exist_ok=True)
    out = []
    for nama, url in json.loads(lampiran_json):
        url = url.replace("www.idx.co.id", "www.idx.id")
        f = LAMPIRAN / url.rsplit("/", 1)[-1]
        if not f.exists():
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                f.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            except Exception:  # noqa: BLE001 - lampiran hilang: lewati
                continue
        t = f.with_suffix(".txt")
        if not t.exists():
            subprocess.run(["pdftotext", "-layout", str(f), str(t)], capture_output=True)
        if t.exists():
            out.append(f"[{nama}]\n" + t.read_text(errors="ignore"))
    return "\n".join(out)


def baca_peristiwa() -> pd.DataFrame:
    d = pd.read_csv(PERISTIWA, parse_dates=["tanggal"])
    return d[(d.tanggal >= MULAI) & (d.tanggal <= AKHIR)].sort_values("tanggal").reset_index(drop=True)


def siap() -> bool:
    return PERISTIWA.exists() and (HARGA / "IHSG.parquet").exists()


def harga(kode: str) -> pd.DataFrame | None:
    f = HARGA / f"{kode}.parquet"
    return pd.read_parquet(f).set_index("t") if f.exists() else None


def satu(r, ihsg: pd.Series) -> dict:
    out = {"kode": r.kode, "tanggal": r.tanggal, "pengendali_baru": r.pengendali_baru, "kuat": bool(r.kuat)}
    p = harga(r.kode)
    if p is None or p.empty:
        return {**out, "ada_harga": False}
    setelah = p[(p.index > r.tanggal) & (p.v > 0)]             # disuspensi saat itu: tunggu transaksi pertama
    if setelah.empty:
        return {**out, "ada_harga": False}
    masuk = setelah.index[0]
    return {**out, "ada_harga": True, "masuk": masuk, "harga_masuk": setelah.c.iloc[0],
            **ipo.tahan(p, ihsg, masuk, (250, 500))}


def hitung_semua() -> pd.DataFrame:
    ihsg = harga("IHSG").c
    return pd.DataFrame([satu(r, ihsg) for r in baca_peristiwa().itertuples()])


def setelah_ara() -> pd.DataFrame:
    """Pembanding (tidak menentukan lolos): beli di penutupan pertama yang tidak terkunci ARA. Terkunci = tutup di
    harga tertinggi dan naik ≥ 9,5% (batas terkecil, Papan Pemantauan Khusus 10%), karena saham kecil sering ARA
    beruntun setelah berita sehingga tidak bisa dibeli di penutupan hari pertama."""
    ihsg, rows = harga("IHSG").c, []
    for r in baca_peristiwa().itertuples():
        p = harga(r.kode)
        s = p[(p.index > r.tanggal) & (p.v > 0)]
        naik = s.c / p.c.shift(1).reindex(s.index) - 1
        bebas = ~((s.c >= s.h * (1 - 1e-9)) & (naik >= 0.095))
        masuk = s.index[int(bebas.to_numpy().argmax())] if bebas.any() else s.index[-1]
        rows.append({"kode": r.kode, "hari_ara": int((s.index < masuk).sum()), **ipo.tahan(p, ihsg, masuk, (250,))})
    return pd.DataFrame(rows)


# Contoh yang sering diceritakan Ko Andri (dipilih justru karena terkenal; hanya ilustrasi): tanggal berita pertama.
CONTOH = {"ARTO": ("2019-08-22", "Jerry Ng dan Patrick Walujo (Bank Jago)"), "BBHI": ("2020-11-02", "CT Corp (Allo Bank)"),
          "PANI": ("2021-10-08", "Agung Sedayu (PIK 2)")}


def contoh_terkenal() -> list[str]:
    ihsg, out = harga("IHSG").c, []
    for kode, (tgl, siapa) in CONTOH.items():
        p = harga(kode)
        if p is None:
            continue
        masuk = p[(p.index > pd.Timestamp(tgl)) & (p.v > 0)].index[0]
        t = ipo.tahan(p, ihsg, masuk, (250, 500))
        out.append(f"{kode} setelah masuknya {siapa}: setahun {_p(t['B250'], 0)}, dua tahun {_p(t['B500'], 0)}")
    return out


def _p(x: float, nd: int = 1) -> str:
    return "–" if pd.isna(x) else f"{100 * x:+.{nd}f}%".replace(".", ",")


def laporan(h: pd.DataFrame) -> list[str]:
    ada = h[h.ada_harga]
    kel = {"Semua peristiwa": ada, "Pengendali kuat": ada[ada.kuat], "Pengendali lain": ada[~ada.kuat]}
    rows, hasil = [], {}
    for nama, d in kel.items():
        r = lolos(d)
        hasil[nama] = r
        rows.append(f"| {nama} | {r['n']} | {_p(r['hasil_median'])} | {_p(r['median'])} | {_p(r['rata'])} | "
                    f"{100 * r['positif']:.0f}% | {_p(r['kohort_1'])} / {_p(r['kohort_2'])} | "
                    f"{'✓' if r['lolos'] else '✗'} |")
    semua, kuat = hasil["Semua peristiwa"], hasil["Pengendali kuat"]
    lolos_utama = semua["lolos"] and kuat["lolos"]
    top = ada.sort_values("B250", ascending=False).head(5)
    b500 = ada.dropna(subset=["B500"])
    b500 = b500[b500.B500_penuh]
    sa = setelah_ara()
    contoh = contoh_terkenal()
    return [
        "## B. Saham backdoor (ganti pengendali)",
        "",
        f"**Hasil singkat: {'LOLOS' if lolos_utama else 'TIDAK LOLOS'}.** Dari {len(h)} peristiwa ganti pengendali "
        f"Agustus 2023 – Oktober 2025 (dari arsip pengumuman resmi BEI), membeli sehari setelah pengumuman lalu "
        f"menahan setahun menghasilkan median {_p(semua['hasil_median'])}; {100 * semua['positif']:.0f}% mengalahkan "
        f"IHSG. Kelompok pengendali kuat (konglomerat, perusahaan besar, bank besar): median "
        f"{_p(kuat['hasil_median'])}, {100 * kuat['positif']:.0f}% mengalahkan IHSG.",
        "",
        "| Kelompok | Peristiwa | Hasil median | Median vs IHSG | Rata-rata vs IHSG | Kalahkan IHSG | "
        "Median vs IHSG Agu 2023–Sep 2024 / Okt 2024–Okt 2025 | Lolos |",
        "|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        f"- Naik paling tinggi dalam setahun: {', '.join(f'{r.kode} ({_p(r.B250, 0)})' for r in top.itertuples())}. "
        f"{(ada.B250 > 1).sum()} peristiwa naik lebih dari 2 kali lipat, {(ada.B250 < -0.5).sum()} turun lebih dari "
        "separuh.",
        f"- Ditahan dua tahun (hanya peristiwa yang sudah genap dua tahun, {len(b500)}): median "
        f"{_p(b500.B500.median())}, {100 * (b500.B500_lebih > 0).mean():.0f}% mengalahkan IHSG."
        if len(b500) else "- Belum ada peristiwa yang genap dua tahun.",
        f"- **Kenyataannya lebih sulit lagi:** {(sa.hari_ara > 0).sum()} dari {len(sa)} saham langsung ARA setelah "
        "berita, jadi tidak bisa dibeli di penutupan hari pertama. Kalau baru bisa membeli setelah ARA-nya berhenti: "
        f"median {_p(sa.B250.median())}, {100 * (sa.B250_lebih > 0).mean():.0f}% mengalahkan IHSG.",
        f"- Tanpa data harga (sudah dihapus dari Yahoo atau tidak pernah bertransaksi lagi): "
        f"{int((~h.ada_harga).sum())} peristiwa; disuspensi lebih dari 6 bulan di akhir masa tahan (dihitung 0): "
        f"{int(ada.B250_nol.sum())} (PTMR, disuspensi sehari setelah dibeli). Belum genap setahun (dihitung sampai "
        f"data terakhir): {int((~ada.B250_penuh).sum())} (TGUK baru bisa dibeli setelah suspensinya dibuka Agustus 2026, "
        "PADA).",
        "- Tidak dihitung karena berita pertamanya sebelum Agustus 2023: SMMT, VOKS, MFIN (Juli 2023), LPGI (2022), INCO. "
        "Juga tidak dihitung: perpindahan di dalam grup atau keluarga (GEMS, INTP, CITY, INKP, BTON, WIRG), "
        "pengendali lama yang menambah saham (BACA, SULI, SMMF), merger (EXCL), restrukturisasi BUMN (APIA, KRAS), dan "
        "penjualan tanpa pengendali baru yang jelas (AKKU, GDST).",
        f"- Contoh lama yang terkenal (hanya ilustrasi, tidak ikut dihitung): {'; '.join(contoh)}. Kasus seperti ini "
        "nyata, tetapi dipilih setelah tahu hasilnya.",
        "- Daftar lengkap, pengendali baru, dan sumbernya: `bot/research/backdoor_peristiwa.csv`; hasil per peristiwa: "
        "`reports/hasil_ipo_backdoor/backdoor_per_peristiwa.csv`.",
        "",
        "### Artinya",
        "",
        "- Membeli setiap saham yang ganti pengendali **seperti melempar koin**: separuh menang, separuh kalah, dan "
        "medianya sedikit di bawah IHSG. Rata-ratanya terlihat besar hanya karena segelintir saham gocapan yang naik "
        "puluhan kali lipat (MINA, KARW, FUTR, IRSX, CNKO), yang tidak bisa dikenali lebih dulu.",
        "- **\"Pilih orangnya\" (pengendali kuat) tidak membantu** di periode ini: dari 12 peristiwa, hanya 5 yang "
        "mengalahkan IHSG. Pemenang besar justru dari pembeli yang tidak dikenal, yang juga paling sering ambruk.",
        "- Ditahan dua tahun hasilnya lebih baik, tetapi baru 18 peristiwa (semuanya Agustus 2023 – Oktober 2024), "
        "terlalu sedikit untuk dipercaya, dan tidak termasuk syarat lolos.",
        "- Batasan: hanya 26 bulan dan 48 peristiwa (arsip BEI yang bisa dicari baru mulai Agustus 2023), dan 2026 adalah "
        "tahun berat bagi IHSG.",
        "",
    ]


def lolos(d: pd.DataFrame, n: int = 250) -> dict:
    kol = f"B{n}_lebih"
    x = d[kol].dropna()
    a = d[d.tanggal < BATAS_KOHORT][kol].median()
    b = d[d.tanggal >= BATAS_KOHORT][kol].median()
    return {"n": len(x), "hasil_median": d[f"B{n}"].median(), "median": x.median(), "rata": x.mean(),
            "positif": (x > 0).mean(), "kohort_1": a, "kohort_2": b, "nol": int(d[f"B{n}_nol"].sum()),
            "lolos": x.mean() > 0 and x.median() > 0 and (x > 0).mean() >= 0.5 and a > 0 and b > 0}
