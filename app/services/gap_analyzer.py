import logging
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.services.taxonomy_engine import taxonomy_index
from app.utils.embedding_utils import embed_skills

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


def _filter_taxonomy_by_role(target_role: str) -> tuple[list[str], list[str], np.ndarray]:
    """
    Semantically filter taxonomy skills relevant to a target role.

    Algorithm:
    1. Embed the target role title
    2. Compute cosine similarity between role embedding and
       every taxonomy skill embedding
    3. Keep skills above ROLE_RELEVANCE_THRESHOLD

    Args:
        target_role: role title string e.g. "Data Scientist"

    Returns:
        tuple of (filtered_names, filtered_categories, filtered_embeddings)
    """
    logger.info(f"Filtering taxonomy for role: '{target_role}'")

    # Embed the role title
    role_embedding = embed_skills([target_role])  # shape (1, 384)

    # Compute similarity between role and every taxonomy skill
    role_similarities = cosine_similarity(
        role_embedding,
        taxonomy_index.embeddings
    )[0]  # shape (n_taxonomy,)

    # Filter skills above relevance threshold
    filtered_names = []
    filtered_categories = []
    filtered_indices = []

    for idx, (name, category, sim) in enumerate(zip(
        taxonomy_index.skill_names,
        taxonomy_index.categories,
        role_similarities
    )):
        if sim >= ROLE_RELEVANCE_THRESHOLD:
            filtered_names.append(name)
            filtered_categories.append(category)
            filtered_indices.append(idx)

    if not filtered_names:
        logger.warning(
            f"No taxonomy skills matched role '{target_role}' "
            f"at threshold {ROLE_RELEVANCE_THRESHOLD}. "
            f"Falling back to full taxonomy."
        )
        return (
            taxonomy_index.skill_names,
            taxonomy_index.categories,
            taxonomy_index.embeddings
        )

    filtered_embeddings = taxonomy_index.embeddings[filtered_indices]

    logger.info(
        f"Role filter: {len(filtered_names)}/{len(taxonomy_index.skill_names)} "
        f"skills relevant to '{target_role}'"
    )

    return filtered_names, filtered_categories, filtered_embeddings


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
        tax_names, tax_categories, tax_embeddings = _filter_taxonomy_by_role(
            target_role.strip()
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

    # Step 2: Embed resume skills
    resume_embeddings = embed_skills(unique_resume_skills)  # shape (n_resume, 384)

    # Step 3: Compare each taxonomy skill against all resume skills
    matches: list[SkillMatch] = []
    threshold = settings.SIMILARITY_THRESHOLD

    for idx, (tax_name, category) in enumerate(zip(tax_names, tax_categories)):
        tax_embedding = tax_embeddings[idx].reshape(1, -1)
        max_sim = _get_max_similarity(resume_embeddings, tax_embedding)

        is_missing = max_sim < threshold
        matches.append(SkillMatch(
            taxonomy_skill_name=tax_name,
            category=category,
            similarity_score=round(max_sim, 4),
            is_missing=is_missing,
            priority_rank=0,
        ))

    # Step 4: Split into present and missing
    present = [m for m in matches if not m.is_missing]
    missing = [m for m in matches if m.is_missing]

    # Step 5: Rank missing skills
    # Filter out completely irrelevant skills (score below 0.20)
    missing = [m for m in missing if m.similarity_score >= 0.20]

    # Sort descending — highest score = most achievable gap = rank 1
    missing.sort(key=lambda m: m.similarity_score, reverse=True)

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