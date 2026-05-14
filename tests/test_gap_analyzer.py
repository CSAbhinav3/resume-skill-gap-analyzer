import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from app.services.gap_analyzer import analyze_gap, GapAnalysisResult
from app.services.taxonomy_engine import TaxonomyIndex


@pytest.fixture
def mock_taxonomy():
    """Create a minimal mock taxonomy for testing."""
    idx = TaxonomyIndex()
    idx.skill_names  = ["Python", "Machine Learning", "Docker", "Communication"]
    idx.categories   = ["technical_skills", "technical_skills", "tools", "soft_skills"]
    idx.embeddings   = np.random.rand(4, 384).astype(np.float32)
    idx._loaded      = True
    return idx


def test_analyze_gap_returns_result(mock_taxonomy):
    with patch("app.services.gap_analyzer.taxonomy_index", mock_taxonomy), \
         patch("app.services.gap_analyzer.embed_skills") as mock_embed:
        mock_embed.return_value = np.random.rand(2, 384).astype(np.float32)
        result = analyze_gap(["Python", "FastAPI"])
        assert isinstance(result, GapAnalysisResult)
        assert result.total_taxonomy_size == 4
        assert result.total_resume_skills == 2


def test_analyze_gap_empty_skills_raises(mock_taxonomy):
    with patch("app.services.gap_analyzer.taxonomy_index", mock_taxonomy):
        with pytest.raises(ValueError, match="empty"):
            analyze_gap([])


def test_analyze_gap_deduplicates_skills(mock_taxonomy):
    with patch("app.services.gap_analyzer.taxonomy_index", mock_taxonomy), \
         patch("app.services.gap_analyzer.embed_skills") as mock_embed:
        mock_embed.return_value = np.random.rand(1, 384).astype(np.float32)
        result = analyze_gap(["Python", "python", "PYTHON"])
        assert result.total_resume_skills == 1


def test_analyze_gap_not_loaded_raises():
    empty_idx = TaxonomyIndex()
    with patch("app.services.gap_analyzer.taxonomy_index", empty_idx):
        with pytest.raises(RuntimeError, match="not loaded"):
            analyze_gap(["Python"])


def test_match_score_between_0_and_1(mock_taxonomy):
    with patch("app.services.gap_analyzer.taxonomy_index", mock_taxonomy), \
         patch("app.services.gap_analyzer.embed_skills") as mock_embed:
        mock_embed.return_value = np.random.rand(1, 384).astype(np.float32)
        result = analyze_gap(["Python"])
        assert 0.0 <= result.overall_match_score <= 1.0