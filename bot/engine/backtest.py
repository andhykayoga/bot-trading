"""Mesin backtest satu akun (satu pasar), di grid M5 bersama semua instrumen.

Aturan global yang diterapkan (rulebook 00):
- G-01  ukuran posisi dari jarak SL: risiko 1% saldo (scalping 0,5%); dipotong kalau
        melewati risiko terbuka 3% (G-08) atau total nilai posisi melewati batas
        leverage pasar (G-16: forex 10× saldo, kripto spot 1×); tidak dibuka kalau di
        bawah ukuran minimum. Akun dalam USD; untung/rugi pair berkuotasi bukan USD
        (USDJPY) dikonversi ke USD.
- G-03  RR minimum dicek ulang dengan harga isi sebenarnya (termasuk spread).
- G-07  set and forget; pengecualian: scalping ditutup setelah 3 jam dan sebelum
        berita, keluar paksa setup (HKI-01).
- G-08  maks 3 transaksi baru per hari, 1 posisi per instrumen, 3 posisi bersamaan;
        sinyal lain di instrumen yang sedang terisi diabaikan.
- G-13  tidak ada posisi baru ±30 menit dari berita high impact.
- G-15  rem harian 3% dan mingguan 6% dari equity (saldo + rugi/untung terbuka).
        Rem drawdown (berhenti total) tidak menghentikan backtest; tanggal saat ia
        akan menyala dicatat di laporan.
- D-10  order pasar diisi di open candle M5 berikutnya; SL dan TP tersentuh di
        candle yang sama → SL dianggap lebih dulu; biaya spread & swap dihitung.
"""
from __future__ import annotations

import bisect
import heapq
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from bot.data import news
from bot.data.candles import Grid, load_grid
from bot.engine.costs import swap_rate
from bot.engine.orders import NEVER, Order
from bot.markets import INSTRUMENTS, MARKETS

NS_H = 3600 * 10**9


@dataclass
class Rules:
    initial_balance: float = 100_000.0
    risk_trading: float = 0.01
    risk_scalping: float = 0.005
    max_trades_day: int = 3
    max_positions: int = 3
    max_open_risk: float = 0.03
    leverage_cap: float | None = None   # None = batas leverage pasar (G-16)
    daily_brake: float = 0.03
    weekly_brake: float = 0.06
    dd_alarm: float = 0.15
    scalp_hours: float = 3.0
    news_filter: bool = True
    min_size: bool = True


@dataclass
class Trade:
    setup: str
    symbol: str
    direction: int
    label: str
    created: int
    entry_idx: int
    entry_time: int
    entry_price: float
    sl: float
    tp: float
    units: float
    risk_amount: float
    exit_idx: int = -1
    exit_time: int = 0
    exit_price: float = np.nan
    exit_reason: str = ""
    pnl: float = 0.0
    swap: float = 0.0
    tags: dict = field(default_factory=dict)
    legs: list = field(default_factory=list)  # [(units, exit_idx, exit_price, reason)] untuk varian bertahap
    conv: float = 1.0   # USD per satuan harga per unit saat entry (USDJPY: 1/harga)

    @property
    def r(self) -> float:
        return self.pnl / self.risk_amount if self.risk_amount else 0.0


