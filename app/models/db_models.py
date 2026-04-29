import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Float, Integer,
    Boolean, DateTime, ForeignKey, JSON,
    UniqueConstraint, Index
)
from sqlalchemy.orm import DeclarativeBase, relationship


def utcnow():
    return datetime.now(timezone.utc)


def new_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────
# TABLE 1: taxonomy_skills
# Skill metadata only. No embedding column.
# Embeddings live in data/taxonomy/embeddings.npy,
# ordered by data/taxonomy/skill_ids.json.
# ─────────────────────────────────────────────
class TaxonomySkill(Base):
    __tablename__ = "taxonomy_skills"

    id              = Column(String(36), primary_key=True, default=new_uuid)
    skill_name      = Column(String(200), nullable=False)
    normalized_name = Column(String(200), nullable=False, index=True)  # lowercase, stripped
    category        = Column(String(50),  nullable=False)              # technical | tool | soft
    frequency_score = Column(Integer,     nullable=False, default=1)   # occurrences across JDs
    created_at      = Column(DateTime,    nullable=False, default=utcnow)

    gap_results = relationship(
        "SkillGapResult",
        back_populates="taxonomy_skill",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<TaxonomySkill {self.normalized_name!r} [{self.category}]>"


# ─────────────────────────────────────────────
# TABLE 2: resumes
# One row per PDF upload. SHA-256 hash prevents
# duplicate processing. updated_at tracks every
# status transition for pipeline monitoring.
#
# Status flow:
#   uploaded → extracted → analyzed → done
#                                   → failed
# ─────────────────────────────────────────────
class Resume(Base):
    __tablename__ = "resumes"

    id          = Column(String(36), primary_key=True, default=new_uuid)
    filename    = Column(String(255), nullable=False)
    file_hash   = Column(String(64),  nullable=False, unique=True)  # SHA-256
    raw_text    = Column(Text, nullable=True)
    clean_text  = Column(Text, nullable=True)
    status      = Column(String(30),  nullable=False, default="uploaded")
    uploaded_at = Column(DateTime,    nullable=False, default=utcnow)
    updated_at  = Column(DateTime,    nullable=False, default=utcnow, onupdate=utcnow)

    extraction   = relationship(
        "SkillExtraction",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan"
    )
    gap_analysis = relationship(
        "GapAnalysis",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Resume {self.filename!r} [{self.status}]>"


# ─────────────────────────────────────────────
# TABLE 3: skill_extractions
# Raw LLM output per resume, split by category.
# all_skills_flat is DROPPED — computed in Python
# as: technical_skills + tools + soft_skills.
# No redundant data, no integrity risk.
# ─────────────────────────────────────────────
class SkillExtraction(Base):
    __tablename__ = "skill_extractions"

    id               = Column(String(36), primary_key=True, default=new_uuid)
    resume_id        = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"),
                              nullable=False, unique=True)
    technical_skills = Column(JSON, nullable=False, default=list)  # ["Python", "FastAPI", ...]
    tools            = Column(JSON, nullable=False, default=list)  # ["Docker", "Git", ...]
    soft_skills      = Column(JSON, nullable=False, default=list)  # ["Communication", ...]
    model_used       = Column(String(100), nullable=False)
    extracted_at     = Column(DateTime, nullable=False, default=utcnow)

    resume = relationship("Resume", back_populates="extraction")

    @property
    def all_skills_flat(self) -> list[str]:
        """Computed union — never stored, always consistent."""
        return self.technical_skills + self.tools + self.soft_skills

    def __repr__(self):
        total = len(self.all_skills_flat)
        return f"<SkillExtraction resume={self.resume_id!r} total_skills={total}>"


# ─────────────────────────────────────────────
# TABLE 4: gap_analyses
# Summary row per resume. No JSON blobs.
# Per-skill detail lives in skill_gap_results.
# ─────────────────────────────────────────────
class GapAnalysis(Base):
    __tablename__ = "gap_analyses"

    id                  = Column(String(36), primary_key=True, default=new_uuid)
    resume_id           = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"),
                                 nullable=False, unique=True)
    overall_match_score = Column(Float,    nullable=False, default=0.0)  # 0.0 – 1.0
    analyzed_at         = Column(DateTime, nullable=False, default=utcnow)

    resume        = relationship("Resume", back_populates="gap_analysis")
    skill_results = relationship(
        "SkillGapResult",
        back_populates="gap_analysis",
        cascade="all, delete-orphan",
        order_by="SkillGapResult.priority_rank"
    )
    roadmap = relationship(
        "Roadmap",
        back_populates="gap_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @property
    def missing_skills(self):
        return [r for r in self.skill_results if r.is_missing]

    @property
    def present_skills(self):
        return [r for r in self.skill_results if not r.is_missing]

    def __repr__(self):
        return f"<GapAnalysis resume={self.resume_id!r} score={self.overall_match_score:.2f}>"


# ─────────────────────────────────────────────
# TABLE 5: skill_gap_results  ← junction table
# One row per (gap_analysis × taxonomy_skill).
# UniqueConstraint prevents duplicate inserts
# on retries. priority_rank=0 means "not a gap".
# ─────────────────────────────────────────────
class SkillGapResult(Base):
    __tablename__ = "skill_gap_results"

    id                = Column(String(36), primary_key=True, default=new_uuid)
    gap_analysis_id   = Column(String(36), ForeignKey("gap_analyses.id",   ondelete="CASCADE"),
                                nullable=False)
    taxonomy_skill_id = Column(String(36), ForeignKey("taxonomy_skills.id", ondelete="CASCADE"),
                                nullable=False)
    similarity_score  = Column(Float,   nullable=False)
    is_missing        = Column(Boolean, nullable=False)
    priority_rank     = Column(Integer, nullable=False, default=0)
    # Convention: 0 = not a gap, 1+ = ranked gap (1 = most critical)

    gap_analysis   = relationship("GapAnalysis",   back_populates="skill_results")
    taxonomy_skill = relationship("TaxonomySkill", back_populates="gap_results")

    __table_args__ = (
        # Prevents duplicate rows on retry/re-upload
        UniqueConstraint("gap_analysis_id", "taxonomy_skill_id", name="uq_gap_skill"),
        # Fast lookup: all gaps for a given analysis
        Index("ix_gap_results_analysis_missing", "gap_analysis_id", "is_missing"),
    )

    def __repr__(self):
        state = "MISSING" if self.is_missing else "PRESENT"
        return f"<SkillGapResult [{state}] rank={self.priority_rank} score={self.similarity_score:.3f}>"


# ─────────────────────────────────────────────
# TABLE 6: roadmaps
# Phases collapsed to a single JSON column.
# Adding a 120-day phase = data change, not
# a schema migration.
#
# phases structure:
# [
#   {
#     "phase": "30_day",
#     "weeks": [
#       {
#         "week": 1,
#         "focus": "...",
#         "topics": ["..."],
#         "resources": ["..."],
#         "goal": "..."
#       }
#     ]
#   },
#   {"phase": "60_day", "weeks": [...]},
#   {"phase": "90_day", "weeks": [...]}
# ]
# ─────────────────────────────────────────────
class Roadmap(Base):
    __tablename__ = "roadmaps"

    id              = Column(String(36), primary_key=True, default=new_uuid)
    gap_analysis_id = Column(String(36), ForeignKey("gap_analyses.id", ondelete="CASCADE"),
                             nullable=False, unique=True)
    phases          = Column(JSON, nullable=False, default=list)  # 30/60/90 day structured plan
    weekly_breakdown = Column(JSON, nullable=False, default=list) # flattened view across all phases
    model_used      = Column(String(100), nullable=False)
    generated_at    = Column(DateTime, nullable=False, default=utcnow)

    gap_analysis = relationship("GapAnalysis", back_populates="roadmap")

    def __repr__(self):
        return f"<Roadmap gap_analysis={self.gap_analysis_id!r}>"