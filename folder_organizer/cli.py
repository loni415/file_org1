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

    while True:
        print("Summary:\n", summary)
        action = prompt(
            "Options: [a]ccept/[r]egenerate/[e]dit/[c]ancel: "
        ).strip().lower()

        if action.startswith("a"):
            metadata = generate_metadata(
                args.path, summary, list_files(args.path)
            )
            print("Metadata:\n", metadata)
            break
        if action.startswith("r"):
            summary = summarize_documents(docs)
            continue
        if action.startswith("e"):
            summary = prompt("Edit summary:", default=summary)
            continue
        if action.startswith("c"):
            break


if __name__ == "__main__":
    main()
