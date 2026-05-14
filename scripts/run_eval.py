"""
Evaluation script — tests the full pipeline on multiple resumes.

Run:
    python scripts/run_eval.py

What it measures:
1. Skill extraction precision — how many extracted skills are real
2. Gap analysis coverage — how many taxonomy skills are identified
3. Roadmap generation success rate
4. End-to-end latency per resume

Results saved to data/eval_outputs/eval_results.json
"""
import asyncio
import json
import time
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.pdf_ingestion import ingest_pdf, PDFIngestionError
from app.services.skill_extractor import extract_skills
from app.services.taxonomy_engine import taxonomy_index
from app.services.gap_analyzer import analyze_gap
from app.services.roadmap_generator import generate_roadmap

SAMPLE_RESUMES_PATH = Path("data/sample_resumes")
EVAL_OUTPUTS_PATH   = Path("data/eval_outputs")
EVAL_OUTPUTS_PATH.mkdir(parents=True, exist_ok=True)

# Define target roles per resume file
# Add your test resumes here with their target roles
EVAL_CONFIG = [
    {"filename": "test.pdf", "target_role": "Data Scientist"},
    {"filename": "test.pdf", "target_role": "ML Engineer"},
    {"filename": "test.pdf", "target_role": "Backend Engineer"},
    # Add more resumes as you collect them:
    # {"filename": "resume2.pdf", "target_role": "Data Analyst"},
    # {"filename": "resume3.pdf", "target_role": "DevOps Engineer"},
]


def compute_precision(extracted: list[str], taxonomy_skills: list[str]) -> float:
    """
    Precision = relevant extracted skills / total extracted skills

    A skill is considered relevant if it matches any taxonomy skill
    with case-insensitive substring matching.
    """
    if not extracted:
        return 0.0

    taxonomy_lower = [s.lower() for s in taxonomy_skills]
    relevant = 0

    for skill in extracted:
        skill_lower = skill.lower()
        # Check if extracted skill matches any taxonomy skill
        for tax_skill in taxonomy_lower:
            if skill_lower in tax_skill or tax_skill in skill_lower:
                relevant += 1
                break

    return round(relevant / len(extracted), 4)


async def evaluate_resume(filename: str, target_role: str) -> dict:
    """Run full pipeline on a single resume and return metrics."""
    filepath = SAMPLE_RESUMES_PATH / filename

    if not filepath.exists():
        return {
            "filename": filename,
            "target_role": target_role,
            "status": "failed",
            "error": f"File not found: {filepath}",
        }

    result = {
        "filename": filename,
        "target_role": target_role,
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "metrics": {},
        "extracted_skills": {},
        "gap_analysis": {},
        "roadmap_summary": {},
        "errors": [],
    }

    start_time = time.time()

    # ── Step 1: PDF Ingestion ──
    try:
        t0 = time.time()
        with open(filepath, "rb") as f:
            ingested = ingest_pdf(f.read())
        result["metrics"]["ingestion_time_sec"] = round(time.time() - t0, 3)
        result["metrics"]["page_count"]         = ingested["page_count"]
        result["metrics"]["clean_char_count"]   = ingested["char_count"]
    except PDFIngestionError as e:
        result["status"] = "failed"
        result["errors"].append(f"Ingestion failed: {e}")
        return result

    # ── Step 2: Skill Extraction ──
    try:
        t0 = time.time()
        skills_data = await extract_skills(ingested["clean_text"])
        result["metrics"]["extraction_time_sec"] = round(time.time() - t0, 3)

        all_skills = (
            skills_data["technical_skills"] +
            skills_data["tools"] +
            skills_data["soft_skills"]
        )
        result["extracted_skills"] = {
            "technical_skills": skills_data["technical_skills"],
            "tools":            skills_data["tools"],
            "soft_skills":      skills_data["soft_skills"],
            "total_count":      len(all_skills),
        }
        result["metrics"]["model_used"] = skills_data["model_used"]

    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(f"Extraction failed: {e}")
        return result

    # ── Step 3: Gap Analysis ──
    try:
        t0 = time.time()
        gap_result = analyze_gap(all_skills, target_role=target_role)
        result["metrics"]["gap_analysis_time_sec"] = round(time.time() - t0, 3)

        all_taxonomy = [s.taxonomy_skill_name for s in
                        gap_result.present_skills + gap_result.missing_skills]

        precision = compute_precision(all_skills, all_taxonomy)

        result["metrics"]["extraction_precision"] = precision
        result["metrics"]["overall_match_score"]  = gap_result.overall_match_score
        result["metrics"]["filtered_taxonomy_size"] = gap_result.filtered_taxonomy_size

        result["gap_analysis"] = {
            "present_count":  len(gap_result.present_skills),
            "missing_count":  len(gap_result.missing_skills),
            "top_5_gaps": [
                {
                    "skill": s.taxonomy_skill_name,
                    "category": s.category,
                    "score": s.similarity_score,
                    "rank": s.priority_rank,
                }
                for s in gap_result.missing_skills[:5]
            ],
        }

    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(f"Gap analysis failed: {e}")
        return result

    # ── Step 4: Roadmap Generation ──
    try:
        t0 = time.time()
        roadmap = await generate_roadmap(gap_result, target_role=target_role)
        result["metrics"]["roadmap_time_sec"] = round(time.time() - t0, 3)

        result["roadmap_summary"] = {
            "phases":            len(roadmap.get("phases", [])),
            "total_weeks":       len(roadmap.get("weekly_breakdown", [])),
            "model_used":        roadmap.get("model_used", ""),
            "week_1_focus":      roadmap["weekly_breakdown"][0]["focus"]
                                 if roadmap.get("weekly_breakdown") else "",
        }

    except Exception as e:
        result["errors"].append(f"Roadmap generation failed (non-fatal): {e}")
        result["roadmap_summary"] = {"error": str(e)}

    # ── Total latency ──
    result["metrics"]["total_time_sec"] = round(time.time() - start_time, 3)

    return result


