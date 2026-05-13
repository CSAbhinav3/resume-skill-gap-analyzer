from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.services.taxonomy_engine import taxonomy_index
from app.api.routes import resume, skills, roadmap
from app.config import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    Runs once when the server starts — not per request.
    """
    # ── STARTUP ──
    logger.info("Starting Resume Skill Gap Analyzer API...")

    # Init database — creates tables if they don't exist
    logger.info("Initialising database...")
    await init_db()
    logger.info("Database ready.")

    # Load taxonomy index into memory
    # This loads embeddings.npy + skill_ids.json once
    # All gap analysis requests use this in-memory index
    logger.info("Loading taxonomy index...")
    taxonomy_index.load()
    logger.info(
        f"Taxonomy index loaded — "
        f"{len(taxonomy_index.skill_names)} skills, "
        f"embeddings shape: {taxonomy_index.embeddings.shape}"
    )

    logger.info("API ready.")
    yield

    # ── SHUTDOWN ──
    logger.info("Shutting down...")


app = FastAPI(
    title="Resume Skill Gap Analyzer",
    description="""
## Resume Skill Gap Analyzer with Roadmap Generator

An end-to-end AI/ML system that:
1. **Ingests** a PDF resume and extracts clean text
2. **Extracts** skills using Groq LLM (llama-3.3-70b-versatile)
3. **Analyzes** skill gaps against a 217-skill market-derived taxonomy using cosine similarity
4. **Generates** a personalised 30/60/90-day learning roadmap with verified resource links

### Usage Flow
1. `POST /resume/upload` — upload your PDF resume → get `resume_id`
2. `POST /skills/analyze` — analyze skills and gaps → get `analysis_id`
3. `POST /roadmap/generate` — generate learning roadmap → get 12-week plan

### Role-Based Filtering
Pass `target_role` (e.g. `"Data Scientist"`, `"ML Engineer"`) to get role-specific gap analysis.
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for development
# Restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(resume.router)
app.include_router(skills.router)
app.include_router(roadmap.router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Resume Skill Gap Analyzer",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "taxonomy_loaded": taxonomy_index.is_loaded(),
        "taxonomy_size": len(taxonomy_index.skill_names) if taxonomy_index.is_loaded() else 0,
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "taxonomy_loaded": taxonomy_index.is_loaded(),
        "database": "connected",
    }