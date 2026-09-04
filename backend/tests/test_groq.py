from app.core.config.settings import settings
from groq import Groq


def main():
    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq API working"
            }
        ],
        temperature=0,
    )

    print("\nResponse:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()