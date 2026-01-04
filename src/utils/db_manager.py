import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from utils.console import Colors

# --- Constants ---

# CRITICAL: We are running this file from *inside* the 'src' directory,
# so we must go UP one level ('..') to find the 'db' folder.
DB_PATH = "../db"
EMBEDDING_MODEL = "mxbai-embed-large"  # Must match the model from ingest.py
LLM_MODEL = "llama3"  # The chat model we just pulled

# --- Simple module-level caches to avoid reloading models repeatedly ---
_embeddings = None
_vector_store = None
# This object knows how to fetch documents based on a query
_retriever = None


def _init_embeddings():
    """
    1. Initialize Models
    This mirrors the earlier inline initialization: create the Ollama embeddings
    model once and reuse it across functions.
    """
    global _embeddings
    if _embeddings is None:
        # 1. Initialize Models
        print(
            f"{Colors.CYAN}Loading embedding model '{EMBEDDING_MODEL}'...{Colors.END}"
        )
        _embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    return _embeddings


def _init_vector_store():
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
        print(
            f"{Colors.CYAN}Loading persistent vector database from '{DB_PATH}'...{Colors.END}"
        )
        _vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        # 3. Create a Retriever
        # This object knows how to fetch documents based on a query
        _retriever = _vector_store.as_retriever(
            search_kwargs={"k": 10}
        )  # Get top 10 relevant chunks
        print(f"{Colors.GREEN}✓ Retriever created successfully.{Colors.END}")
    return _vector_store
