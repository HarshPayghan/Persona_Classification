from google import genai
from google.genai import types

from src.config import (
    GEMINI_API_KEY,
    LLM_MODEL
)

from src.escalator import Escalator


class AdaptiveResponseGenerator:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.escalator = Escalator()

    def get_persona_prompt(
        self,
        persona
    ):

        if persona == "Technical Expert":

            return """
You are a Senior Systems Engineer.

Guidelines:

* Be technically detailed.
* Explain root causes.
* Include API details if available.
* Use structured steps.
* Include code snippets when useful.
"""

        elif persona == "Frustrated User":

            return """
You are an empathetic Customer Support Specialist.

Guidelines:

* Acknowledge frustration.
* Use simple language.
* Give clear action steps.
* Avoid excessive technical jargon.
* Be reassuring and polite.
"""

        else:

            return """
You are a Business Relations Manager.

Guidelines:

* Be concise.
* Focus on business impact.
* Mention timelines when available.
* Avoid deep technical explanations.
"""

    def generate_response(
        self,
        user_query,
        persona,
        context_chunks
    ):

        if self.escalator.should_escalate(
            user_query,
            context_chunks
        ):

            return {
                "escalated": True,
                "response":
                (
                    "Your request has been "
                    "escalated to a human "
                    "support specialist."
                ),
                "handoff":
                self.escalator.generate_handoff(
                    user_query,
                    persona,
                    context_chunks
                )
            }

        persona_prompt = self.get_persona_prompt(
            persona
        )

        context_text = "\n\n".join(
            [
                f"[SOURCE: {chunk['source']}]\n"
                f"{chunk['text']}"
                for chunk in context_chunks
            ]
        )

        system_prompt = f"""
{persona_prompt}

IMPORTANT RULES:

1. Use ONLY the provided context.
2. Do NOT hallucinate information.
3. If information is missing,
   clearly mention it.
4. Be accurate and professional.

CONTEXT:

{context_text}
"""

        response = self.client.models.generate_content(
            model=LLM_MODEL,
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2
            )
        )

        return {
            "escalated": False,
            "response": response.text,
            "handoff": None
        }


if __name__ == "__main__":

    generator = AdaptiveResponseGenerator()

    sample_context = [
        {
            "source":
            "password_reset_guide.pdf",

            "text":
            (
                "Users can reset their "
                "password from the "
                "Forgot Password page."
            ),

            "score": 0.92
        }
    ]

    result = generator.generate_response(
        user_query=
        "How do I reset my password?",

        persona=
        "Technical Expert",

        context_chunks=
        sample_context
    )

    print(result["response"])