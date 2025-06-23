"""Document summarization utilities."""
from __future__ import annotations

from typing import List

from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOllama

from langchain.docstore.document import Document


def summarize_documents(docs: List[Document]) -> str:
    """Summarize documents using a map-reduce chain.

    Parameters
    ----------
    docs : list of Document
        Documents to summarize.

    Returns
    -------
    str
        The summarized text.
    """
    llm = ChatOllama(model="llama2")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)
