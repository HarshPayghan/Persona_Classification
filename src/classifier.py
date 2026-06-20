import json
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY, LLM_MODEL


class PersonaClassifier:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def classify(self, user_message: str) -> dict:
        """
        Classify incoming user message into a persona.

        Returns:
        {
            "persona": "...",
            "confidence": 0.95,
            "reasoning": "..."
        }
        """

        system_prompt = """
You are a customer persona classification engine.

Classify into EXACTLY ONE category:

1. Technical Expert
- Uses technical terms such as API, logs, authentication,
  database, code, server, deployment, configuration,
  backend, frontend, debugging, integration.
- Discusses troubleshooting or implementation details.

2. Frustrated User
- Explicitly expresses frustration, anger, urgency,
  disappointment, or dissatisfaction.
- Uses words like:
  frustrated, angry, upset, urgent, immediately,
  terrible, broken, unacceptable, disappointed.

3. Business Executive
- Focuses on business impact, customers, revenue,
  timelines, deadlines, ROI, operations, management,
  executive reporting.

IMPORTANT RULES:
- Simple support questions are NOT Frustrated User.
- Password reset requests are NOT Frustrated User.
- Login help requests are NOT Frustrated User unless
  emotional language is present.
- Only classify as Frustrated User when emotional
  language is clearly expressed.
- If uncertain, prefer Technical Expert.

Return ONLY valid JSON.
"""

        schema = {
            "type": "OBJECT",
            "properties": {
                "persona": {
                    "type": "STRING",
                    "enum": [
                        "Technical Expert",
                        "Frustrated User",
                        "Business Executive"
                    ]
                },
                "confidence": {
                    "type": "NUMBER"
                },
                "reasoning": {
                    "type": "STRING"
                }
            },
            "required": [
                "persona",
                "confidence",
                "reasoning"
            ]
        }

        try:
            response = self.client.models.generate_content(
                model=LLM_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.1
                )
            )

            return json.loads(response.text)

        except json.JSONDecodeError:
            return {
                "persona": "Technical Expert",
                "confidence": 0.50,
                "reasoning": "Failed to parse Gemini JSON response."
            }

        except Exception as e:
            print(f"Gemini Classification Error: {e}")

            # Simple rule-based fallback
            text = user_message.lower()

            if any(word in text for word in [
                "frustrated",
                "angry",
                "upset",
                "terrible",
                "urgent",
                "immediately"
            ]):
                persona = "Frustrated User"

            elif any(word in text for word in [
                "revenue",
                "business",
                "customer impact",
                "timeline",
                "roi",
                "operations"
            ]):
                persona = "Business Executive"

            else:
                persona = "Technical Expert"

            return {
                "persona": persona,
                "confidence": 0.50,
                "reasoning": "Rule-based fallback due to Gemini API unavailability."
            }


if __name__ == "__main__":

    classifier = PersonaClassifier()

    test_message = (
        "Our production API returns 401 errors "
        "after updating authentication headers."
    )

    result = classifier.classify(test_message)

    print(json.dumps(result, indent=4))