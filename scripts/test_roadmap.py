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

    print('=== WEEKLY BREAKDOWN ===')
    for week in roadmap['weekly_breakdown']:
        print(f"Week {week['week']} [{week['phase']}]: {week['focus']}")
        print(f"  Goal: {week['goal']}")
        print()

    print(f"Model: {roadmap['model_used']}")


asyncio.run(test())