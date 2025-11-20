"""Minimal, clean GUE calculation helpers used by the notebook and tests.

This module exposes a small, well-documented set of helpers extracted from
the notebook. Functions are small, typed, and include concise docstrings so
they are easy to test and reuse.
"""

from __future__ import annotations
from typing import Iterable, Optional, Dict
import math

# Tank definitions used by tests and notebook helpers.
tanks: Dict[str, Dict[str, int]] = {
    'AL80': {'rated_vol': 77, 'rated_PSI': 3000},
    '2xAL80': {'rated_vol': 154, 'rated_PSI': 3000},
    # Additional tanks used by the notebook (approximate volumes and standard PSI)
    'AL40': {'rated_vol': 40, 'rated_PSI': 3000},
    '2xLP85': {'rated_vol': 170, 'rated_PSI': 2640},
    '2xHP100': {'rated_vol': 200, 'rated_PSI': 3442},
    '2xHP133': {'rated_vol': 266, 'rated_PSI': 3442},
}


def calcpTot(gasses: Iterable[float]) -> Optional[float]:
    """Return the sum of provided gas values or ``None`` if the sum > 100.

    Args:
        gasses: Iterable of gas values (percent as numbers, e.g. 21 or 0.21).

    Returns:
        The numeric sum, or ``None`` when the sum is greater than 100.
    """
    total = 0.0
    for g in gasses:
        total += float(g)
    return None if total > 100.0 else total

# Example:
# >>> calcpTot([21, 35, 44])
# 100.0
# >>> calcpTot([0.21, 0.35, 0.44])
# 1.0


def calcpGas(ata: float, f_gas: float) -> float:
    """Partial pressure (absolute) of a gas at ambient ATA.

    Args:
        ata: Ambient pressure in ATA.
        f_gas: Fraction (e.g. 0.21) of the gas.

    Returns:
        Partial pressure as same units as ``ata`` times ``f_gas``.
    """
    return ata * f_gas


def calcATA(depth: float, water: str = 'salt') -> float:
    """Return ATA at depth (rounded to 1 decimal).

    Formulae:
      - Salt water: ATA = 1 + depth/33
      - Fresh water: ATA = 1 + depth/34

    Args:
        depth: Depth in feet.
        water: 'salt' (default) or 'fresh'.
    """
    divisor = 34.0 if water == 'fresh' else 33.0
    return round((depth / divisor) + 1.0, 1)

# Example:
# >>> calcATA(0)
# 1.0
# >>> calcATA(33, 'salt')
# 2.0
# >>> calcATA(34, 'fresh')
# 2.0


def calcPPO2(depth: float = 0, percent_O2: float = 0.21) -> float:
    """Partial pressure of oxygen (PPO2) at the given depth.

    Args:
        depth: Depth in feet.
        percent_O2: Fractional oxygen (default air 0.21).
    """
    return calcATA(depth) * percent_O2


def calcTimeToStop(depth: float, gas_switch_depth: float = 0) -> int:
    """Estimate minutes required to ascend (or to a gas switch).

    Uses the standard GUE Minimum Gas planning heuristic:
    - Ascent rate: 10 ft/min (conservative average to account for stress/sharing).
    - Initial delay: +1 minute to solve the problem.
    - Gas switch: +1 additional minute (implied if gas_switch_depth > 0).

    Args:
        depth: Current depth in feet.
        gas_switch_depth: Depth of the gas switch in feet (default 0 for surface).

    Returns:
        Total minutes (integer) for the ascent.
    """
    if gas_switch_depth > 0:
        return int(((depth - gas_switch_depth) / 10.0) + 2)
    return int((depth / 10.0) + 1)


