"""Folder Organizer package."""

from .loader import load_documents
from .summarizer import summarize_documents
from .metadata import generate_metadata

__all__ = [
    "load_documents",
    "summarize_documents",
    "generate_metadata",
]
