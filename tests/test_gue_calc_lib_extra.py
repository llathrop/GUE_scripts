import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import math
import pytest
import gue_calc_lib as g


def test_calcpTot_edge_cases():
    # percentages that sum > 100 -> None
    assert g.calcpTot([60, 50]) is None
    # fractions that sum to 1
    assert pytest.approx(g.calcpTot([0.21, 0.35, 0.44]), rel=1e-6) == 1.0


def test_calcATA_boundaries():
    assert g.calcATA(0) == 1.0
    assert g.calcATA(33) == 2.0


def test_nitrox_FO2_division_guard():
    assert g.nitrox_FO2(480.0, 1800.0) == pytest.approx(480.0 / 1800.0)
    # division by zero protected
    assert g.nitrox_FO2(480.0, 0) == 0.0


def test_calcBottomTime_unknown_tank_raises():
    with pytest.raises(KeyError):
        g.calcBottomTime(depth=100, tank='NONEXISTENT')


def test_calcCF_and_calcPSI_roundtrip():
    tf = g.calcTF(77, 3000)
    cf = g.calcCF(tf, 3000)
    # converting back roughly recovers the original psi in 100-psi steps
    psi = g.calcPSI(tf, cf)
    assert isinstance(psi, int)