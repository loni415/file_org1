"""Document summarization utilities."""
from __future__ import annotations

from typing import List
import logging
from langchain_ollama import ChatOllama, OllamaLLM
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

def summarize_documents(docs: List[Document]) -> str:
    """Summarize documents using a map-reduce chain."""
    logger.info("Summarizing %d document(s)", len(docs))
    
    # Check if documents need chunking
    chunked_docs = []
    for doc in docs:
        if len(doc.page_content.split()) > 800:  # Rough token estimate
            chunks = chunk_text(doc.page_content, max_tokens=800)
            for chunk in chunks:
                chunked_docs.append(Document(page_content=chunk, metadata=doc.metadata))
        else:
            chunked_docs.append(doc)
    
    logger.info("Processing %d document chunks", len(chunked_docs))
    
    model_name = "minicpm-v:8b-2.6-q4_K_M"
    llm = ChatOllama(model=model_name)
    logger.debug("Created ChatOllama with model %s", model_name)

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    logger.debug("Loaded summarize chain")
    
    try:
        result = chain.invoke({"input_documents": chunked_docs})
        logger.debug("Summary result: %s", result)
    except OllamaEndpointNotFoundError as exc:
        logger.error("Ollama model not found", exc_info=True)
        raise RuntimeError(
            "Ollama model not found. Run 'ollama pull minicpm-v:8b-2.6-q4_K_M' first."
        ) from exc

    if isinstance(result, dict):
        summary_text = result.get("output_text", "")
    else:
        summary_text = str(result)
    
    logger.info("Generated summary of length %d", len(summary_text))
    return summary_text

def chunk_text(text: str, max_tokens: int = 800) -> List[str]:
    """Split text into chunks that fit within token limits."""
    # Simple word-based chunking - you may want to use a proper tokenizer
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        # Rough estimate: 1 token ≈ 0.75 words
        if len(current_chunk) * 0.75 > max_tokens:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

