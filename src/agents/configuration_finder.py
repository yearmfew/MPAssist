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
        self.project_documents_path = "project_documents/"
        self.halisunation_errors = {}

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

    def _get_dataset_chunks_by_references(self, chunks: list) -> list:
        datatype_names = set()

        for chunk in chunks:
            if "references" in chunk.metadata and chunk.metadata["references"]:
                refs = chunk.metadata["references"].split(",")
                datatype_names.update([ref.strip() for ref in refs if ref.strip()])

        if not datatype_names:
            return []

        datatype_chunks = []
        for datatype_name in datatype_names:
            matching_chunks = self.get_chunks(
                query="",
                k=K,
                filter={
                    "$and": [
                        {"category": "datatype"},
                        {"datatype_name": datatype_name},
                    ]
                },
            )
            datatype_chunks.extend(matching_chunks)

        return datatype_chunks

    def _check_for_halisunations(
        self,
        configurations,
        config_object_id,
        context,
    ) -> str:
        validation_result = self.halisunation_checker.validate_config(
            config_obj=json.loads(configurations),
            config_object_id=config_object_id,
        )

        if validation_result["valid"]:
            self.halisunation_errors[config_object_id] = {"valid": True, "errors": []}
            return configurations
        else:
            self.print_nice(
                title=f"HALISUNATION DETECTED {config_object_id} CONFIGURATIONS",
                message=f"The generated {config_object_id} configurations contain errors according to the schema validation.",
            )

            errors = validation_result["errors"]
            self.halisunation_errors[config_object_id] = {"valid": False, "errors": errors}

            halisunation_fix_prompt = self.create_prompt_template(
                template=TEMPLATE_HALISUNATION_FIXER,
                context=context,
                errors=json.dumps(errors, indent=2),
                configuration_to_fix=configurations,
            )

            llm_response = self.invoke_llm(halisunation_fix_prompt)
            correctedConfigurations = self.extract_json_from_response(llm_response)

        return correctedConfigurations

    def get_module_configurations(self, requirements: str) -> str:
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={"category": "modulesConfigDocumentation"},
        )

        datatype_chunks = self._get_dataset_chunks_by_references(chunks)

        labelled_chunks = self._label_chunks(
            chunks + datatype_chunks,
            priority_map={
                "modulesConfigDocumentation": "CRITICAL",
            },
            templateName="TEMPLATE_MODULE_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_section_configuration = self.read_file(file_path=f"{self.project_documents_path}/defaults/section.json")

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
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        documentation_chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={
                "category": [
                    "layerConfigDocumentation",
                ]
            },
        )

        layer_chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={
                "category": [
                    "layerDocumentation",
                ]
            },
        )

        layer_datatype_chunks = self._get_dataset_chunks_by_references(layer_chunks)
        documentation_datatype_chunks = self._get_dataset_chunks_by_references(documentation_chunks)
        datatype_chunks = layer_datatype_chunks + documentation_datatype_chunks

        labelled_chunks = self._label_chunks(
            documentation_chunks + layer_chunks + datatype_chunks,
            templateName="TEMPLATE_LAYER_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_layer_config = self.read_file(file_path=f"{self.project_documents_path}/defaults/layerConfig.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_LAYER_FINDER,
            context=context_text,
            requirements=requirements,
            default_layer_config=default_layer_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        try:
            layerConfigurations = self.extract_json_from_response(llm_response)

            if not layerConfigurations or layerConfigurations == "{}":
                self.print_nice(
                    title="Warning: Empty layer configuration from LLM",
                    message="LLM returned empty layer configuration. Using default structure.",
                )
                layerConfigurations = '{"layerConfig": []}'

        except json.JSONDecodeError as e:
            self.print_nice(
                title="Error parsing layer configurations JSON",
                message=f"An error occurred while parsing the layer configurations JSON: {str(e)}\n\nLLM Response was:\n{llm_response}",
            )
            layerConfigurations = '{"layerConfig": []}'

        self.print_nice(
            title="Layer Configurations before halisunation check",
            message=json.dumps(layerConfigurations, indent=2),
        )

        try:
            ## Check for halisunation
            layerConfigurations = self._check_for_halisunations(
                configurations=layerConfigurations,
                context=context_text,
                config_object_id="layerConfig",
            )
        except Exception as e:
            self.print_nice(
                title="Error during halisunation check for layer configurations",
                message=f"An error occurred during the halisunation check for layer configurations: {str(e)}\n\nLLM Response was:\n{llm_response}",
            )

        return layerConfigurations

    def get_map_configurations(self, requirements: str) -> str:
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={"category": "mapConfigDocumentation"},
        )

        datatype_chunks = self._get_dataset_chunks_by_references(chunks)

        priority_map = {
            "mapConfigDocumentation": "CRITICAL",
        }

        labelled_chunks = self._label_chunks(
            chunks + datatype_chunks,
            templateName="TEMPLATE_MAP_FINDER",
            priority_map=priority_map,
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_map_config = self.read_file(file_path=f"{self.project_documents_path}/defaults/map.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_MAP_FINDER,
            context=context_text,
            requirements=requirements,
            default_map_config=default_map_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        mapConfigurations = self.extract_json_from_response(llm_response)

        # Check for halisunation
        mapConfigurations = self._check_for_halisunations(
            configurations=mapConfigurations,
            context=context_text,
            config_object_id="map",
        )

        return mapConfigurations

    def get_menu_configurations(self, requirements: str, module_configurations: str, history: list) -> str:
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={"category": ["menuConfigDocumentation"]},
        )

        datatype_chunks = self._get_dataset_chunks_by_references(chunks)

        labelled_chunks = self._label_chunks(
            chunks + datatype_chunks,
            templateName="TEMPLATE_MENU_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        main_menu_default_configurations = self.read_file(
            file_path=f"{self.project_documents_path}/defaults/mainMenu.json"
        )

        secondary_menu_default_configurations = self.read_file(
            file_path=f"{self.project_documents_path}/defaults/secondaryMenu.json"
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
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={"category": "portalFooterConfigDocumentation"},
        )
        datatype_chunks = self._get_dataset_chunks_by_references(chunks)
        labelled_chunks = self._label_chunks(
            chunks + datatype_chunks,
            templateName="TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        default_portal_footer_config = self.read_file(
            file_path=f"{self.project_documents_path}/defaults/portalFooter.json"
        )

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_PORTAL_FOOTER_CONFIG_FINDER,
            context=context_text,
            requirements=requirements,
            history=history,
            default_portal_footer_config=default_portal_footer_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        portalFooterConfigurations = self.extract_json_from_response(llm_response)

        ## Check for halisunation
        portalFooterConfigurations = self._check_for_halisunations(
            configurations=portalFooterConfigurations,
            context=context_text,
            config_object_id="portalFooter",
        )

        return portalFooterConfigurations

    def get_tree_configurations(self, requirements: str, history: list) -> str:
        query_str = str(requirements) if not isinstance(requirements, list) else " ".join(map(str, requirements))

        chunks = self.get_chunks(
            query=query_str,
            k=K,
            filter={"category": "treeConfigDocumentation"},
        )
        datatype_chunks = self._get_dataset_chunks_by_references(chunks)
        labelled_chunks = self._label_chunks(
            chunks + datatype_chunks,
            templateName="TEMPLATE_TREE_CONFIG_FINDER",
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)
        default_tree_config = self.read_file(file_path=f"{self.project_documents_path}/defaults/tree.json")

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_TREE_CONFIG_FINDER,
            context=context_text,
            requirements=requirements,
            default_tree_config=default_tree_config,
        )

        llm_response = self.invoke_llm(full_prompt)
        treeConfigurations = self.extract_json_from_response(llm_response)

        ## Check for halisunation
        treeConfigurations = self._check_for_halisunations(
            configurations=treeConfigurations,
            context=context_text,
            config_object_id="tree",
        )

        return treeConfigurations
