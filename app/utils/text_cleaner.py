import re
import unicodedata


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters to ASCII where possible.
    Handles accented characters, special quotes, em dashes etc.
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def remove_urls(text: str) -> str:
    """Remove http/https URLs and bare www links."""
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)
    return text


def remove_emails(text: str) -> str:
    """Remove email addresses."""
    return re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", " ", text)


def remove_phone_numbers(text: str) -> str:
    """Remove common phone number formats."""
    return re.sub(r"(\+?\d[\d\s\-\(\)]{7,}\d)", " ", text)


def remove_special_characters(text: str) -> str:
    """
    Remove special characters but keep:
    - Alphanumeric
    - Spaces
    - Common punctuation useful for skill parsing: . , / + # -
    """
    return re.sub(r"[^\w\s\.\,\/\+\#\-]", " ", text)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs/newlines into single space."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def remove_noise_lines(text: str) -> str:
    """
    Remove lines that are pure noise:
    - Lines with only special characters or numbers
    - Very short lines (1-2 chars) that are formatting artifacts
    - Page numbers (standalone digits)
    """
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip empty lines
        if not stripped:
            continue
        # Skip standalone page numbers
        if re.match(r"^\d{1,3}$", stripped):
            continue
        # Skip lines that are purely punctuation/symbols
        if re.match(r"^[\W_]+$", stripped):
            continue
        # Skip very short lines (likely formatting artifacts)
        if len(stripped) <= 2:
            continue
        cleaned.append(stripped)
    return "\n".join(cleaned)


def clean_text(raw_text: str) -> str:
    """
    Master cleaning pipeline. Call this on any raw PDF-extracted text.
    Order matters — normalize unicode first, whitespace last.
    
    Returns clean, normalized text ready for LLM processing.
    """
    if not raw_text or not raw_text.strip():
        return ""

    text = normalize_unicode(raw_text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_special_characters(text)
    text = remove_noise_lines(text)
    text = normalize_whitespace(text)

    return text