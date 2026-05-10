"""
Scrape job postings from Adzuna API and build skill taxonomy.

Run this to replace the manual taxonomy with market-derived skills:
    python scripts/scrape_taxonomy.py

What it does:
1. Fetches 50 job postings per role from Adzuna
2. Extracts skills from each JD using Groq LLM
3. Counts skill frequency across all postings
4. Normalizes and deduplicates skills
5. Rebuilds skill_taxonomy.json from scraped data
6. Regenerates embeddings and reseeds database

Adzuna free tier: 1000 requests/month
50 posts x 15 roles = 750 requests total
"""
import asyncio
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from groq import AsyncGroq
client = AsyncGroq(api_key=settings.GROQ_API_KEY)
from app.config import settings
from app.db.session import init_db, AsyncSessionLocal
from app.models.db_models import TaxonomySkill
from app.utils.embedding_utils import embed_skills, save_embeddings, save_skill_ids
from app.utils.llm_client import call_llm
from sqlalchemy import delete


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ROLES_TO_SCRAPE = [
    "Data Scientist",
    "Machine Learning Engineer",
    "Data Analyst",
    "Data Engineer",
    "Backend Engineer",
    "Full Stack Engineer",
    "Frontend Engineer",
    "DevOps Engineer",
    "Cloud Engineer",
    "Software Engineer",
    "AI Engineer",
    "MLOps Engineer",
    "Database Administrator",
    "Cybersecurity Engineer",
    "Site Reliability Engineer",
]

POSTS_PER_ROLE  = 50
ADZUNA_COUNTRY  = "in"          # India
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
RESULTS_PER_PAGE = 50           # Adzuna max per page

TAXONOMY_PATH    = Path("data/taxonomy/skill_taxonomy.json")
EMBEDDINGS_PATH  = "data/taxonomy/embeddings.npy"
SKILL_IDS_PATH   = "data/taxonomy/skill_ids.json"
RAW_JDS_PATH     = Path("data/taxonomy/raw_job_descriptions")

# Minimum frequency for a skill to enter the taxonomy
MIN_FREQUENCY = 3

SKILL_EXTRACTION_PROMPT = """
You are an expert technical recruiter.

Extract ALL skills from this job description and return them as JSON.

DEFINITIONS:
- technical_skills: Programming languages, frameworks, algorithms, ML concepts, engineering practices
- tools: Software tools, platforms, cloud services, databases, DevOps tools
- soft_skills: Communication, leadership, teamwork, problem-solving

RULES:
1. Extract ONLY skills explicitly mentioned in the job description
2. Normalize skill names (e.g. "python" -> "Python", "ml" -> "Machine Learning")
3. Remove duplicates
4. Maximum 4 words per skill
5. Return ONLY JSON, no markdown, no explanation

OUTPUT FORMAT:
{
  "technical_skills": ["skill1", "skill2"],
  "tools": ["tool1", "tool2"],
  "soft_skills": ["skill1", "skill2"]
}

JOB DESCRIPTION:
{jd_text}
"""


