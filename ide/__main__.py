# ───────────────────────────────────────────────────────────────────────────
# ide/__main__.py  ──  `python -m ide` launches the graphical IDE.
# ───────────────────────────────────────────────────────────────────────────
import sys

from . import launch

if __name__ == "__main__":
    sys.exit(launch() or 0)
