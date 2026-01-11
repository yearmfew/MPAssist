from agents.requirement_finder import RequirementFinder
from agents.config_file_creator import ConfigFileCreator
from agents.configuration_finder import ConfigurationFinder


class Orchestrator:
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
        requirements = (
            self.requirement_finder.extract_requirements_from_message_as_list(
                str(llm_response)
            )
        )
        requirements = [req.strip() for req in requirements if req.strip()]

        if not requirements:
            return

        requirements_text = "\n".join(f"- {req}" for req in requirements)
        module_configurations = self.configuration_finder.get_module_configurations(
            requirements_text
        )
        config_json = self.config_file_creator.generate_config_file(
            module_configurations
        )

        yield f"\n\n Here is config.json: \n\n```json\n{config_json}\n```"
