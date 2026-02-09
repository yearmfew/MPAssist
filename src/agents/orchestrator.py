import json
from datetime import datetime
from pathlib import Path
from agents.requirement_finder import RequirementFinder
from agents.config_file_creator import ConfigFileCreator
from agents.configuration_finder import ConfigurationFinder
from agents.base_agent import BaseAgent
from utils.template import TEMPLATE_REVIEW
from utils.settings import K


class Orchestrator(BaseAgent):
    def __init__(self):
        super().__init__()
        self.requirement_finder = RequirementFinder()
        self.configuration_finder = ConfigurationFinder()
        self.config_file_creator = ConfigFileCreator()
        self.conversation_for_requirements = ""
        self.latest_config_json = None
        self.review_mode = False

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
        yield "1. Erstelle Map Konfiguration..."
        try:
            map_configurations = self.configuration_finder.get_map_configurations(summary["requirements"])
        except Exception as e:
            self.print_nice(
                title="Error generating map configuration",
                message=f"Failed to generate map configuration: {str(e)}",
            )
            map_configurations = "{}"

        self.print_nice(
            title="Map Configurations",
            message=str(map_configurations),
        )

        yield "2. Erstelle Portal-Footer Konfiguration..."

        try:
            portal_footer_configurations = self.configuration_finder.get_portal_footer_configurations(
                requirements=summary["requirements"],
                history=history,
            )
        except Exception as e:
            self.print_nice(
                title="Error generating portal footer configuration",
                message=f"Failed to generate portal footer configuration: {str(e)}",
            )
            portal_footer_configurations = "{}"
        self.print_nice(
            title="Portal Footer Configurations",
            message=str(portal_footer_configurations),
        )

        yield "3. Erstelle Tree Konfiguration..."

        try:
            tree_configurations = self.configuration_finder.get_tree_configurations(
                requirements=summary["requirements"],
                history=history,
            )
        except Exception as e:
            self.print_nice(
                title="Error generating tree configuration",
                message=f"Failed to generate tree configuration: {str(e)}",
            )
            tree_configurations = "{}"
        self.print_nice(
            title="Tree Configurations",
            message=str(tree_configurations),
        )

        yield "4. Erstelle Module Konfiguration..."

        try:
            module_configurations = self.configuration_finder.get_module_configurations(
                requirements=summary["requirements"],
            )
        except Exception as e:
            self.print_nice(
                title="Error generating module configuration",
                message=f"Failed to generate module configuration: {str(e)}",
            )
            module_configurations = "{}"
        self.print_nice(
            title="Module Configurations",
            message=str(module_configurations),
        )

        yield "5. Erstelle Menu Konfiguration..."

        try:
            menu_configurations = self.configuration_finder.get_menu_configurations(
                requirements=summary["requirements"],
                module_configurations=module_configurations,
                history=history,
            )
        except Exception as e:
            self.print_nice(
                title="Error generating menu configuration",
                message=f"Failed to generate menu configuration: {str(e)}",
            )
            menu_configurations = "{}"
        self.print_nice(
            title="Menu Configurations",
            message=str(menu_configurations),
        )

        yield "6. Erstelle Layer Konfiguration..."

        try:
            layer_configurations = self.configuration_finder.get_layer_configurations(
                requirements=summary["requirements"],
            )
        except Exception as e:
            self.print_nice(
                title="Error generating layer configuration",
                message=f"Failed to generate layer configuration: {str(e)}",
            )
            layer_configurations = "{}"

        self.print_nice(
            title="Layer Configurations",
            message=str(layer_configurations),
        )

        yield "7. Einen Moment noch. Der letzte Schritt... Stelle finale config.json zusammen..."

        try:
            map_config_parsed = json.loads(self.remove_comments(map_configurations))
        except json.JSONDecodeError as e:
            raise Exception(f"Map Configuration JSON Parse Error: {str(e)}\n\nContent:\n{map_configurations[:500]}")

        try:
            portal_footer_parsed = json.loads(self.remove_comments(portal_footer_configurations))
        except json.JSONDecodeError as e:
            raise Exception(
                f"Portal Footer Configuration JSON Parse Error: {str(e)}\n\nContent:\n{portal_footer_configurations[:500]}"
            )

        try:
            tree_config_parsed = json.loads(self.remove_comments(tree_configurations))
        except json.JSONDecodeError as e:
            raise Exception(f"Tree Configuration JSON Parse Error: {str(e)}\n\nContent:\n{tree_configurations[:500]}")

        try:
            menu_config_parsed = json.loads(self.remove_comments(menu_configurations))
        except json.JSONDecodeError as e:
            raise Exception(f"Menu Configuration JSON Parse Error: {str(e)}\n\nContent:\n{menu_configurations[:500]}")

        try:
            layer_config_parsed = json.loads(self.remove_comments(layer_configurations))
        except json.JSONDecodeError as e:
            raise Exception(f"Layer Configuration JSON Parse Error: {str(e)}\n\nContent:\n{layer_configurations[:500]}")

        self.print_nice(
            title="Parsed Configurations",
            message=(
                f"Map: {map_config_parsed}\n\n"
                f"Portal Footer: {portal_footer_parsed}\n\n"
                f"Tree: {tree_config_parsed}\n\n"
                f"Menu: {menu_config_parsed}\n\n"
                f"Layer: {layer_config_parsed}\n\n"
            ),
        )

        config_json = self.config_file_creator.generate_config_json(
            layer_configurations=layer_config_parsed,
            map_configurations=map_config_parsed,
            menu_configurations=menu_config_parsed,
            portal_footer_configurations=portal_footer_parsed,
            tree_configurations=tree_config_parsed,
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

        self.latest_config_json = config_json

        yield "Config.json ist erstellt."

    def review_config(self, message: str, history: list):
        """Review and edit the generated configuration based on user feedback."""
        if not self.latest_config_json:
            yield "No configuration available to review. Please generate a configuration first."
            return

        chunks = self.get_chunks(
            query=str(message),
            k=K,
            filter={"category": "mainDocumentation"},
        )

        context_text = "\n\n---\n\n".join(chunks)

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_REVIEW,
            context=context_text,
            message=message,
            config_file=self.latest_config_json,
        )

        llm_response = self.invoke_llm(full_prompt)
        self.latest_config_json = self.extract_json_from_response(llm_response)

        yield "Konfiguration wird überprüft..."

        yield "Überprüfung der Konfiguration abgeschlossen."

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
