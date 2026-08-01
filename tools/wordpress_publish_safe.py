#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wordpress_publish import main


def normalize_application_password(value: str) -> str:
    """Remove display whitespace from a WordPress Application Password."""
    return re.sub(r"\s+", "", value)


def run() -> int:
    password = os.environ.get("WP_APPLICATION_PASSWORD", "")
    if password:
        os.environ["WP_APPLICATION_PASSWORD"] = normalize_application_password(password)
    return main()


if __name__ == "__main__":
    raise SystemExit(run())
