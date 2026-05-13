from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# SHARED
# ─────────────────────────────────────────────
class SkillSet(BaseModel):
    technical_skills: list[str] = Field(default_factory=list)
    tools:            list[str] = Field(default_factory=list)
    soft_skills:      list[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# RESUME UPLOAD
# ─────────────────────────────────────────────
class ResumeUploadResponse(BaseModel):
    resume_id:  str
    filename:   str
    file_hash:  str
    page_count: int
    char_count: int
    status:     str
    message:    str


# ─────────────────────────────────────────────
# SKILL ANALYSIS
# ─────────────────────────────────────────────
class SkillAnalysisRequest(BaseModel):
    resume_id:   str
    target_role: Optional[str] = Field(
        default=None,
        description="Target job role for role-filtered gap analysis. "
                    "E.g. 'Data Scientist', 'ML Engineer', 'Backend Engineer'. "
                    "If not provided, full 217-skill taxonomy is used."
    )


class SkillGapItem(BaseModel):
    skill:            str
    category:         str
    similarity_score: float
    priority_rank:    int


class SkillAnalysisResponse(BaseModel):
    resume_id:             str
    target_role:           Optional[str]
    extracted_skills:      SkillSet
    present_skills:        list[SkillGapItem]
    missing_skills:        list[SkillGapItem]
    overall_match_score:   float = Field(description="0.0 to 1.0")
    total_taxonomy_size:   int
    filtered_taxonomy_size: int
    analysis_id:           str
    message:               str


# ─────────────────────────────────────────────
# ROADMAP
# ─────────────────────────────────────────────
class RoadmapRequest(BaseModel):
    resume_id:   str
    target_role: Optional[str] = Field(
        default=None,
        description="Target role for roadmap personalisation. "
                    "Should match the role used in /analyze-skills."
    )


class WeeklyItem(BaseModel):
    week:      int
    phase:     str
    focus:     str
    goal:      str
    topics:    list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)


class RoadmapPhase(BaseModel):
    phase:   str   # 30_day | 60_day | 90_day
    goal:    str
    weeks:   list[WeeklyItem]


class RoadmapResponse(BaseModel):
    resume_id:        str
    roadmap_id:       str
    target_role:      Optional[str]
    overall_match_score: float
    phases:           list[RoadmapPhase]
    weekly_breakdown: list[WeeklyItem]
    model_used:       str
    message:          str


# ─────────────────────────────────────────────
# ERROR
# ─────────────────────────────────────────────
class ErrorResponse(BaseModel):
    error:   str
    detail:  str
    status:  int