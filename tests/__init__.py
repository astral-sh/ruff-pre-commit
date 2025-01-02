"""This is required to get tests running and mypy to check test files."""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = (Path(__file__).parent.parent / "src").as_posix()
if SRC_DIR not in sys.path:  # pragma: no cover
    sys.path.append(SRC_DIR)
