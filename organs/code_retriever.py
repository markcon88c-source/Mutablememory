#!/usr/bin/env python3
# code_retriever.py

import json
import os
import sys

REGISTRY_PATH = os.path.expanduser("~/.memo2/pipeline_registry.json")


def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        print("No pipeline registry found. Run `memo2 pipeline` first.")
        sys.exit(1)

    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(registry):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def fuzzy_match(name, registry):
    name = name.lower()

    # exact raw match
    if name in registry:
        return name

    # exact common name match
    for raw, info in registry.items():
        if info["common_name"].lower() == name:
            return raw

    # partial match
    for raw, info in registry.items():
        if name in raw.lower() or name in info["common_name"].lower():
            return raw

    return None


def print_code(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        print(f.read())


def cli():
    if len(sys.argv) < 3:
        print("Usage: memo2 code <organ>")
        sys.exit(1)

    organ_name = " ".join(sys.argv[2:])
    registry = load_registry()

    match = fuzzy_match(organ_name, registry)
    if not match:
        print(f"No organ found matching: {organ_name}")
        sys.exit(1)

    path = registry[match]["path"]
    print_code(path)


if __name__ == "__main__":
    cli()
