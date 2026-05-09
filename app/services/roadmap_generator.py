import json
import logging
import re

from app.config import settings
from app.services.gap_analyzer import GapAnalysisResult
from app.utils.llm_client import call_llm

logger = logging.getLogger(__name__)


ROADMAP_PROMPT = """
You are an expert technical career coach and learning path designer.

Your task is to generate a personalized 30/60/90 day learning roadmap based on a candidate's skill gaps.

CANDIDATE PROFILE:
- Target Role: {target_role}
- Overall Match Score: {match_score}%
- Skills Already Present: {present_skills}

SKILL GAPS TO ADDRESS (ranked by priority, rank 1 = most critical):
{missing_skills}

INSTRUCTIONS:
1. Generate a structured 30/60/90 day roadmap addressing the TOP skill gaps
2. Focus on the highest priority gaps first (rank 1, 2, 3...)
3. Each phase should build on the previous one
4. Include specific, actionable resources (real course names, documentation links, books)
5. Weekly breakdown must be concrete — what to study each week, not vague goals
6. Tailor recommendations to someone already skilled in: {present_skills_short}
7. Do NOT repeat skills already present in the resume
8. Return ONLY valid JSON — no markdown, no explanation, no preamble

OUTPUT FORMAT (strictly follow this structure):
{{
  "target_role": "{target_role}",
  "overall_match_score": {match_score},
  "phases": [
    {{
      "phase": "30_day",
      "goal": "Foundation — close the most critical gaps",
      "weeks": [
        {{
          "week": 1,
          "focus": "skill name",
          "topics": ["specific topic 1", "specific topic 2"],
          "resources": ["resource name and link", "resource name and link"],
          "goal": "what you will be able to do by end of week"
        }},
        {{
          "week": 2,
          "focus": "skill name",
          "topics": ["specific topic 1", "specific topic 2"],
          "resources": ["resource name and link", "resource name and link"],
          "goal": "what you will be able to do by end of week"
        }},
        {{
          "week": 3,
          "focus": "skill name",
          "topics": ["specific topic 1"],
          "resources": ["resource name and link"],
          "goal": "what you will be able to do by end of week"
        }},
        {{
          "week": 4,
          "focus": "consolidation and projects",
          "topics": ["build a project combining week 1-3 skills"],
          "resources": ["GitHub", "personal projects"],
          "goal": "have a working project on GitHub demonstrating 30-day skills"
        }}
      ]
    }},
    {{
      "phase": "60_day",
      "goal": "Intermediate — expand into adjacent skill gaps",
      "weeks": [
        {{"week": 5, "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 6, "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 7, "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 8, "focus": "...", "topics": [], "resources": [], "goal": "..."}}
      ]
    }},
    {{
      "phase": "90_day",
      "goal": "Advanced — production-ready skills and portfolio",
      "weeks": [
        {{"week": 9,  "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 10, "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 11, "focus": "...", "topics": [], "resources": [], "goal": "..."}},
        {{"week": 12, "focus": "...", "topics": [], "resources": [], "goal": "..."}}
      ]
    }}
  ],
  "weekly_breakdown": [
    {{"week": 1, "phase": "30_day", "focus": "...", "goal": "..."}},
    {{"week": 2, "phase": "30_day", "focus": "...", "goal": "..."}},
    {{"week": 3, "phase": "30_day", "focus": "...", "goal": "..."}},
    {{"week": 4, "phase": "30_day", "focus": "...", "goal": "..."}},
    {{"week": 5, "phase": "60_day", "focus": "...", "goal": "..."}},
    {{"week": 6, "phase": "60_day", "focus": "...", "goal": "..."}},
    {{"week": 7, "phase": "60_day", "focus": "...", "goal": "..."}},
    {{"week": 8, "phase": "60_day", "focus": "...", "goal": "..."}},
    {{"week": 9,  "phase": "90_day", "focus": "...", "goal": "..."}},
    {{"week": 10, "phase": "90_day", "focus": "...", "goal": "..."}},
    {{"week": 11, "phase": "90_day", "focus": "...", "goal": "..."}},
    {{"week": 12, "phase": "90_day", "focus": "...", "goal": "..."}}
  ]
}}
"""


