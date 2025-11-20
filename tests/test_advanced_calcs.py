import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
import gue_calc_lib as g

def test_calcMOD():
    # Nitrox 32 @ 1.4 -> 111 ft. Conservative 100ft?
    # Formula: (1.4 / 0.32 - 1) * 33 = (4.375 - 1) * 33 = 3.375 * 33 = 111.375
    assert g.calcMOD(0.32) == 111

    # Nitrox 32 @ 1.6 (Deco)
    # (1.6 / 0.32 - 1) * 33 = (5 - 1) * 33 = 132
    assert g.calcMOD(0.32, ppo2_limit=1.6) == 132

    # Oxygen 100% @ 1.6
    # (1.6 / 1.0 - 1) * 33 = 0.6 * 33 = 19.8 -> 19 (int)
    # Wait, int() truncates. 19.8 -> 19.
    # Usually we say 20ft. But 1.6 ATA *exactly* is 19.8ft.
    # If code uses int(), it's conservative (shallower).
    assert g.calcMOD(1.0, ppo2_limit=1.6) == 19

def test_calcEND():
    # Trimix 18/45 (18% O2, 45% He) at 150ft.
    # Salt water (33).
    # ATA = 150/33 + 1 = 4.54 + 1 = 5.54
    # Narcotic ATA = 5.54 * (1 - 0.45) = 5.54 * 0.55 = 3.05
    # END = (3.05 - 1) * 33 = 2.05 * 33 = 67.65 -> 67ft.
    # Standard GUE 18/45 END at 150ft?
    # END = (150 + 33) * (1 - 0.45) - 33 = 183 * 0.55 - 33 = 100.65 - 33 = 67.65.
    assert g.calcEND(150, 0.45) == 67

    # Trimix 30/30 at 100ft.
    # END = (100 + 33) * (1 - 0.30) - 33 = 133 * 0.70 - 33 = 93.1 - 33 = 60.1 -> 60ft.
    assert g.calcEND(100, 0.30) == 60

def test_calcEAD():
    # EAD for Nitrox 32 at 100ft.
    # EAD = ((100 + 33) / 33) * (0.68 / 0.79) * 33 - 33
    #     = 4.03 * 0.86 * 33 - 33
    #     = (100 + 33) * (0.68 / 0.79) - 33
    #     = 133 * 0.8607 - 33 = 114.4 - 33 = 81.4 -> 81ft.
    # Standard chart check: EAD for 32% at 100ft is approx 81-82ft.
    assert g.calcEAD(100, 0.32) in [81, 82]
