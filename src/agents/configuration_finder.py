from agents.base_agent import BaseAgent
from utils import db_manager
from utils.template import TEMPLATE_TOOL_FINDER


class ConfigurationFinder(BaseAgent):
    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()

    def get_module_configurations(self, requirements: str) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=5,
            filter={"category": "docs_for_modules"},
        )

        labelled_chunks = self._label_chunks(chunks)

        context_text = "\n\n---\n\n".join(labelled_chunks)

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_TOOL_FINDER,
            context=context_text,
            requirements=requirements,
        )

        moduleConfigurations = self.invoke_llm(full_prompt)

        return moduleConfigurations

    def _label_chunks(self, chunks: list) -> list:
        PRIORITY_MAP = {
            "docs_for_modules": "MEDIUM",
            "documentation": "MEDIUM",
            "example": "CRITICAL",
        }
        labeled_chunks = []

        for chunk in chunks:
            category = chunk.metadata.get("category", "unknown")

            agents_str = chunk.metadata.get("agents", "")
            agents = agents_str.split(",") if agents_str else []
            priority = (
                "CRITICAL"
                if "tool_finder" in agents
                else PRIORITY_MAP.get(category, "LOW")
            )
            includes_str = chunk.metadata.get("includes", "")
            includes = includes_str.split(",") if includes_str else []
            labeled_chunk = (
                f"[CATEGORY]: {category}\n"
                f"[PRIORITY]: {priority}\n"
                f"[INCLUDES]: {', '.join(includes)}\n\n"
                f"{chunk.page_content}"
            )
            labeled_chunks.append(labeled_chunk)

        return labeled_chunks
