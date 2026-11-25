#!/usr/bin/env python3
"""Verify the existing site without regenerating it.

Thin wrapper around `python3 tools/build_site.py --verify-only`.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

BUILD = Path(__file__).with_name("build_site.py")
sys.argv = [str(BUILD), "--verify-only", *sys.argv[1:]]
runpy.run_path(str(BUILD), run_name="__main__")
