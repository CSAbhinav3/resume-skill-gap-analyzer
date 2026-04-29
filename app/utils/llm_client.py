import google.generativeai as genai
from app.config import settings

# Configure once at import time
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_model() -> genai.GenerativeModel:
    """Returns a configured Gemini model instance."""
    return genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        generation_config=genai.GenerationConfig(
            temperature=0.2,        # low temp = consistent structured output
            max_output_tokens=4096,
        )
    )


async def call_llm(prompt: str) -> str:
    """
    Single async wrapper for all LLM calls in the app.
    Returns the text content of the first candidate.
    Raises on API error — caller handles retry/fallback.
    """
    model = get_model()
    response = await model.generate_content_async(prompt)

    if not response.candidates:
        raise ValueError("Gemini returned no candidates. Check prompt or API quota.")

    return response.text.strip()