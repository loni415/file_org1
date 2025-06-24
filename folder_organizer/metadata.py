"""Metadata generation utilities."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
import logging

from jsonschema import Draft7Validator

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "metadata.schema.json"

with SCHEMA_PATH.open("r", encoding="utf-8") as f:
    METADATA_SCHEMA = json.load(f)

VALIDATOR = Draft7Validator(METADATA_SCHEMA)

logger = logging.getLogger(__name__)


def generate_metadata(path: str, summary: str, source_files: List[str]) -> Dict[str, Any]:
    """Generate and validate metadata for a folder or file."""
    logger.info("Generating metadata for %s", path)
    metadata = {
        "path": path,
        "summary": summary,
        "tags": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_files": source_files,
    }
    VALIDATOR.validate(metadata)
    logger.debug("Metadata validated successfully")
    return metadata