class Simulator:
    def __init__(self, market: str = "forex", rules: Rules | None = None):
        self.market = MARKETS[market]
        self.rules = rules or Rules()
        self.g: Grid = load_grid(market)
        self.syms = list(self.market.instruments)
        self.lev_cap = self.rules.leverage_cap or self.market.leverage_cap
        g = self.g
        self.spread = {s: INSTRUMENTS[s].spread(g.c[s]) for s in self.syms}
        self.live_idx = {s: np.flatnonzero(g.live[s]) for s in self.syms}
        self.live_t = {s: g.t[self.live_idx[s]] for s in self.syms}
        # batas hari dan minggu (indeks grid pertama tiap hari/minggu trading)
        d = g.day
        starts = np.r_[0, np.flatnonzero(np.diff(d)) + 1]
        self.day_start_idx = np.repeat(starts, np.diff(np.r_[starts, len(d)]))
        w = g.week
        wst = np.r_[0, np.flatnonzero(np.diff(w)) + 1]
        self.week_start_idx = np.repeat(wst, np.diff(np.r_[wst, len(w)]))

    # ------------------------------------------------------------ util harga
    def bid_ask(self, s, i, field_):
        mid = getattr(self.g, field_)[s][i]
        half = self.spread[s][i] / 2
        return mid - half, mid + half

    def first_live(self, s, t_ns):
        """Indeks grid candle asli pertama instrumen s dengan waktu buka ≥ t."""
        li = self.live_idx[s]
        k = np.searchsorted(self.live_t[s], t_ns, side="left")
        return int(li[k]) if k < len(li) else -1

    # ------------------------------------------------------------ pengisian order
    def find_fill(self, o: Order, i0: int, i_end: int):
        """Cari candle tempat order limit/stop terisi. Kembalikan (indeks, harga) atau (−1, nan)."""
        g, s = self.g, o.symbol
        i_exp = min(i_end, int(np.searchsorted(g.t, o.expiry, side="left"))) if o.expiry != NEVER else i_end
        if i_exp <= i0:
            return -1, np.nan
        sl_ = slice(i0, i_exp)
        h, l, op = g.h[s][sl_], g.l[s][sl_], g.o[s][sl_]
        half = self.spread[s][sl_] / 2
        live = g.live[s][sl_]
        d = o.direction
        if o.kind == "limit":
            # long limit terisi saat ask ≤ harga; short limit saat bid ≥ harga
            trig = (l + half <= o.price) if d > 0 else (h - half >= o.price)
        else:
            # buy stop terisi saat ask ≥ harga; sell stop saat bid ≤ harga
            trig = (h + half >= o.price) if d > 0 else (l - half <= o.price)
        trig &= live
        canc = np.zeros(len(trig), bool)
        if not np.isnan(o.cancel_above):
            canc |= h >= o.cancel_above
        if not np.isnan(o.cancel_below):
            canc |= l <= o.cancel_below
        ti = int(np.argmax(trig)) if trig.any() else -1
        ci = int(np.argmax(canc)) if canc.any() else -1
        if ti < 0 or (ci >= 0 and ci <= ti):
            return -1, np.nan
        j = i0 + ti
        px = o.price
        # celah harga: kalau open sudah melewati harga order, isi di open
        ask_o, bid_o = op[ti] + half[ti], op[ti] - half[ti]
        if o.kind == "limit":
            px = min(px, ask_o) if d > 0 else max(px, bid_o)
        else:
            px = max(px, ask_o) if d > 0 else min(px, bid_o)
        return j, px

    # ------------------------------------------------------------ keluar posisi
    def find_exit(self, s, d, j0, entry_kind, sl, tp, i_end, t_forced):
        """Cari keluar pertama: SL/TP di candle [j0, k) atau keluar waktu di open candle k.
        Kembalikan (indeks, harga, alasan)."""
        g = self.g
        k = i_end  # keluar waktu (open candle k) atau akhir periode
        reason_t = "akhir periode"
        if t_forced is not None and t_forced[0] < NEVER:
            kk = self.first_live(s, t_forced[0])
            if 0 <= kk < k:
                k, reason_t = kk, t_forced[1]
        j = j0
        step = 2048
        while j < k:
            e = min(k, j + step)
            sl_ = slice(j, e)
            h, l = g.h[s][sl_], g.l[s][sl_]
            half = self.spread[s][sl_] / 2
            if d > 0:
                hit_sl = l - half <= sl
                hit_tp = h - half >= tp if not np.isnan(tp) else np.zeros(len(h), bool)
            else:
                hit_sl = h + half >= sl
                hit_tp = l + half <= tp if not np.isnan(tp) else np.zeros(len(h), bool)
            if j == j0 and entry_kind == "limit":
                hit_tp[0] = False  # TP di candle isi limit dianggap terjadi sebelum isi
            any_ = hit_sl | hit_tp
            if any_.any():
                r = int(np.argmax(any_))
                i = j + r
                op = g.o[s][i]
                hf = half[r]
                gap_ok = not (i == j0 and entry_kind != "market")
                if hit_sl[r]:
                    px = sl
                    if gap_ok:
                        px = min(sl, op - hf) if d > 0 else max(sl, op + hf)
                    return i, px, "SL"
                px = tp
                if gap_ok:
                    px = max(tp, op - hf) if d > 0 else min(tp, op + hf)
                return i, px, "TP"
            j = e
            step *= 2
        if k >= i_end:
            i = i_end - 1
            mid = g.c[s][i]
            hf = self.spread[s][i] / 2
            return i, (mid - hf if d > 0 else mid + hf), reason_t
        mid = g.o[s][k]
        hf = self.spread[s][k] / 2
        return k, (mid - hf if d > 0 else mid + hf), reason_t

    # ------------------------------------------------------------ equity untuk rem G-15
    def min_equity(self, a: int, b: int, base_balance: float, trades: list[Trade], opens: list[Trade]):
        """Equity terendah di candle [a, b) dengan saldo awal `base_balance`."""
        if b <= a:
            return base_balance
        eq = np.full(b - a, base_balance)
        for t in trades + opens:
            if t.entry_idx >= b:
                continue
            ex = t.exit_idx if t.exit_idx >= 0 else NEVER
            if ex < a and ex >= 0:
                continue
            lo, hi = max(a, t.entry_idx), min(b, ex if ex >= 0 else b)
            if hi > lo:
                s = t.symbol
                hf = self.spread[s][lo:hi] / 2
                if t.direction > 0:
                    worst = self.g.l[s][lo:hi] - hf - t.entry_price
                else:
                    worst = t.entry_price - (self.g.h[s][lo:hi] + hf)
                eq[lo - a: hi - a] += worst * t.units * t.conv
            if 0 <= ex < b and t.exit_idx >= 0:
                eq[max(ex, a) - a:] += t.pnl
        return float(eq.min())

    # ------------------------------------------------------------ simulasi
    def run(self, orders: list[Order], start: int, end: int) -> "Result":
        g, R = self.g, self.rules
        i_start = int(np.searchsorted(g.t, start, side="left"))
        i_end = int(np.searchsorted(g.t, end, side="left"))
        orders = sorted((o for o in orders if start <= o.created < end), key=lambda o: o.created)
        balance = R.initial_balance
        closed: list[Trade] = []
        opens: dict[str, Trade] = {}
        pending: dict[str, tuple[Order, int]] = {}  # symbol -> (order, seq)
        trades_per_day: dict[int, int] = {}
        brake_day: set[int] = set()
        brake_week: set[int] = set()
        stats = {"orders": len(orders), "rejected": {}}
        heap: list = []
        seq = 0
        # prioritas: keluar (0) → isi (1) → order baru (2), pada indeks candle yang sama
        for o in orders:
            i0 = int(np.searchsorted(g.t, o.created, side="left"))
            heapq.heappush(heap, (i0, 2, seq, "create", o))
            seq += 1

        def reject(why):
            stats["rejected"][why] = stats["rejected"].get(why, 0) + 1

        closed_exit: list[int] = []   # indeks keluar transaksi tertutup (urut, karena keluar diproses urut waktu)
        cum_pnl: list[float] = []

        def balance_at(idx):
            # saldo pada awal candle idx = awal + untung/rugi transaksi yang keluar sebelum idx
            k = bisect.bisect_left(closed_exit, idx)
            return R.initial_balance + (cum_pnl[k - 1] if k else 0.0)

        def closed_since(idx):
            return closed[bisect.bisect_left(closed_exit, idx):]

        def account_ok(o: Order, j: int) -> bool:
            if o.symbol in opens:
                reject("instrumen sudah ada posisi"); return False
            if len(opens) >= R.max_positions:
                reject("3 posisi bersamaan"); return False
            day = int(g.day[j])
            if trades_per_day.get(day, 0) >= R.max_trades_day:
                reject("3 transaksi per hari"); return False
            if R.news_filter and news.in_blackout(o.symbol, g.t[j]):
                reject("jendela berita"); return False
            if day in brake_day or int(g.week[j]) in brake_week:
                reject("rem darurat"); return False
            ds = int(self.day_start_idx[j]); ws = int(self.week_start_idx[j])
            ol = list(opens.values())
            b_day = balance_at(ds)
            if self.min_equity(ds, j, b_day, closed_since(ds), ol) <= b_day * (1 - R.daily_brake):
                brake_day.add(day); reject("rem darurat"); return False
            b_week = balance_at(ws)
            if self.min_equity(ws, j, b_week, closed_since(ws), ol) <= b_week * (1 - R.weekly_brake):
                brake_week.add(int(g.week[j])); reject("rem darurat"); return False
            return True

        while heap:
            i, _, _, kind, obj = heapq.heappop(heap)
            if kind == "create":
                o: Order = obj
                s = o.symbol
                if i >= i_end:
                    continue
                if s in opens:
                    reject("instrumen sudah ada posisi"); continue
                if s in pending:
                    po, _ = pending[s]
                    if po.setup == o.setup:
                        del pending[s]  # order baru dari setup yang sama menggantikan order lama
                    else:
                        reject("instrumen sudah ada order"); continue
                if o.kind == "market":
                    j = self.first_live(s, g.t[i])
                    if j < 0 or j >= i_end:
                        continue
                    hf = self.spread[s][j] / 2
                    px = g.o[s][j] + hf if o.direction > 0 else g.o[s][j] - hf
                    heapq.heappush(heap, (j, 1, seq, "fill", (o, px, seq))); seq += 1
                else:
                    j, px = self.find_fill(o, i, i_end)
                    if j < 0:
                        continue
                    pending[s] = (o, seq)
                    heapq.heappush(heap, (j, 1, seq, "fill", (o, px, seq))); seq += 1
            elif kind == "fill":
                o, px, myseq = obj
                s = o.symbol
                if o.kind != "market":
                    if pending.get(s, (None, -1))[1] != myseq:
                        continue  # sudah digantikan order baru dari setup yang sama
                    del pending[s]
                j = i
                if not account_ok(o, j):
                    continue
                d = o.direction
                dist = (px - o.sl) * d
                if dist <= 0:
                    reject("SL di sisi salah"); continue
                tp = o.tp if not np.isnan(o.tp) else px + d * o.tp_rr * dist
                rr = (tp - px) * d / dist
                if rr < o.min_rr - 1e-9:
                    reject("RR kurang dari minimum"); continue
                bal = balance_at(j)
                inst = INSTRUMENTS[s]
                conv = inst.usd_per_quote(px)
                risk_pct = R.risk_scalping if o.label == "scalping" else R.risk_trading
                units = bal * risk_pct / (dist * conv)
                open_risk = sum(t.risk_amount for t in opens.values())
                room = bal * R.max_open_risk - open_risk
                units = min(units, max(room, 0) / (dist * conv))
                notional_open = sum(INSTRUMENTS[t.symbol].notional_usd(t.units, t.entry_price) for t in opens.values())
                units = min(units, max(bal * self.lev_cap - notional_open, 0) / inst.notional_usd(1.0, px))
                if R.min_size and units < inst.min_units:
                    reject("di bawah ukuran minimum"); continue
                if units <= 0:
                    reject("batas risiko terbuka"); continue
                tr = Trade(o.setup, s, d, o.label, o.created, j, int(g.t[j]), px, o.sl, tp, units,
                           units * dist * conv, tags=dict(o.tags), conv=conv)
                # keluar waktu: scalping 3 jam, sebelum berita, atau keluar paksa setup
                forced = []
                if o.label == "scalping":
                    hours = R.scalp_hours if np.isnan(o.hold_hours) else o.hold_hours
                    forced.append((int(g.t[j]) + int(hours * NS_H), "batas waktu scalping"))
                    if R.news_filter:
                        forced.append((news.next_window_start(s, int(g.t[j])), "tutup sebelum berita"))
                if o.exit_times is not None and len(o.exit_times):
                    k = np.searchsorted(o.exit_times, g.t[j], side="right")
                    if k < len(o.exit_times):
                        forced.append((int(o.exit_times[k]), "keluar paksa setup"))
                tf = min(forced) if forced else None
                if o.partial and not np.isnan(o.tp2):
                    self._exit_partial(tr, o, j, i_end, tf)
                else:
                    ei, ep, why = self.find_exit(s, d, j, o.kind, o.sl, tp, i_end, tf)
                    tr.exit_idx, tr.exit_price, tr.exit_reason = ei, ep, why
                    tr.legs = [(units, ei, ep, why)]
                tr.exit_idx = max(l_[1] for l_ in tr.legs)
                tr.exit_time = int(g.t[tr.exit_idx])
                self._settle(tr)
                trades_per_day[int(g.day[j])] = trades_per_day.get(int(g.day[j]), 0) + 1
                opens[s] = tr
                heapq.heappush(heap, (tr.exit_idx, 0, seq, "exit", tr)); seq += 1
            elif kind == "exit":
                tr = obj
                if opens.get(tr.symbol) is tr:
                    del opens[tr.symbol]
                balance += tr.pnl
                closed.append(tr)
                closed_exit.append(tr.exit_idx)
                cum_pnl.append((cum_pnl[-1] if cum_pnl else 0.0) + tr.pnl)
        closed.sort(key=lambda t: t.entry_idx)
        return Result(self, closed, i_start, i_end, stats)

    def _exit_partial(self, tr: Trade, o: Order, j, i_end, tf):
        """Varian pembanding Q-08: 50% ditutup di TP1, SL sisanya ke titik impas, sisanya ke TP2."""
        s, d = tr.symbol, tr.direction
        half_u = tr.units / 2
        ei, ep, why = self.find_exit(s, d, j, o.kind, o.sl, tr.tp, i_end, tf)
        if why != "TP":
            tr.legs = [(tr.units, ei, ep, why)]
            return
        legs = [(half_u, ei, ep, "TP1")]
        if ei + 1 < i_end:
            e2, p2, w2 = self.find_exit(s, d, ei + 1, "market", tr.entry_price, o.tp2, i_end, tf)
            legs.append((half_u, e2, p2, "BE" if w2 == "SL" else ("TP2" if w2 == "TP" else w2)))
        else:
            legs.append((half_u, ei, ep, "TP1"))
        tr.legs = legs

    def _settle(self, tr: Trade):
        inst = INSTRUMENTS[tr.symbol]
        pnl = 0.0
        swap = 0.0
        ym = pd.Timestamp(tr.entry_time, tz="UTC").strftime("%Y-%m")
        rate = swap_rate(inst.base_ccy, inst.quote_ccy, tr.direction, ym, inst.swap_markup) if inst.swap else 0.0
        for units, ei, ep, _ in tr.legs:
            pnl += units * (ep - tr.entry_price) * tr.direction * inst.usd_per_quote(ep)
            nights = int(self.g.day[ei] - self.g.day[tr.entry_idx])
            swap += inst.notional_usd(units, tr.entry_price) * rate * nights / 365.0
        tr.exit_price = tr.legs[-1][2]
        tr.exit_reason = "+".join(l_[3] for l_ in tr.legs) if len(tr.legs) > 1 else tr.legs[0][3]
        tr.swap = swap
        tr.pnl = pnl + swap


