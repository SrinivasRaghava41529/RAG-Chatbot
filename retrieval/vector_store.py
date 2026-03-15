from langchain_community.vectorstores import FAISS
from ingestion.embeddings import get_embeddings
from config.settings import settings
import os


def create_vector_store(chunks):

    embeddings = get_embeddings()

    # If index already exists → load it
    if os.path.exists(settings.VECTOR_DB_PATH):

        vectorstore = FAISS.load_local(
            settings.VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        vectorstore.add_documents(chunks)

    else:

        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )

    vectorstore.save_local(settings.VECTOR_DB_PATH)

    return vectorstore


def load_vector_store():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        settings.VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore