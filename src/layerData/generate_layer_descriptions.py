## The descriptions for layers are not in documentation. They are in metaver saved.
## They are fetched from there one time when creating the docker container.
## Or one time while creating the data for the application.

import requests
import xml.etree.ElementTree as ET
import json
from typing import Dict, Optional, List


def create_csw_url(dataset: Dict) -> str:
    csw_url = dataset.get("csw_url")
    md_id = dataset.get("md_id")

    if not csw_url or not md_id:
        raise ValueError("Dataset must contain 'csw_url' and 'md_id' fields")

    request_url = f"{csw_url}?" f"REQUEST=GetRecordById&" f"SERVICE=CSW&" f"VERSION=2.0.2&" f"id={md_id}"

    return request_url


def fetch_and_parse_metadata(url: str) -> Dict[str, Optional[str]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    namespaces = {
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gco": "http://www.isotc211.org/2005/gco",
        "csw": "http://www.opengis.net/cat/csw/2.0.2",
    }

    abstract_element = root.find(".//gmd:abstract/gco:CharacterString", namespaces)
    description = abstract_element.text if abstract_element is not None else None

    return {"description": description}


def process_services(input_file: str, output_file: str, start: int = 0, limit: Optional[int] = None):
    with open(input_file, "r", encoding="utf-8") as f:
        services_data = json.load(f)

    results = []
    metadata_cache = {}
    failed_requests = []

    for i, service in enumerate(services_data):
        if i < start:
            continue
        if limit and i >= start + limit:
            break
        if "datasets" not in service or not service["datasets"]:
            continue

        dataset = service["datasets"][0]

        service_id = service.get("id")
        service_name = service.get("name")

        md_id = dataset.get("md_id")

        try:
            if md_id in metadata_cache:
                metadata = metadata_cache[md_id]
            else:
                csw_url = create_csw_url(dataset)
                metadata = fetch_and_parse_metadata(csw_url)
                metadata_cache[md_id] = metadata

            result = {"id": service_id, "name": service_name, "description": metadata.get("description")}

            results.append(result)

        except Exception as e:
            failed_requests.append(
                {
                    "service_id": service_id,
                    "service_name": service_name,
                    "md_id": md_id,
                    "csw_url": dataset.get("csw_url"),
                    "error": str(e),
                }
            )
            print(f"Failed to fetch metadata for service {service_id} ({service_name}): {str(e)}")

        if (i + 1) % 30 == 0:
            print(f"Processed {i + 1}/{len(services_data)} services")

    print(f"Completed: {len(results)} services processed, {len(failed_requests)} failed")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    if failed_requests:
        error_log_file = output_file.replace(".json", "_errors.json")
        with open(error_log_file, "w", encoding="utf-8") as f:
            json.dump(failed_requests, f, ensure_ascii=False, indent=2)
        print(f"Error log saved to: {error_log_file}")

    # Generate report
    md_id_counts = {}
    for md_id in metadata_cache.keys():
        count = sum(1 for s in services_data if s.get("datasets") and s["datasets"][0].get("md_id") == md_id)
        md_id_counts[md_id] = count

    total_cached = sum(1 for count in md_id_counts.values() if count > 1)
    total_unique_fetched = len(metadata_cache)

    report = {
        "summary": {
            "total_services_processed": len(results),
            "total_services_failed": len(failed_requests),
            "unique_metadata_fetched": total_unique_fetched,
            "metadata_reused_from_cache": len(results) - total_unique_fetched,
        },
        "md_id_usage": [
            {"md_id": md_id, "service_count": count}
            for md_id, count in sorted(md_id_counts.items(), key=lambda x: x[1], reverse=True)
        ],
    }

    report_file = output_file.replace(".json", "_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    input_file = "services-intranet.json"
    output_file = "layerDescriptions.json"

    process_services(input_file, output_file)
