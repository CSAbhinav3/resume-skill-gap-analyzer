import logging
from groq import AsyncGroq
from app.config import settings

logger = logging.getLogger(__name__)

# Single client instance — reused across all calls
client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def call_llm(prompt: str) -> str:
    """
    Single async wrapper for all LLM calls in the app.
    Uses Groq's chat completions API.
    Returns the text content of the first choice.
    Raises RuntimeError on API failure — caller handles retry.
    """
    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that returns structured JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=2048,
        )
    except Exception as e:
        raise RuntimeError(f"Groq API call failed: {e}") from e

    choices = response.choices
    if not choices:
        raise RuntimeError("Groq returned no choices. Check your API key or model name.")

    text = choices[0].message.content.strip()

    if not text:
        raise RuntimeError("Groq returned empty response.")

    logger.debug(f"LLM response length: {len(text)} chars")
    return text