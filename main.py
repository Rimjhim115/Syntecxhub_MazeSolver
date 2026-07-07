#!/usr/bin/env python3
"""Thin entry point so `python main.py ...` works without installing the package."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pathfinding.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
