"""Jurnal sinyal otomatis: tiap sinyal dicatat di jurnal/sinyal.csv (disimpan GitHub Actions ke repo), dan jawaban
tombol Telegram ("✅ ambil" / "❌ lewati") dicatat di kolom `diambil` saat bot berjalan berikutnya.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

from bot import telegram

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "jurnal"
JURNAL = FOLDER / "sinyal.csv"
STATUS = FOLDER / "telegram.json"
KOLOM = ["id", "tanggal", "strategi", "skor", "aset", "aksi", "harga", "diambil", "waktu_jawab"]


def baca() -> pd.DataFrame:
    if not JURNAL.exists():
        return pd.DataFrame(columns=KOLOM)
    return pd.read_csv(JURNAL, dtype=str, keep_default_na=False)


def tulis(d: pd.DataFrame) -> None:
    FOLDER.mkdir(exist_ok=True)
    d[KOLOM].to_csv(JURNAL, index=False, quoting=csv.QUOTE_MINIMAL)


def catat(sinyal: list[dict]) -> list[dict]:
    """Tambahkan sinyal baru (dilewati kalau id-nya sudah ada, misalnya run diulang). Kembalikan yang baru."""
    d = baca()
    baru = [s for s in sinyal if s["id"] not in set(d["id"])]
    if baru:
        tambah = pd.DataFrame([{**{k: "" for k in KOLOM}, **{k: str(v) for k, v in s.items() if k in KOLOM}}
                               for s in baru])
        tulis(pd.concat([d, tambah], ignore_index=True))
    return baru


def tarik_jawaban() -> int:
    """Ambil jawaban tombol dari Telegram (getUpdates) dan isi kolom `diambil`. Telegram menyimpan jawaban 24 jam,
    jadi bot perlu berjalan paling tidak sekali sehari. Kembalikan jumlah jawaban yang dicatat."""
    if not telegram.siap():
        return 0
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {"offset": 0}
    d, n = baca(), 0
    for u in telegram.updates(status["offset"]):
        status["offset"] = u["update_id"] + 1
        q = u.get("callback_query")
        if not q or str(q.get("message", {}).get("chat", {}).get("id")) != telegram.chat_id():
            continue
        jenis, _, sid = q.get("data", "").partition("|")
        m = d["id"] == sid
        if m.any() and jenis in ("a", "l"):
            d.loc[m, "diambil"] = "ya" if jenis == "a" else "tidak"
            d.loc[m, "waktu_jawab"] = pd.Timestamp(q["message"]["date"], unit="s").strftime("%Y-%m-%d")
            n += 1
        telegram.jawab_tombol(q["id"], "Tercatat ✅" if jenis == "a" else "Tercatat: dilewati")
    if n:
        tulis(d)
    FOLDER.mkdir(exist_ok=True)
    STATUS.write_text(json.dumps(status))
    return n


def tombol(sinyal: list[dict]) -> dict | None:
    """Satu baris tombol per sinyal: ambil atau lewati."""
    if not sinyal:
        return None
    return {"inline_keyboard": [[{"text": f"✅ {s['aksi']} {s['aset']} · {s['singkat']}",
                                  "callback_data": f"a|{s['id']}"},
                                 {"text": "❌ Lewati", "callback_data": f"l|{s['id']}"}] for s in sinyal]}


def ringkas() -> str:
    d = baca()
    if d.empty:
        return "Jurnal: belum ada sinyal tercatat."
    return (f"Jurnal: {len(d)} sinyal sejak {d.tanggal.min()}, {int((d.diambil == 'ya').sum())} Anda ambil, "
            f"{int((d.diambil == '').sum())} belum dijawab.")
