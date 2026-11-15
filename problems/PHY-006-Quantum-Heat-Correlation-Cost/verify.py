#!/usr/bin/env python3
"""GitHub Actions entrypoint for the PHY-006 exact primary verifier."""
from pathlib import Path
from runpy import run_path
run_path(str(Path(__file__).with_name("verify_optimal.py")), run_name="__main__")
