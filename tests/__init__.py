"""To get tests to work we need to add the src directory to the sys.path."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
