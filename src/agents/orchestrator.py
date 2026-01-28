import re
import json
from agents.requirement_finder import RequirementFinder
from agents.config_file_creator import ConfigFileCreator
from agents.configuration_finder import ConfigurationFinder
from agents.base_agent import BaseAgent


class Orchestrator(BaseAgent):
    def __init__(self):
        self.requirement_finder = RequirementFinder()
        self.configuration_finder = ConfigurationFinder()
        self.config_file_creator = ConfigFileCreator()

    def run(self, message: str, history: list):
        response = self.requirement_finder.chat_to_find_requirements(message, history)
        yield response["llm_response"]

        if response.get("isFinished"):
            yield from self._generate_final_config(llm_response=response["llm_response"], history=history)

    def _generate_final_config(self, llm_response, history):

        summary = self.requirement_finder.extract_requirements_as_dict(llm_response)

        self.print_nice(
            title="Extracted JSON Summary",
            message=str(summary),
        )

        if not summary:
            return

        module_configurations = self.configuration_finder.get_module_configurations(summary["requirements"])

        menu_configurations = self.configuration_finder.get_menu_configurations(
            requirements=summary["requirements"],
            module_configurations=module_configurations,
            history=history,
        )
        layer_configurations = self.configuration_finder.get_layer_configurations(summary["requirements"])
        map_configurations = self.configuration_finder.get_map_configurations(summary["requirements"])

        portal_footer_configurations = self.configuration_finder.get_portal_footer_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        tree_configurations = self.configuration_finder.get_tree_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        self.print_nice(
            title="Generated Map Configurations",
            message=map_configurations,
        )

        self.print_nice(
            title="Generated PORTAL FOOTER Configurations",
            message=portal_footer_configurations,
        )

        self.print_nice(
            title="Generated TREE Configurations",
            message=tree_configurations,
        )

        self.print_nice(
            title="Generated MENU Configurations",
            message=menu_configurations,
        )

        config_json = self.config_file_creator.generate_config_json(
            layer_configurations=json.loads(layer_configurations),
            map_configurations=json.loads(map_configurations),
            menu_configurations=json.loads(menu_configurations),
            portal_footer_configurations=json.loads(portal_footer_configurations),
            tree_configurations=json.loads(tree_configurations),
        )

        yield f"\n\n Here is config.json: \n\n```json\n{config_json}\n```"