async def main():
    print("=== Resume Skill Gap Analyzer — Evaluation ===\n")

    # Load taxonomy
    print("Loading taxonomy index...")
    taxonomy_index.load()
    print(f"Taxonomy loaded — {len(taxonomy_index.skill_names)} skills\n")

    results = []
    all_precisions = []
    all_match_scores = []

    for i, config in enumerate(EVAL_CONFIG, 1):
        print(f"[{i}/{len(EVAL_CONFIG)}] Evaluating: {config['filename']} "
              f"→ {config['target_role']}")

        result = await evaluate_resume(config["filename"], config["target_role"])
        results.append(result)

        if result["status"] == "success":
            m = result["metrics"]
            p = m.get("extraction_precision", 0)
            s = m.get("overall_match_score", 0)
            all_precisions.append(p)
            all_match_scores.append(s)

            print(f"  Status: success")
            print(f"  Skills extracted:   {result['extracted_skills']['total_count']}")
            print(f"  Extraction precision: {p:.2%}")
            print(f"  Match score:        {s:.2%}")
            print(f"  Gaps identified:    {result['gap_analysis']['missing_count']}")
            print(f"  Total time:         {m['total_time_sec']}s")
            print(f"  Top gap:            {result['gap_analysis']['top_5_gaps'][0]['skill'] if result['gap_analysis']['top_5_gaps'] else 'N/A'}")
        else:
            print(f"  Status: failed — {result['errors']}")

        print()

        # Rate limit pause between LLM calls
        if i < len(EVAL_CONFIG):
            await asyncio.sleep(3.0)

    # ── Aggregate metrics ──
    summary = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "total_evaluations":    len(results),
        "successful":           sum(1 for r in results if r["status"] == "success"),
        "failed":               sum(1 for r in results if r["status"] == "failed"),
        "avg_extraction_precision": round(
            sum(all_precisions) / len(all_precisions), 4
        ) if all_precisions else 0,
        "avg_match_score": round(
            sum(all_match_scores) / len(all_match_scores), 4
        ) if all_match_scores else 0,
        "results": results,
    }

    # Save to file
    output_path = EVAL_OUTPUTS_PATH / "eval_results.json"
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("=== Evaluation Summary ===")
    print(f"Total evaluations:        {summary['total_evaluations']}")
    print(f"Successful:               {summary['successful']}")
    print(f"Failed:                   {summary['failed']}")
    print(f"Avg extraction precision: {summary['avg_extraction_precision']:.2%}")
    print(f"Avg match score:          {summary['avg_match_score']:.2%}")
    print(f"\nResults saved → {output_path}")


if __name__ == "__main__":
    asyncio.run(main())