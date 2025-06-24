"""Utility helpers."""
from __future__ import annotations

from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


def list_files(path: str) -> List[str]:
    """Return list of file paths under a directory."""
    p = Path(path)
    if p.is_dir():
        files = [str(f) for f in p.rglob("*") if f.is_file()]
        logger.debug("Listing %d files in %s", len(files), path)
        return files
    if p.exists():
        logger.debug("Listing single file %s", path)
        return [str(p)]
    logger.warning("Path does not exist: %s", path)
    return []
