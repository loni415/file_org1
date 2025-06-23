"""Document loading utilities."""
from __future__ import annotations

from pathlib import Path
from typing import List

from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain.docstore.document import Document


def load_documents(path: str) -> List[Document]:
    """Load documents from the provided path.

    Parameters
    ----------
    path : str
        Path to a file or directory.

    Returns
    -------
    List[Document]
        Loaded documents.
    """
    p = Path(path)
    docs: List[Document] = []

    if p.is_dir():
        for file in p.rglob("*"):
            docs.extend(_load_file(file))
    else:
        docs.extend(_load_file(p))
    return docs


def _load_file(file: Path) -> List[Document]:
    """Load a single file."""
    if not file.exists():
        return []
    if file.suffix.lower() == ".pdf":
        return PyPDFLoader(str(file)).load()
    else:
        return TextLoader(str(file)).load()
