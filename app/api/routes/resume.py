import hashlib
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.dependencies import get_db
from app.models.db_models import Resume
from app.models.schemas import ResumeUploadResponse
from app.services.pdf_ingestion import ingest_pdf, PDFIngestionError

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    summary="Upload a PDF resume",
    description="Accepts a PDF file, extracts and cleans text, stores in DB. "
                "Returns resume_id for use in subsequent endpoints. "
                "Duplicate uploads (same file) return the cached result."
)
async def upload_resume(
    file: UploadFile = File(..., description="PDF resume file"),
    db:   AsyncSession = Depends(get_db)
):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )

    # Read file bytes
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Check for duplicate — return cached if same file uploaded before
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    existing = await db.execute(
        select(Resume).where(Resume.file_hash == file_hash)
    )
    existing_resume = existing.scalar_one_or_none()

    if existing_resume:
        return ResumeUploadResponse(
            resume_id=existing_resume.id,
            filename=existing_resume.filename,
            file_hash=existing_resume.file_hash,
            page_count=0,
            char_count=len(existing_resume.clean_text or ""),
            status=existing_resume.status,
            message="Duplicate detected — returning cached resume. "
                    "Proceed to /analyze-skills with this resume_id."
        )

    # Ingest PDF
    try:
        ingested = ingest_pdf(file_bytes)
    except PDFIngestionError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Save to DB
    resume = Resume(
        id=str(uuid.uuid4()),
        filename=file.filename,
        file_hash=ingested["file_hash"],
        raw_text=ingested["raw_text"],
        clean_text=ingested["clean_text"],
        status="uploaded",
    )
    db.add(resume)
    await db.flush()

    return ResumeUploadResponse(
        resume_id=resume.id,
        filename=resume.filename,
        file_hash=resume.file_hash,
        page_count=ingested["page_count"],
        char_count=ingested["char_count"],
        status=resume.status,
        message="Resume uploaded and processed successfully. "
                "Proceed to /analyze-skills with this resume_id."
    )