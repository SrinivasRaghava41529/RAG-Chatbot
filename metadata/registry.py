import json
from pathlib import Path

REGISTRY_PATH = Path("metadata/registry.json")


def load_registry():

    if not REGISTRY_PATH.exists():
        return {}

    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(data):

    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def document_exists(doc_hash):

    registry = load_registry()

    return doc_hash in registry


def register_document(doc_hash, file_name, chunk_count):

    registry = load_registry()

    registry[doc_hash] = {
        "file_name": file_name,
        "chunks": chunk_count
    }

    save_registry(registry)