def calcMG(depth: float, gas_switch_depth: float = 0, c: float = 1.5, verbose: bool = False) -> int:
    """Compute Minimum Gas (CAT) requirement and return integer cubic-feet.

    Formula used: MG = C * A * T where
      - C is consumption (ft^3/min at surface),
      - A is average ATA between start and gas switch,
      - T is estimated minutes to surface/switch.

    Returns the value rounded to the nearest integer.
    """
    a = (calcATA(depth) + calcATA(gas_switch_depth)) / 2.0
    t = calcTimeToStop(depth, gas_switch_depth)
    if verbose:
        print('Consumption:', c, 'Average ATA:', a, 'time:', t)
    mg = c * a * t
    return math.floor(mg + 0.5)

# Example:
# >>> calcMG(100)
# 41


def calcTF(rated_vol: float, rated_psi: float) -> float:
    """Tank factor: ft^3 per 100 PSI (rounded to nearest 0.5).

    Args:
        rated_vol: tank internal volume in ft^3.
        rated_psi: tank working pressure in PSI.
    """
    return round(((rated_vol / rated_psi) * 100 * 2)) / 2.0


def calcPSI(tank_factor: float, gas_cf: float) -> int:
    """Convert cubic-feet requirement into an approximate PSI value.

    PSI values are rounded to 100-psi steps to match notebook expectations.
    """
    return int(gas_cf / tank_factor) * 100


def trimix_PO2(f_o2: float = 0.16, p: float = 3000.0) -> float:
    """Return O2 partial pressure in PSI for a trimix blend at pressure p."""
    return f_o2 * p


def trimix_P_He(f_he: float = 0.40, p: float = 3000.0) -> float:
    """Return He partial pressure in PSI for a trimix blend at pressure p."""
    return f_he * p


def nitrox_p(trimix_p_he: float, p: float = 3000.0) -> float:
    """Return the pressure remaining for nitrox after adding helium."""
    return p - trimix_p_he


def nitrox_FO2(trimix_po2: float, nitrox_p_val: float) -> float:
    """Compute the fractional O2 for the nitrox portion of a blend.

    Returns 0.0 when the pressure available for nitrox is zero.
    """
    if nitrox_p_val == 0:
        return 0.0
    return trimix_po2 / nitrox_p_val

# Example (protects division-by-zero):
# >>> nitrox_FO2(480.0, 1800.0)
# 0.26666666666666666
# >>> nitrox_FO2(480.0, 0)
# 0.0


def calcCF(tank_factor: float, gas_psi: float) -> float:
    """Convert PSI to cubic feet using the tank factor.

    Args:
        tank_factor: cu ft per 100 PSI.
        gas_psi: Pressure in PSI.

    Returns:
        Cubic feet available at gas_psi.
    """
    return (gas_psi * tank_factor) / 100.0


def calcTimeToSurface(depth: float) -> int:
    """Compatibility wrapper: estimated minutes to surface from depth."""
    return calcTimeToStop(depth, gas_switch_depth=0)


def calcSCR(volume_consumed: float, ata: float, minutes: float) -> float:
    """Calculate Surface Consumption Rate (SCR).

    SCR = volume consumed / ATA / minutes
    """
    return volume_consumed / ata / minutes


def calcGasVolCons(scr: float, ata: float, minutes: float) -> float:
    """Gas volume consumed for given SCR, ATA and minutes."""
    return scr * ata * minutes


def calcUG(curr_psi: float = 3000.0, mg_psi: float = 500.0, method: str = 'ALL') -> float:
    """Compute usable gas (PSI) after reserving minimum gas and partitioning."""
    methods = {'ALL': 1, 'HALF': 2, 'THIRDS': 3}
    if method not in methods:
        raise KeyError(f'Unknown method: {method}; expected one of {list(methods)}')
    return (curr_psi - mg_psi) / methods[method]


def calcBottomTime(depth: float = 100.0, tank: str = '2xAL80', method: str = 'ALL', scr: float = 1.5) -> float:
    """Estimate bottom time available given tank, depth and SCR."""
    ata = calcATA(depth)
    tank_info = tanks.get(tank)
    if tank_info is None:
        raise KeyError(f'Unknown tank: {tank}')
    tf = calcTF(tank_info['rated_vol'], tank_info['rated_PSI'])
    mg_cf = calcMG(depth, verbose=False)
    mg_psi = calcPSI(tf, mg_cf)
    ug = calcUG(tank_info['rated_PSI'], mg_psi, method=method)
    # return minutes
    return ug / (scr * ata)


