"""
Build skill taxonomy from scraped job descriptions.

Processes all 750 scraped JDs using keyword matching.
No LLM calls needed — rule-based extraction is more
accurate and consistent for taxonomy building.

Run:
    python scripts/build_taxonomy_from_scraped.py

What it does:
1. Loads all scraped JDs from raw_job_descriptions/
2. Matches skills using keyword dictionary
3. Counts frequency across all 750 JDs
4. Filters by minimum frequency threshold
5. Rebuilds skill_taxonomy.json
6. Regenerates embeddings and reseeds database
"""
import asyncio
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import init_db, AsyncSessionLocal
from app.models.db_models import TaxonomySkill
from app.utils.embedding_utils import embed_skills, save_embeddings, save_skill_ids
from sqlalchemy import delete
from collections import defaultdict


# ─────────────────────────────────────────────
# MASTER SKILL KEYWORD DICTIONARY
# Comprehensive list covering all 15 roles
# ─────────────────────────────────────────────
SKILL_KEYWORDS = {
    "technical_skills": [
        # Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
        "Bash", "Shell Scripting", "PowerShell",

        # ML / AI
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Reinforcement Learning", "Statistical Modeling",
        "Feature Engineering", "Model Evaluation", "Hyperparameter Tuning",
        "Transfer Learning", "Neural Networks", "Generative AI", "LLM",
        "Prompt Engineering", "MLOps", "Data Science",

        # ML Algorithms
        "Linear Regression", "Logistic Regression", "Random Forest",
        "Gradient Boosting", "XGBoost", "LightGBM", "SVM", "K-Means",
        "LSTM", "Transformer", "BERT", "CNN", "RNN", "Decision Trees",
        "Naive Bayes", "PCA", "Dimensionality Reduction",

        # Data
        "Data Analysis", "Exploratory Data Analysis", "Data Visualization",
        "Data Pipelines", "ETL", "Data Warehousing", "Data Modeling",
        "Data Mining", "Feature Selection", "Data Cleaning",
        "Time Series Analysis", "Anomaly Detection", "A/B Testing",
        "Statistical Analysis", "Predictive Modeling",

        # Backend / Systems
        "REST APIs", "GraphQL", "Microservices", "System Design",
        "Object Oriented Programming", "Functional Programming",
        "Data Structures", "Algorithms", "Dynamic Programming",
        "Distributed Systems", "Concurrent Programming",
        "Database Design", "Query Optimization", "Indexing",
        "API Design", "gRPC", "WebSockets",

        # DevOps / Cloud concepts
        "CI/CD", "DevOps", "Infrastructure as Code", "Site Reliability",
        "Agile", "Scrum", "Test Driven Development", "Code Review",
        "Microservices Architecture", "Event Driven Architecture",
        "Load Balancing", "Caching", "Message Queues",

        # Security
        "Cybersecurity", "Network Security", "Penetration Testing",
        "Vulnerability Assessment", "Cryptography", "OAuth", "JWT",
        "Zero Trust", "SIEM", "Incident Response", "Threat Modeling",

        # Web
        "HTML", "CSS", "Responsive Design", "Web Performance",
        "SEO", "Accessibility", "Progressive Web Apps",

        # Database
        "SQL", "NoSQL", "Database Administration", "Backup Recovery",
        "High Availability", "Replication", "Sharding",
    ],

    "tools": [
        # Version Control
        "Git", "GitHub", "GitLab", "Bitbucket",

        # Containerization / Orchestration
        "Docker", "Kubernetes", "Helm", "Istio", "containerd",

        # Cloud Platforms
        "AWS", "Google Cloud Platform", "Microsoft Azure", "GCP",
        "Amazon S3", "EC2", "Lambda", "CloudFormation",
        "Azure DevOps", "Google BigQuery",

        # IaC / Config
        "Terraform", "Ansible", "Puppet", "Chef", "Vagrant",

        # CI/CD Tools
        "Jenkins", "GitHub Actions", "CircleCI", "GitLab CI",
        "ArgoCD", "Spinnaker", "Travis CI",

        # Monitoring / Observability
        "Prometheus", "Grafana", "Datadog", "New Relic",
        "ELK Stack", "Splunk", "PagerDuty", "Jaeger",

        # Web Frameworks
        "FastAPI", "Django", "Flask", "Spring Boot", "Express.js",
        "Node.js", "NestJS", "Laravel", "Ruby on Rails", "ASP.NET",

        # Frontend Frameworks
        "React", "Vue.js", "Angular", "Next.js", "Svelte",
        "Redux", "TypeScript", "Webpack", "Vite",

        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Cassandra", "DynamoDB", "Oracle", "SQLite", "CouchDB",
        "Neo4j", "InfluxDB", "Snowflake", "BigQuery", "Redshift",

        # Data / ML Tools
        "Apache Kafka", "Apache Spark", "Apache Airflow", "dbt",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Keras", "Hugging Face", "LangChain", "OpenCV", "NLTK",
        "Matplotlib", "Seaborn", "Plotly",

        # MLOps Tools
        "MLflow", "Weights and Biases", "DVC", "Kubeflow",
        "SageMaker", "Vertex AI", "BentoML", "Seldon",

        # Dev Tools
        "Jupyter Notebook", "VS Code", "PyCharm", "IntelliJ",
        "Postman", "Swagger", "Linux", "Unix",

        # Project Management
        "JIRA", "Confluence", "Notion", "Trello", "Slack",

        # Security Tools
        "Nmap", "Wireshark", "Metasploit", "Burp Suite",
        "OWASP", "Nessus", "Vault",

        # Deployment
        "Render", "Heroku", "Vercel", "Netlify", "DigitalOcean",
        "Nginx", "Apache", "HAProxy",

        # Message Queues
        "RabbitMQ", "Celery", "Apache Kafka", "AWS SQS",

        # IoT / Embedded
        "ESP32", "Arduino", "Raspberry Pi", "MQTT", "ThingSpeak",
    ],

    "soft_skills": [
        "Communication", "Technical Communication", "Written Communication",
        "Verbal Communication", "Presentation Skills",
        "Problem Solving", "Analytical Thinking", "Critical Thinking",
        "Logical Reasoning", "Troubleshooting",
        "Teamwork", "Collaboration", "Cross Functional Collaboration",
        "Interpersonal Skills",
        "Leadership", "Team Leadership", "Mentoring", "Coaching",
        "Project Management", "Time Management", "Prioritization",
        "Deadline Management", "Multitasking",
        "Adaptability", "Fast Learning", "Self Directed Learning",
        "Continuous Learning", "Growth Mindset",
        "Attention to Detail", "Thoroughness", "Quality Focus",
        "Creativity", "Innovation", "Research", "Experimentation",
        "Stakeholder Management", "Client Communication",
        "Data Driven Decision Making", "Business Acumen",
        "Ownership", "Accountability", "Initiative",
        "Agile Mindset", "Scrum", "Kanban",
    ]
}

