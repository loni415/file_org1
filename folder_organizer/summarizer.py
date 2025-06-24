"""Document summarization utilities."""
from __future__ import annotations

from typing import List
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_community.llms import Ollama
from langchain_ollama.chat_models import ChatOllama
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
from langchain.docstore.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM

logger = logging.getLogger(__name__)

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
    logger.info("Summarizing %d document(s)", len(docs))
    model_name = "minicpm-v:8b-2.6-q4_K_M"
    llm = ChatOllama(model=model_name)
    logger.debug("Created ChatOllama with model %s", model_name)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    logger.debug("Loaded summarize chain")
    try:
        result = chain.invoke({"input_documents": docs})
        logger.debug("Summary result: %s", result)
    except OllamaEndpointNotFoundError as exc:
        logger.error("Ollama model not found", exc_info=True)
        raise RuntimeError(
            "Ollama model not found. Run 'ollama pull' first."
        ) from exc

    if isinstance(result, dict):
        summary_text = result.get("output_text", "")
    else:
        summary_text = str(result)
    logger.info("Generated summary of length %d", len(summary_text))
    return summary_text

