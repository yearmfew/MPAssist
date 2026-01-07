import os
from agents.base_agent import BaseAgent
from template import TEMPLATE_CONFIG_GENERATOR, TEMPLATE_STRUCTURE_FIXER
from langchain_core.prompts import PromptTemplate
from utils import db_manager
from agents.halisunation_checker import HalisunationChecker


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
        # Load example config.json template
        self.example_template = self._load_example_template()
        # Initialize vector store for RAG retrieval
        db_manager._init_vector_store()
        # Initialize halisunation_checker
        self.halisunation_checker = HalisunationChecker()

    def _load_example_template(self) -> str:
        """
        Load the basic/config.json file as base template.
        This is a working, valid Masterportal config that we will edit.

        Returns:
            Content of basic/config.json as string
        """
        # Get the path to basic/config.json (working example)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_config_path = os.path.join(
            # current_dir, "..", "..", "examples", "example.config.json"
            current_dir,
            "..",
            "..",
            "masterportal-docs",
            "examples",
            "example.config.json",
        )

        try:
            with open(base_config_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Fallback: try masterportal-docs path
            fallback_path = os.path.join(
                current_dir,
                "..",
                "..",
                "masterportal-docs",
                "examples",
                "example.config.json",
            )
            try:
                with open(fallback_path, "r", encoding="utf-8") as f:
                    return f.read()
            except FileNotFoundError:
                # Last resort fallback
                return "{}"

    def execute(self, tools_and_layers: str) -> str:
        """
        Generate config.json based on selected tools/layers.

        This function:
        1. Retrieves relevant context from vector DB with priority labels
        2. Loads the example.config.json template
        3. Combines tools/layers, context, and template
        4. Formats the TEMPLATE_CONFIG_GENERATOR prompt
        5. Invokes LLM to generate the config.json
        6. Returns the complete configuration

        Args:
            tools_and_layers: Selected tools and layers from ToolFinder

        Returns:
            Generated config.json as string
        """

        # Retrieve relevant context from vector DB with priority-based routing
        if db_manager._retriever is not None:
            # Stage 1: Get docs_for_modules (CRITICAL priority)
            try:
                example_docs = db_manager._vector_store.similarity_search(
                    tools_and_layers,
                    k=4,
                    filter={"category": "example"},
                )
            except Exception:
                example_docs = []

            # Stage 2: Get documentation if needed
            remaining_k = max(0, 8 - len(example_docs))
            if remaining_k > 0:
                try:
                    doc_docs = db_manager._vector_store.similarity_search(
                        tools_and_layers,
                        k=remaining_k,
                        filter={"category": "documentation"},
                    )
                except Exception:
                    doc_docs = db_manager._retriever.invoke(tools_and_layers)[
                        :remaining_k
                    ]
            else:
                doc_docs = []

            # Combine and label chunks with priority
            all_docs = example_docs + doc_docs

            # Priority mapping for different document categories
            PRIORITY_MAP = {
                "docs_for_modules": "LOW",
                "documentation": "LOW",
                "example": "CRITICAL",
            }

            context_parts = []
            for d in all_docs:
                category = d.metadata.get("category", "unknown")

                agents_str = d.metadata.get("agents", "")
                agents = agents_str.split(",") if agents_str else []
                priority = (
                    "CRITICAL"
                    if "config_file_creator" in agents
                    else PRIORITY_MAP.get(category, "LOW")
                )

                # Assign priority based on category using mapping
                # priority = PRIORITY_MAP.get(category, "LOW")

                includes_str = d.metadata.get("includes", "")
                includes = includes_str.split(",") if includes_str else []
                labeled_chunk = f"[CATEGORY: {category}] [PRIORITY: {priority}] [INCLUDES: {', '.join(includes)}]\n{d.page_content}"
                context_parts.append(labeled_chunk)

            rag_context = "\n\n---\n\n".join(context_parts)
        else:
            rag_context = "(No additional context available)"

        # Build comprehensive context with base config for editing
        context = f"""
            EXAMPLE.CONFIG.JSON TEMPLATE:
            ```json
            {self.example_template}
            ```
            This is a working, valid, example Masterportal configuration. Also called "example.config.json".

            SELECTED TOOLS & LAYERS:
            {tools_and_layers}

            RELEVANT DOCUMENTATION (with priority labels):
            {rag_context}
        """

        # Format the template with context
        prompt_template = PromptTemplate.from_template(TEMPLATE_CONFIG_GENERATOR)

        try:
            full_prompt = prompt_template.format(
                context=context,
                question="Generate the config.json using the EXAMPLE.CONFIG.JSON TEMPLATE above: add required modules/layers, modify values as needed, and keep existing reasonable defaults. Be conservative with deletions.",
            )
        except Exception:
            # Fallback formatting
            full_prompt = TEMPLATE_CONFIG_GENERATOR.replace(
                "{context}", context
            ).replace(
                "{question}",
                "Generate the config.json using the EXAMPLE.CONFIG.JSON TEMPLATE above: add required modules/layers, modify values as needed, and keep existing reasonable defaults. Be conservative with deletions.",
            )

        # Invoke LLM to generate config.json
        config_output = self.invoke_llm(full_prompt)
        return config_output

        # Validate and fix structure using HalisunationChecker
        # validated_config = self.check_halisunation(config_output)
        # return validated_config

    def check_halisunation(self, current_config: str) -> str:
        """
        Validate and fix structural errors in config.json.

        Args:
            current_config: Initial config.json from LLM

        Returns:
            Validated and potentially fixed config.json as string
        """

        # Validation and fixing loop (max 3 attempts)
        max_retries = 3

        for attempt in range(max_retries):
            # Validate structure using HalisunationChecker
            structure_errors = self.halisunation_checker._validate_structure(
                self._parse_config(current_config)
            )

            if not structure_errors:
                # No structural errors, return the config
                print(f"✓ Validation passed on attempt {attempt + 1}")
                return current_config

            # There are errors, try to fix them
            print(
                f"\n✗ Validation failed on attempt {attempt + 1}: {len(structure_errors)} error(s) found"
            )
            print(f"Errors:")
            for err in structure_errors:
                print(f"  - {err}")

            print("\n" + "-" * 70)
            print(f"CONFIG.JSON (Attempt {attempt + 1})")
            print("-" * 70)
            print(current_config)
            print("-" * 70 + "\n")

            if attempt < max_retries - 1:
                # Not the last attempt, try to fix
                print(f"Attempting to fix structural errors...\n")
                current_config = self.fix_structure(current_config, structure_errors)
            else:
                # Last attempt failed, return config with errors
                print(
                    f"⚠ Maximum retries ({max_retries}) reached. Returning config with errors.\n"
                )

        return current_config

    def _parse_config(self, config_str: str) -> dict:
        """
        Parse config.json string and extract the JSON object.

        Args:
            config_str: Raw LLM output containing config.json

        Returns:
            Parsed config dictionary
        """
        import json

        # Try to extract JSON from markdown code blocks
        if "```json" in config_str:
            start = config_str.find("```json") + 7
            end = config_str.find("```", start)
            json_str = config_str[start:end].strip()
        elif "```" in config_str:
            start = config_str.find("```") + 3
            end = config_str.find("```", start)
            json_str = config_str[start:end].strip()
        else:
            # Try to find JSON object directly
            json_str = config_str.strip()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If parsing fails, return empty dict
            return {}

    def fix_structure(self, current_config: str, validation_errors: list) -> str:
        """
        Fix structural validation errors in a config.json.

        This method is called when HalisunationChecker detects structural issues.
        It uses only the example_template to fix the structure without changing content.

        Args:
            current_config: The config.json with structural errors
            validation_errors: List of error messages from HalisunationChecker

        Returns:
            Fixed config.json as string
        """

        # Extract JSON from current_config if it's wrapped in markdown
        parsed_config = self._parse_config(current_config)
        import json

        clean_config = json.dumps(parsed_config, indent=2)

        # Format validation errors as a numbered list
        errors_text = "\n".join(
            [f"{i+1}. {err}" for i, err in enumerate(validation_errors)]
        )

        # Format the structure fixer prompt
        prompt_template = PromptTemplate.from_template(TEMPLATE_STRUCTURE_FIXER)

        try:
            full_prompt = prompt_template.format(
                example_template=self.example_template,
                current_config=clean_config,
                validation_errors=errors_text,
            )
        except Exception:
            # Fallback formatting
            full_prompt = (
                TEMPLATE_STRUCTURE_FIXER.replace(
                    "{example_template}", self.example_template
                )
                .replace("{current_config}", clean_config)
                .replace("{validation_errors}", errors_text)
            )

        # Invoke LLM to fix structural issues
        fixed_config = self.invoke_llm(full_prompt)

        return fixed_config
