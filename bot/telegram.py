"""Kirim pesan ke Telegram lewat Bot API.

Token bot dan chat id dibaca dari variabel lingkungan TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID. Di GitHub keduanya
disimpan sebagai secret (Settings → Secrets and variables → Actions), jadi tidak pernah tertulis di kode.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request


def siap() -> bool:
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"))


def chat_id() -> str:
    return os.environ.get("TELEGRAM_CHAT_ID", "").strip()


def _api(metode: str, **param) -> dict:
    data = urllib.parse.urlencode({k: json.dumps(v) if isinstance(v, dict) else v for k, v in param.items()}).encode()
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/{metode}"
    r = json.loads(urllib.request.urlopen(url, data=data, timeout=30).read())
    if not r.get("ok"):
        raise RuntimeError(f"Telegram menolak {metode}: {r.get('description')}")
    return r


def kirim(teks: str, tombol: dict | None = None) -> None:
    """Kirim satu pesan berformat HTML Telegram (<b>, <i>, <a>), opsional dengan tombol di bawahnya."""
    param = {"chat_id": chat_id(), "text": teks, "parse_mode": "HTML", "disable_web_page_preview": "true"}
    if tombol:
        param["reply_markup"] = tombol
    _api("sendMessage", **param)


def updates(offset: int) -> list[dict]:
    return _api("getUpdates", offset=offset, timeout=0, allowed_updates='["callback_query"]')["result"]


def jawab_tombol(qid: str, teks: str) -> None:
    try:
        _api("answerCallbackQuery", callback_query_id=qid, text=teks)
    except Exception:  # noqa: BLE001 - tombol yang sudah lama (>15 menit) tidak bisa dijawab lagi; tidak apa-apa
        pass
