import json
import logging
import re

from app.config import settings
from app.utils.llm_client import call_llm

logger = logging.getLogger(__name__)


SKILL_EXTRACTION_PROMPT = """
You are an expert technical recruiter and resume parser.

Your task is to extract ALL skills from the resume text below and return them as a structured JSON object.

DEFINITIONS:
- technical_skills: Programming languages, frameworks, libraries, algorithms, ML/AI concepts, data concepts, engineering practices
- tools: Software tools, platforms, cloud services, databases, DevOps tools, IDEs, APIs
- soft_skills: Communication, leadership, teamwork, problem-solving, analytical thinking, interpersonal skills

RULES:
1. Extract ONLY skills explicitly mentioned or clearly implied in the resume
2. Do NOT invent or hallucinate skills not present in the resume
3. Normalize skill names: use standard names (e.g. "Python" not "python", "Machine Learning" not "ML/AI")
4. Remove duplicates within each category
5. Keep skills concise — maximum 4 words per skill
6. If a category has no skills, return an empty list for that category
7. Return ONLY the JSON object — no explanation, no markdown, no preamble

OUTPUT FORMAT (strictly follow this):
{
  "technical_skills": ["skill1", "skill2", ...],
  "tools": ["tool1", "tool2", ...],
  "soft_skills": ["skill1", "skill2", ...]
}

RESUME TEXT:
{resume_text}
"""


def parse_llm_response(response_text: str) -> dict:
    """
    Parse LLM response into a validated skill dict.
    
    Handles 3 cases:
    1. Clean JSON response (ideal)
    2. JSON wrapped in markdown code blocks (common LLM behavior)
    3. Malformed response (raises ValueError)
    """
    text = response_text.strip()

    # Strip markdown code blocks if present
    # Handles ```json ... ``` and ``` ... ```
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw response: {response_text[:300]}")

    # Validate structure
    required_keys = {"technical_skills", "tools", "soft_skills"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"LLM response missing required keys: {missing}")

    # Ensure all values are lists of strings
    for key in required_keys:
        if not isinstance(data[key], list):
            raise ValueError(f"Key '{key}' must be a list, got {type(data[key])}")
        # Coerce all items to strings and strip whitespace
        data[key] = [str(item).strip() for item in data[key] if str(item).strip()]

    return data


async def extract_skills(clean_text: str) -> dict:
    """
    Extract skills from clean resume text using Gemini.

    Args:
        clean_text: Preprocessed resume text from pdf_ingestion

    Returns:
        {
            "technical_skills": [...],
            "tools": [...],
            "soft_skills": [...],
            "model_used": "gemini-2.0-flash"
        }

    Raises:
        ValueError: if LLM returns malformed response after retries
        Exception: if LLM API call fails
    """
    if not clean_text or not clean_text.strip():
        raise ValueError("Cannot extract skills from empty text.")

    prompt = SKILL_EXTRACTION_PROMPT.replace("{resume_text}", clean_text)

    logger.info("Calling Gemini for skill extraction...")

    # Retry once on parse failure — LLMs occasionally return malformed JSON
    last_error = None
    for attempt in range(2):
        try:
            response_text = await call_llm(prompt)
            skills = parse_llm_response(response_text)
            skills["model_used"] = settings.GROQ_MODEL

            logger.info(
                f"Skill extraction complete — "
                f"technical: {len(skills['technical_skills'])}, "
                f"tools: {len(skills['tools'])}, "
                f"soft: {len(skills['soft_skills'])}"
            )
            return skills

        except ValueError as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            continue

    raise ValueError(f"Skill extraction failed after 2 attempts: {last_error}")