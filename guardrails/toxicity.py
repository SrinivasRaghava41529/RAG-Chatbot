from transformers import pipeline


class ToxicityGuard:

    def __init__(self):

        self.classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert"
        )

        self.max_length = 512  # model limit

    def is_toxic(self, text):

        if not text:
            return False

        # 🔥 Truncate text to avoid overflow
        truncated_text = text[:1000]  # approx safe char limit

        try:
            result = self.classifier(
                truncated_text,
                truncation=True,
                max_length=self.max_length
            )[0]

            label = result["label"]
            score = result["score"]

            if label == "toxic" and score > 0.6:
                return True

            return False

        except Exception as e:
            print("Toxicity check failed:", e)
            return False