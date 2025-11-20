import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import gue_calc_lib as g

def test_calcATA_fresh_water():
    # 34 feet fresh water = 2 ATA
    assert g.calcATA(34, water='fresh') == 2.0
    # 0 feet = 1 ATA
    assert g.calcATA(0, water='fresh') == 1.0
    # Salt water check (default)
    assert g.calcATA(33, water='salt') == 2.0
    assert g.calcATA(33) == 2.0
