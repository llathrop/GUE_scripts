import subprocess
import sys
import pytest

def run_cli(args):
    """Helper to run the CLI and return stdout."""
    cmd = [sys.executable, 'gue_calc_cli.py'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def test_cli_min_gas():
    out, err, code = run_cli(['min_gas', '100'])
    assert code == 0
    assert "41 cf" in out

def test_cli_mod():
    out, err, code = run_cli(['mod', '0.32'])
    assert code == 0
    assert "111 ft" in out

def test_cli_tank_error():
    out, err, code = run_cli(['tank', 'INVALID'])
    assert code == 1
    assert "Error: Tank 'INVALID' not found" in out
