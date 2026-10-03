import logging
from openai import AsyncOpenAI

from config import AI_API_KEY, AI_MODEL

logger = logging.getLogger(__name__)

_client = None


def get_client():
    global _client

    if not AI_API_KEY:
        raise ValueError("AI_API_KEY is not configured")

    if _client is None:
        _client = AsyncOpenAI(api_key=AI_API_KEY)

    return _client


async def generate_caption(text: str, language: str = "বাংলা") -> str:
    try:
        client = get_client()

        system_prompt = f"""
You are an AI caption writer and editor.

Supported output language:
{language}

Your tasks:
- Create attractive social-media captions.
- Edit and improve captions.
- Fix grammar and spelling.
- Keep the meaning unless the user asks for a rewrite.
- Do not add unnecessary explanations.
- Return only the final caption.
"""

        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.8,
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError("AI returned an empty response")

        return result.strip()

    except Exception:
        logger.exception("AI caption generation failed")
        raise
