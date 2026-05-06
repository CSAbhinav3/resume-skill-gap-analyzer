import json
import logging
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)

# Module-level model — loaded once, reused across all calls
_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """
    Returns the embedding model, loading it on first call.
    Subsequent calls return the cached instance.
    """
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding model loaded.")
    return _model


def embed_skills(skills: list[str]) -> np.ndarray:
    """
    Generate embeddings for a list of skill strings.

    Args:
        skills: list of skill name strings

    Returns:
        numpy array of shape (len(skills), embedding_dim)
        embedding_dim = 384 for all-MiniLM-L6-v2
    """
    if not skills:
        raise ValueError("Cannot embed empty skill list.")

    model = get_embedding_model()
    embeddings = model.encode(skills, show_progress_bar=False, normalize_embeddings=True)
    return np.array(embeddings, dtype=np.float32)


def save_embeddings(embeddings: np.ndarray, path: str) -> None:
    """Save embeddings array to .npy file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.save(path, embeddings)
    logger.info(f"Saved embeddings: shape={embeddings.shape} → {path}")


def load_embeddings(path: str) -> np.ndarray:
    """Load embeddings array from .npy file."""
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Embeddings file not found at {path}. "
            f"Run scripts/build_taxonomy.py first."
        )
    embeddings = np.load(path)
    logger.info(f"Loaded embeddings: shape={embeddings.shape} ← {path}")
    return embeddings


def save_skill_ids(skill_ids: list[str], path: str) -> None:
    """Save ordered list of taxonomy skill IDs to JSON."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(skill_ids, f, indent=2)
    logger.info(f"Saved {len(skill_ids)} skill IDs → {path}")


def load_skill_ids(path: str) -> list[str]:
    """Load ordered list of taxonomy skill IDs from JSON."""
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Skill IDs file not found at {path}. "
            f"Run scripts/build_taxonomy.py first."
        )
    with open(path) as f:
        return json.load(f)