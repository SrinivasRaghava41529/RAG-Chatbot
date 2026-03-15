from retrieval.retriever import get_retriever
from retrieval.reranker import Reranker
from retrieval.bm25_retriever import BM25Retriever

from orchestration.llm import get_llm
from orchestration.prompts import RAG_PROMPT

from monitoring.latency import LatencyTracker
from monitoring.logging_config import setup_logger

from guardrails.confidence import compute_confidence
from guardrails.toxicity import ToxicityGuard

from evaluation.ragas_eval import check_faithfulness

from guardrails.validation import validate_answer

import math


def safe_float(x):
    """
    Prevent NaN / None values from breaking JSON responses
    """
    if x is None:
        return 0.0

    if isinstance(x, float) and math.isnan(x):
        return 0.0

    return float(x)


class RAGPipeline:

    def __init__(self):

        self.retriever = get_retriever()
        self.reranker = Reranker()
        self.bm25 = BM25Retriever()

        self.llm = get_llm()

        self.logger = setup_logger()
        self.toxicity_guard = ToxicityGuard()

    def run(self, question):

        tracker = LatencyTracker()

        self.logger.info(f"Query: {question}")

        # --------------------------------
        # Input Guardrail (User Query)
        # --------------------------------
        if self.toxicity_guard.is_toxic(question):

            self.logger.warning("Toxic user input detected")

            return {
                "answer": "⚠ Your query was blocked because it contains unsafe or toxic content.",
                "confidence": 0.0,
                "faithfulness": 0.0,
                "sources": [],
                "latency": {}
            }

        # --------------------------------
        # Retrieval
        # --------------------------------
        tracker.start("retrieval")

        # Vector retrieval
        vector_docs = self.retriever.invoke(question)

        # BM25 retrieval
        bm25_docs = self.bm25.retrieve(question)

        # Merge results
        docs = vector_docs + bm25_docs

        # Remove duplicates
        unique_docs = []
        seen = set()

        for doc in docs:
            text = doc.page_content
            if text not in seen:
                unique_docs.append(doc)
                seen.add(text)

        docs = unique_docs

        tracker.end("retrieval")

        # Some retrievers don't return similarity scores
        retrieval_scores = [
            doc.metadata.get("score", 0.5)
            for doc in docs
        ]

        # --------------------------------
        # Reranking
        # --------------------------------
        tracker.start("rerank")

        reranked_docs, rerank_scores = self.reranker.rerank(
            question,
            docs
        )

        tracker.end("rerank")

        # --------------------------------
        # Build Context
        # --------------------------------
        context = "\n\n".join(
            [doc.page_content for doc in reranked_docs]
        )

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        # --------------------------------
        # LLM Generation
        # --------------------------------
        tracker.start("generation")

        response = self.llm.invoke(prompt)

        tracker.end("generation")

        answer_text = response.content

        # --------------------------------
        # Output Guardrail (LLM Response)
        # --------------------------------
        if self.toxicity_guard.is_toxic(answer_text):

            self.logger.warning("Toxic model output detected")

            answer_text = "⚠ The generated response was blocked due to unsafe content."

        answer_text = validate_answer(answer_text)

        latency = tracker.get_latency()

        # --------------------------------
        # Confidence Score
        # --------------------------------
        confidence = compute_confidence(
            retrieval_scores,
            rerank_scores,
            answer_text
        )

        # --------------------------------
        # Faithfulness Evaluation (RAGAS)
        # --------------------------------
        contexts = [
            doc.page_content
            for doc in reranked_docs
        ]

        faithfulness_score = check_faithfulness(
            question,
            answer_text,
            contexts
        )

        # --------------------------------
        # Safety: prevent NaN
        # --------------------------------
        confidence = safe_float(confidence)
        faithfulness_score = safe_float(faithfulness_score)

        # --------------------------------
        # Logging
        # --------------------------------
        self.logger.info(
            f"Confidence: {confidence}, Faithfulness: {faithfulness_score}"
        )

        self.logger.info(
            f"Latency: {latency}"
        )

        # --------------------------------
        # Final Response
        # --------------------------------
        return {
            "answer": answer_text,
            "confidence": confidence,
            "faithfulness": faithfulness_score,
            "sources": [
                {
                    "file": doc.metadata.get("file"),
                    "page": doc.metadata.get("page")
                }
                for doc in reranked_docs
            ],
            "latency": latency
        }


def build_rag_chain():
    return RAGPipeline()