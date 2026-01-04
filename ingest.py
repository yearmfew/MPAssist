import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# --- Settings ---
DOCS_PATH = "masterportal-docs"
DB_PATH = "db"
# OLLAMA_EMBEDDING_MODEL = "nomic-embed-text" // needs prefix. Using another model for now.
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"

# Define a batch size to avoid overwhelming Ollama
BATCH_SIZE = 50


def add_custom_metadata(docs):
    """
    Custom function to add metadata to each document.
    Assigns categories and priorities for routing:
    - docs_for_modules: Primary source for tool/module definitions (critical priority)
    - documentation: General Masterportal documentation (medium priority)
    - example: Example configurations (low priority)
    """

    for doc in docs:
        source_path = doc.metadata.get("source", "")

        # Priority 1: modules_doc files (PRIMARY reference for tool/module definitions)
        if "modules_docs" in source_path:
            doc.metadata["category"] = "docs_for_modules"
            doc.metadata["agents"] = "tool_finder"

        # Priority 2: Examples (structure reference only)
        elif "examples" in source_path or "modules_examples" in source_path:
            doc.metadata["category"] = "example"
            doc.metadata["agents"] = "config_file_creator"

        # cleanedDocs files
        elif "cleanedDocs" in source_path:
            if "layerConfig.md" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "layerConfig configurations"
            elif "layerConfigBaseLayer" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "layers"
            elif "layerConfigSubjectLayer" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "layers"
            elif "portalConfig.md" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = ""
            elif "portalConfigMainMenu" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "modules"
            elif "portalConfigMap" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "maps"
            elif "portalConfigPortalFooter" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = ""
            elif "portalConfigSecondaryMenu" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = "tool_finder"
                doc.metadata["includes"] = "modules"
            elif "portalConfigTree" in source_path:
                doc.metadata["category"] = "documentation"
                doc.metadata["agents"] = ""

        # Priority 3: General documentation
        else:
            doc.metadata["category"] = "documentation"
            doc.metadata["agents"] = "config_file_creator"

    return docs


def main():
    """
    Main data ingestion function.
    1. Loads documents.
    2. Splits them into chunks.
    3. Initializes the embedding model.
    4. Creates and saves the vector store IN BATCHES.
    """

    # 1. Load Documents
    print(f"Loading documents from '{DOCS_PATH}'...")
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True,
    )
    documents = loader.load()

    # Add custom metadata to documents
    documents = add_custom_metadata(documents)

    if not documents:
        print(f"WARNING: No documents found in '{DOCS_PATH}'.")
        return
    print(f"Successfully loaded {len(documents)} documents.")

    # 2. Split into Chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} chunks.")

    # 3. Initialize Embedding Model
    print(f"Initializing Ollama embedding model '{OLLAMA_EMBEDDING_MODEL}'...")

    # Use the correct, non-deprecated class
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)

    print("Embedding model initialized successfully.")

    # 4. Create and Save Vector Store (IN BATCHES)
    if os.path.exists(DB_PATH):
        print(f"Old database found at '{DB_PATH}'. Removing it...")
        shutil.rmtree(DB_PATH)

    print("Creating new vector store (this may take a while)...")

    # Initialize an empty vector store first
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

    # Loop over the chunks in batches
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        print(
            f"Adding batch {i//BATCH_SIZE + 1}/{len(chunks)//BATCH_SIZE + 1} ({len(batch)} chunks)..."
        )

        # Add the current batch to the vector store
        vector_store.add_documents(documents=batch)

    print("\n--- 🚀 Success! ---")
    print(f"Vector store created and saved successfully at '{DB_PATH}'.")
    print(f"A total of {len(chunks)} document chunks were added to the database.")


if __name__ == "__main__":
    main()
