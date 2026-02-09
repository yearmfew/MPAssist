"""
Extracts all layer IDs and names from layerDescriptionsCleaned.json
and creates a flat array of {id, name} objects.
"""

import json


def extract_layer_ids_and_names(input_file: str, output_file: str):
    """
    Extract all layer IDs and names into a flat array.

    Handles two formats:
    1. Direct layers: {"id": "...", "name": "...", "description": "..."}
    2. Grouped layers: {"description": "...", "layers": [{"id": "...", "name": "..."}]}

    Args:
        input_file: Path to layerDescriptionsCleaned.json
        output_file: Path to save the flat array
    """
    print(f"Loading data from {input_file}...")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    layer_list = []

    for entry in data:
        if "layers" in entry:
            # It's a grouped entry - extract all layers
            for layer in entry["layers"]:
                layer_list.append({"id": layer["id"], "name": layer["name"]})
        else:
            # It's a direct layer entry
            layer_list.append({"id": entry["id"], "name": entry["name"]})

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(layer_list, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Extracted {len(layer_list)} layers")
    print(f"📄 Saved to: {output_file}")

    # Print first 5 as preview
    print(f"\n📋 Preview (first 5):")
    for layer in layer_list[:5]:
        print(f"  - ID: {layer['id']}, Name: {layer['name']}")


if __name__ == "__main__":
    input_file = "layerDescriptionsCleaned.json"
    output_file = "layerIdNameCouples.json"

    extract_layer_ids_and_names(input_file, output_file)
