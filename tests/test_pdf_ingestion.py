import pytest
from app.services.pdf_ingestion import ingest_pdf, PDFIngestionError
from app.utils.text_cleaner import clean_text


def test_clean_text_removes_email():
    raw = "Contact me at john@example.com for more info"
    result = clean_text(raw)
    assert "john@example.com" not in result


def test_clean_text_removes_phone():
    raw = "Call me at +91-9341238907 anytime"
    result = clean_text(raw)
    assert "9341238907" not in result


def test_clean_text_removes_url():
    raw = "Visit https://www.example.com for details"
    result = clean_text(raw)
    assert "https://www.example.com" not in result


def test_clean_text_normalizes_whitespace():
    raw = "Python    Java     SQL"
    result = clean_text(raw)
    assert "  " not in result


def test_ingest_pdf_rejects_empty_bytes():
    with pytest.raises(PDFIngestionError):
        ingest_pdf(b"")


def test_ingest_pdf_rejects_non_pdf():
    with pytest.raises(PDFIngestionError):
        ingest_pdf(b"this is not a pdf file at all")


def test_ingest_pdf_real_resume():
    with open("data/sample_resumes/test.pdf", "rb") as f:
        result = ingest_pdf(f.read())

    assert result["file_hash"] is not None
    assert len(result["file_hash"]) == 64       # SHA-256 hex
    assert result["page_count"] == 2
    assert result["char_count"] > 100
    assert "abhinavcs360@gmail.com" not in result["clean_text"]
    assert "9341238907" not in result["clean_text"]