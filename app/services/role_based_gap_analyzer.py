import logging
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.services.taxonomy_engine import taxonomy_index
from app.utils.embedding_utils import embed_skills
from app.data.role_skill_map import ROLE_SKILL_MAP
from app.data.skill_aliases import SKILL_ALIASES

logger = logging.getLogger(__name__)


# Minimum similarity between role title and taxonomy skill
# to consider that skill relevant to the role
ROLE_RELEVANCE_THRESHOLD = 0.30


@dataclass
class SkillMatch:
    """Represents a single skill comparison result."""
    taxonomy_skill_name: str
    category:            str
    similarity_score:    float
    is_missing:          bool
    priority_rank:       int   # 0 = present, 1+ = ranked gap


@dataclass
class GapAnalysisResult:
    """Full result of a gap analysis."""
    missing_skills:       list[SkillMatch]
    present_skills:       list[SkillMatch]
    overall_match_score:  float
    total_taxonomy_size:  int
    filtered_taxonomy_size: int   # size after role filtering (= total if no role)
    total_resume_skills:  int
    target_role:          str | None


def _get_max_similarity(
    resume_embeddings: np.ndarray,
    taxonomy_embedding: np.ndarray
) -> float:
    """
    For a single taxonomy skill, compute max cosine similarity
    against all resume skill embeddings.

    Handles phrasing differences:
    e.g. "ML" in resume vs "Machine Learning" in taxonomy → high similarity
    """
    similarities = cosine_similarity(taxonomy_embedding, resume_embeddings)
    return float(np.max(similarities))


def _filter_taxonomy_by_role(
    target_role: str
) -> tuple[list[str], list[str], np.ndarray, dict]:
    """
    Filter taxonomy using curated role skill map instead of
    semantic role embeddings.

    Prevents semantic drift by restricting comparison
    to role-specific required skills only.
    """

    logger.info(f"Applying role-based filtering for: '{target_role}'")

    # ------------------------------------------------------------
    # Normalize role input
    # ------------------------------------------------------------
    normalized_role = target_role.lower().strip()

    normalized_role_map = {
        role.lower().strip(): skills
        for role, skills in ROLE_SKILL_MAP.items()
    }

    # ------------------------------------------------------------
    # Fallback if role not found
    # ------------------------------------------------------------
    if normalized_role not in normalized_role_map:

        logger.warning(
            f"Role '{target_role}' not found in ROLE_SKILL_MAP. "
            f"Using full taxonomy."
        )

        return (
            taxonomy_index.skill_names,
            taxonomy_index.categories,
            taxonomy_index.embeddings,
            {}
        )

    role_skill_weights = normalized_role_map[normalized_role]

    filtered_names = []
    filtered_categories = []
    filtered_indices = []

    # ------------------------------------------------------------
    # Keep ONLY skills relevant to this role
    # ------------------------------------------------------------
    for idx, (name, category) in enumerate(
        zip(
            taxonomy_index.skill_names,
            taxonomy_index.categories
        )
    ):

        if name in role_skill_weights:
            filtered_names.append(name)
            filtered_categories.append(category)
            filtered_indices.append(idx)

    # ------------------------------------------------------------
    # Safety fallback
    # ------------------------------------------------------------
    if not filtered_names:

        logger.warning(
            f"No taxonomy skills matched curated role map for "
            f"'{target_role}'. Using full taxonomy."
        )

        return (
            taxonomy_index.skill_names,
            taxonomy_index.categories,
            taxonomy_index.embeddings,
            {}
        )

    print("\n======================")
    print("ROLE:", target_role)

    print("\nROLE MAP SKILLS:")
    for skill in role_skill_weights.keys():
        print(skill)

    print("\nMATCHED SKILLS:")
    for skill in filtered_names:
        print(skill)

    print("\nMISSING FROM TAXONOMY:")

    normalized_taxonomy = {
        s.lower().strip()
        for s in taxonomy_index.skill_names
    }

    for skill in role_skill_weights.keys():

        if skill.lower().strip() not in normalized_taxonomy:
            print(skill)

    print("======================\n")
    filtered_embeddings = taxonomy_index.embeddings[filtered_indices]

    logger.info(
        f"Role filter applied: "
        f"{len(filtered_names)}/{len(taxonomy_index.skill_names)} "
        f"skills retained for '{target_role}'"
    )

    return (
        filtered_names,
        filtered_categories,
        filtered_embeddings,
        role_skill_weights
    )

