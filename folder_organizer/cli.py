"""Command line interface for folder organizer."""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

# Remove prompt_toolkit import, use built-in input() instead

from .loader import load_documents
from .summarizer import summarize_documents
from .metadata import generate_metadata
from .utils import list_files

logger = logging.getLogger(__name__)

# Ensure logs are written to the project root
LOG_FILE = Path(__file__).resolve().parent.parent / "folder_organizer.log.txt"


def main() -> None:
    """Entry point for the CLI."""
    try:
        level_name = os.getenv("LOGLEVEL", "DEBUG").upper()
        level = getattr(logging, level_name, logging.INFO)
        
        # Configure logging to both file and console
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(str(LOG_FILE)),
                logging.StreamHandler()  # Add console output
            ]
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
            print("\nSummary:")
            print(summary)
            print("\nOptions: [a]ccept/[r]egenerate/[e]dit/[c]ancel")
            
            try:
                action = input("Your choice: ").strip().lower()
                logger.debug("User selected action: %s", action)
            except (EOFError, KeyboardInterrupt):
                logger.info("User interrupted")
                break

            if action.startswith("a"):
                logger.info("User accepted summary; generating metadata")
                metadata = generate_metadata(
                    args.path, summary, list_files(args.path)
                )
                logger.debug("Generated metadata: %s", metadata)

                print("\nMetadata:")
                print(metadata)
                break
            elif action.startswith("r"):
                logger.info("Regenerating summary")
                summary = summarize_documents(docs)
                continue
            elif action.startswith("e"):
                logger.info("Editing summary")
                print("Enter new summary (press Enter on empty line to finish):")
                lines = []
                while True:
                    try:
                        line = input()
                        if line == "":
                            break
                        lines.append(line)
                    except (EOFError, KeyboardInterrupt):
                        break
                summary = "\n".join(lines) if lines else summary
                continue
            elif action.startswith("c"):
                logger.info("User cancelled")
                break
            else:
                logger.warning("Invalid option: %s", action)
                print("Invalid option, please try again.")
                continue
                
    except Exception as e:
        logger.error("Application error: %s", e)
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
