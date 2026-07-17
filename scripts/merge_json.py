#!/usr/bin/env python3
"""
merge_json.py

Merge multiple voice assistant JSON datasets into a single dataset.

Usage:
    python merge_json.py input_folder output_file.json

Example:
    python merge_json.py data/ all_samples.json

Features:
    - Merge multiple JSON files
    - Preserve categories
    - Remove duplicate samples
    - Generate unique IDs
    - Create combined dataset
"""

import json
import sys
from pathlib import Path


def load_json(file_path):
    """Load JSON file safely."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {file_path}")
        print(error)
        return None


def extract_samples(data, category_name):
    """Extract samples from different JSON formats."""

    samples = []

    if isinstance(data, dict):

        if "samples" in data:
            samples.extend(data["samples"])

        elif "data" in data:
            samples.extend(data["data"])

    elif isinstance(data, list):
        samples.extend(data)

    for sample in samples:

        if "category" not in sample:
            sample["category"] = category_name

    return samples


def create_sample_key(sample):
    """Create unique key for duplicate detection."""

    return (
        sample.get("query", "").lower().strip(),
        sample.get("intent", "").lower().strip()
    )


def merge_datasets(input_folder):
    """Merge all JSON files from folder."""

    folder = Path(input_folder)

    if not folder.exists():
        print(
            f"Folder not found: {input_folder}"
        )
        sys.exit(1)

    merged_samples = []
    seen = set()

    json_files = sorted(
        folder.glob("*.json")
    )

    if not json_files:
        print(
            "No JSON files found."
        )
        sys.exit(1)

    for file_path in json_files:

        print(
            f"Loading: {file_path.name}"
        )

        data = load_json(file_path)

        if data is None:
            continue

        category = file_path.stem

        samples = extract_samples(
            data,
            category
        )

        for sample in samples:

            key = create_sample_key(sample)

            if key in seen:
                continue

            seen.add(key)

            merged_samples.append(
                sample
            )

    for index, sample in enumerate(
        merged_samples,
        start=1
    ):
        sample["id"] = index

    return merged_samples


def save_json(samples, output_file):
    """Save merged dataset."""

    dataset = {
        "dataset_name": "voice_assistant_all_samples",
        "version": "1.0",
        "total_samples": len(samples),
        "samples": samples
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nCreated: {output_file}"
    )

    print(
        f"Total samples: {len(samples)}"
    )


def main():

    if len(sys.argv) < 3:

        print(
            "Usage: python merge_json.py <input_folder> <output_file>"
        )

        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    samples = merge_datasets(
        input_folder
    )

    save_json(
        samples,
        output_file
    )


if __name__ == "__main__":
    main()
