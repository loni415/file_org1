"""Document loading utilities."""
from __future__ import annotations

from pathlib import Path
from typing import List
from zipfile import is_zipfile

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
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
    if is_zipfile(file):
        # Skip archives
        return []
    suffix = file.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file))
    elif suffix in {".docx", ".doc"}:
        loader = Docx2txtLoader(str(file))
    elif suffix == ".md":
        loader = UnstructuredMarkdownLoader(str(file))
    elif suffix in {".txt", ""}:
        loader = TextLoader(str(file), autodetect_encoding=True)
    else:
        # unsupported file type
        return []

    try:
        return loader.load()
    except Exception:
        # skip files that cannot be read (e.g. unknown encoding)
        return []
