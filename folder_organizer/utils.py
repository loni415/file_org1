"""Utility helpers."""
from __future__ import annotations

from pathlib import Path
from typing import List


def list_files(path: str) -> List[str]:
    """Return list of file paths under a directory."""
    p = Path(path)
    if p.is_dir():
        return [str(f) for f in p.rglob("*") if f.is_file()]
    if p.exists():
        return [str(p)]
    return []
