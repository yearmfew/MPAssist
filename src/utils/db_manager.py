import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from utils.settings import EMBEDDING_MODEL, DB_PATH


# --- Simple module-level caches to avoid reloading models repeatedly ---
_embeddings = None
_vector_store = None
# This object knows how to fetch documents based on a query
_retriever = None


def _init_embeddings():
    """
    1. Initialize Models
    Initialize local HuggingFace embeddings.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def _init_vector_store(k=10):
    """
    2. Load Vector Database & Create Retriever
    This centralizes the logic that previously lived in `main()`:
    - ensure DB exists (same warning as before)
    - create Chroma vector store using the shared embeddings
    - expose a retriever for fetching relevant context
    """
    global _vector_store, _retriever
    if _vector_store is None:
        # 2. Load Vector Database
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(
                f"Database not found at '{DB_PATH}'. Run ingest.py first."
            )
        embeddings = _init_embeddings()

        _vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        # 3. Create a Retriever
        _retriever = _vector_store.as_retriever(search_kwargs={"k": k})
    return _vector_store
