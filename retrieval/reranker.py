from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    def rerank(self, query, documents, top_k=4):

        pairs = [
            (query, doc.page_content)
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        scored_docs = list(zip(documents, scores))

        scored_docs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        top_docs = scored_docs[:top_k]

        docs = [d[0] for d in top_docs]
        scores = [float(d[1]) for d in top_docs]

        return docs, scores