import os
import re
import shutil
import json
from altair import layer
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# --- Settings ---
DOCS_PATH = "./project_documents"
DB_PATH = "./db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Define a batch size
BATCH_SIZE = 50

CONFIG_SECTIONS_MAPPING = {
    "layerConfig": {
        "section": "layerConfig",
        "category": "layerConfigDocumentation",
        "template": "TEMPLATE_LAYER_FINDER",
    },
    "portalConfig.map": {
        "section": "portalConfig.map",
        "category": "mapConfigDocumentation",
        "template": "TEMPLATE_MAP_FINDER",
    },
    "portalConfig.menu": {
        "section": "portalConfig.menu",
        "category": "menuConfigDocumentation",
        "template": "TEMPLATE_MENU_CONFIG_FINDER",
    },
    "portalConfig.tree": {
        "section": "portalConfig.tree",
        "category": "treeConfigDocumentation",
        "template": "TEMPLATE_TREE_CONFIG_FINDER",
    },
    "portalConfig.portalFooter": {
        "section": "portalConfig.portalFooter",
        "category": "portalFooterConfigDocumentation",
        "template": "TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER",
    },
}


def extract_references(content):
    """
    Extract internal anchor references from markdown content.
    Only extracts links in format: **[text](#anchor)** and starts with 'datatypes'.
    Returns list of lowercase anchor names that start with 'datatypes'.
    """
    pattern = r"\*\*\[([^\]]+)\]\(#([^\)]+)\)\*\*"
    matches = re.findall(pattern, content)

    references = [anchor.lower() for text, anchor in matches if anchor.lower().startswith("datatypes")]
    return list(set(references))


def extract_section(content, section_name):
    level = section_name.count(".") + 2
    header_pattern = "#" * level

    pattern = rf"^{header_pattern}\s+{re.escape(section_name)}(?:\s+\{{.*?\}})?\s*$\n(.*?)(?=^#{{1,{level}}}\s|\Z)"

    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if match:
        return f"{header_pattern} {section_name}\n\n{match.group(1).strip()}"

    return None


def extract_datatype_section(content, datatype_name):
    """
    Extract a single Datatypes.XXX section from the Datatypes section.
    Returns the content of that specific datatype.
    """
    pattern = rf"^###\s+{re.escape(datatype_name)}(?:\s+\{{.*?\}})?\s*$\n(.*?)(?=^###\s|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if match:
        return f"### {datatype_name}\n\n{match.group(1).strip()}"

    return None


def extract_datatypes(content, file_path):
    """
    Extract all Datatypes.XXX sections from the Datatypes section.
    Each datatype becomes a separate document (not chunked).
    Returns list of Documents.
    """
    documents = []

    datatypes_section = extract_section(content, "Datatypes")
    if not datatypes_section:
        print("  WARNING: Datatypes section not found")
        return documents

    pattern = r"^###\s+(Datatypes\.[^\s{]+)"
    matches = re.findall(pattern, datatypes_section, re.MULTILINE)

    for datatype_name in matches:
        datatype_content = extract_datatype_section(datatypes_section, datatype_name)

        if datatype_content:
            references = extract_references(datatype_content)

            doc = Document(
                page_content=datatype_content,
                metadata={
                    "source": file_path,
                    "section": datatype_name,
                    "category": "datatype",
                    "datatype_name": datatype_name.lower().replace(".", ""),
                    "references": ",".join(references),
                    "type": "config",
                },
            )
            documents.append(doc)

    return documents


def process_config_documentation(file_path):
    print(f"Processing configuration documentation from '{file_path}'...")
    documents = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Process normal sections
    for key, mapping in CONFIG_SECTIONS_MAPPING.items():
        section_name = mapping["section"]
        section_content = extract_section(content, section_name)

        if section_content:
            references = extract_references(section_content)
            print(
                f"  Extracted section '{section_name}': {len(section_content)} characters, {len(references)} references"
            )

            doc_metadata = {
                "section": section_name,
                "category": mapping["category"],
                "references": ",".join(references),
            }

            if "template" in mapping and mapping["template"]:
                doc_metadata["template"] = mapping["template"]

            doc = Document(
                page_content=section_content,
                metadata=doc_metadata,
            )
            documents.append(doc)
        else:
            print(f"  WARNING: Section '{section_name}' not found in document")

    # Process Datatypes separately
    print("  Processing Datatypes...")
    datatype_docs = extract_datatypes(content, file_path)

    documents.extend(datatype_docs)

    return documents