# ─────────────────────────────────────────────
# STEP 1: FETCH JOB POSTINGS
# ─────────────────────────────────────────────
async def fetch_jobs_for_role(
    client: httpx.AsyncClient,
    role: str,
    num_posts: int = POSTS_PER_ROLE
) -> list[dict]:
    """
    Fetch job postings for a given role from Adzuna API.
    Returns list of job dicts with title and description.
    """
    jobs = []
    pages_needed = (num_posts + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    for page in range(1, pages_needed + 1):
        url = f"{ADZUNA_BASE_URL}/{ADZUNA_COUNTRY}/search/{page}"
        params = {
            "app_id":         settings.ADZUNA_APP_ID,
            "app_key":        settings.ADZUNA_APP_KEY,
            "what":           role,
            "results_per_page": RESULTS_PER_PAGE,
            "content-type":   "application/json",
        }

        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                print(f"    No results on page {page} for '{role}'")
                break

            for job in results:
                description = job.get("description", "").strip()
                title = job.get("title", "").strip()
                if description and len(description) > 100:
                    jobs.append({
                        "title":       title,
                        "description": description,
                        "role":        role,
                    })

            print(f"    Page {page}: fetched {len(results)} postings")

            # Rate limiting — be respectful to Adzuna
            await asyncio.sleep(1.0)

        except httpx.HTTPStatusError as e:
            print(f"    HTTP error for '{role}' page {page}: {e.response.status_code}")
            break
        except Exception as e:
            print(f"    Error fetching '{role}' page {page}: {e}")
            break

    return jobs[:num_posts]


# ─────────────────────────────────────────────
# STEP 2: EXTRACT SKILLS FROM JD
# ─────────────────────────────────────────────
async def extract_skills_from_jd(jd_text: str) -> dict:
    """
    Extract skills from a single job description.
    Uses llama-3.1-8b-instant — separate daily quota from main app model.
    """
    truncated = jd_text[:2000]
    prompt = SKILL_EXTRACTION_PROMPT.replace("{jd_text}", truncated)

    try:
        # Use scraper model directly — bypass call_llm() which uses main model
        response = await client.chat.completions.create(
            model=settings.GROQ_SCRAPER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that returns structured JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=500,   # skills list is short, no need for 2048
        )

        text = response.choices[0].message.content.strip()

        import re
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        data = json.loads(text.strip())
        return {
            "technical_skills": data.get("technical_skills", []),
            "tools":            data.get("tools", []),
            "soft_skills":      data.get("soft_skills", []),
        }

    except Exception as e:
        print(f"      Skill extraction failed: {e}")
        return {"technical_skills": [], "tools": [], "soft_skills": []}

# ─────────────────────────────────────────────
# STEP 4: BUILD TAXONOMY FROM FREQUENCY MAP
# ─────────────────────────────────────────────
def build_taxonomy_from_frequency(
    frequency_map: dict,
    min_frequency: int = MIN_FREQUENCY
) -> dict:
    """
    Filter skills by minimum frequency and organize into taxonomy.

    Returns taxonomy dict:
    {
        "technical_skills": ["Python", "Machine Learning", ...],
        "tools": ["Docker", "Git", ...],
        "soft_skills": ["Communication", ...]
    }
    """
    taxonomy = {
        "technical_skills": [],
        "tools":            [],
        "soft_skills":      [],
    }

    for key, data in frequency_map.items():
        if data["count"] >= min_frequency:
            category = data["category"]
            name = data.get("name", key.title())
            if category in taxonomy:
                taxonomy[category].append(name)

    # Sort each category by name for consistency
    for category in taxonomy:
        taxonomy[category] = sorted(set(taxonomy[category]))

    total = sum(len(v) for v in taxonomy.values())
    print(f"\nTaxonomy built: {total} skills "
          f"(min frequency: {min_frequency})")
    for cat, skills in taxonomy.items():
        print(f"  {cat}: {len(skills)} skills")

    return taxonomy


# ─────────────────────────────────────────────
# STEP 5: SEED DATABASE
# ─────────────────────────────────────────────
async def seed_database(
    taxonomy: dict,
    frequency_map: dict
) -> list[str]:
    """
    Clear and reseed taxonomy_skills table.
    Returns ordered list of skill names.
    """
    async with AsyncSessionLocal() as session:
        await session.execute(delete(TaxonomySkill))
        await session.commit()
        print("\nCleared existing taxonomy from DB.")

        ordered_names = []
        total = 0

        for category, skills in taxonomy.items():
            for skill_name in skills:
                key = skill_name.lower()
                freq = frequency_map.get(key, {}).get("count", 1)

                skill = TaxonomySkill(
                    skill_name=skill_name,
                    normalized_name=key,
                    category=category,
                    frequency_score=freq,
                )
                session.add(skill)
                ordered_names.append(skill_name)
                total += 1

        await session.commit()
        print(f"Seeded {total} skills into taxonomy_skills table.")
        return ordered_names


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    print("=== Scraping Job Postings & Building Taxonomy ===\n")

    if not settings.ADZUNA_APP_ID or not settings.ADZUNA_APP_KEY:
        print("ERROR: ADZUNA_APP_ID and ADZUNA_APP_KEY must be set in .env")
        sys.exit(1)

    # Create raw JDs directory
    RAW_JDS_PATH.mkdir(parents=True, exist_ok=True)

    # Init DB
    print("1. Initializing database...")
    await init_db()
    print("   Done.\n")

    # Fetch all job postings
    print(f"2. Fetching job postings ({POSTS_PER_ROLE} per role)...")
    all_jobs = []

    async with httpx.AsyncClient() as client:
        for role in ROLES_TO_SCRAPE:
            print(f"\n  Fetching: {role}")
            jobs = await fetch_jobs_for_role(client, role)
            all_jobs.extend(jobs)
            print(f"  Total fetched for '{role}': {len(jobs)}")

            # Save raw JDs for reference
            safe_name = role.lower().replace(" ", "_")
            raw_path = RAW_JDS_PATH / f"{safe_name}.json"
            with open(raw_path, "w") as f:
                json.dump(jobs, f, indent=2)

    print(f"\nTotal job postings fetched: {len(all_jobs)}")

    # Extract skills from all JDs
    print(f"\n3. Extracting skills from {len(all_jobs)} job descriptions...")
    print("   (This will take several minutes due to LLM calls + rate limiting)\n")

    all_extractions = []
    failed = 0

    for idx, job in enumerate(all_jobs):
        if idx % 10 == 0:
            print(f"   Progress: {idx}/{len(all_jobs)}")

        extraction = await extract_skills_from_jd(job["description"])
        extraction["role"] = job["role"]
        all_extractions.append(extraction)

        # Rate limit — Groq free tier allows ~30 requests/minute
        await asyncio.sleep(0.5)

    print(f"\n   Extractions complete. Failed: {failed}")

    # Save extractions for debugging
    extractions_path = Path("data/taxonomy/extractions.json")
    with open(extractions_path, "w") as f:
        json.dump(all_extractions, f, indent=2)
    print(f"   Saved extractions → {extractions_path}")

    # Build frequency map
    print("\n4. Building frequency map...")
    frequency_map = build_frequency_map(all_extractions)
    print(f"   Unique skills found: {len(frequency_map)}")

    # Save frequency map for inspection
    freq_path = Path("data/taxonomy/frequency_map.json")
    sorted_freq = dict(
        sorted(frequency_map.items(), key=lambda x: x[1]["count"], reverse=True)
    )
    with open(freq_path, "w") as f:
        json.dump(sorted_freq, f, indent=2)
    print(f"   Saved frequency map → {freq_path}")

    # Build taxonomy
    print("\n5. Building taxonomy from frequency data...")
    taxonomy = build_taxonomy_from_frequency(frequency_map, MIN_FREQUENCY)

    # Save taxonomy JSON
    with open(TAXONOMY_PATH, "w") as f:
        json.dump(taxonomy, f, indent=2)
    print(f"   Saved taxonomy → {TAXONOMY_PATH}")

    # Seed database
    print("\n6. Seeding database...")
    ordered_names = await seed_database(taxonomy, frequency_map)

    # Generate embeddings
    print("\n7. Generating embeddings...")
    embeddings = embed_skills(ordered_names)
    print(f"   Embeddings shape: {embeddings.shape}")

    # Save embeddings
    save_embeddings(embeddings, EMBEDDINGS_PATH)
    save_skill_ids(ordered_names, SKILL_IDS_PATH)

    print("\n=== Scraping Complete ===")
    print(f"   Total jobs scraped:  {len(all_jobs)}")
    print(f"   Total extractions:   {len(all_extractions)}")
    print(f"   Unique skills found: {len(frequency_map)}")
    print(f"   Taxonomy size:       {len(ordered_names)}")
    print(f"   Embeddings:          {EMBEDDINGS_PATH}")
    print(f"   Raw JDs:             {RAW_JDS_PATH}/")


if __name__ == "__main__":
    asyncio.run(main())