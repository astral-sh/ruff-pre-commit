"""This is required to get tests running and mypy to check test files."""

from __future__ import annotations

import sys
from pathlib import Path

if (SRC_DIR := (Path(__file__).parent.parent / "src").as_posix()) not in sys.path:
    sys.path.append(SRC_DIR)
