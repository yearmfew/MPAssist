import json
import re
from jsonschema import Draft7Validator
from agents.base_agent import BaseAgent


class HalisunationChecker(BaseAgent):
    def __init__(self):
        super().__init__()

        self.configObjectSchemas = {
            "map": json.loads(self.read_file("src/schemas/map_schema.json")),
            "tree": json.loads(self.read_file("src/schemas/tree_schema.json")),
            "portalFooter": json.loads(self.read_file("src/schemas/portal_footer_schema.json")),
            "mainMenu": json.loads(self.read_file("src/schemas/mainMenu_schema.json")),
            "secondaryMenu": json.loads(self.read_file("src/schemas/secondaryMenu_schema.json")),
            "layerConfig": json.loads(self.read_file("src/schemas/layerConfig_schema.json")),
        }

    def validate_config(self, config_obj: dict, config_object_id: str) -> dict:
        if config_object_id not in self.configObjectSchemas:
            self.print_nice(title="VALIDATION ERROR", message=f"Schema for '{config_object_id}' not found!")
            return {"valid": False, "errors": [{"message": "Schema not found"}]}

        validator = Draft7Validator(self.configObjectSchemas[config_object_id])
        errors = list(validator.iter_errors(config_obj))
        formatted_errors = []

        if not errors:
            self.print_nice(title="VALIDATION SUCCESS", message=f"Valid {config_object_id}!")

            return {"valid": True, "errors": []}

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

        self.print_nice(title="VALIDATION ERRORS", message=json.dumps(formatted_errors, indent=2))

        return {"valid": False, "errors": formatted_errors}
