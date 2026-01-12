from regex import template
from agents.base_agent import BaseAgent
from utils import db_manager
from utils.template import (
    TEMPLATE_MODULE_FINDER,
    TEMPLATE_LAYER_FINDER,
    TEMPLATE_MAP_FINDER,
    TEMPLATE_MENU_CONFIG_FINDER,
)


class ConfigurationFinder(BaseAgent):
    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()

    def get_module_configurations(self, requirements: str) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=4,
            filter={"category": "modulesConfigDocumentation"},
        )

        labelled_chunks = self._label_chunks(
            chunks,
            priority_map={
                "modulesConfigDocumentation": "CRITICAL",
            },
            templateName="TEMPLATE_MODULE_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_section_configuration = self.read_file(
            file_path="masterportal-docs/defaults/section.json"
        )

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_MODULE_FINDER,
            context=context_text,
            requirements=requirements,
            default_section_configuration=default_section_configuration,
        )

        llm_response = self.invoke_llm(full_prompt)
        moduleConfigurations = self.extract_json_from_response(llm_response)

        return moduleConfigurations

    def get_layer_configurations(self, requirements: str) -> str:

        ## I need to have layer documentation from udp manager. The data I have does not have much info about layers.!!!!
        # rest-services.json
        chunks = self.get_chunks(
            query=requirements,
            k=4,
            filter={"includes": "layerConfig"},
        )

        priority_map = {
            "docs_for_modules": "LOW",
            "documentation": "MEDIUM",
            "mainDocumentation": "HIGH",
            "example": "LOW",
        }

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_LAYER_FINDER",
            priority_map=priority_map,
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_LAYER_FINDER,
            context=context_text,
            requirements=requirements,
        )

        llm_response = self.invoke_llm(full_prompt)
        layerConfigurations = self.extract_json_from_response(llm_response)

        return layerConfigurations

    def get_map_configurations(self, requirements: str) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=4,
            filter={"category": "mapConfigDocumentation"},
        )

        priority_map = {
            "mapConfigDocumentation": "CRITICAL",
        }

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_MAP_FINDER",
            priority_map=priority_map,
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_map_config = self.read_file(
            file_path="masterportal-docs/defaults/map.json"
        )

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_MAP_FINDER,
            context=context_text,
            requirements=requirements,
            default_map_config=default_map_config,
        )

        llm_response = self.invoke_llm(full_prompt)

        mapConfigurations = self.extract_json_from_response(llm_response)

        return mapConfigurations

    def get_menu_configurations(
        self, requirements: str, module_configurations: str
    ) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=4,
            filter={
                "category": [
                    "mainMenuConfigDocumentation",
                    "secondaryMenuConfigDocumentation",
                ]
            },
        )

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_MENU_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        main_menu_default_configurations = self.read_file(
            file_path="masterportal-docs/defaults/mainMenu.json"
        )

        secondary_menu_default_configurations = self.read_file(
            file_path="masterportal-docs/defaults/secondaryMenu.json"
        )

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_MENU_CONFIG_FINDER,
            context=context_text,
            requirements=requirements,
            main_menu_default_configurations=main_menu_default_configurations,
            secondary_menu_default_configurations=secondary_menu_default_configurations,
            module_configurations=module_configurations,
        )

        llm_response = self.invoke_llm(full_prompt)
        menuConfigurations = self.extract_json_from_response(llm_response)

        return menuConfigurations

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

            labeled_chunk = (
                f"[CATEGORY]: {category}\n"
                f"[PRIORITY]: {priority}\n"
                f"{chunk.page_content}"
            )

            labeled_chunks.append(labeled_chunk)

        return labeled_chunks
