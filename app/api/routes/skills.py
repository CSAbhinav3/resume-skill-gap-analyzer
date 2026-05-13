import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.dependencies import get_db
from app.models.db_models import Resume, SkillExtraction, GapAnalysis, SkillGapResult
from app.models.schemas import SkillAnalysisRequest, SkillAnalysisResponse, SkillSet, SkillGapItem
from app.services.skill_extractor import extract_skills
from app.services.gap_analyzer import analyze_gap
from app.services.taxonomy_engine import taxonomy_index

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post(
    "/analyze",
    response_model=SkillAnalysisResponse,
    summary="Extract skills and analyze gaps",
    description="Extracts skills from uploaded resume using LLM, "
                "compares against taxonomy using cosine similarity, "
                "returns ranked skill gaps. Optionally filter by target role."
)
async def analyze_skills(
    request: SkillAnalysisRequest,
    db:      AsyncSession = Depends(get_db)
):
    # Fetch resume
    result = await db.execute(
        select(Resume).where(Resume.id == request.resume_id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=404,
            detail=f"Resume not found: {request.resume_id}. Upload first via /resume/upload."
        )

    if not resume.clean_text:
        raise HTTPException(
            status_code=422,
            detail="Resume has no clean text. Re-upload the PDF."
        )

    # Extract skills via LLM
    try:
        skills_data = await extract_skills(resume.clean_text)
    except Exception as e:
        await db.execute(
            Resume.__table__.update()
            .where(Resume.id == resume.id)
            .values(status="failed")
        )
        raise HTTPException(
            status_code=502,
            detail=f"Skill extraction failed: {str(e)}"
        )

    # Save extraction to DB
    extraction = SkillExtraction(
        id=str(uuid.uuid4()),
        resume_id=resume.id,
        technical_skills=skills_data["technical_skills"],
        tools=skills_data["tools"],
        soft_skills=skills_data["soft_skills"],
        model_used=skills_data["model_used"],
    )
    db.add(extraction)

    # Update resume status
    resume.status = "extracted"

    # Run gap analysis
    all_skills = extraction.all_skills_flat
    if not all_skills:
        raise HTTPException(
            status_code=422,
            detail="No skills extracted from resume. "
                   "Check if resume has sufficient text content."
        )

    try:
        gap_result = analyze_gap(all_skills, target_role=request.target_role)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gap analysis failed: {str(e)}"
        )

    # Save gap analysis to DB
    gap_analysis = GapAnalysis(
        id=str(uuid.uuid4()),
        resume_id=resume.id,
        overall_match_score=gap_result.overall_match_score,
    )
    db.add(gap_analysis)
    await db.flush()

    # Save per-skill results to DB
    # Get taxonomy skill IDs from DB for junction table
    from sqlalchemy import select as sel
    from app.models.db_models import TaxonomySkill

    tax_result = await db.execute(sel(TaxonomySkill))
    tax_skills = {ts.normalized_name: ts.id for ts in tax_result.scalars().all()}

    for skill_match in gap_result.missing_skills + gap_result.present_skills:
        tax_id = tax_skills.get(skill_match.taxonomy_skill_name.lower())
        if tax_id:
            gap_row = SkillGapResult(
                id=str(uuid.uuid4()),
                gap_analysis_id=gap_analysis.id,
                taxonomy_skill_id=tax_id,
                similarity_score=skill_match.similarity_score,
                is_missing=skill_match.is_missing,
                priority_rank=skill_match.priority_rank,
            )
            db.add(gap_row)

    resume.status = "analyzed"

    # Build response
    return SkillAnalysisResponse(
        resume_id=resume.id,
        target_role=request.target_role,
        extracted_skills=SkillSet(
            technical_skills=skills_data["technical_skills"],
            tools=skills_data["tools"],
            soft_skills=skills_data["soft_skills"],
        ),
        present_skills=[
            SkillGapItem(
                skill=s.taxonomy_skill_name,
                category=s.category,
                similarity_score=s.similarity_score,
                priority_rank=s.priority_rank,
            ) for s in gap_result.present_skills
        ],
        missing_skills=[
            SkillGapItem(
                skill=s.taxonomy_skill_name,
                category=s.category,
                similarity_score=s.similarity_score,
                priority_rank=s.priority_rank,
            ) for s in gap_result.missing_skills
        ],
        overall_match_score=gap_result.overall_match_score,
        total_taxonomy_size=gap_result.total_taxonomy_size,
        filtered_taxonomy_size=gap_result.filtered_taxonomy_size,
        analysis_id=gap_analysis.id,
        message=f"Analysis complete. "
                f"{len(gap_result.present_skills)} skills matched, "
                f"{len(gap_result.missing_skills)} gaps identified."
    )