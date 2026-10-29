"""Daftar semua setup forex, urut prioritas (Q: setup forex dulu, lalu mentor saham–kripto)."""
from bot.setups.afs_fib_dow import AFS04, AFS05, AFS09, AFS10
from bot.setups.afs_indicators import (AFS12, AFS13A, AFS13B, AFS14, AFS15, AFS16P, AFS16T, AFS17, AFS18,
                                       AFS19, AFS20B, AFS20R, AFS21)
from bot.setups.afs_research import AFS01, AFS02, AFS03
from bot.setups.afs_smc import AFS06, AFS07, AFS08
from bot.setups.ichimoku import ICH01, ICH02, ICH03
from bot.setups.kms_hki import HKI01D1, HKI01H4, KMS02
from bot.setups.pln01 import PolaN

ALL = [PolaN, ICH01, ICH02, ICH03,
       AFS01, AFS02, AFS03, AFS04, AFS05, AFS06, AFS07, AFS08, AFS09, AFS10, AFS12, AFS13A, AFS13B,
       AFS14, AFS15, AFS16P, AFS16T, AFS17, AFS18, AFS19, AFS20R, AFS20B, AFS21, KMS02, HKI01D1, HKI01H4]
REGISTRY = {cls.id: cls for cls in ALL}
