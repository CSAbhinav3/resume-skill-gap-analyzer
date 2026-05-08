import logging
import uuid
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.services.taxonomy_engine import taxonomy_index
from app.utils.embedding_utils import embed_skills

logger = logging.getLogger(__name__)


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
    missing_skills:      list[SkillMatch]
    present_skills:      list[SkillMatch]
    overall_match_score: float
    total_taxonomy_size: int
    total_resume_skills: int


def _get_max_similarity(
    resume_embeddings: np.ndarray,
    taxonomy_embedding: np.ndarray
) -> float:
    """
    For a single taxonomy skill embedding, compute the maximum
    cosine similarity against all resume skill embeddings.

    This handles the case where a resume skill is phrased differently
    from the taxonomy skill but means the same thing.
    e.g. "ML" in resume vs "Machine Learning" in taxonomy → high similarity

    Args:
        resume_embeddings: shape (n_resume_skills, 384)
        taxonomy_embedding: shape (1, 384)

    Returns:
        float: maximum similarity score 0.0 – 1.0
    """
    similarities = cosine_similarity(taxonomy_embedding, resume_embeddings)
    return float(np.max(similarities))


def analyze_gap(resume_skills: list[str]) -> GapAnalysisResult:
    """
    Core gap analysis function.

    Algorithm:
    1. Embed all resume skills into vector space
    2. For each taxonomy skill, compute max cosine similarity
       against all resume skill embeddings
    3. Skills above SIMILARITY_THRESHOLD → present
    4. Skills below threshold → missing, ranked by similarity score
       (lowest score = biggest gap = highest priority)

    Args:
        resume_skills: flat list of skills from skill extraction
                      (all_skills_flat property on SkillExtraction)

    Returns:
        GapAnalysisResult with missing/present skills and match score
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

    logger.info(
        f"Analyzing gap — resume skills: {len(unique_resume_skills)}, "
        f"taxonomy size: {len(taxonomy_index.skill_names)}"
    )

    # Step 1: Embed resume skills
    resume_embeddings = embed_skills(unique_resume_skills)  # shape (n_resume, 384)

    # Step 2: Compare each taxonomy skill against all resume skills
    matches: list[SkillMatch] = []
    threshold = settings.SIMILARITY_THRESHOLD

    for idx, (tax_name, category) in enumerate(
        zip(taxonomy_index.skill_names, taxonomy_index.categories)
    ):
        tax_embedding = taxonomy_index.embeddings[idx].reshape(1, -1)  # shape (1, 384)
        max_sim = _get_max_similarity(resume_embeddings, tax_embedding)

        is_missing = max_sim < threshold
        matches.append(SkillMatch(
            taxonomy_skill_name=tax_name,
            category=category,
            similarity_score=round(max_sim, 4),
            is_missing=is_missing,
            priority_rank=0,  # assigned below
        ))

    # Step 3: Split into present and missing
    present = [m for m in matches if not m.is_missing]
    missing = [m for m in matches if m.is_missing]

    # Step 4: Rank missing skills
    # Filter out completely irrelevant skills (score below 0.20)
    # These are skills with zero semantic relation to the resume
    missing = [m for m in missing if m.similarity_score >= 0.20]

    # Sort by similarity score DESCENDING — highest score among missing
    # = closest to threshold = most achievable gap to close
    missing.sort(key=lambda m: m.similarity_score, reverse=True)

    # Cap at MAX_MISSING_SKILLS
    missing = missing[:settings.MAX_MISSING_SKILLS]
    # Assign priority ranks
    for rank, skill in enumerate(missing, start=1):
        skill.priority_rank = rank

    # Step 5: Compute overall match score
    # = number of present skills / total taxonomy size
    overall_match_score = round(len(present) / len(taxonomy_index.skill_names), 4)

    logger.info(
        f"Gap analysis complete — "
        f"present: {len(present)}, "
        f"missing: {len(missing)}, "
        f"match_score: {overall_match_score:.2%}"
    )

    return GapAnalysisResult(
        missing_skills=missing,
        present_skills=present,
        overall_match_score=overall_match_score,
        total_taxonomy_size=len(taxonomy_index.skill_names),
        total_resume_skills=len(unique_resume_skills),
    )