RAW_JDS_PATH     = Path("data/taxonomy/raw_job_descriptions")
TAXONOMY_PATH    = Path("data/taxonomy/skill_taxonomy.json")
EMBEDDINGS_PATH  = "data/taxonomy/embeddings.npy"
SKILL_IDS_PATH   = "data/taxonomy/skill_ids.json"

MIN_FREQUENCY_PERCENT = 1.0


# ─────────────────────────────────────────────
# STEP 1: LOAD ALL JDs
# ─────────────────────────────────────────────
def load_all_jds() -> list[dict]:
    """Load all scraped JDs from raw_job_descriptions/"""
    all_jobs = []
    for f in sorted(RAW_JDS_PATH.glob("*.json")):
        with open(f) as file:
            jobs = json.load(file)
        all_jobs.extend(jobs)
        print(f"  Loaded {len(jobs)} JDs from {f.stem}")
    return all_jobs


# ─────────────────────────────────────────────
# STEP 2: KEYWORD EXTRACTION
# ─────────────────────────────────────────────
def extract_skills_from_text(text: str) -> dict[str, set]:
    """
    Extract skills from text using keyword matching.

    Uses word boundary regex to avoid partial matches:
    e.g. "R" should not match inside "React" or "Docker"

    Returns dict of {category: set of matched skills}
    """
    text_lower = text.lower()
    found = {cat: set() for cat in SKILL_KEYWORDS}

    for category, skills in SKILL_KEYWORDS.items():
        for skill in skills:
            # Build pattern — word boundary match, case insensitive
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found[category].add(skill)

    return found


