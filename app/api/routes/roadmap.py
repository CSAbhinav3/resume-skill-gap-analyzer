import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.dependencies import get_db
from app.models.db_models import Resume, GapAnalysis, SkillGapResult, TaxonomySkill, Roadmap
from app.models.schemas import RoadmapRequest, RoadmapResponse, RoadmapPhase, WeeklyItem
from app.services.gap_analyzer import GapAnalysisResult, SkillMatch
from app.services.roadmap_generator import generate_roadmap

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


@router.post(
    "/generate",
    response_model=RoadmapResponse,
    summary="Generate 30/60/90 day learning roadmap",
    description="Generates a personalised learning roadmap based on skill gaps. "
                "Requires /analyze-skills to have been called first for this resume_id. "
                "Uses verified resource links — no hallucinated URLs."
)
async def generate_roadmap_endpoint(
    request: RoadmapRequest,
    db:      AsyncSession = Depends(get_db)
):
    # Fetch resume
    resume_result = await db.execute(
        select(Resume).where(Resume.id == request.resume_id)
    )
    resume = resume_result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=404,
            detail=f"Resume not found: {request.resume_id}."
        )

    # Fetch gap analysis
    gap_result_db = await db.execute(
        select(GapAnalysis).where(GapAnalysis.resume_id == request.resume_id)
    )
    gap_analysis = gap_result_db.scalar_one_or_none()
    if not gap_analysis:
        raise HTTPException(
            status_code=404,
            detail="No gap analysis found for this resume. "
                   "Call /analyze-skills first."
        )

    # Fetch skill gap results with taxonomy skill names
    sgr_result = await db.execute(
        select(SkillGapResult, TaxonomySkill)
        .join(TaxonomySkill, SkillGapResult.taxonomy_skill_id == TaxonomySkill.id)
        .where(SkillGapResult.gap_analysis_id == gap_analysis.id)
        .order_by(SkillGapResult.priority_rank)
    )
    rows = sgr_result.all()

    # Reconstruct GapAnalysisResult from DB
    missing = []
    present = []
    for sgr, ts in rows:
        skill_match = SkillMatch(
            taxonomy_skill_name=ts.skill_name,
            category=ts.category,
            similarity_score=sgr.similarity_score,
            is_missing=sgr.is_missing,
            priority_rank=sgr.priority_rank,
        )
        if sgr.is_missing:
            missing.append(skill_match)
        else:
            present.append(skill_match)

    gap_analysis_result = GapAnalysisResult(
        missing_skills=missing,
        present_skills=present,
        overall_match_score=gap_analysis.overall_match_score,
        total_taxonomy_size=217,
        filtered_taxonomy_size=len(missing) + len(present),
        total_resume_skills=len(present),
        target_role=request.target_role,
    )

    if not gap_analysis_result.missing_skills:
        raise HTTPException(
            status_code=422,
            detail="No skill gaps found — resume already covers the full taxonomy."
        )

    # Generate roadmap via LLM
    try:
        roadmap_data = await generate_roadmap(
            gap_analysis_result,
            target_role=request.target_role
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Roadmap generation failed: {str(e)}"
        )

    # Save roadmap to DB
    roadmap_db = Roadmap(
        id=str(uuid.uuid4()),
        gap_analysis_id=gap_analysis.id,
        phases=roadmap_data["phases"],
        weekly_breakdown=roadmap_data["weekly_breakdown"],
        model_used=roadmap_data["model_used"],
    )
    db.add(roadmap_db)
    resume.status = "done"

    # Build response
    phases = []
    for phase_data in roadmap_data["phases"]:
        weeks = []
        for w in phase_data.get("weeks", []):
            weeks.append(WeeklyItem(
                week=w.get("week", 0),
                phase=phase_data["phase"],
                focus=w.get("focus", ""),
                goal=w.get("goal", ""),
                topics=w.get("topics", []),
                resources=w.get("resources", []),
            ))
        phases.append(RoadmapPhase(
            phase=phase_data["phase"],
            goal=phase_data.get("goal", ""),
            weeks=weeks,
        ))

    weekly_breakdown = []
    for w in roadmap_data.get("weekly_breakdown", []):
        weekly_breakdown.append(WeeklyItem(
            week=w.get("week", 0),
            phase=w.get("phase", ""),
            focus=w.get("focus", ""),
            goal=w.get("goal", ""),
            topics=w.get("topics", []),
            resources=w.get("resources", []),
        ))

    return RoadmapResponse(
        resume_id=resume.id,
        roadmap_id=roadmap_db.id,
        target_role=request.target_role,
        overall_match_score=gap_analysis.overall_match_score,
        phases=phases,
        weekly_breakdown=weekly_breakdown,
        model_used=roadmap_data["model_used"],
        message=f"Roadmap generated successfully. "
                f"12-week plan targeting {request.target_role or 'general skills'}."
    )