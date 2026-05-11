import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.pdf_ingestion import ingest_pdf
from app.services.skill_extractor import extract_skills
from app.services.taxonomy_engine import taxonomy_index
from app.services.gap_analyzer import analyze_gap
from app.services.roadmap_generator import generate_roadmap


async def test():
    taxonomy_index.load()

    with open('data/sample_resumes/test.pdf', 'rb') as f:
        ingested = ingest_pdf(f.read())

    skills = await extract_skills(ingested['clean_text'])
    all_skills = skills['technical_skills'] + skills['tools'] + skills['soft_skills']

    gap_result = analyze_gap(all_skills, target_role='Data Scientist')

    print(f'Generating roadmap for Data Scientist...')
    print(f'Missing skills: {[s.taxonomy_skill_name for s in gap_result.missing_skills]}')
    print()

    roadmap = await generate_roadmap(gap_result, target_role='Data Scientist')

    print('=== FULL ROADMAP WITH RESOURCES ===')
    for phase in roadmap['phases']:
        print(f"\n{'='*60}")
        print(f"PHASE: {phase['phase'].upper()} — {phase['goal']}")
        print(f"{'='*60}")
        for week in phase['weeks']:
            print(f"\nWeek {week['week']}: {week['focus']}")
            print(f"  Goal: {week['goal']}")
            print(f"  Topics:")
            for t in week.get('topics', []):
                print(f"    - {t}")
            print(f"  Resources:")
            for r in week.get('resources', []):
                print(f"    * {r}")

    print(f"\nModel: {roadmap['model_used']}")


asyncio.run(test())