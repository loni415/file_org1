"""Command line interface for folder organizer."""
from __future__ import annotations

import argparse
from prompt_toolkit import prompt

from .loader import load_documents
from .summarizer import summarize_documents
from .metadata import generate_metadata
from .utils import list_files


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Summarize a folder")
    parser.add_argument("--path", required=True, help="Path to folder or file")
    args = parser.parse_args()

    docs = load_documents(args.path)
    summary = summarize_documents(docs)
    print("Summary:\n", summary)

    confirm = prompt("Accept summary? (y/n) ")
    if confirm.lower().startswith("y"):
        metadata = generate_metadata(args.path, summary, list_files(args.path))
        print("Metadata:\n", metadata)


if __name__ == "__main__":
    main()
