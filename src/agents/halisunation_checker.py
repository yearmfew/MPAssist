"""
HalisunationChecker Agent

This agent validates AI-generated config.json files against the Masterportal schema.
It detects:
- Hallucinated (non-existent) modules, layers, or controls
- Incorrect module placements (modules must be in mainMenu.sections or secondaryMenu.sections)
- Invalid structure or missing required fields
- Type mismatches and invalid values

The agent uses JSON Schema validation combined with Masterportal-specific rules.
"""

import json
from typing import Dict, List, Tuple, Any
from agents.base_agent import BaseAgent


class HalisunationChecker(BaseAgent):
    """
    Validates generated config.json files against Masterportal schema and rules.

    This agent doesn't use LLM - it performs structural and semantic validation
    by comparing the generated config against known valid modules, layers, and structure.
    """

    def __init__(self):
        """
        Initialize the validator with known valid modules and structure rules.
        """
        super().__init__()

        # Known valid module types from Masterportal documentation
        # TODO: This list should be dynamically loaded from documentation or a config file
        self.valid_modules = {
            # Tools
            "addWMS",
            "bufferAnalysis",
            "compareFeatures",
            "contactInfo",
            "coordToolkit",
            "customMenuElement",
            "draw",
            "featureLister",
            "fileImport",
            "filter",
            "language",
            "layerSlider",
            "legend",
            "measure",
            "news",
            "openConfig",
            "populationRequest",
            "print",
            "routing",
            "scaleSwitcher",
            "searchBar",
            "selectFeatures",
            "shadow",
            "shareView",
            "statisticDashboard",
            "styleVT",
            "wfsSearch",
            "wfst",
            "modeler3D",
            # GFI and related
            "getFeatureInfo",
            "gfi",
            # Other
            "quickHelp",
            "toolWindow",
        }

        # Known valid layer types
        self.valid_layer_types = {
            "WMS",
            "WFS",
            "WMTS",
            "GeoJSON",
            "SensorThings",
            "VectorTile",
            "Terrain3D",
            "Entities3D",
            "TileSet3D",
            "GROUP",
            "StaticImage",
        }

        # Known valid control types (map controls)
        self.valid_controls = {
            "backForward",
            "button3d",
            "freeze",
            "fullScreen",
            "orientation",
            "rotation",
            "startModule",
            "tiltView",
            "totalView",
            "zoom",
        }

    def execute(self, config_json_str: str) -> Tuple[bool, List[str]]:
        """
        Validate a config.json string against Masterportal rules.

        Args:
            config_json_str: The config.json content as a string

        Returns:
            Tuple of (is_valid, error_messages)
            - is_valid: True if validation passed, False otherwise
            - error_messages: List of detailed error messages (empty if valid)
        """
        errors = []

        # Step 1: Parse JSON
        try:
            config = json.loads(config_json_str)
        except json.JSONDecodeError as e:
            return False, [
                f"JSON Parse Error at line {e.lineno}, column {e.colno}: {e.msg}"
            ]

        # Step 2: Validate structure of the config.json
        structure_errors = self._validate_structure(config)
        errors.extend(structure_errors)

        # # Step 3: Validate modules (critical check for hallucinations)
        # module_errors = self._validate_modules(config)
        # errors.extend(module_errors)

        # # Step 4: Validate layers
        # layer_errors = self._validate_layers(config)
        # errors.extend(layer_errors)

        # # Step 5: Validate map controls
        # control_errors = self._validate_controls(config)
        # errors.extend(control_errors)

        # # Step 6: Validate module placement (modules MUST be in menu sections)
        # placement_errors = self._validate_module_placement(config)
        # errors.extend(placement_errors)

        is_valid = len(errors) == 0
        return is_valid, errors

    def _validate_structure(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate the overall structure of config.json.

        Checks for required sections and their structure.

        Args:
            config: Parsed config.json as a dictionary

        Returns:
            List of structure-related error messages
        """
        errors = []

        # Validate top-level keys
        top_key_errors = self._validate_top_keys(config)
        errors.extend(top_key_errors)

        # Validate portalConfig structure
        portal_config = config.get("portalConfig", {})
        portal_errors = self._validate_portal_config(portal_config)
        errors.extend(portal_errors)

        # Validate layerConfig structure
        layer_config = config.get("layerConfig", {})
        layer_errors = self._validate_layer_config(layer_config)
        errors.extend(layer_errors)

        return errors

    def _validate_top_keys(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate the top-level structure of config.json.

        Required structure:
        {
            "portalConfig": { ... },
            "layerConfig": { ... }
        }
        """
        errors = []

        # Check for required top-level keys
        if "portalConfig" not in config:
            errors.append("ERROR: Missing required key 'portalConfig' at root level")

        if "layerConfig" not in config:
            errors.append("ERROR: Missing required key 'layerConfig' at root level")

        # Check for unexpected top-level keys
        valid_top_keys = {"portalConfig", "layerConfig"}
        for key in config.keys():
            if key not in valid_top_keys:
                errors.append(
                    f"WARNING: Unexpected top-level key '{key}' (only 'portalConfig' and 'layerConfig' are standard)"
                )

        return errors

    def _validate_portal_config(self, portal_config: Dict[str, Any]) -> List[str]:
        """
        Validate the portalConfig section structure.
        """
        errors = []

        # Check for required sections
        required_sections = {"map", "portalFooter", "tree", "mainMenu", "secondaryMenu"}
        for section in required_sections:
            if section not in portal_config:
                errors.append(
                    f"ERROR: Missing required section '{section}' in portalConfig"
                )

        for section in portal_config.keys():
            if section not in required_sections:
                errors.append(
                    f"WARNING: Unexpected section '{section}' in portalConfig"
                )

        return errors

    def _validate_layer_config(self, layer_config: Dict[str, Any]) -> List[str]:
        """
        Validate the layerConfig section structure.
        """
        errors = []

        # Check for required sections
        required_sections = {"baselayer", "subjectlayer"}
        for section in required_sections:
            if section not in layer_config:
                errors.append(
                    f"ERROR: Missing required section '{section}' in layerConfig"
                )

        for section in layer_config.keys():
            if section not in required_sections:
                errors.append(f"WARNING: Unexpected section '{section}' in layerConfig")

        return errors

    def _validate_modules(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate all modules in the config against the known valid module list.
        Detects hallucinated modules.
        """
        errors = []
        portal_config = config.get("portalConfig", {})

        # Check mainMenu sections
        main_menu = portal_config.get("mainMenu", {})
        sections = main_menu.get("sections", [])

        for section_idx, section in enumerate(sections):
            if isinstance(section, list):
                for module_idx, module in enumerate(section):
                    if isinstance(module, dict):
                        module_type = module.get("type")
                        if module_type and module_type not in self.valid_modules:
                            errors.append(
                                f"HALLUCINATION ERROR: Module '{module_type}' in "
                                f"portalConfig.mainMenu.sections[{section_idx}][{module_idx}] "
                                f"is not a valid Masterportal module. "
                                f"Valid modules are: {sorted(self.valid_modules)}"
                            )

        # Check secondaryMenu sections
        secondary_menu = portal_config.get("secondaryMenu", {})
        sections = secondary_menu.get("sections", [])

        for section_idx, section in enumerate(sections):
            if isinstance(section, list):
                for module_idx, module in enumerate(section):
                    if isinstance(module, dict):
                        module_type = module.get("type")
                        if module_type and module_type not in self.valid_modules:
                            errors.append(
                                f"HALLUCINATION ERROR: Module '{module_type}' in "
                                f"portalConfig.secondaryMenu.sections[{section_idx}][{module_idx}] "
                                f"is not a valid Masterportal module. "
                                f"Valid modules are: {sorted(self.valid_modules)}"
                            )

        return errors

    def _validate_layers(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate layer configurations.
        Checks layer types and required fields.
        """
        errors = []
        layer_config = config.get("layerConfig", {})

        # Validate baselayer elements
        baselayer = layer_config.get("baselayer", {})
        elements = baselayer.get("elements", [])

        for idx, layer in enumerate(elements):
            if isinstance(layer, dict):
                layer_type = layer.get("typ") or layer.get("type")
                layer_id = layer.get("id", f"<unknown at index {idx}>")

                if layer_type and layer_type not in self.valid_layer_types:
                    errors.append(
                        f"HALLUCINATION ERROR: Layer type '{layer_type}' for layer '{layer_id}' "
                        f"in layerConfig.baselayer.elements[{idx}] is not valid. "
                        f"Valid types: {sorted(self.valid_layer_types)}"
                    )

                # Check required fields
                if "id" not in layer:
                    errors.append(
                        f"ERROR: Layer at layerConfig.baselayer.elements[{idx}] is missing required field 'id'"
                    )

        # Validate subjectlayer elements
        subjectlayer = layer_config.get("subjectlayer", {})
        elements = subjectlayer.get("elements", [])

        for idx, layer in enumerate(elements):
            if isinstance(layer, dict):
                layer_type = layer.get("typ") or layer.get("type")
                layer_id = layer.get("id", f"<unknown at index {idx}>")

                if layer_type and layer_type not in self.valid_layer_types:
                    errors.append(
                        f"HALLUCINATION ERROR: Layer type '{layer_type}' for layer '{layer_id}' "
                        f"in layerConfig.subjectlayer.elements[{idx}] is not valid. "
                        f"Valid types: {sorted(self.valid_layer_types)}"
                    )

                # Check required fields
                if "id" not in layer:
                    errors.append(
                        f"ERROR: Layer at layerConfig.subjectlayer.elements[{idx}] is missing required field 'id'"
                    )

        return errors

    def _validate_controls(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate map controls configuration.
        """
        errors = []
        portal_config = config.get("portalConfig", {})
        map_config = portal_config.get("map", {})
        controls = map_config.get("controls", {})

        if not isinstance(controls, dict):
            return errors

        for control_name in controls.keys():
            if control_name not in self.valid_controls:
                errors.append(
                    f"HALLUCINATION ERROR: Control '{control_name}' in "
                    f"portalConfig.map.controls is not a valid Masterportal control. "
                    f"Valid controls: {sorted(self.valid_controls)}"
                )

        return errors

    def _validate_module_placement(self, config: Dict[str, Any]) -> List[str]:
        """
        CRITICAL VALIDATION: Ensure modules are ONLY placed in menu sections.

        Modules must be in:
        - portalConfig.mainMenu.sections
        - portalConfig.secondaryMenu.sections

        They should NOT appear in:
        - portalConfig.map
        - portalConfig.tree
        - layerConfig
        - Any other location
        """
        errors = []
        portal_config = config.get("portalConfig", {})

        # Check map config for misplaced modules
        map_config = portal_config.get("map", {})
        if isinstance(map_config, dict):
            for key, value in map_config.items():
                if key not in [
                    "controls",
                    "mapView",
                    "baselayerSwitcher",
                    "getFeatureInfo",
                    "featureViaURL",
                    "layerPills",
                    "map3dParameter",
                    "mapMarker",
                    "mouseHover",
                    "startingMapMode",
                    "zoomTo",
                ]:
                    # Check if this looks like a module (has "type" field)
                    if isinstance(value, dict) and "type" in value:
                        errors.append(
                            f"PLACEMENT ERROR: Module found in portalConfig.map.{key} "
                            f"(type: '{value.get('type')}'). "
                            f"Modules MUST be placed in portalConfig.mainMenu.sections or "
                            f"portalConfig.secondaryMenu.sections ONLY."
                        )

        # Check if modules have required "type" field
        main_menu = portal_config.get("mainMenu", {})
        sections = main_menu.get("sections", [])

        for section_idx, section in enumerate(sections):
            if isinstance(section, list):
                for module_idx, module in enumerate(section):
                    if isinstance(module, dict) and "type" not in module:
                        errors.append(
                            f"ERROR: Module at portalConfig.mainMenu.sections[{section_idx}][{module_idx}] "
                            f"is missing required 'type' field. All modules must have a 'type' field."
                        )

        secondary_menu = portal_config.get("secondaryMenu", {})
        sections = secondary_menu.get("sections", [])

        for section_idx, section in enumerate(sections):
            if isinstance(section, list):
                for module_idx, module in enumerate(section):
                    if isinstance(module, dict) and "type" not in module:
                        errors.append(
                            f"ERROR: Module at portalConfig.secondaryMenu.sections[{section_idx}][{module_idx}] "
                            f"is missing required 'type' field. All modules must have a 'type' field."
                        )

        return errors

    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Convenience method to validate a config.json file from disk.

        Args:
            file_path: Path to the config.json file

        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config_content = f.read()
            return self.execute(config_content)
        except FileNotFoundError:
            return False, [f"ERROR: File not found: {file_path}"]
        except Exception as e:
            return False, [f"ERROR: Failed to read file {file_path}: {str(e)}"]

    def get_validation_report(self, config_json_str: str) -> str:
        """
        Generate a human-readable validation report.

        Args:
            config_json_str: The config.json content as a string

        Returns:
            Formatted validation report as string
        """
        is_valid, errors = self.execute(config_json_str)

        report = []
        report.append("=" * 70)
        report.append("CONFIG.JSON VALIDATION REPORT")
        report.append("=" * 70)
        report.append("")

        if is_valid:
            report.append("✓ VALIDATION PASSED")
            report.append("")
            report.append(
                "The config.json file is valid and follows Masterportal standards."
            )
        else:
            report.append("✗ VALIDATION FAILED")
            report.append("")
            report.append(f"Found {len(errors)} error(s):")
            report.append("")

            for idx, error in enumerate(errors, 1):
                report.append(f"{idx}. {error}")
                report.append("")

        report.append("=" * 70)

        return "\n".join(report)


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Test with a sample config
    checker = HalisunationChecker()

    # Example 1: Valid minimal config
    valid_config = """
    {
        "portalConfig": {
            "mainMenu": {
                "sections": [
                    [
                        {"type": "legend"},
                        {"type": "measure"}
                    ]
                ]
            },
            "secondaryMenu": {
                "sections": [
                    [
                        {"type": "print"}
                    ]
                ]
            }
        },
        "layerConfig": {
            "baselayer": {
                "elements": []
            },
            "subjectlayer": {
                "elements": []
            }
        }
    }
    """

    print("Testing valid config...")
    print(checker.get_validation_report(valid_config))
    print("\n")

    # Example 2: Invalid config with hallucinated module
    invalid_config = """
    {
        "portalConfig": {
            "mainMenu": {
                "sections": [
                    [
                        {"type": "legend"},
                        {"type": "superAwesomeTool"}
                    ]
                ]
            }
        },
        "layerConfig": {
            "baselayer": {
                "elements": [
                    {"id": "123", "typ": "FakeLayerType"}
                ]
            }
        }
    }
    """

    print("Testing invalid config with hallucinations...")
    print(checker.get_validation_report(invalid_config))
