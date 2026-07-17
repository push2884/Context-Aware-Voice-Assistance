#!/usr/bin/env python3
"""
validate_datasets.py

Validates voice assistant JSON datasets against a defined structure.

Usage:
    python validate_datasets.py data/all_samples.json

Features:
    - JSON syntax validation
    - Required field validation
    - Intent validation
    - Entity structure validation
    - Response validation
    - Dataset summary report
"""

import json
import sys
from pathlib import Path


REQUIRED_SAMPLE_FIELDS = [
    "query",
    "intent",
    "entities",
    "response"
]

ALLOWED_MODALITIES = [
    "audio",
    "text",
    "visual",
    "multimodal"
]


def load_json(file_path):
    """Load JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    except json.JSONDecodeError as error:
        print(f"❌ Invalid JSON format: {error}")
        sys.exit(1)


def validate_dataset_structure(data):
    """Validate top-level dataset structure."""

    errors = []

    if not isinstance(data, dict):
        errors.append("Dataset root must be an object.")
        return errors

    if "samples" not in data:
        errors.append("Missing required field: samples")

    elif not isinstance(data["samples"], list):
        errors.append("samples must be an array.")

    return errors


def validate_sample(sample, index):
    """Validate individual sample."""

    errors = []

    if not isinstance(sample, dict):
        return [
            f"Sample {index} must be an object."
        ]

    for field in REQUIRED_SAMPLE_FIELDS:
        if field not in sample:
            errors.append(
                f"Sample {index}: Missing field '{field}'"
            )

    if "query" in sample and not isinstance(sample["query"], str):
        errors.append(
            f"Sample {index}: query must be string"
        )

    if "intent" in sample and not isinstance(sample["intent"], str):
        errors.append(
            f"Sample {index}: intent must be string"
        )

    if "entities" in sample:
        if not isinstance(sample["entities"], dict):
            errors.append(
                f"Sample {index}: entities must be object"
            )

    if "response" in sample:
        if not isinstance(sample["response"], str):
            errors.append(
                f"Sample {index}: response must be string"
            )

    if "modality" in sample:
        if sample["modality"] not in ALLOWED_MODALITIES:
            errors.append(
                f"Sample {index}: Invalid modality '{sample['modality']}'"
            )

    if "confidence" in sample:
        confidence = sample["confidence"]

        if not isinstance(confidence, (float, int)):
            errors.append(
                f"Sample {index}: confidence must be number"
            )

        elif confidence < 0 or confidence > 1:
            errors.append(
                f"Sample {index}: confidence must be between 0 and 1"
            )

    return errors


def generate_report(data):
    """Generate dataset statistics."""

    samples = data.get("samples", [])

    intents = {}
    categories = {}

    for sample in samples:

        intent = sample.get("intent", "unknown")
        category = sample.get("category", "unknown")

        intents[intent] = intents.get(intent, 0) + 1
        categories[category] = categories.get(category, 0) + 1

    return {
        "total_samples": len(samples),
        "total_intents": len(intents),
        "categories": categories,
        "top_intents": intents
    }


def validate_file(file_path):
    """Run complete validation."""

    print("\nVoice Assistant Dataset Validator")
    print("=" * 40)

    data = load_json(file_path)

    errors = []

    errors.extend(
        validate_dataset_structure(data)
    )

    if "samples" in data:

        for index, sample in enumerate(
            data["samples"],
            start=1
        ):
            errors.extend(
                validate_sample(sample, index)
            )

    if errors:

        print("\n❌ Validation Failed")
        print("-" * 40)

        for error in errors:
            print(error)

        return False

    print("\n✅ Dataset Validation Successful")
    print("-" * 40)

    report = generate_report(data)

    print(
        f"Samples: {report['total_samples']}"
    )

    print(
        f"Intents: {report['total_intents']}"
    )

    print("\nCategories:")

    for category, count in report["categories"].items():
        print(
            f"  - {category}: {count}"
        )

    return True


def main():

    if len(sys.argv) < 2:
        print(
            "Usage: python validate_datasets.py <dataset.json>"
        )
        sys.exit(1)

    dataset_path = Path(sys.argv[1])

    success = validate_file(dataset_path)

    sys.exit(
        0 if success else 1
    )


if __name__ == "__main__":
    main()
