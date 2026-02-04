import json
from datetime import datetime
from pathlib import Path
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

    def generate_config(self, history: list):
        if not self.conversation_for_requirements:
            yield "Please chat first to specify your requirements."
            return

        self.configuration_finder.halisunation_errors = {}

        try:
            summary = self.requirement_finder.extract_requirements_as_dict(self.conversation_for_requirements)

            self.print_nice(
                title="Extracted JSON Summary",
                message=str(summary),
            )

            if not summary:
                return
        except Exception as e:
            self.print_nice(
                title="Error extracting requirements",
                message=f"Failed to extract requirements: {str(e)}",
            )
            return
        yield "1. Erstelle Kartenkonfiguration..."
        map_configurations = self.configuration_finder.get_map_configurations(summary["requirements"])

        yield "2. Erstelle Portal-Footer-Konfiguration..."
        portal_footer_configurations = self.configuration_finder.get_portal_footer_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        yield "3. Erstelle Baumstruktur-Konfiguration..."
        tree_configurations = self.configuration_finder.get_tree_configurations(
            requirements=summary["requirements"],
            history=history,
        )

        yield "4. Erstelle Modul-Konfiguration..."
        module_configurations = self.configuration_finder.get_module_configurations(summary["requirements"])

        yield "5. Erstelle Menü-Konfiguration..."
        menu_configurations = self.configuration_finder.get_menu_configurations(
            requirements=summary["requirements"],
            module_configurations=module_configurations,
            history=history,
        )

        yield "6. Erstelle Layer-Konfiguration..."
        layer_configurations = self.configuration_finder.get_layer_configurations(summary["requirements"])

        yield "7. Einen Moment noch. Der letzte Schritt... Stelle finale config.json zusammen..."
        config_json = self.config_file_creator.generate_config_json(
            layer_configurations=json.loads(self.remove_comments(layer_configurations)),
            map_configurations=json.loads(self.remove_comments(map_configurations)),
            menu_configurations=json.loads(self.remove_comments(menu_configurations)),
            portal_footer_configurations=json.loads(self.remove_comments(portal_footer_configurations)),
            tree_configurations=json.loads(self.remove_comments(tree_configurations)),
        )

        self._save_generation_log(
            history=history,
            configurations={
                "map": map_configurations,
                "portalFooter": portal_footer_configurations,
                "tree": tree_configurations,
                "modules": module_configurations,
                "menu": menu_configurations,
                "layers": layer_configurations,
            },
            final_config=config_json,
            halisunation_errors=self.configuration_finder.halisunation_errors,
        )

        yield f"\n\nHier ist die config.json: \n\n```json\n{config_json}\n```"

    def _save_generation_log(self, history: list, configurations: dict, final_config: str, halisunation_errors: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        workspace_root = Path(__file__).parent.parent.parent
        log_dir = workspace_root / "logs"
        log_dir.mkdir(exist_ok=True)

        def parse_json(value):
            try:
                return json.loads(value) if isinstance(value, str) else value
            except:
                return value

        log_data = {
            "timestamp": timestamp,
            "conversation_history": history,
            "generated_configurations": {k: parse_json(v) for k, v in configurations.items()},
            "halisunation_errors": halisunation_errors,
            "final_config_json": parse_json(final_config),
        }

        log_file = log_dir / f"config_generation_{timestamp}.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        self.print_nice(
            title="LOG SAVED",
            message=f"Generation log saved to {log_file}",
        )