def normalize_skill(skill: str) -> str:
    """
    Normalize skill names using aliases and formatting cleanup.
    """

    normalized = skill.lower().strip()

    if normalized in SKILL_ALIASES:
        return SKILL_ALIASES[normalized]

    return skill.strip()

def analyze_gap(
    resume_skills: list[str],
    target_role: str | None = None
) -> GapAnalysisResult:
    """
    Core gap analysis function.

    Algorithm:
    1. If target_role provided — filter taxonomy semantically to
       role-relevant skills only (Option B: semantic role filtering)
    2. Embed all resume skills
    3. For each (filtered) taxonomy skill, compute max cosine similarity
       against all resume embeddings
    4. Skills above SIMILARITY_THRESHOLD → present
    5. Skills below threshold → missing, ranked by similarity descending
       (highest score = closest to threshold = most achievable gap)

    Args:
        resume_skills: flat list of skills from skill extraction
        target_role:   optional role title e.g. "Data Scientist"
                       If None, uses full taxonomy (no role filtering)

    Returns:
        GapAnalysisResult with missing/present skills and scores
    """
    if not taxonomy_index.is_loaded():
        raise RuntimeError(
            "Taxonomy index not loaded. "
            "Call taxonomy_index.load() at app startup."
        )

    if not resume_skills:
        raise ValueError("Resume skills list is empty.")

    # Deduplicate resume skills (case-insensitive)
    seen = set()
    unique_resume_skills = []
    for skill in resume_skills:
        normalized = skill.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique_resume_skills.append(skill)

    # Step 1: Get taxonomy to compare against
    if target_role and target_role.strip():
        tax_names, tax_categories, tax_embeddings, role_skill_weights = (
    _filter_taxonomy_by_role(target_role.strip())
    )
    else:
        tax_names      = taxonomy_index.skill_names
        tax_categories = taxonomy_index.categories
        tax_embeddings = taxonomy_index.embeddings

    logger.info(
        f"Analyzing gap — resume skills: {len(unique_resume_skills)}, "
        f"taxonomy size: {len(tax_names)}, "
        f"role: {target_role or 'none (full taxonomy)'}"
    )
    normalized_resume_skills = set()

    for skill in unique_resume_skills:

        normalized = normalize_skill(skill)

        normalized_resume_skills.add(
            normalized.lower().strip()
        )

    matches: list[SkillMatch] = []

    # Step 3: Direct role-skill matching
    for tax_name, category in zip(tax_names, tax_categories):

        normalized_tax_skill = normalize_skill(tax_name).lower().strip()

        is_present = normalized_tax_skill in normalized_resume_skills

        weight = role_skill_weights.get(tax_name, 0.5)

        matches.append(
            SkillMatch(
                taxonomy_skill_name=tax_name,
                category=category,
                similarity_score=round(weight, 4),
                is_missing=not is_present,
                priority_rank=0,
            )
        )
    # Step 4: Split into present and missing
    present = [m for m in matches if not m.is_missing]
    missing = [m for m in matches if m.is_missing]

    # Step 5: Rank missing skills
    # Sort by role importance weight
    missing.sort(
        key=lambda m: m.similarity_score,
        reverse=True
    )

    # Cap at MAX_MISSING_SKILLS
    missing = missing[:settings.MAX_MISSING_SKILLS]

    # Assign priority ranks
    for rank, skill in enumerate(missing, start=1):
        skill.priority_rank = rank

    # Step 6: Compute overall match score
    overall_match_score = round(len(present) / len(tax_names), 4)

    logger.info(
        f"Gap analysis complete — "
        f"present: {len(present)}, "
        f"missing: {len(missing)}, "
        f"match_score: {overall_match_score:.2%}, "
        f"role: {target_role or 'none'}"
    )

    return GapAnalysisResult(
        missing_skills=missing,
        present_skills=present,
        overall_match_score=overall_match_score,
        total_taxonomy_size=len(taxonomy_index.skill_names),
        filtered_taxonomy_size=len(tax_names),
        total_resume_skills=len(unique_resume_skills),
        target_role=target_role,
    )