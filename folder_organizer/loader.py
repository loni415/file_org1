"""Document loading utilities."""
from __future__ import annotations

from pathlib import Path
from typing import List
from zipfile import is_zipfile
import logging

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)


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
    logger.info("Loading documents from path %s", path)
    p = Path(path)
    docs: List[Document] = []

    if p.is_dir():
        for file in p.rglob("*"):
            docs.extend(_load_file(file))
    else:
        docs.extend(_load_file(p))
    logger.debug("Loaded %d document(s)", len(docs))
    return docs


def _load_file(file: Path) -> List[Document]:
    """Load a single file."""
    if not file.exists():
        logger.warning("File does not exist: %s", file)
        return []
    if is_zipfile(file):
        logger.info("Skipping archive %s", file)
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
        logger.info("Unsupported file type: %s", file)
        return []

    try:
        logger.debug("Loading file %s", file)
        docs = loader.load()
        logger.debug("Loaded %d doc(s) from %s", len(docs), file)
        return docs

    except Exception as exc:
        logger.warning("Failed to load %s: %s", file, exc)
        # skip files that cannot be read (e.g. unknown encoding)
        return []
