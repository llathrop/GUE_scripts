#!/usr/bin/env python3
"""Command-line interface for GUE Gas Planning calculations."""

import argparse
import sys
from typing import Optional

import gue_calc_lib as g

def cmd_min_gas(args):
    """Calculate Minimum Gas."""
    mg = g.calcMG(args.depth, args.switch_depth, verbose=False)
    print(f"Minimum Gas for {args.depth}ft" +
          (f" with switch at {args.switch_depth}ft" if args.switch_depth > 0 else "") +
          f": {mg} cf")

def cmd_mod(args):
    """Calculate Maximum Operating Depth."""
    mod = g.calcMOD(args.f_o2, args.ppo2, args.water)
    print(f"MOD for {int(args.f_o2 * 100)}% O2 @ {args.ppo2} PPO2 ({args.water}): {mod} ft")

def cmd_end(args):
    """Calculate Equivalent Narcotic Depth."""
    end = g.calcEND(args.depth, args.f_he, args.water)
    print(f"END for {args.depth}ft with {int(args.f_he * 100)}% He ({args.water}): {end} ft")

def cmd_ead(args):
    """Calculate Equivalent Air Depth."""
    ead = g.calcEAD(args.depth, args.f_o2, args.water)
    print(f"EAD for {args.depth}ft with {int(args.f_o2 * 100)}% O2 ({args.water}): {ead} ft")

def cmd_tank(args):
    """Show tank specifications."""
    if args.tank_name not in g.tanks:
        print(f"Error: Tank '{args.tank_name}' not found. Available tanks: {', '.join(g.tanks.keys())}")
        sys.exit(1)

    t = g.tanks[args.tank_name]
    tf = g.calcTF(t['rated_vol'], t['rated_PSI'])
    print(f"Tank: {args.tank_name}")
    print(f"  Rated Volume: {t['rated_vol']} cf")
    print(f"  Rated Pressure: {t['rated_PSI']} psi")
    print(f"  Tank Factor: {tf} cf/100psi")

def main():
    parser = argparse.ArgumentParser(description="GUE Gas Planning Calculator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True

    # min_gas
    p_mg = subparsers.add_parser('min_gas', help='Calculate Minimum Gas')
    p_mg.add_argument('depth', type=float, help='Depth in feet')
    p_mg.add_argument('switch_depth', type=float, nargs='?', default=0, help='Gas switch depth in feet (default: 0)')
    p_mg.set_defaults(func=cmd_min_gas)

    # mod
    p_mod = subparsers.add_parser('mod', help='Calculate Maximum Operating Depth (MOD)')
    p_mod.add_argument('f_o2', type=float, help='Fraction of Oxygen (e.g. 0.32)')
    p_mod.add_argument('--ppo2', type=float, default=1.4, help='PPO2 limit (default: 1.4)')
    p_mod.add_argument('--water', choices=['salt', 'fresh'], default='salt', help='Water type (default: salt)')
    p_mod.set_defaults(func=cmd_mod)

    # end
    p_end = subparsers.add_parser('end', help='Calculate Equivalent Narcotic Depth (END)')
    p_end.add_argument('depth', type=float, help='Depth in feet')
    p_end.add_argument('f_he', type=float, help='Fraction of Helium (e.g. 0.35)')
    p_end.add_argument('--water', choices=['salt', 'fresh'], default='salt', help='Water type (default: salt)')
    p_end.set_defaults(func=cmd_end)

    # ead
    p_ead = subparsers.add_parser('ead', help='Calculate Equivalent Air Depth (EAD)')
    p_ead.add_argument('depth', type=float, help='Depth in feet')
    p_ead.add_argument('f_o2', type=float, help='Fraction of Oxygen (e.g. 0.32)')
    p_ead.add_argument('--water', choices=['salt', 'fresh'], default='salt', help='Water type (default: salt)')
    p_ead.set_defaults(func=cmd_ead)

    # tank
    p_tank = subparsers.add_parser('tank', help='Show tank specifications')
    p_tank.add_argument('tank_name', help='Name of the tank (e.g. 2xAL80)')
    p_tank.set_defaults(func=cmd_tank)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
