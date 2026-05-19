FROM python:3.11-slim

LABEL maintainer="C S Abhinav"
LABEL description="Resume Skill Gap Analyzer with Roadmap Generator"
LABEL version="1.0.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY streamlit_app.py .
COPY data/taxonomy/skill_taxonomy.json ./data/taxonomy/skill_taxonomy.json

# Create required directories
RUN mkdir -p data/taxonomy data/sample_resumes data/eval_outputs

# Build taxonomy embeddings at image build time
RUN python scripts/build_taxonomy.py

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default: run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]