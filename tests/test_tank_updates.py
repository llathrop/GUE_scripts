import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import gue_calc_lib as g

def test_tank_factors_new_defs():
    # 2xHP100: 200cf @ 3442.
    # TF = (200 / 3442) * 100 * 2 = 11.62... round -> 12. / 2 = 6.0
    tf_hp100 = g.calcTF(200, 3442)
    assert tf_hp100 == 6.0

    # 2xLP85: 170cf @ 2640.
    # TF = (170 / 2640) * 100 * 2 = 12.87... round -> 13. / 2 = 6.5
    tf_lp85 = g.calcTF(170, 2640)
    assert tf_lp85 == 6.5

    # 2xAL80: 154cf @ 3000.
    # TF = (154 / 3000) * 100 * 2 = 10.26... round -> 10. / 2 = 5.0
    tf_al80_d = g.calcTF(154, 3000)
    assert tf_al80_d == 5.0
