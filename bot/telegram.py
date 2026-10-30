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


def kirim(teks: str) -> None:
    """Kirim satu pesan berformat HTML Telegram (<b>, <i>, <a>)."""
    data = urllib.parse.urlencode({"chat_id": os.environ["TELEGRAM_CHAT_ID"], "text": teks, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"
    r = json.loads(urllib.request.urlopen(url, data=data, timeout=30).read())
    if not r.get("ok"):
        raise RuntimeError(f"Telegram menolak pesan: {r.get('description')}")
