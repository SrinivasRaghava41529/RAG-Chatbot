import math


def safe_value(x):
    if x is None or math.isnan(x):
        return 0.0
    return float(x)


def compute_confidence(retrieval_scores, rerank_scores, answer):

    if not retrieval_scores or not rerank_scores:
        return 0.0

    retrieval_score = safe_value(sum(retrieval_scores) / len(retrieval_scores))
    rerank_score = safe_value(sum(rerank_scores) / len(rerank_scores))

    answer_length_score = min(len(answer) / 500, 1)

    confidence = (
        0.5 * rerank_score +
        0.3 * retrieval_score +
        0.2 * answer_length_score
    )

    return round(safe_value(confidence), 2)