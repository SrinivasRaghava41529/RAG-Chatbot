from rank_bm25 import BM25Okapi
from retrieval.vector_store import load_vector_store


class BM25Retriever:

    def __init__(self):

        vectorstore = load_vector_store()

        docs = vectorstore.docstore._dict.values()

        self.documents = list(docs)

        corpus = [
            doc.page_content.split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(corpus)

    def retrieve(self, query, top_k=20):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        scored_docs = list(zip(self.documents, scores))

        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in scored_docs[:top_k]]