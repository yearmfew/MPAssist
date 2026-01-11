from re import M

from agents.base_agent import BaseAgent
from utils.template import TEMPLATE_CONFIG_GENERATOR, TEMPLATE_STRUCTURE_FIXER
from utils import db_manager
from agents.halisunation_checker import HalisunationChecker
from pathlib import Path


class ConfigFileCreator(BaseAgent):
    """
    ConfigFileCreator Agent

    Responsibility: Generates the final config.json file.
    - Takes user selected tools/layers from ToolFinder
    - Uses TEMPLATE_CONFIG_GENERATOR with example template and context
    - Invokes LLM to produce complete, valid config.json
    - Returns the generated configuration as a string

    This is the final step in the pipeline that produces the actual deliverable.
    """

    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()
        self.halisunation_checker = HalisunationChecker()

    def _load_example_template(self) -> str:
        """
        Load the example.config.json file.

        Returns:
            Content of example.config.json as string
        """
        base_config_path = (
            Path(__file__).resolve().parents[2]
            / "masterportal-docs"
            / "examples"
            / "example.config.json"
        )

        try:

            file = base_config_path.read_text()
            self.printNice(title="example file", message=file)
            return file

        except FileNotFoundError:
            self.printNice(
                title=f"❌ Error: example.config.json not found at {base_config_path}. ",
                message="Please ensure the masterportal-docs repository is cloned correctly.",
            )
            return ""

    def _label_chunks(self, chunks: list) -> list:
        PRIORITY_MAP = {
            "docs_for_modules": "LOW",
            "documentation": "LOW",
            "example": "CRITICAL",
        }
        labeled_chunks = []

        for chunk in chunks:
            category = chunk.metadata.get("category", "unknown")

            agents_str = chunk.metadata.get("agents", "")
            agents = agents_str.split(",") if agents_str else []
            priority = (
                "CRITICAL"
                if "config_file_creator" in agents
                else PRIORITY_MAP.get(category, "LOW")
            )

            includes_str = chunk.metadata.get("includes", "")
            includes = includes_str.split(",") if includes_str else []
            labeled_chunk = f"[CATEGORY: {category}] [PRIORITY: {priority}] [INCLUDES: {', '.join(includes)}]\n{chunk.page_content}"
            labeled_chunks.append(labeled_chunk)

        return labeled_chunks

    def generate_config_file(self, module_configurations: str) -> str:
        if db_manager._retriever is not None:
            example_docs = self.getChunks(
                query=module_configurations,
                k=4,
                filter={"category": "example"},
            )

            remaining_k = max(0, 8 - len(example_docs))
            if remaining_k > 0:
                doc_docs = self.getChunks(
                    query=module_configurations,
                    k=remaining_k,
                    filter={"category": "documentation"},
                )
            else:
                doc_docs = []

            all_docs = example_docs + doc_docs
            labeled_chunks = self._label_chunks(all_docs)
            context = "\n\n---\n\n".join(labeled_chunks)
        else:
            context = "(No additional context available)"

        # Build comprehensive context with base config for editing
        context = f"""
            EXAMPLE.CONFIG.JSON TEMPLATE:
            ```json
            {self._load_example_template()}
            ```
            This is a working, valid, example Masterportal configuration. Also called "example.config.json".

            SELECTED TOOLS & LAYERS:
            {module_configurations}

            RELEVANT DOCUMENTATION (with priority labels):
            {context}
        """

        full_prompt = self.createPromptTemplate(
            template=TEMPLATE_CONFIG_GENERATOR,
            context=context,
            question="Generate the config.json using the EXAMPLE.CONFIG.JSON TEMPLATE above: add required modules/layers, modify values as needed, and keep existing reasonable defaults. Be conservative with deletions.",
        )

        config_output = self.invoke_llm(full_prompt)

        return config_output

    # def check_halisunation(self, current_config: str) -> str:
    #     """
    #     Validate and fix structural errors in config.json.

    #     Args:
    #         current_config: Initial config.json from LLM

    #     Returns:
    #         Validated and potentially fixed config.json as string
    #     """

    #     # Validation and fixing loop (max 3 attempts)
    #     max_retries = 3

    #     for attempt in range(max_retries):
    #         # Validate structure using HalisunationChecker
    #         structure_errors = self.halisunation_checker._validate_structure(
    #             self._parse_config(current_config)
    #         )

    #         if not structure_errors:
    #             self.printNice(
    #                 message=f"Validation passed on attempt {attempt + 1}",
    #                 title="VALIDATION SUCCESS",
    #             )
    #             return current_config

    #         errors_msg = f"Validation failed on attempt {attempt + 1}: {len(structure_errors)} error(s) found\n\nErrors:\n"
    #         for err in structure_errors:
    #             errors_msg += f"  - {err}\n"

    #         self.printNice(message=errors_msg, title="VALIDATION FAILED")

    #         self.printNice(
    #             message=current_config, title=f"CONFIG.JSON (Attempt {attempt + 1})"
    #         )

    #         if attempt < max_retries - 1:
    #             self.printNice(
    #                 message="Attempting to fix structural errors...", title="FIXING"
    #             )
    #             current_config = self.fix_structure(current_config, structure_errors)
    #         else:
    #             self.printNice(
    #                 message=f"Maximum retries ({max_retries}) reached. Returning config with errors.",
    #                 title="WARNING",
    #             )

    #     return current_config

    # def _parse_config(self, config_str: str) -> dict:
    #     """
    #     Parse config.json string and extract the JSON object.

    #     Args:
    #         config_str: Raw LLM output containing config.json

    #     Returns:
    #         Parsed config dictionary
    #     """
    #     import json

    #     # Try to extract JSON from markdown code blocks
    #     if "```json" in config_str:
    #         start = config_str.find("```json") + 7
    #         end = config_str.find("```", start)
    #         json_str = config_str[start:end].strip()
    #     elif "```" in config_str:
    #         start = config_str.find("```") + 3
    #         end = config_str.find("```", start)
    #         json_str = config_str[start:end].strip()
    #     else:
    #         # Try to find JSON object directly
    #         json_str = config_str.strip()

    #     try:
    #         return json.loads(json_str)
    #     except json.JSONDecodeError:
    #         # If parsing fails, return empty dict
    #         return {}

    # def fix_structure(self, current_config: str, validation_errors: list) -> str:
    #     """
    #     Fix structural validation errors in a config.json.

    #     This method is called when HalisunationChecker detects structural issues.
    #     It uses only the example_template to fix the structure without changing content.

    #     Args:
    #         current_config: The config.json with structural errors
    #         validation_errors: List of error messages from HalisunationChecker

    #     Returns:
    #         Fixed config.json as string
    #     """

    #     # Extract JSON from current_config if it's wrapped in markdown
    #     parsed_config = self._parse_config(current_config)
    #     import json

    #     clean_config = json.dumps(parsed_config, indent=2)

    #     errors_text = "\n".join(
    #         [f"{i+1}. {err}" for i, err in enumerate(validation_errors)]
    #     )

    #     full_prompt = self.createPromptTemplate(
    #         template=TEMPLATE_STRUCTURE_FIXER,
    #         context="",
    #         example_template=self.example_template,
    #         current_config=clean_config,
    #         validation_errors=errors_text,
    #     )

    #     fixed_config = self.invoke_llm(full_prompt)

    #     return fixed_config
