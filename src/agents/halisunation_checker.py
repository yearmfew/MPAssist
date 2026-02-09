import json
from jsonschema import Draft7Validator
from agents.base_agent import BaseAgent


class HalisunationChecker(BaseAgent):
    def __init__(self):
        super().__init__()

        self.configObjectSchemas = {
            "map": json.loads(self.read_file("src/schemas/map_schema.json")),
            "tree": json.loads(self.read_file("src/schemas/tree_schema.json")),
            "portalFooter": json.loads(self.read_file("src/schemas/portalFooter_schema.json")),
            "mainMenu": json.loads(self.read_file("src/schemas/mainMenu_schema.json")),
            "secondaryMenu": json.loads(self.read_file("src/schemas/secondaryMenu_schema.json")),
            "layerConfig": json.loads(self.read_file("src/schemas/layerConfig_schema.json")),
        }

        VALID_LAYER_DATA = json.loads(self.read_file("src/layerData/layerIdNameCouples.json"))
        self.VALID_LAYER_IDS = {str(item["id"]) for item in VALID_LAYER_DATA}
        self.VALID_LAYER_NAMES = {item["name"] for item in VALID_LAYER_DATA}

    def validate_layer_ids_names(self, layer_config: dict) -> dict:
        """
        Validate layer IDs and names against the valid layer data.
        Uses set operations for efficient lookup without explicit loops.

        Args:
            layer_config: The layerConfig object containing baselayer and/or subjectlayer

        Returns:
            dict with 'valid' boolean and 'errors' list
        """
        errors = []

        all_elements = layer_config.get("baselayer", {}).get("elements", []) + layer_config.get("subjectlayer", {}).get(
            "elements", []
        )

        invalid_ids = [
            {"path": f"elements[{idx}].id", "message": f"Invalid layer ID: {elem.get('id')}", "validator": "enum"}
            for idx, elem in enumerate(all_elements)
            if elem.get("id") and str(elem.get("id")) not in self.VALID_LAYER_IDS
        ]

        invalid_names = [
            {"path": f"elements[{idx}].name", "message": f"Invalid layer name: {elem.get('name')}", "validator": "enum"}
            for idx, elem in enumerate(all_elements)
            if elem.get("name") and elem.get("name") not in self.VALID_LAYER_NAMES
        ]

        errors.extend(invalid_ids + invalid_names)

        if not errors:
            # self.print_nice(title="LAYER VALIDATION SUCCESS", message="All layer IDs and names are valid!")
            return {"valid": True, "errors": []}

        # self.print_nice(title="LAYER VALIDATION ERRORS", message=json.dumps(errors, indent=2))
        return {"valid": False, "errors": errors}

    def validate_config(self, config_obj: dict, config_object_id: str) -> dict:
        if config_object_id not in self.configObjectSchemas:
            self.print_nice(title="VALIDATION ERROR", message=f"Schema for '{config_object_id}' not found!")

            return {"valid": False, "errors": [{"message": "Schema not found"}]}

        validator = Draft7Validator(self.configObjectSchemas[config_object_id])
        errors = list(validator.iter_errors(config_obj))
        formatted_errors = []

        for error in errors:
            current_schema = error.schema
            valid_properties = current_schema.get("properties", {}).keys()

            formatted_errors.append(
                {
                    "path": ".".join(str(p) for p in error.absolute_path),
                    "message": error.message,
                    "validator": error.validator,
                    "valid_properties": list(valid_properties),
                }
            )

        if config_object_id == "layerConfig":
            layer_data = config_obj.get("layerConfig", config_obj) if "layerConfig" in config_obj else config_obj
            layer_validation = self.validate_layer_ids_names(layer_data)

            if not layer_validation["valid"]:
                formatted_errors.extend(layer_validation["errors"])

        if formatted_errors:
            # self.print_nice(title="VALIDATION ERRORS", message=json.dumps(formatted_errors, indent=2))

            return {"valid": False, "errors": formatted_errors}

        # self.print_nice(title="VALIDATION SUCCESS", message=f"Valid {config_object_id}!")

        return {"valid": True, "errors": []}
