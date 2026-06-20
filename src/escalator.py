import json

from src.config import (
    CONFIDENCE_THRESHOLD,
    SENSITIVE_TOPICS
)


class Escalator:

    def __init__(self):
        pass

    def contains_sensitive_topic(
        self,
        user_query: str
    ) -> bool:

        user_query = user_query.lower()

        for keyword in SENSITIVE_TOPICS:

            if keyword.lower() in user_query:
                return True

        return False

    def low_confidence(
        self,
        context_chunks: list
    ) -> bool:

        if not context_chunks:
            return True

        best_score = max(
            chunk["score"]
            for chunk in context_chunks
        )

        return best_score < CONFIDENCE_THRESHOLD

    def should_escalate(
        self,
        user_query: str,
        context_chunks: list
    ) -> bool:

        if self.contains_sensitive_topic(
            user_query
        ):
            return True

        if self.low_confidence(
            context_chunks
        ):
            return True

        return False

    def generate_handoff(
        self,
        user_query: str,
        persona: str,
        context_chunks: list
    ) -> str:

        confidence_score = 0.0

        retrieved_sources = []

        if context_chunks:

            confidence_score = max(
                chunk["score"]
                for chunk in context_chunks
            )

            retrieved_sources = [
                chunk["source"]
                for chunk in context_chunks
            ]

        handoff = {
            "persona": persona,
            "issue_summary": user_query,
            "retrieved_sources": retrieved_sources,
            "confidence_score": confidence_score,
            "recommended_action":
            (
                "Human review required. "
                "Customer issue could not be "
                "safely resolved automatically."
            )
        }

        return json.dumps(
            handoff,
            indent=4
        )


if __name__ == "__main__":

    escalator = Escalator()

    sample_query = (
        "I was charged twice and "
        "want an immediate refund."
    )

    sample_context = [
        {
            "source": "billing_policy.txt",
            "score": 0.39
        }
    ]

    print(
        escalator.should_escalate(
            sample_query,
            sample_context
        )
    )

    print(
        escalator.generate_handoff(
            sample_query,
            "Frustrated User",
            sample_context
        )
    )