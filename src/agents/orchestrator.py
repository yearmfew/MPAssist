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
        self.conversation_for_requirements = ""

    def run(self, message: str, history: list):
        response = self.requirement_finder.chat_to_find_requirements(message, history)
        self.conversation_for_requirements = str(response["llm_response"])

        yield self.conversation_for_requirements

        if response.get("isFinished"):
            yield from self._generate_final_config(llm_response=self.conversation_for_requirements, history=history)

    def generate_config(self, history: list):
        if not self.conversation_for_requirements:
            yield "Please chat first to specify your requirements."
            return

        yield from self._generate_final_config(llm_response=self.conversation_for_requirements, history=history)

    def _generate_final_config(self, llm_response, history):

        summary = self.requirement_finder.extract_requirements_as_dict(llm_response)

        self.print_nice(
            title="Extracted JSON Summary",
            message=str(summary),
        )

        if not summary:
            return

        map_configurations = self.configuration_finder.get_map_configurations(summary["requirements"])

        portal_footer_configurations = self.configuration_finder.get_portal_footer_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        tree_configurations = self.configuration_finder.get_tree_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        module_configurations = self.configuration_finder.get_module_configurations(summary["requirements"])

        menu_configurations = self.configuration_finder.get_menu_configurations(
            requirements=summary["requirements"],
            module_configurations=module_configurations,
            history=history,
        )
        layer_configurations = self.configuration_finder.get_layer_configurations(summary["requirements"])

        self.print_nice(
            title="Generated Map Configurations",
            message=map_configurations,
        )

        # self.print_nice(
        #     title="Generated PORTAL FOOTER Configurations",
        #     message=portal_footer_configurations,
        # )

        # self.print_nice(
        #     title="Generated TREE Configurations",
        #     message=tree_configurations,
        # )

        # self.print_nice(
        #     title="Generated MENU Configurations",
        #     message=menu_configurations,
        # )

        # self.print_nice(
        #     title="Generated Layer Configurations",
        #     message=layer_configurations,
        # )

        config_json = self.config_file_creator.generate_config_json(
            layer_configurations=json.loads(self.remove_comments(layer_configurations)),
            map_configurations=json.loads(self.remove_comments(map_configurations)),
            menu_configurations=json.loads(self.remove_comments(menu_configurations)),
            portal_footer_configurations=json.loads(self.remove_comments(portal_footer_configurations)),
            tree_configurations=json.loads(self.remove_comments(tree_configurations)),
        )

        yield f"\n\n Here is config.json: \n\n```json\n{config_json}\n```"