def process_layer_data(file_path):
    """
    Process layer data JSON file.
    Each object in the JSON array becomes a separate document (not chunked).
    Returns list of Documents.
    """
    print(f"Processing layer data from '{file_path}'...")
    documents = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            layer_data = json.load(f)

        if not isinstance(layer_data, list):
            print(f"  WARNING: Expected a list, got {type(layer_data)}")
            return documents

        for idx, layer_obj in enumerate(layer_data):
            # Convert object to formatted JSON string as content
            page_content = json.dumps(layer_obj, ensure_ascii=False, indent=2)

            doc = Document(
                page_content=page_content,
                metadata={
                    "category": "layerDocumentation",
                    "template": "TEMPLATE_LAYER_FINDER",
                    "name": layer_obj.get("name", f"layer_{idx}"),
                    "id": layer_obj.get("id", f"layer_{idx}"),
                },
            )
            documents.append(doc)

        print(f"  Extracted {len(documents)} layer objects")

    except Exception as e:
        print(f"  ERROR processing layer data: {e}")

    return documents


def add_custom_metadata(docs):
    """
    Custom function to add metadata to each document.
    Assigns categories and priorities for routing:
    - documentation: General Masterportal documentation
    - example: Example configurations
    """

    for doc in docs:
        source_path = doc.metadata.get("source", "")

        if "examples" in source_path:
            doc.metadata["category"] = "example"
            doc.metadata["template"] = ""

        elif "configDocumentation" in source_path:
            doc.metadata["category"] = "mainDocumentation"
            doc.metadata["template"] = ""

        else:
            doc.metadata["category"] = "documentation"

    return docs


def get_documents_from_path(path: str) -> list:
    extensions = ["**/*.md", "**/*.json"]
    documents = []

    for extension in extensions:

        loader = DirectoryLoader(
            path,
            glob=extension,
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True,
        )
        documents.extend(loader.load())

    return documents


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

    ## extract data from configDocumentation.json.de.md file using headings..
    documents = process_config_documentation(
        f"{DOCS_PATH}/masterportal-docs/User/Portal-Config/configDocumentation.json.de.md"
    )

    ## Process layer data JSON file (each object becomes a document)
    layer_data_docs = process_layer_data(f"{DOCS_PATH}/layers/layerDescriptionsCleaned.json")

    ## Add other documents from directory
    exampleDocuments = get_documents_from_path(f"{DOCS_PATH}/examples")

    # # Add custom metadata to documents
    exampleDocuments = add_custom_metadata(exampleDocuments)

    # documents.extend(layerDocuments)
    documents.extend(exampleDocuments)

    if not documents:
        print(f"WARNING: No documents found in '{DOCS_PATH}'.")
        return
    print(f"Successfully loaded {len(documents)} documents.")

    # 2. Separate normal sections and datatypes (layer data already separate)
    normal_docs = [d for d in documents if d.metadata.get("category") != "datatype"]
    datatype_docs = [d for d in documents if d.metadata.get("category") == "datatype"]

    print(f"  Normal sections: {len(normal_docs)} documents")
    print(f"  Datatypes: {len(datatype_docs)} documents (will not be chunked)")
    print(f"  Layer data: {len(layer_data_docs)} documents (will not be chunked)")

    # 3. Split normal sections into Chunks (datatypes and layer data stay whole)
    print("Splitting normal sections into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", "},", "],", " ", ""],
    )
    normal_chunks = text_splitter.split_documents(normal_docs + exampleDocuments)

    # Combine chunked normal sections with whole datatypes and layer data
    all_chunks = normal_chunks + datatype_docs + layer_data_docs
    print(
        f"Total chunks: {len(normal_chunks)} (from normal sections) + {len(datatype_docs)} (datatypes) + {len(layer_data_docs)} (layer data) = {len(all_chunks)}"
    )

    # 4. Initialize Embedding Model
    print(f"Initializing embedding model '{EMBEDDING_MODEL}'...")

    # Use local HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # 5. Create and Save Vector Store (IN BATCHES)
    if os.path.exists(DB_PATH):
        print(f"Old database found at '{DB_PATH}'. Removing it...")
        shutil.rmtree(DB_PATH)

    print("Creating new vector store (this may take a while)...")

    # Initialize an empty vector store first
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

    # Loop over all chunks in batches
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i : i + BATCH_SIZE]
        print(f"Adding batch {i//BATCH_SIZE + 1}/{len(all_chunks)//BATCH_SIZE + 1} ({len(batch)} chunks)...")

        # Add the current batch to the vector store
        vector_store.add_documents(documents=batch)

    print("\n--- 🚀 Success! ---")
    print(f"Vector store created and saved successfully at '{DB_PATH}'.")
    print(
        f"Total documents added: {len(all_chunks)} ({len(normal_chunks)} chunked sections + {len(datatype_docs)} datatypes + {len(layer_data_docs)} layer objects)"
    )


if __name__ == "__main__":
    main()
