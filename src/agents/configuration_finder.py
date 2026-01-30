import json
from agents.base_agent import BaseAgent
from agents.halisunation_checker import HalisunationChecker
from utils import db_manager
from utils.template import (
    TEMPLATE_MODULE_FINDER,
    TEMPLATE_LAYER_FINDER,
    TEMPLATE_MAP_FINDER,
    TEMPLATE_MENU_CONFIG_FINDER,
    TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER,
    TEMPLATE_TREE_CONFIG_FINDER,
    TEMPLATE_HALISUNATION_FIXER,
)
from utils.settings import K


class ConfigurationFinder(BaseAgent):
    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()
        self.halisunation_checker = HalisunationChecker()

    def _label_chunks(self, chunks: list, templateName: str = "", priority_map: dict = {}) -> list:
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

    def _check_for_halisunations(
        self,
        configurations,
        default_configurations,
        config_object_id,
        context,
    ) -> str:
        validation_result = self.halisunation_checker.validate_config(
            config_obj=json.loads(configurations),
            config_object_id=config_object_id,
        )

        if validation_result["valid"]:
            return configurations
        else:
            self.print_nice(
                title="HALISUNATION DETECTED IN MAP CONFIGURATIONS",
                message="The generated map configurations contain errors according to the schema validation.",
            )
            errors = validation_result["errors"]

            halisunation_fix_prompt = self.create_prompt_template(
                template=TEMPLATE_HALISUNATION_FIXER,
                context=context,
                errors=json.dumps(errors, indent=2),
                configuration_to_fix=configurations,
                default_config=default_configurations,
            )

            llm_response = self.invoke_llm(halisunation_fix_prompt)
            correctedConfigurations = self.extract_json_from_response(llm_response)

            self.print_nice(
                title="HALISUNATION FIXED",
                message=correctedConfigurations,
            )

        return correctedConfigurations

    def get_module_configurations(self, requirements: str) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=K,
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

        default_section_configuration = self.read_file(file_path="masterportal-docs/defaults/section.json")

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
            k=K,
            filter={
                "category": [
                    "subjectLayerConfigDocumentation",
                    "baseLayerConfigDocumentation",
                ]
            },
        )

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_LAYER_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_layer_config = self.read_file(file_path="masterportal-docs/defaults/layerConfig.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_LAYER_FINDER,
            context=context_text,
            requirements=requirements,
            default_layer_config=default_layer_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        layerConfigurations = self.extract_json_from_response(llm_response)

        return layerConfigurations

    def get_map_configurations(self, requirements: str) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=K,
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

        default_map_config = self.read_file(file_path="masterportal-docs/defaults/map.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_MAP_FINDER,
            context=context_text,
            requirements=requirements,
            default_map_config=default_map_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        mapConfigurations = self.extract_json_from_response(llm_response)

        ## Check for halisunation
        ## Will be activated later..
        # mapConfigurations = self._check_for_halisunations(
        #     configurations=mapConfigurations,
        #     default_configurations=default_map_config,
        #     context=context_text,
        #     config_object_id="map",
        # )

        return mapConfigurations

    def get_menu_configurations(self, requirements: str, module_configurations: str, history: list) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=K,
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

        main_menu_default_configurations = self.read_file(file_path="masterportal-docs/defaults/mainMenu.json")

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

    def get_portal_footer_configurations(self, requirements: str, history: list) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=K,
            filter={"category": "portalFooterConfigDocumentation"},
        )

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_portal_footer_config = self.read_file(file_path="masterportal-docs/defaults/portalFooter.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER,
            context=context_text,
            requirements=requirements,
            history=history,
            default_portal_footer_config=default_portal_footer_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        portalFooterConfigurations = self.extract_json_from_response(llm_response)

        return portalFooterConfigurations

    def get_tree_configurations(self, requirements: str, history: list) -> str:
        chunks = self.get_chunks(
            query=requirements,
            k=K,
            filter={"category": "treeConfigDocumentation"},
        )

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_TREE_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)
        default_tree_config = self.read_file(file_path="masterportal-docs/defaults/tree.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_TREE_CONFIG_FINDER,
            context=context_text,
            requirements=requirements,
            history=history,
            default_tree_config=default_tree_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        treeConfigurations = self.extract_json_from_response(llm_response)

        return treeConfigurations
