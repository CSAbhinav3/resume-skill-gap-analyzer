import hashlib
import io
import logging
from pathlib import Path

import pdfplumber

from app.utils.text_cleaner import clean_text

logger = logging.getLogger(__name__)


class PDFIngestionError(Exception):
    """Raised when PDF cannot be processed."""
    pass


def compute_file_hash(file_bytes: bytes) -> str:
    """
    SHA-256 hash of raw PDF bytes.
    Used to deduplicate uploads — same resume uploaded twice
    returns cached result instead of re-running extraction.
    """
    return hashlib.sha256(file_bytes).hexdigest()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract raw text from PDF bytes using pdfplumber.
    
    Handles:
    - Multi-page PDFs
    - Tables (extracted as text, not structure)
    - Missing/empty pages (skipped gracefully)
    
    Returns raw concatenated text across all pages.
    Raises PDFIngestionError if extraction fails or yields no text.
    """
    raw_pages = []

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            if not pdf.pages:
                raise PDFIngestionError("PDF has no pages.")

            for page_num, page in enumerate(pdf.pages, start=1):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        raw_pages.append(page_text)
                    else:
                        logger.warning(f"Page {page_num} yielded no text — skipping.")
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num}: {e} — skipping.")
                    continue

    except PDFIngestionError:
        raise
    except Exception as e:
        raise PDFIngestionError(f"Failed to open or parse PDF: {e}") from e

    if not raw_pages:
        raise PDFIngestionError(
            "No text could be extracted from this PDF. "
            "It may be scanned/image-based. OCR is not supported in this version."
        )

    return "\n".join(raw_pages)


def ingest_pdf(file_bytes: bytes) -> dict:
    """
    Full ingestion pipeline for a PDF resume.
    
    Steps:
    1. Compute SHA-256 hash (for deduplication)
    2. Extract raw text via pdfplumber
    3. Clean and normalize text via text_cleaner
    4. Validate minimum content length
    
    Returns:
        {
            "file_hash": str,       # SHA-256 hex digest
            "raw_text": str,        # unprocessed extracted text
            "clean_text": str,      # normalized, noise-free text
            "page_count": int,      # number of pages in PDF
            "char_count": int,      # character count of clean text
        }
    
    Raises:
        PDFIngestionError: if PDF cannot be processed or yields insufficient text.
    """
    if not file_bytes:
        raise PDFIngestionError("Empty file received.")

    # Step 1: Hash
    file_hash = compute_file_hash(file_bytes)
    logger.info(f"Processing PDF — hash: {file_hash[:12]}...")

    # Step 2: Extract raw text + page count
    page_count = 0
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            page_count = len(pdf.pages)
    except Exception as e:
        raise PDFIngestionError(f"Cannot read PDF metadata: {e}") from e

    raw_text = extract_text_from_pdf(file_bytes)

    # Step 3: Clean
    cleaned = clean_text(raw_text)

    # Step 4: Validate minimum content
    MIN_CHARS = 100
    if len(cleaned) < MIN_CHARS:
        raise PDFIngestionError(
            f"Extracted text is too short ({len(cleaned)} chars). "
            f"Resume may be image-based or corrupted."
        )

    logger.info(
        f"PDF ingested — pages: {page_count}, "
        f"raw_chars: {len(raw_text)}, clean_chars: {len(cleaned)}"
    )

    return {
        "file_hash": file_hash,
        "raw_text": raw_text,
        "clean_text": cleaned,
        "page_count": page_count,
        "char_count": len(cleaned),
    }