import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import gue_calc_lib as g

def test_calcTimeToStop_gue_heuristic():
    # 100ft -> Surface.
    # 100/10 = 10 min ascent. + 1 min solve = 11.
    assert g.calcTimeToStop(100) == 11

    # 30ft -> Surface.
    # 30/10 = 3 min. + 1 min solve = 4.
    assert g.calcTimeToStop(30) == 4

    # 100ft -> Switch at 70ft.
    # Distance = 30ft.
    # 30/10 = 3 min ascent.
    # +1 min solve + 1 min switch = +2.
    # Total 5.
    assert g.calcTimeToStop(100, gas_switch_depth=70) == 5
