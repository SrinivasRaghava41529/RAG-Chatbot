from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en"
    )

    return embeddings