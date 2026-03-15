from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset
import math

from orchestration.llm import get_llm


def check_faithfulness(question, answer, contexts):

    try:

        llm = get_llm()

        data = {
            "question": [question],
            "answer": [answer],
            "contexts": [contexts]
        }

        dataset = Dataset.from_dict(data)

        result = evaluate(
            dataset,
            metrics=[faithfulness],
            llm=llm
        )

        score = result["faithfulness"][0]

        # Fix NaN values
        if score is None or math.isnan(score):
            return 0.0

        return round(float(score), 2)

    except Exception as e:

        print("RAGAS evaluation failed:", e)

        return 0.0