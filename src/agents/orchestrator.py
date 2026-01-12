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
            yield from self._generate_final_config(response["llm_response"])

    def _generate_final_config(self, llm_response):

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
        )

        layer_configurations = self.configuration_finder.get_layer_configurations(summary["requirements"])

        map_configurations = self.configuration_finder.get_map_configurations(summary["requirements"])

        self.print_nice(
            title="Generated MODULE Configurations",
            message=module_configurations,
        )
        self.print_nice(
            title="Generated MENU Configurations",
            message=menu_configurations,
        )
        self.print_nice(
            title="Generated Layer Configurations",
            message=layer_configurations,
        )
        self.print_nice(
            title="Generated Map Configurations",
            message=map_configurations,
        )

        menu_config_dict = json.loads(menu_configurations)
        layer_config_dict = json.loads(layer_configurations)
        map_config_dict = json.loads(map_configurations)

        config_json = self.config_file_creator.generate_config_json(
            layer_configurations=layer_config_dict,
            map_configurations=map_config_dict,
            menu_configurations=menu_config_dict,
        )

        yield f"\n\n Here is config.json: \n\n```json\n{config_json}\n```"
