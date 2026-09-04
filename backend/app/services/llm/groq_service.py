from groq import Groq

from app.core.config.settings import settings


class GroqService:
    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def invoke(
        self,
        prompt: str,
        model: str = "llama-3.3-70b-versatile",
        
    ) -> str:

        response = self.client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content