def O2_PSI_to_add(target_fraction_o2: float = 0.32, p: float = 3000.0) -> float:
    """PSI of O2 to add to achieve target FO2 (partial-pressure blending)."""
    return ((target_fraction_o2 - 0.21) / 0.79) * p


def trimixPP(f_o2: float = 0.16, f_he: float = 0.40, p: float = 3000.0) -> None:
    """Print a simple partial-pressure mixing plan for a trimix blend."""
    p_he_to_add = trimix_P_He(f_he, p)
    t_po2 = trimix_PO2(f_o2, p)
    nit_p = nitrox_p(p_he_to_add, p)
    nit_fo2 = nitrox_FO2(t_po2, nit_p)

    print('for trimix:', int(f_o2 * 100), '/', int(f_he * 100))
    print('add He:', p_he_to_add)
    print('add O2:', O2_PSI_to_add(nit_fo2, nit_p))
    print('fill with air')


def calcMOD(f_o2: float, ppo2_limit: float = 1.4, water: str = 'salt') -> int:
    """Calculate Maximum Operating Depth (MOD) in feet.

    Formula: MOD = 33 * (PO2_limit / f_o2 - 1) for salt water.
             MOD = 34 * (PO2_limit / f_o2 - 1) for fresh water.

    Args:
        f_o2: Fraction of Oxygen (e.g. 0.32).
        ppo2_limit: PPO2 limit in ATA (default 1.4).
        water: 'salt' or 'fresh'.
    """
    if f_o2 <= 0:
        return 0
    factor = 34.0 if water == 'fresh' else 33.0
    ata = ppo2_limit / f_o2
    return int((ata - 1.0) * factor)


def calcEND(depth: float, f_he: float, water: str = 'salt') -> int:
    """Calculate Equivalent Narcotic Depth (END) in feet.

    Formula: END = (Depth + 33) * (1 - f_he) - 33.
    Treats O2 as narcotic (standard GUE approach).
    """
    factor = 34.0 if water == 'fresh' else 33.0
    ata = (depth / factor) + 1.0
    # Effective narcotic ATA = Total ATA * (1 - Fraction of Helium)
    # Since (1 - He) = N2 + O2.
    narcotic_ata = ata * (1.0 - f_he)
    return int((narcotic_ata - 1.0) * factor)


def calcEAD(depth: float, f_o2: float, water: str = 'salt') -> int:
    """Calculate Equivalent Air Depth (EAD) in feet.

    Formula: EAD = ((Depth + 33) / 33) * (f_n2 / 0.79) * 33 - 33.
             Simplified: (ATA * (1 - f_o2) / 0.79 - 1) * 33.
    """
    factor = 34.0 if water == 'fresh' else 33.0
    ata = (depth / factor) + 1.0
    f_n2 = 1.0 - f_o2
    ead_ata = ata * (f_n2 / 0.79)
    return int((ead_ata - 1.0) * factor)


__all__ = [
    'tanks', 'calcpTot', 'calcpGas', 'calcATA', 'calcPPO2', 'calcTimeToStop', 'calcMG',
    'calcTF', 'calcPSI', 'trimix_PO2', 'trimix_P_He', 'nitrox_p', 'nitrox_FO2',
    'calcMOD', 'calcEND', 'calcEAD'
]


if __name__ == '__main__':
    # quick smoke checks
    print('test pTot: (expect 100%)', calcpTot([21, 35, 44]))
    print('test pGas: (expect 1.05)', calcpGas(5, 0.21))
    print('test ATA-surface:(expect 1)', calcATA(0))
    print('test PPO2-surface:(expect .21)', calcPPO2())
    print('test calc Min Gas:(expect approx 41)', calcMG(depth=100, verbose=True))
