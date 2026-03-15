import argparse
import os

from ingestion.loaders import load_pdf
from ingestion.chunking import chunk_documents
from retrieval.vector_store import create_vector_store
from ingestion.utils import compute_file_hash

from metadata.registry import document_exists, register_document


def ingest(file_path):

    print("Checking document hash...")

    doc_hash = compute_file_hash(file_path)

    if document_exists(doc_hash):

        print("⚠ Document already ingested. Skipping.")
        return

    print("Loading document...")
    docs = load_pdf(file_path)

    print(f"Loaded {len(docs)} pages")

    print("Chunking document...")
    chunks = chunk_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("Creating vector store...")
    create_vector_store(chunks)

    register_document(
        doc_hash,
        os.path.basename(file_path),
        len(chunks)
    )

    print("✅ Document ingestion complete")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)

    args = parser.parse_args()

    ingest(args.file)