# ─────────────────────────────────────────────
# STEP 3: BUILD FREQUENCY MAP
# ─────────────────────────────────────────────
def build_frequency_map(all_jobs: list[dict]) -> dict:
    """
    Count how many JDs mention each skill.
    One count per JD (not total occurrences within a JD).
    """
    frequency = defaultdict(lambda: {"category": "", "count": 0})

    for job in all_jobs:
        text = job.get("description", "") + " " + job.get("title", "")
        found = extract_skills_from_text(text)

        for category, skills in found.items():
            for skill in skills:
                key = skill.lower()
                frequency[key]["category"] = category
                frequency[key]["name"]     = skill
                frequency[key]["count"]   += 1

    return dict(frequency)


# ─────────────────────────────────────────────
# STEP 4: BUILD TAXONOMY
# ─────────────────────────────────────────────
def build_taxonomy(
    frequency_map: dict,
    total_jds: int,
    min_pct: float = MIN_FREQUENCY_PERCENT
) -> dict:
    """
    Filter skills by minimum frequency percentage.
    Skills must appear in at least min_pct% of all JDs.
    """
    min_count = max(2, int(total_jds * min_pct / 100))
    print(f"\nMinimum frequency: {min_pct}% of {total_jds} JDs = {min_count} JDs")

    taxonomy = {
        "technical_skills": [],
        "tools":            [],
        "soft_skills":      [],
    }

    for key, data in frequency_map.items():
        if data["count"] >= min_count:
            category = data["category"]
            name     = data["name"]
            if category in taxonomy:
                taxonomy[category].append(name)

    # Sort alphabetically within each category
    for cat in taxonomy:
        taxonomy[cat] = sorted(set(taxonomy[cat]))

    return taxonomy

def build_taxonomy_with_role_boost(
    frequency_map: dict,
    all_jobs: list[dict],
    total_jds: int,
    min_pct: float = 1.0,
    role_boost_pct: float = 15.0
) -> dict:
    """
    Two-pass taxonomy building:
    Pass 1: Skills in min_pct% of ALL 750 JDs
    Pass 2: Skills in role_boost_pct% of ANY single role's 50 JDs
    """
    min_count = max(2, int(total_jds * min_pct / 100))

    taxonomy = {
        "technical_skills": [],
        "tools":            [],
        "soft_skills":      [],
    }

    # Pass 1: Global frequency
    globally_added = set()
    for key, data in frequency_map.items():
        if data["count"] >= min_count:
            category = data["category"]
            name     = data["name"]
            if category in taxonomy:
                taxonomy[category].append(name)
                globally_added.add(key)

    print(f"Pass 1 (global >{min_pct}%): "
          f"{sum(len(v) for v in taxonomy.values())} skills")

    # Pass 2: Per-role frequency boost
    # Group jobs by role
    role_jobs = defaultdict(list)
    for job in all_jobs:
        role = job.get("role", "unknown")
        role_jobs[role].append(job)

    role_added = set()
    for role, jobs in role_jobs.items():
        role_min = max(2, int(len(jobs) * role_boost_pct / 100))

        # Count skill occurrences within this role's JDs
        role_skill_counts = defaultdict(lambda: {"count": 0, "category": "", "name": ""})

        for job in jobs:
            text = job.get("description", "") + " " + job.get("title", "")
            found = extract_skills_from_text(text)

            for category, skills in found.items():
                for skill in skills:
                    key = skill.lower()
                    role_skill_counts[key]["count"] += 1
                    role_skill_counts[key]["category"] = category
                    role_skill_counts[key]["name"] = skill

        # Add skills that meet role threshold but aren't already in taxonomy
        for key, data in role_skill_counts.items():
            if (data["count"] >= role_min
                    and key not in globally_added
                    and key not in role_added):
                category = data["category"]
                name     = data["name"]
                if category in taxonomy:
                    taxonomy[category].append(name)
                    role_added.add(key)

    print(f"Pass 2 (role-specific >{role_boost_pct}% of role JDs): "
          f"+{len(role_added)} skills")

    # Sort alphabetically
    for cat in taxonomy:
        taxonomy[cat] = sorted(set(taxonomy[cat]))

    return taxonomy

