from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
import os


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    # Add metadata
    for chunk in chunks:

        source = chunk.metadata.get("source", "unknown")

        chunk.metadata["file"] = os.path.basename(source)

    return chunks