import json
import logging
from pathlib import Path

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.db_models import TaxonomySkill
from app.utils.embedding_utils import (
    embed_skills,
    load_embeddings,
    load_skill_ids,
)

logger = logging.getLogger(__name__)


def normalize_skill_name(name: str) -> str:
    """Lowercase, strip whitespace. Used for matching."""
    return name.lower().strip()


def load_taxonomy_json() -> dict:
    """
    Load skill taxonomy from JSON file.
    Returns dict with technical_skills, tools, soft_skills keys.
    """
    taxonomy_path = Path("data/taxonomy/skill_taxonomy.json")
    if not taxonomy_path.exists():
        raise FileNotFoundError(
            f"Taxonomy file not found at {taxonomy_path}. "
            f"Create data/taxonomy/skill_taxonomy.json first."
        )
    with open(taxonomy_path) as f:
        return json.load(f)


class TaxonomyIndex:
    """
    In-memory taxonomy index.
    Loaded once at app startup, reused for all gap analyses.

    Attributes:
        skill_names:    ordered list of all skill name strings
        skill_ids:      ordered list of taxonomy_skill DB IDs
        categories:     ordered list of category strings
        embeddings:     numpy array of shape (n_skills, 384)
    """

    def __init__(self):
        self.skill_names: list[str] = []
        self.skill_ids: list[str] = []
        self.categories: list[str] = []
        self.embeddings: np.ndarray | None = None
        self._loaded = False

    def load(self) -> None:
        """
        Load taxonomy embeddings and skill IDs from disk.
        Call once at app startup via lifespan event.
        """
        if self._loaded:
            return

        logger.info("Loading taxonomy index from disk...")

        self.skill_ids = load_skill_ids(settings.TAXONOMY_IDS_PATH)
        self.embeddings = load_embeddings(settings.TAXONOMY_EMB_PATH)

        # Load skill metadata from taxonomy JSON for names + categories
        taxonomy = load_taxonomy_json()
        all_skills = []
        for category, skills in taxonomy.items():
            for skill in skills:
                all_skills.append({
                    "name": skill,
                    "category": category
                })

        # Build ordered lists matching skill_ids order
        skill_map = {s["name"]: s for s in all_skills}

        # skill_ids file stores skill names (not DB UUIDs) for simplicity
        self.skill_names = self.skill_ids  # skill_ids.json stores names
        self.categories = [
            skill_map.get(name, {}).get("category", "unknown")
            for name in self.skill_names
        ]

        self._loaded = True
        logger.info(
            f"Taxonomy index loaded — "
            f"{len(self.skill_names)} skills, "
            f"embeddings shape: {self.embeddings.shape}"
        )

    def is_loaded(self) -> bool:
        return self._loaded


# Global singleton — imported and used by gap_analyzer
taxonomy_index = TaxonomyIndex()