def _format_missing_skills(gap_result: GapAnalysisResult) -> str:
    """Format missing skills list for prompt injection."""
    lines = []
    for skill in gap_result.missing_skills:
        lines.append(
            f"  Rank {skill.priority_rank}: {skill.taxonomy_skill_name} "
            f"({skill.category}) — similarity score: {skill.similarity_score}"
        )
    return "\n".join(lines)


def _format_present_skills(gap_result: GapAnalysisResult) -> str:
    """Format present skills as comma-separated string."""
    return ", ".join(s.taxonomy_skill_name for s in gap_result.present_skills)


def _format_present_skills_short(gap_result: GapAnalysisResult) -> str:
    """Format top 10 present skills for prompt context."""
    top = gap_result.present_skills[:10]
    return ", ".join(s.taxonomy_skill_name for s in top)


def parse_roadmap_response(response_text: str) -> dict:
    """
    Parse LLM response into validated roadmap dict.

    Handles:
    1. Clean JSON response
    2. JSON wrapped in markdown code blocks
    3. Malformed response — raises ValueError
    """
    text = response_text.strip()

    # Strip markdown code blocks
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Roadmap LLM returned invalid JSON: {e}\n"
            f"Raw response (first 500 chars): {response_text[:500]}"
        )

    # Validate required keys
    required_keys = {"phases", "weekly_breakdown"}
    missing_keys = required_keys - set(data.keys())
    if missing_keys:
        raise ValueError(f"Roadmap response missing keys: {missing_keys}")

    # Validate phases
    if not isinstance(data["phases"], list) or len(data["phases"]) != 3:
        raise ValueError(
            f"Expected 3 phases, got {len(data.get('phases', []))}"
        )

    phase_names = {p.get("phase") for p in data["phases"]}
    expected_phases = {"30_day", "60_day", "90_day"}
    if phase_names != expected_phases:
        raise ValueError(f"Expected phases {expected_phases}, got {phase_names}")

    # Validate weekly breakdown
    if not isinstance(data["weekly_breakdown"], list):
        raise ValueError("weekly_breakdown must be a list")

    return data


async def generate_roadmap(
    gap_result: GapAnalysisResult,
    target_role: str | None = None
) -> dict:
    """
    Generate a 30/60/90 day learning roadmap from gap analysis results.

    Args:
        gap_result:  result from analyze_gap()
        target_role: role title string e.g. "Data Scientist"
                     Falls back to gap_result.target_role if not provided

    Returns:
        {
            "phases": [...],           # 30/60/90 day structured plan
            "weekly_breakdown": [...], # flattened 12-week view
            "target_role": str,
            "overall_match_score": float,
            "model_used": str
        }

    Raises:
        ValueError: if LLM returns malformed response after retries
    """
    if not gap_result.missing_skills:
        raise ValueError(
            "No missing skills to generate roadmap from. "
            "Resume already covers the full taxonomy."
        )

    role = target_role or gap_result.target_role or "Software Engineer"
    match_pct = round(gap_result.overall_match_score * 100, 1)

    prompt = ROADMAP_PROMPT.replace("{target_role}", role)
    prompt = prompt.replace("{match_score}", str(match_pct))
    prompt = prompt.replace("{present_skills}", _format_present_skills(gap_result))
    prompt = prompt.replace("{present_skills_short}", _format_present_skills_short(gap_result))
    prompt = prompt.replace("{missing_skills}", _format_missing_skills(gap_result))

    logger.info(f"Generating roadmap for role: '{role}'...")

    # Retry once on parse failure
    last_error = None
    for attempt in range(2):
        try:
            response_text = await call_llm(prompt)
            roadmap = parse_roadmap_response(response_text)
            roadmap["model_used"] = settings.GROQ_MODEL

            logger.info(
                f"Roadmap generated — "
                f"phases: {len(roadmap['phases'])}, "
                f"weeks: {len(roadmap['weekly_breakdown'])}"
            )
            return roadmap

        except ValueError as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            continue

    raise ValueError(f"Roadmap generation failed after 2 attempts: {last_error}")