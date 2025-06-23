"""Document summarization utilities."""
from __future__ import annotations

from typing import List

from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
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
    try:
        result = chain.invoke({"input_documents": docs})
    except OllamaEndpointNotFoundError as exc:
        raise RuntimeError(
            "Ollama model 'llama2' not found. Run 'ollama pull llama2' first."
        ) from exc

    if isinstance(result, dict):
        return result.get("output_text", "")
    return str(result)

