"""
After downloading layer data from metaver, we have noticed that some layers are duplicated.
These duplicates have the same name and description but different IDs.
This script cleans duplicate layers that have the same name and description but different IDs.
For grouped layers, removes duplicates within each group.
"""

import json
from typing import List, Dict


def clean_grouped_layers(layers: List[Dict]) -> tuple[List[Dict], List[Dict]]:
    """
    Remove duplicate layers based on name within a group.
    If multiple layers have the same name, keep only the first one.

    Args:
        layers: List of layer dicts with 'id' and 'name'

    Returns:
        Cleaned list of layers without name duplicates
    """
    seen_names = set()
    cleaned_layers = []
    duplicates_removed = []

    for layer in layers:
        name = layer.get("name")
        if name not in seen_names:
            seen_names.add(name)
            cleaned_layers.append(layer)
        else:
            duplicates_removed.append(layer)

    return cleaned_layers, duplicates_removed


def clean_layer_descriptions(input_file: str, output_file: str):
    """
    Main function to clean layer descriptions file.
    Removes duplicate layers with same name within grouped descriptions.

    Args:
        input_file: Path to layerDescriptions.json
        output_file: Path to save cleaned output
    """
    print(f"Loading data from {input_file}...")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total entries in input: {len(data)}")

    cleaned_data = []
    report = {
        "summary": {
            "total_input_entries": len(data),
            "unique_layers_count": 0,
            "grouped_descriptions_count": 0,
            "total_duplicates_removed": 0,
        },
        "grouped_entries_details": [],
        "all_duplicates_removed": [],
    }

    total_duplicates = 0
    converted_to_unique = 0

    for entry in data:
        # Check if it's a grouped entry
        if "layers" in entry:
            # It's a grouped entry
            original_count = len(entry["layers"])
            cleaned_layers, duplicates = clean_grouped_layers(entry["layers"])

            duplicates_count = len(duplicates)
            total_duplicates += duplicates_count

            # Add to report if duplicates were found
            if duplicates_count > 0:
                report["grouped_entries_details"].append(
                    {
                        "description": (
                            entry["description"][:100] + "..."
                            if len(entry["description"]) > 100
                            else entry["description"]
                        ),
                        "original_layer_count": original_count,
                        "cleaned_layer_count": len(cleaned_layers),
                        "duplicates_removed": duplicates_count,
                        "removed_layers": [{"id": d["id"], "name": d["name"]} for d in duplicates],
                    }
                )

                report["all_duplicates_removed"].extend(
                    [
                        {"id": d["id"], "name": d["name"], "description": entry["description"][:100] + "..."}
                        for d in duplicates
                    ]
                )

            # Check if only one layer remains after cleaning
            if len(cleaned_layers) == 1:
                # Convert to normal format (id, name, description)
                cleaned_data.append(
                    {
                        "id": cleaned_layers[0]["id"],
                        "name": cleaned_layers[0]["name"],
                        "description": entry["description"],
                    }
                )
                converted_to_unique += 1
                report["summary"]["unique_layers_count"] += 1
            else:
                # Keep as grouped format
                cleaned_data.append({"description": entry["description"], "layers": cleaned_layers})
                report["summary"]["grouped_descriptions_count"] += 1

        else:
            # It's a unique layer entry - keep as is
            cleaned_data.append(entry)
            report["summary"]["unique_layers_count"] += 1

    report["summary"]["total_duplicates_removed"] = total_duplicates
    report["summary"]["converted_to_unique"] = converted_to_unique
    report["summary"]["total_output_entries"] = len(cleaned_data)

    # Calculate total layers before and after
    total_layers_before = 0
    total_layers_after = 0

    for entry in data:
        if "layers" in entry:
            total_layers_before += len(entry["layers"])
        else:
            total_layers_before += 1

    for entry in cleaned_data:
        if "layers" in entry:
            total_layers_after += len(entry["layers"])
        else:
            total_layers_after += 1

    report["summary"]["total_layers_before"] = total_layers_before
    report["summary"]["total_layers_after"] = total_layers_after
    report["summary"]["layers_removed"] = total_layers_before - total_layers_after

    # Save cleaned data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Cleaned data saved to: {output_file}")

    # Save report
    report_file = output_file.replace(".json", "_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"📊 Report saved to: {report_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)
    print(f"Input entries: {report['summary']['total_input_entries']}")
    print(f"Output entries: {report['summary']['total_output_entries']}")
    print(f"\nTotal layers before: {report['summary']['total_layers_before']}")
    print(f"Total layers after: {report['summary']['total_layers_after']}")
    print(f"Duplicates removed: {report['summary']['total_duplicates_removed']}")
    print(f"\nUnique layers (no grouping): {report['summary']['unique_layers_count']}")
    print(f"Grouped descriptions: {report['summary']['grouped_descriptions_count']}")
    print(f"Converted to unique (single layer after cleaning): {report['summary']['converted_to_unique']}")

    if report["grouped_entries_details"]:
        print(f"\nGroups with duplicates cleaned: {len(report['grouped_entries_details'])}")
        print("\nTop 5 groups with most duplicates:")
        sorted_groups = sorted(report["grouped_entries_details"], key=lambda x: x["duplicates_removed"], reverse=True)[
            :5
        ]
        for i, group in enumerate(sorted_groups, 1):
            print(f"\n{i}. Description: {group['description']}")
            print(f"   Original: {group['original_layer_count']} layers")
            print(f"   Cleaned: {group['cleaned_layer_count']} layers")
            print(f"   Removed: {group['duplicates_removed']} duplicates")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    input_file = "layerDescriptions.json"
    output_file = "layerDescriptionsCleaned.json"

    clean_layer_descriptions(input_file, output_file)
