# 🎯 Resume Skill Gap Analyzer with Roadmap Generator

An end-to-end AI/ML system that analyzes a candidate’s resume against a market-derived skill taxonomy and generates a personalised 30/60/90-day learning roadmap.

🔗 **Live Demo:**  
[https://resume-skill-gap-analyzer-dtqer5mn58wss9fkbasiec.streamlit.app/](https://resume-skill-gap-analyzer-sv6fbdsutzuvufjdph9nek.streamlit.app/)

## 🎥 Demo Video

▶️ [Watch the Project Demo](https://www.loom.com/share/8fbc181d5fed41ce8cc77ec1a6f2be82)
---

# 📌 Overview

This project helps users understand how well their current resume aligns with a target technical role by:

- Extracting skills from resumes using LLMs
- Comparing them against a market-driven taxonomy
- Detecting missing skills using semantic similarity
- Generating a structured 12-week learning roadmap
- Providing verified learning resources

The system combines:
- Applied NLP
- LLM Engineering
- Embedding-based semantic analysis
- FastAPI backend architecture
- Streamlit frontend deployment

---

# 🚀 Features

## Resume Skill Extraction
- Upload PDF resumes
- Automatic text cleaning and parsing
- Structured skill extraction using Groq LLM

## Semantic Gap Analysis
- Embedding-based similarity matching
- Role-aware taxonomy filtering
- Cosine similarity scoring
- Ranked missing skill prioritization

## 30/60/90-Day Learning Roadmap
- Personalized weekly roadmap generation
- Learning goals and milestones
- Curated verified learning resources
- Structured progression from beginner → advanced

## Market-Derived Skill Taxonomy
- Built from 750 real job postings
- 217 technical skills across multiple engineering domains
- Frequency-based skill insights

## Production Features
- FastAPI backend
- Async architecture
- SQLite persistence
- SHA-256 resume deduplication
- Precomputed embeddings
- Streamlit Cloud deployment

---

# 🏗️ System Architecture

```text
PDF Resume
    ↓
PDF Ingestion Pipeline
(pdfplumber + cleaning)
    ↓
Skill Extraction
(Groq LLM → structured JSON)
    ↓
Taxonomy Engine
(sentence-transformer embeddings)
    ↓
Gap Analysis
(cosine similarity + semantic filtering)
    ↓
Roadmap Generator
(Groq LLM → 12-week roadmap)
    ↓
FastAPI Backend + Streamlit Frontend
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| LLM | Groq (llama-3.3-70b-versatile) |
| NLP Embeddings | sentence-transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Similarity Engine | scikit-learn cosine similarity |
| PDF Parsing | pdfplumber |
| Database | SQLite + SQLAlchemy |
| Job Data | Adzuna REST API |
| Testing | pytest |
| Deployment | Streamlit Community Cloud |

---

# 📂 Project Structure

```text
resume-skill-gap-analyzer/
│
├── app/
│   ├── api/routes/
│   ├── models/
│   ├── services/
│   │   ├── pdf_ingestion.py
│   │   ├── skill_extractor.py
│   │   ├── taxonomy_engine.py
│   │   ├── gap_analyzer.py
│   │   └── roadmap_generator.py
│   │
│   ├── utils/
│   ├── db/
│   ├── config.py
│   └── main.py
│
├── data/taxonomy/
│   ├── skill_taxonomy.json
│   ├── embeddings.npy
│   └── skill_ids.json
│
├── scripts/
│   ├── scrape_taxonomy.py
│   ├── build_taxonomy.py
│   ├── merge_taxonomy.py
│   └── run_eval.py
│
├── tests/
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

# 🗄️ Database Schema

The system uses 6 normalized tables:

| Table | Purpose |
|---|---|
| `taxonomy_skills` | Stores taxonomy skills and metadata |
| `resumes` | Resume metadata and extracted text |
| `skill_extractions` | LLM extracted skills |
| `gap_analyses` | Resume match analysis |
| `skill_gap_results` | Ranked missing skills |
| `roadmaps` | Generated learning roadmaps |

---

# ⚙️ How Gap Analysis Works

## Step 1 — Skill Embedding

Resume skills are converted into 384-dimensional embeddings using:

```python
all-MiniLM-L6-v2
```

---

## Step 2 — Semantic Role Filtering

If a target role is provided:
- The role title is embedded
- Taxonomy skills are filtered semantically
- Only relevant skills are retained

---

## Step 3 — Similarity Matching

Cosine similarity is computed between:
- Resume skill embeddings
- Taxonomy skill embeddings

---

## Step 4 — Gap Detection

| Similarity Score | Classification |
|---|---|
| ≥ 0.65 | Present Skill |
| < 0.65 | Skill Gap |

---

## Step 5 — Gap Ranking

Missing skills are ranked by:
- semantic closeness
- relevance to target role
- estimated learning accessibility

---

# 📊 Taxonomy Dataset

The taxonomy was built using:
- 750 real job postings
- 15 engineering domains
- Adzuna job market data
- Manual taxonomy enrichment

## Roles Included

- Data Scientist
- ML Engineer
- Data Analyst
- Backend Engineer
- Full Stack Engineer
- DevOps Engineer
- Cloud Engineer
- AI Engineer
- MLOps Engineer
- SRE
- Cybersecurity
- DBA
- Frontend Engineer
- Data Engineer
- Software Engineer

---

# 📈 Example Output

The system provides:
- overall resume match score
- extracted skills
- ranked missing skills
- personalized roadmap
- weekly learning milestones
- recommended resources

---

# 🔌 API Endpoints

## POST `/resume/upload`

Upload PDF resume.

### Response

```json
{
  "resume_id": "uuid",
  "filename": "resume.pdf",
  "status": "uploaded"
}
```

---

## POST `/skills/analyze`

Analyze resume skill gaps.

### Request

```json
{
  "resume_id": "uuid",
  "target_role": "Data Scientist"
}
```

---

## POST `/roadmap/generate`

Generate personalized roadmap.

### Response

```json
{
  "30_day": {},
  "60_day": {},
  "90_day": {}
}
```

---

# 🧪 Testing

Run tests:

```bash
pytest tests/ -v
```

Includes:
- PDF ingestion tests
- Skill extraction tests
- Taxonomy analysis tests
- API route tests
- Roadmap generation tests

---

# 🚀 Local Setup

## Prerequisites

- Python 3.11
- Groq API key

---

## Clone Repository

```bash
git clone https://github.com/CSAbhinav3/resume-skill-gap-analyzer.git
cd resume-skill-gap-analyzer
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Build Taxonomy

```bash
python scripts/build_taxonomy.py
```

---

## Run Streamlit App

```bash
streamlit run streamlit_app.py
```

---

## Run FastAPI Backend

```bash
uvicorn app.main:app --reload --port 8000
```

---

# 🐳 Docker Setup

```bash
docker-compose up --build
```

---

# 🌐 Deployment

## Streamlit Cloud

1. Connect GitHub repository
2. Set main file:
```text
streamlit_app.py
```

3. Add Streamlit secrets:

```toml
GROQ_API_KEY = "your_api_key"
GROQ_MODEL = "llama-3.3-70b-versatile"
```

4. Deploy

---

# 📁 Key Engineering Decisions

## ✅ LLM Calls Minimized

LLM is called only twice:
1. skill extraction
2. roadmap generation

Everything else is deterministic Python logic.

---

## ✅ Precomputed Embeddings

Taxonomy embeddings are generated once and stored locally:

```text
embeddings.npy
```

This avoids recomputation and improves latency.

---

## ✅ Semantic Role Filtering

Role filtering is embedding-based rather than keyword-based.

This allows:
- flexible role matching
- generalized role support
- improved semantic relevance

---

## ✅ Verified Resource Mapping

Resource links are curated manually to avoid hallucinated URLs.

---

## ✅ Resume Deduplication

SHA-256 hashing prevents repeated processing of identical resumes.

---

# 🔮 Future Improvements

- Job description upload
- ATS score analysis
- Resume bullet optimization
- Recruiter feedback mode
- Vector database integration
- Multilingual resume support
- User authentication
- Historical progress tracking
- RAG-based roadmap generation

---

# 👨‍💻 Author

## C S Abhinav
AI/ML Engineer Intern — Altruist Technologies

- GitHub: https://github.com/CSAbhinav3
- LinkedIn: https://linkedin.com/in/cs-abhinav

---
