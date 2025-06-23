"""Document summarization utilities."""
from __future__ import annotations

from typing import List
from langchain_ollama.llms import OllamaLLM
from langchain_community.llms import Ollama
from langchain_ollama.chat_models import ChatOllama
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
from langchain.docstore.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM

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
    llm = ChatOllama(model="minicpm-v:8b-2.6-q4_K_M")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    try:
        result = chain.invoke({"input_documents": docs})
    except OllamaEndpointNotFoundError as exc:
        raise RuntimeError(
            "Ollama model not found. Run 'ollama pull' first."
        ) from exc

    if isinstance(result, dict):
        return result.get("output_text", "")
    return str(result)

