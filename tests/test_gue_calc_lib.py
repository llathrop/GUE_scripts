import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import gue_calc_lib as g


def test_calcATA_and_PPO2():
    assert g.calcATA(0) == 1.0
    assert g.calcATA(33) == 2.0
    assert round(g.calcPPO2(0, 0.21), 2) == 0.21


def test_calcMG_basic():
    # Known value from notebook: calcMG(100) ≈ 41
    assert g.calcMG(100) == 41


def test_calcPSI_and_CF():
    tf = g.calcTF(77, 3000)
    # tank factor ~ 2.5
    assert tf == 2.5
    psi = g.calcPSI(tf, 77)
    assert psi == 3000 or psi == 2900 or psi == 3100


def test_trimix_helpers():
    assert g.trimix_PO2() == 480.0
    assert g.trimix_P_He() == 1200.0
    nit_p = g.nitrox_p(g.trimix_P_He(), 3000)
    assert round(g.nitrox_FO2(g.trimix_PO2(), nit_p), 3) == round(480.0 / 1800.0, 3)
