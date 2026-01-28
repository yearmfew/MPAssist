from agents.base_agent import BaseAgent
from utils.template import TEMPLATE_CONFIG_GENERATOR
from utils import db_manager
from agents.halisunation_checker import HalisunationChecker
from pathlib import Path
import json
import re


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
            Path(__file__).resolve().parents[2] / "masterportal-docs" / "examples" / "example.config.json"
        )

        try:
            return base_config_path.read_text()

        except FileNotFoundError:
            self.print_nice(
                title=f"❌ Error: example.config.json not found at {base_config_path}. ",
                message="Please ensure the masterportal-docs repository is cloned correctly.",
            )
            return ""

    def _label_chunks(
        self,
        chunks: list,
        templateName: str = "",
        priority_map: dict = {},
    ) -> list:

        labeled_chunks = []

        for chunk in chunks:
            category = chunk.metadata.get("category", "unknown")

            templateFromMetadata = chunk.metadata.get("template", "")

            if templateName == templateFromMetadata:
                priority = "CRITICAL"
            else:
                priority = priority_map.get(category, "LOW")

            labeled_chunk = f"[CATEGORY]: {category}\n" f"[PRIORITY]: {priority}\n" f"{chunk.page_content}"

            labeled_chunks.append(labeled_chunk)

        return labeled_chunks

    def generate_config_file(
        self,
        module_configurations: str,
        layer_configurations: str,
        map_configurations: str,
        menu_configurations: str,
    ) -> str:

        chunks_for_example_templates = self.get_chunks(
            query="config.json",
            k=4,
            filter={"category": "example"},
        )

        labeled_chunks_for_example_templates = self._label_chunks(
            chunks_for_example_templates,
            priority_map={
                "example": "CRITICAL",
            },
        )

        module_configurations_context = "\n\n---\n\n".join(module_configurations)
        layer_configurations_context = "\n\n---\n\n".join(layer_configurations)
        map_configurations_context = "\n\n---\n\n".join(map_configurations)
        menu_configurations_context = "\n\n---\n\n".join(menu_configurations)

        example_template_context = "\n\n---\n\n".join(labeled_chunks_for_example_templates)

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_CONFIG_GENERATOR,
            context=example_template_context,
            module_configurations=module_configurations_context,
            layer_configurations=layer_configurations_context,
            map_configurations=map_configurations_context,
            menu_configurations=menu_configurations_context,
        )

        config_output = self.invoke_llm(full_prompt)

        return config_output

    def generate_config_json(
        self,
        layer_configurations: dict,
        map_configurations: dict,
        menu_configurations: dict,
        portal_footer_configurations: dict,
        tree_configurations: dict,
    ) -> str:

        default_config_json = self.read_file(file_path="masterportal-docs/examples/example.config.json")
        # default_config_json = self.read_file(file_path="masterportal-docs/defaults/default.config.json")

        if not default_config_json:
            return "{}"

        try:
            merged_config = json.loads(default_config_json)
        except json.JSONDecodeError:
            self.print_nice(
                title="❌ Error: Failed to parse example.config.json",
                message="The file is not valid JSON.",
            )
            return "{}"

        merged_config["portalConfig"]["map"] = map_configurations["map"]
        merged_config["portalConfig"]["portalFooter"] = portal_footer_configurations["portalFooter"]
        merged_config["portalConfig"]["tree"] = tree_configurations["tree"]
        merged_config["portalConfig"]["mainMenu"] = menu_configurations["portalConfig"]["mainMenu"]
        merged_config["portalConfig"]["secondaryMenu"] = menu_configurations["portalConfig"]["secondaryMenu"]
        merged_config["layerConfig"] = layer_configurations["layerConfig"]

        return json.dumps(merged_config, indent=4)
