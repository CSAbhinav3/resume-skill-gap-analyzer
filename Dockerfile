# ── Base image ──
# Python 3.11 slim — smaller than 3.13, better Docker compatibility
FROM python:3.11-slim

# ── Metadata ──
LABEL maintainer="C S Abhinav"
LABEL description="Resume Skill Gap Analyzer with Roadmap Generator"
LABEL version="1.0.0"

# ── Environment variables ──
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# ── Working directory ──
WORKDIR /app

# ── System dependencies ──
# libgomp1 required by sentence-transformers (OpenMP)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ──
# Copy requirements first — Docker layer caching
# Only reinstalls if requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy application code ──
COPY app/ ./app/
COPY data/taxonomy/skill_taxonomy.json ./data/taxonomy/skill_taxonomy.json

# ── Copy scripts ──
COPY scripts/ ./scripts/

# ── Create required directories ──
RUN mkdir -p data/taxonomy data/sample_resumes data/eval_outputs

# ── Build taxonomy embeddings at image build time ──
# This runs build_taxonomy.py during docker build
# Embeddings baked into image — no runtime delay
ARG GROQ_API_KEY
ENV GROQ_API_KEY=$GROQ_API_KEY
RUN python scripts/build_taxonomy.py

# ── Expose port ──
EXPOSE 8000

# ── Health check ──
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ── Start command ──
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]