# ─────────────────────────────────────────────
# STEP 5: SEED DATABASE
# ─────────────────────────────────────────────
async def seed_database(taxonomy: dict, frequency_map: dict) -> list[str]:
    """Clear and reseed taxonomy_skills table."""
    async with AsyncSessionLocal() as session:
        await session.execute(delete(TaxonomySkill))
        await session.commit()
        print("\nCleared existing taxonomy from DB.")

        ordered_names = []
        total = 0

        for category, skills in taxonomy.items():
            for skill_name in skills:
                key  = skill_name.lower()
                freq = frequency_map.get(key, {}).get("count", 1)

                skill = TaxonomySkill(
                    skill_name=skill_name,
                    normalized_name=key,
                    category=category,
                    frequency_score=freq,
                )
                session.add(skill)
                ordered_names.append(skill_name)
                total += 1

        await session.commit()
        print(f"Seeded {total} skills into taxonomy_skills table.")
        return ordered_names


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    print("=== Building Taxonomy from Scraped JDs ===\n")

    # Init DB
    print("1. Initializing database...")
    await init_db()
    print("   Done.\n")

    # Load JDs
    print("2. Loading scraped job descriptions...")
    all_jobs = load_all_jds()
    print(f"\n   Total JDs loaded: {len(all_jobs)}\n")

    # Extract skills
    print("3. Extracting skills via keyword matching...")
    frequency_map = build_frequency_map(all_jobs)
    print(f"   Unique skills found: {len(frequency_map)}")

    # Save frequency map
    freq_path = Path("data/taxonomy/frequency_map.json")
    sorted_freq = dict(
        sorted(frequency_map.items(),
               key=lambda x: x[1]["count"], reverse=True)
    )
    with open(freq_path, "w") as f:
        json.dump(sorted_freq, f, indent=2)
    print(f"   Saved frequency map → {freq_path}")

    # Build taxonomy
    print("\n4. Building taxonomy...")
    taxonomy = build_taxonomy_with_role_boost(
    frequency_map, all_jobs, len(all_jobs),
    min_pct=1.0,
    role_boost_pct=20.0
)

    total_skills = sum(len(v) for v in taxonomy.values())
    print(f"\nTaxonomy summary:")
    for cat, skills in taxonomy.items():
        print(f"  {cat}: {len(skills)} skills")
    print(f"  Total: {total_skills} skills")

    # Print top 20 by frequency
    print("\nTop 20 skills by market frequency:")
    top = sorted(frequency_map.items(),
                 key=lambda x: x[1]["count"], reverse=True)[:20]
    for key, data in top:
        pct = data["count"] / len(all_jobs) * 100
        print(f"  {data['name']} ({data['category']}): "
              f"{data['count']}/{len(all_jobs)} JDs ({pct:.1f}%)")

    # Save taxonomy JSON
    with open(TAXONOMY_PATH, "w") as f:
        json.dump(taxonomy, f, indent=2)
    print(f"\nSaved taxonomy → {TAXONOMY_PATH}")

    # Seed database
    print("\n5. Seeding database...")
    ordered_names = await seed_database(taxonomy, frequency_map)

    # Generate embeddings
    print("\n6. Generating embeddings...")
    embeddings = embed_skills(ordered_names)
    print(f"   Shape: {embeddings.shape}")

    # Save
    save_embeddings(embeddings, EMBEDDINGS_PATH)
    save_skill_ids(ordered_names, SKILL_IDS_PATH)

    print("\n=== Taxonomy Build Complete ===")
    print(f"   JDs processed:  {len(all_jobs)}")
    print(f"   Skills found:   {len(frequency_map)}")
    print(f"   Taxonomy size:  {len(ordered_names)}")
    print(f"   Embeddings:     {EMBEDDINGS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())