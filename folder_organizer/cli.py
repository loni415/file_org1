"""Command line interface for folder organizer."""
from __future__ import annotations

import argparse
from prompt_toolkit import prompt
import logging
import os
from pathlib import Path


from .loader import load_documents
from .summarizer import summarize_documents
from .metadata import generate_metadata
from .utils import list_files

logger = logging.getLogger(__name__)

# Ensure logs are written to the project root
LOG_FILE = Path(__file__).resolve().parent.parent / "folder_organizer.log.txt"


def main() -> None:
    """Entry point for the CLI."""
    level_name = os.getenv("LOGLEVEL", "DEBUG").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        filename=str(LOG_FILE),
    )
    parser = argparse.ArgumentParser(description="Summarize a folder")
    parser.add_argument("--path", required=True, help="Path to folder or file")
    args = parser.parse_args()

    logger.info("Loading documents from %s", args.path)
    docs = load_documents(args.path)
    logger.info("Summarizing %d documents", len(docs))
    summary = summarize_documents(docs)
    logger.debug("Initial summary: %s", summary)

    while True:
        print("Summary:\n", summary)
        action = prompt(
            "Options: [a]ccept/[r]egenerate/[e]dit/[c]ancel: "
        ).strip().lower()
        logger.debug("User selected action: %s", action)

        if action.startswith("a"):
            logger.info("User accepted summary; generating metadata")
            metadata = generate_metadata(
                args.path, summary, list_files(args.path)
            )
            logger.debug("Generated metadata: %s", metadata)

            print("Metadata:\n", metadata)
            break
        if action.startswith("r"):
            logger.info("Regenerating summary")
            summary = summarize_documents(docs)
            continue
        if action.startswith("e"):
            logger.info("Editing summary")
            summary = prompt("Edit summary:", default=summary)
            continue
        if action.startswith("c"):
            logger.info("User cancelled")
            break
        else:
            logger.warning("Invalid option: %s", action)
            print("Invalid option, please try again.")
            continue


if __name__ == "__main__":
    main()
