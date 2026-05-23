import json
import logging
import re

from app.config import settings
from app.utils.llm_client import call_llm
from app.services.taxonomy_engine import taxonomy_index

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

OUTPUT FORMAT:
{
  "technical_skills": ["skill1", "skill2"],
  "tools": ["tool1", "tool2"],
  "soft_skills": ["skill1", "skill2"]
}

RESUME TEXT:
{resume_text}
"""


def parse_llm_response(response_text: str) -> dict:

    text = response_text.strip()

    # Remove markdown wrappers
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        data = json.loads(text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON: {e}\n"
            f"Raw response: {response_text[:300]}"
        )

    required_keys = {
        "technical_skills",
        "tools",
        "soft_skills"
    }

    missing = required_keys - set(data.keys())

    if missing:
        raise ValueError(
            f"LLM response missing required keys: {missing}"
        )

    # Validate lists
    for key in required_keys:

        if not isinstance(data[key], list):
            raise ValueError(
                f"Key '{key}' must be a list"
            )

        cleaned = []

        for item in data[key]:

            item = str(item).strip()

            if item:
                cleaned.append(item)

        data[key] = cleaned

    return data


def normalize_skill(skill: str) -> str:
    """
    Normalize for deduplication.
    """

    return skill.lower().strip()


def merge_skills(llm_skills, recovered_skills):

    merged = {}

    for skill in llm_skills + recovered_skills:

        normalized = normalize_skill(skill)

        if normalized not in merged:
            merged[normalized] = skill

    return list(merged.values())


async def extract_skills(clean_text: str) -> dict:
    """
    Extract skills using:
    1. LLM extraction
    2. Deterministic taxonomy recovery
    """

    if not clean_text or not clean_text.strip():
        raise ValueError(
            "Cannot extract skills from empty text."
        )

    prompt = SKILL_EXTRACTION_PROMPT.replace(
        "{resume_text}",
        clean_text
    )

    logger.info("Calling LLM for skill extraction...")

    last_error = None

    for attempt in range(2):

        try:

            response_text = await call_llm(prompt)

            skills = parse_llm_response(response_text)

            # ===================================================
            # Deterministic taxonomy recovery
            # ===================================================

            resume_text_lower = clean_text.lower()

            recovered_technical = []
            recovered_tools = []
            recovered_soft = []

            for skill_name, category in zip(
                taxonomy_index.skill_names,
                taxonomy_index.categories
            ):

                if skill_name.lower() in resume_text_lower:

                    if category == "technical_skills":
                        recovered_technical.append(skill_name)

                    elif category == "tools":
                        recovered_tools.append(skill_name)

                    elif category == "soft_skills":
                        recovered_soft.append(skill_name)

            # ===================================================
            # Merge LLM + deterministic recovery
            # ===================================================

            skills["technical_skills"] = merge_skills(
                skills["technical_skills"],
                recovered_technical
            )

            skills["tools"] = merge_skills(
                skills["tools"],
                recovered_tools
            )

            skills["soft_skills"] = merge_skills(
                skills["soft_skills"],
                recovered_soft
            )

            skills["model_used"] = settings.GROQ_MODEL

            logger.info(
                f"Skill extraction complete — "
                f"technical: {len(skills['technical_skills'])}, "
                f"tools: {len(skills['tools'])}, "
                f"soft: {len(skills['soft_skills'])}"
            )

            logger.info(
                f"Recovered deterministic skills — "
                f"technical: {len(recovered_technical)}, "
                f"tools: {len(recovered_tools)}, "
                f"soft: {len(recovered_soft)}"
            )

            return skills

        except ValueError as e:

            last_error = e

            logger.warning(
                f"Attempt {attempt + 1} failed: {e}"
            )

            continue

    raise ValueError(
        f"Skill extraction failed after 2 attempts: {last_error}"
    )