"""
Build taxonomy embeddings and seed the database.

Run this once before starting the app:
    python scripts/build_taxonomy.py

What it does:
1. Loads skill_taxonomy.json
2. Generates sentence-transformer embeddings for all skills
3. Saves embeddings.npy and skill_ids.json to data/taxonomy/
4. Seeds taxonomy_skills table in the database
"""
import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.embedding_utils import embed_skills, save_embeddings, save_skill_ids
from app.db.session import init_db, AsyncSessionLocal
from app.models.db_models import TaxonomySkill
from sqlalchemy import select, delete


TAXONOMY_PATH = Path("data/taxonomy/skill_taxonomy.json")
EMBEDDINGS_PATH = "data/taxonomy/embeddings.npy"
SKILL_IDS_PATH = "data/taxonomy/skill_ids.json"


def load_taxonomy() -> dict:
    with open(TAXONOMY_PATH) as f:
        return json.load(f)


async def seed_database(taxonomy: dict) -> list[str]:
    """
    Insert all taxonomy skills into DB.
    Clears existing taxonomy first to avoid duplicates on re-run.
    Returns ordered list of skill names matching embedding order.
    """
    async with AsyncSessionLocal() as session:
        # Clear existing taxonomy
        await session.execute(delete(TaxonomySkill))
        await session.commit()
        print("Cleared existing taxonomy from DB.")

        ordered_names = []
        total = 0

        for category, skills in taxonomy.items():
            # Count frequency — all start at 1 (from taxonomy definition)
            # In production you'd derive this from real JD analysis
            for skill_name in skills:
                normalized = skill_name.lower().strip()
                skill = TaxonomySkill(
                    skill_name=skill_name,
                    normalized_name=normalized,
                    category=category,
                    frequency_score=1,
                )
                session.add(skill)
                ordered_names.append(skill_name)
                total += 1

        await session.commit()
        print(f"Seeded {total} skills into taxonomy_skills table.")
        return ordered_names


async def main():
    print("=== Building Taxonomy ===\n")

    # Step 1: Init DB
    print("1. Initializing database...")
    await init_db()
    print("   DB tables created.\n")

    # Step 2: Load taxonomy
    print("2. Loading taxonomy JSON...")
    taxonomy = load_taxonomy()
    total_skills = sum(len(v) for v in taxonomy.values())
    print(f"   Loaded {total_skills} skills across {len(taxonomy)} categories.\n")

    # Step 3: Seed DB
    print("3. Seeding database...")
    ordered_names = await seed_database(taxonomy)
    print()

    # Step 4: Generate embeddings
    print("4. Generating embeddings (this may take 30-60 seconds)...")
    embeddings = embed_skills(ordered_names)
    print(f"   Generated embeddings: shape={embeddings.shape}\n")

    # Step 5: Save to disk
    print("5. Saving embeddings to disk...")
    save_embeddings(embeddings, EMBEDDINGS_PATH)
    save_skill_ids(ordered_names, SKILL_IDS_PATH)
    print()

    print("=== Taxonomy Build Complete ===")
    print(f"   Skills: {len(ordered_names)}")
    print(f"   Embeddings: {EMBEDDINGS_PATH}")
    print(f"   Skill IDs: {SKILL_IDS_PATH}")
    print(f"   Database: dev.db")


if __name__ == "__main__":
    asyncio.run(main())