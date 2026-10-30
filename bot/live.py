"""Kerangka menjalankan bot secara live — BELUM terhubung ke broker.

Alur (rulebook README, "Urutan kerja bot"):
1. Ambil candle terbaru (yang sudah close) dari sumber data pasar.
2. Setiap setup yang dinyalakan di config/setups.toml menghasilkan order untuk candle itu.
3. Aturan global (G-01, G-08, G-13, G-15, G-16) diterapkan sebelum order dikirim.
4. Order dikirim ke broker bersama SL dan TP (G-12).

Untuk menyambungkan broker sungguhan, buat kelas turunan `Broker` (mis. MetaTrader 5
untuk forex, API exchange berizin OJK untuk kripto) dan isi metodenya. Mesin backtest
dan live memakai setup dan objek `Order` yang sama, jadi perilaku keduanya konsisten.
Pemeriksaan keselamatan live G-15 (posisi tanpa SL, order dobel, koneksi putus > 15 menit)
dilakukan di `safety_check` sebelum setiap putaran.
"""
from __future__ import annotations

import tomllib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from bot.data.candles import load_instrument
from bot.engine.orders import Order
from bot.markets import MARKETS
from bot.setups import REGISTRY

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Position:
    symbol: str
    direction: int
    units: float
    entry: float
    sl: float
    tp: float
    label: str = "trading"


class Broker(ABC):
    """Antarmuka broker/exchange. Satu objek = satu akun (G-16: forex dan kripto terpisah)."""

    @abstractmethod
    def balance(self) -> float: ...

    @abstractmethod
    def equity(self) -> float: ...

    @abstractmethod
    def positions(self) -> list[Position]: ...

    @abstractmethod
    def send(self, order: Order, units: float) -> None:
        """Kirim order beserta SL dan TP dalam satu permintaan (G-12)."""

    @abstractmethod
    def close(self, symbol: str) -> None: ...


@dataclass
class PaperBroker(Broker):
    """Broker kertas untuk mencoba alur live tanpa uang (tidak mensimulasikan harga)."""
    cash: float = 10_000.0
    open: list[Position] = field(default_factory=list)
    sent: list[tuple[Order, float]] = field(default_factory=list)

    def balance(self):
        return self.cash

    def equity(self):
        return self.cash

    def positions(self):
        return list(self.open)

    def send(self, order, units):
        self.sent.append((order, units))

    def close(self, symbol):
        self.open = [p for p in self.open if p.symbol != symbol]


def enabled_setups(market: str = "forex"):
    cfg = tomllib.loads((ROOT / "config" / "setups.toml").read_text())
    return [REGISTRY[s]() for s in cfg[market]["enabled"]]


def safety_check(broker: Broker) -> list[str]:
    """G-15: posisi tanpa SL langsung ditutup; order dobel (lebih dari 1 posisi per instrumen)."""
    problems = []
    seen = set()
    for p in broker.positions():
        if p.sl is None:
            broker.close(p.symbol)
            problems.append(f"{p.symbol}: posisi tanpa SL ditutup")
        if p.symbol in seen:
            problems.append(f"{p.symbol}: order dobel")
        seen.add(p.symbol)
    return problems


def latest_orders(market: str = "forex", params: dict[str, dict] | None = None) -> list[Order]:
    """Order dari candle terakhir yang sudah close untuk semua setup yang dinyalakan.
    `params` = pilihan parameter terkunci per setup (dari hasil backtest)."""
    m = MARKETS[market]
    data = {s: load_instrument(s) for s in m.instruments}
    newest = max(d["M5"].t_close[-1] for d in data.values())
    out = []
    for st in enabled_setups(market):
        p = st.params(**(params or {}).get(st.id, {}))
        for o in st.signals(data, p):
            # hanya sinyal dari candle yang baru saja close (dalam 5 menit terakhir data)
            if o.created >= newest - 5 * 60 * 10**9:
                out.append(o)
    return out
