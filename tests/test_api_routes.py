import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app


@pytest.fixture(autouse=True)
def mock_taxonomy():
    """Mock taxonomy index for all API tests."""
    with patch("app.services.taxonomy_engine.taxonomy_index") as mock:
        mock.is_loaded.return_value = True
        mock.skill_names = ["Python", "Machine Learning", "Docker"]
        mock.categories  = ["technical_skills", "technical_skills", "tools"]
        import numpy as np
        mock.embeddings  = np.random.rand(3, 384).astype(np.float32)
        yield mock


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Resume Skill Gap Analyzer"


@pytest.mark.asyncio
async def test_upload_non_pdf_rejected():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/resume/upload",
            files={"file": ("test.txt", b"some text content", "text/plain")}
        )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_skills_resume_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/skills/analyze",
            json={"resume_id": "nonexistent-id", "target_role": "Data Scientist"}
        )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_roadmap_no_gap_analysis_returns_404():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/roadmap/generate",
            json={"resume_id": "nonexistent-id", "target_role": "Data Scientist"}
        )
    assert response.status_code == 404