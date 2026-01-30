## To check schemas in python terminal independently of the agent system

import json
import re
from jsonschema import Draft7Validator
from pathlib import Path
from typing import Any, Dict, List


def print_nice(message: str, title: str = "INFO"):
    print(f"\033[94m┌─ {title} {'─' * (100 - len(title) - 4)}┐\033[91m")
    print(message)
    print(f"\033[94m└{'─' * 100}┘\033[0m")


def read_file(file_path: str) -> str:
    """
    Load the file form given path file.

    Returns:
        Content of example.config.json as string
    """
    base_config_path = Path(__file__).resolve().parents[2] / file_path

    try:
        return base_config_path.read_text()

    except FileNotFoundError:
        print_nice(
            title=f"❌ Error: file is not found at {base_config_path}. ",
            message="Please ensure the file is in the directory",
        )
        return ""


configObjectSchemas = {
    "map": json.loads(read_file("src/schemas/map_schema.json")),
    "tree": json.loads(read_file("src/schemas/tree_schema.json")),
    "portalFooter": json.loads(read_file("src/schemas/portalFooter_schema.json")),
    "mainMenu": json.loads(read_file("src/schemas/mainMenu_schema.json")),
    "secondaryMenu": json.loads(read_file("src/schemas/secondaryMenu_schema.json")),
    "layerConfig": json.loads(read_file("src/schemas/layerConfig_schema.json")),
}


def getConfigs(key: str) -> List[Dict[str, Any]]:
    result = []
    folder_path = "src/portalconfigs"
    base_folder = Path(__file__).resolve().parents[2] / folder_path

    for json_file in base_folder.glob("*.json"):
        try:
            relative_path = json_file.relative_to(Path(__file__).resolve().parents[2])
            content = read_file(str(relative_path))
            if content:
                data = json.loads(content)
                if isinstance(data, dict):
                    if key in data:
                        result.append({json_file.stem: {key: data[key]}})
                    elif (
                        "portalConfig" in data
                        and isinstance(data["portalConfig"], dict)
                        and key in data["portalConfig"]
                    ):
                        result.append({json_file.stem: {key: data["portalConfig"][key]}})
        except Exception:
            pass

    return result


def validate_config(config_obj: dict, config_object_id: str) -> dict:
    if config_object_id not in configObjectSchemas:
        print_nice(title="VALIDATION ERROR", message=f"Schema for '{config_object_id}' not found!")
        return {"valid": False, "errors": [{"message": "Schema not found"}]}

    validator = Draft7Validator(configObjectSchemas[config_object_id])
    errors = list(validator.iter_errors(config_obj))
    formatted_errors = []

    if not errors:
        print_nice(title="VALIDATION SUCCESS", message=f"Valid {config_object_id}!")

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

    print_nice(title="VALIDATION ERRORS", message=json.dumps(formatted_errors, indent=2))

    return {"valid": False, "errors": formatted_errors}


def testConfig(config_key: str):
    print_nice(title="TEST", message=f"Testing {config_key} objects from portalconfigs...")

    configs = getConfigs(config_key)

    if not configs:
        print_nice(title="NO CONFIGS FOUND", message=f"No {config_key} objects found in portalconfigs.")
        return

    for idx, config_obj in enumerate(configs, 1):
        config_title = list(config_obj.keys())[0]
        config_data = config_obj[config_title]

        print_nice(
            title=f"VALIDATING CONFIG - {config_title}",
            message=f"Validating {config_key} object for '{config_title}'...",
        )
        validate_config(config_obj=config_data, config_object_id=config_key)


if __name__ == "__main__":

    testConfig("portalFooter")
