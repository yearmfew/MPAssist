from agents.base_agent import BaseAgent
import utils.db_manager as db_manager
from template import TEMPLATE_TOOL_FINDER
from langchain_core.prompts import PromptTemplate
from utils.console import (
    print_box,
    print_box_end,
)


class ToolFinder(BaseAgent):
    """
    ToolFinder Agent

    Responsibility: Finds suitable Masterportal tools and layers based on requirements.
    - Takes user requirements as input
    - Performs RAG retrieval from vector database to find relevant tools/layers
    - Uses TEMPLATE_TOOL_FINDER to structure the analysis
    - Invokes LLM to determine which tools and layers are needed
    - Returns structured recommendations (tool IDs, layer configs, etc.)

    This is the intermediate step between requirement gathering and config generation.
    """

    def __init__(self):
        super().__init__()
        # Initialize vector store for RAG retrieval
        db_manager._init_vector_store()

    def execute(self, requirements: str) -> str:
        """
        Find and recommend tools/layers based on user requirements.

        Uses two-stage retrieval with metadata-based routing:
        1. STAGE 1: Retrieve from module_reference (PRIMARY - tool/module definitions)
        2. STAGE 2: Supplement with documentation if needed (SECONDARY - general info)
        3. Format context with metadata labels and invoke LLM

        Args:
            requirements: User requirements text (formatted list)

        Returns:
            Structured string with tool and layer recommendations
        """
        # Ensure retriever is initialized
        if db_manager._retriever is None:
            raise RuntimeError(
                "Retriever is not initialized. Ensure the vector DB exists and _init_vector_store() succeeded."
            )

        # ============================================================================
        # STAGE 1: Retrieve from docs_for_modules (PRIMARY SOURCE)
        # ============================================================================
        # Get module definitions - these are the authoritative source for tool/module info
        try:
            module_docs = db_manager._vector_store.similarity_search(
                requirements, k=5, filter={"category": "docs_for_modules"}
            )
        except Exception:
            # Fallback if filter not supported or no matches
            module_docs = []

        print_box("Tools & Layers (from ToolFinder)", "BLUE", 60)
        # Optionally print the tools (commented out to reduce noise)
        print(module_docs)
        print_box_end(60, "BLUE")

        # Priority mapping for different document categories
        PRIORITY_MAP = {
            "docs_for_modules": "MEDIUM",
            "documentation": "MEDIUM",
            "example": "CRITICAL",
        }

        # Join retrieved chunks into context WITH METADATA LABELS AND DYNAMIC PRIORITY
        context_parts = []
        for d in module_docs:
            # Get metadata category
            category = d.metadata.get("category", "unknown")

            ## still thinking about how to best set priority dynamically, thats why here is not good enough!!!
            agents_str = d.metadata.get("agents", "")
            agents = agents_str.split(",") if agents_str else []
            priority = (
                "CRITICAL"
                if "tool_finder" in agents
                else PRIORITY_MAP.get(category, "LOW")
            )
            # Format each chunk with category and dynamic priority labels (one-per-line for readability)
            includes_str = d.metadata.get("includes", "")
            includes = includes_str.split(",") if includes_str else []
            labeled_chunk = (
                f"[CATEGORY]: {category}\n"
                f"[PRIORITY]: {priority}\n"
                f"[INCLUDES]: {', '.join(includes)}\n\n"
                f"{d.page_content}"
            )
            context_parts.append(labeled_chunk)

        context_text = "\n\n---\n\n".join(context_parts)

        # Format the template with retrieved context and requirements
        prompt_template = PromptTemplate.from_template(TEMPLATE_TOOL_FINDER)

        try:
            full_prompt = prompt_template.format(
                context=context_text, question=requirements
            )
        except Exception:
            # Fallback formatting
            full_prompt = TEMPLATE_TOOL_FINDER.replace(
                "{context}", context_text
            ).replace("{question}", requirements)

        # Invoke LLM to analyze and select tools/layers
        tools_and_layers = self.invoke_llm(full_prompt)

        return tools_and_layers

    # Optional: Override for custom LLM behavior
    # def invoke_llm(self, prompt: str, **kwargs) -> str:
    #     """
    #     Custom LLM invocation for ToolFinder.
    #     Example: Use lower temperature for more deterministic results.
    #     """
    #     kwargs.setdefault('temperature', 0.0)
    #     return super().invoke_llm(prompt, **kwargs)
