from agents.base_agent import BaseAgent
from utils import db_manager
from agents.halisunation_checker import HalisunationChecker
import json


class ConfigFileCreator(BaseAgent):
    """
    ConfigFileCreator Agent

    Responsibility: Generates the final config.json file.
    - Takes created configurations from other agents as input.
    - Returns the generated config.json

    This is the final step in the pipeline that produces the actual deliverable.
    """

    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()
        self.halisunation_checker = HalisunationChecker()

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

    def generate_config_json(
        self,
        layer_configurations: dict,
        map_configurations: dict,
        menu_configurations: dict,
        portal_footer_configurations: dict,
        tree_configurations: dict,
    ) -> str:

        default_config_json = self.read_file(file_path="masterportal-docs/defaults/default.config.json")

        if not default_config_json:
            return "{}"

        try:
            config_json = json.loads(default_config_json)
        except json.JSONDecodeError:
            self.print_nice(
                title="❌ Error: Failed to parse default.config.json",
                message="The file is not valid JSON.",
            )
            return "{}"

        config_json["portalConfig"]["map"] = map_configurations["map"]
        config_json["portalConfig"]["portalFooter"] = portal_footer_configurations["portalFooter"]
        config_json["portalConfig"]["tree"] = tree_configurations["tree"]
        config_json["portalConfig"]["mainMenu"] = menu_configurations["portalConfig"]["mainMenu"]
        config_json["portalConfig"]["secondaryMenu"] = menu_configurations["portalConfig"]["secondaryMenu"]
        config_json["layerConfig"] = layer_configurations["layerConfig"]

        return json.dumps(config_json, indent=2)
