import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- Settings ---
DOCS_PATH = "./masterportal-docs"
DB_PATH = "./db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Define a batch size
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

        if "examples" in source_path:
            doc.metadata["category"] = "example"

        # cleanedDocs files
        elif "cleanedDocs" in source_path:
            if "layerConfig.md" in source_path:
                doc.metadata["category"] = "layerConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_LAYER_FINDER"
            elif "portalConfig.md" in source_path:
                doc.metadata["category"] = "portalConfigDocumentation"
            elif "portalConfigMap" in source_path:
                doc.metadata["category"] = "mapConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_MAP_FINDER"
            elif "portalConfigModules" in source_path:
                doc.metadata["category"] = "modulesConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_MODULE_FINDER"
            elif "portalConfigPortalFooter" in source_path:
                doc.metadata["category"] = "portalFooterConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER"
            elif "portalConfigTree" in source_path:
                doc.metadata["category"] = "treeConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_TREE_CONFIG_FINDER"
            elif "portalConfigMainMenu" in source_path:
                doc.metadata["category"] = "mainMenuConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_MENU_CONFIG_FINDER"
            elif "portalConfigSecondaryMenu" in source_path:
                doc.metadata["category"] = "secondaryMenuConfigDocumentation"
                doc.metadata["template"] = "TEMPLATE_MENU_CONFIG_FINDER"

        elif "configDocumentation" in source_path:
            doc.metadata["category"] = "mainDocumentation"

        elif "layerDocumentation" in source_path:
            doc.metadata["category"] = "layerDocumentation"
            doc.metadata["template"] = "TEMPLATE_LAYER_FINDER"
        else:
            doc.metadata["category"] = "documentation"

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

    extensions = ["**/*.md", "**/*.json"]
    documents = []
    for extension in extensions:

        loader = DirectoryLoader(
            DOCS_PATH,
            glob=extension,
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True,
        )
        documents.extend(loader.load())

    # Add custom metadata to documents
    documents = add_custom_metadata(documents)

    if not documents:
        print(f"WARNING: No documents found in '{DOCS_PATH}'.")
        return
    print(f"Successfully loaded {len(documents)} documents.")

    # 2. Split into Chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", "},", "],", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} chunks.")

    # 3. Initialize Embedding Model
    print(f"Initializing embedding model '{EMBEDDING_MODEL}'...")

    # Use local HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

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
        print(f"Adding batch {i//BATCH_SIZE + 1}/{len(chunks)//BATCH_SIZE + 1} ({len(batch)} chunks)...")

        # Add the current batch to the vector store
        vector_store.add_documents(documents=batch)

    print("\n--- 🚀 Success! ---")
    print(f"Vector store created and saved successfully at '{DB_PATH}'.")
    print(f"A total of {len(chunks)} document chunks were added to the database.")


if __name__ == "__main__":
    main()