class Result:
    def __init__(self, sim: Simulator, trades: list[Trade], i_start: int, i_end: int, stats: dict):
        self.sim, self.trades, self.i_start, self.i_end, self.stats = sim, trades, i_start, i_end, stats

    def equity(self) -> np.ndarray:
        """Equity per candle M5 (saldo + untung/rugi terbuka terburuk di candle itu)."""
        sim, g = self.sim, self.sim.g
        a, b = self.i_start, self.i_end
        R0 = sim.rules.initial_balance
        eq = np.full(b - a, R0)
        for t in self.trades:
            for units, ei, ep, _ in t.legs:
                lo, hi = t.entry_idx, ei
                if hi > lo:
                    hf = sim.spread[t.symbol][lo:hi] / 2
                    if t.direction > 0:
                        w = g.l[t.symbol][lo:hi] - hf - t.entry_price
                    else:
                        w = t.entry_price - (g.h[t.symbol][lo:hi] + hf)
                    eq[lo - a: hi - a] += w * units * t.conv
            eq[t.exit_idx - a:] += t.pnl
        return eq

    def frame(self) -> pd.DataFrame:
        rows = []
        for t in self.trades:
            rows.append({
                "setup": t.setup, "symbol": t.symbol, "dir": "long" if t.direction > 0 else "short",
                "label": t.label,
                "entry_time": pd.Timestamp(t.entry_time, tz="UTC"), "entry": t.entry_price,
                "sl": t.sl, "tp": t.tp, "units": t.units, "risk": t.risk_amount,
                "exit_time": pd.Timestamp(t.exit_time, tz="UTC"), "exit": t.exit_price,
                "reason": t.exit_reason, "swap": t.swap, "pnl": t.pnl, "R": t.r, **t.tags})
        return pd.DataFrame(rows)
