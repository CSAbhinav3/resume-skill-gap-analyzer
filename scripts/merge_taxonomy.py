"""
Merge scraped taxonomy (market-validated) with manual taxonomy (comprehensive).

Scraped taxonomy: real frequency scores from 750 Adzuna JDs
Manual taxonomy:  comprehensive skill coverage

Priority rules:
1. If skill exists in scraped taxonomy → use scraped frequency score
2. If skill only in manual taxonomy → add with frequency_score = 1
3. No duplicates (case-insensitive deduplication)

Run:
    python scripts/merge_taxonomy.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import init_db, AsyncSessionLocal
from app.models.db_models import TaxonomySkill
from app.utils.embedding_utils import embed_skills, save_embeddings, save_skill_ids
from sqlalchemy import delete


SCRAPED_TAXONOMY_PATH = Path("data/taxonomy/skill_taxonomy.json")
FREQUENCY_MAP_PATH    = Path("data/taxonomy/frequency_map.json")
EMBEDDINGS_PATH       = "data/taxonomy/embeddings.npy"
SKILL_IDS_PATH        = "data/taxonomy/skill_ids.json"

# Manual taxonomy — comprehensive coverage
MANUAL_TAXONOMY = {
    "technical_skills": [
        # Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        "Bash", "Shell Scripting",

        # ML / AI
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Reinforcement Learning", "Statistical Modeling",
        "Feature Engineering", "Model Evaluation", "Hyperparameter Tuning",
        "Transfer Learning", "Neural Networks", "Generative AI",
        "Prompt Engineering", "MLOps", "Data Science", "LLM",

        # ML Algorithms
        "Linear Regression", "Logistic Regression", "Random Forest",
        "Gradient Boosting", "XGBoost", "LightGBM", "SVM",
        "LSTM", "Transformer", "BERT", "CNN", "RNN", "Decision Trees",
        "K-Means", "Anomaly Detection",

        # Data
        "Data Analysis", "Exploratory Data Analysis", "Data Visualization",
        "Data Pipelines", "ETL", "Data Warehousing", "Data Modeling",
        "Data Mining", "Feature Selection", "Time Series Analysis",
        "A/B Testing", "Statistical Analysis", "Predictive Modeling",

        # Backend / Systems
        "REST APIs", "GraphQL", "Microservices", "System Design",
        "Object Oriented Programming", "Functional Programming",
        "Data Structures", "Algorithms", "Distributed Systems",
        "Database Design", "Query Optimization", "API Design",
        "CI/CD", "DevOps", "Infrastructure as Code",
        "Agile", "Test Driven Development", "Code Review",

        # Security
        "Cybersecurity", "Network Security", "Penetration Testing",
        "Cryptography", "OAuth", "JWT", "Threat Modeling",

        # Web
        "HTML", "CSS", "Responsive Design",

        # Site Reliability
        "Site Reliability", "Load Balancing", "High Availability",
    ],

    "tools": [
        # Version Control
        "Git", "GitHub", "GitLab", "Bitbucket",

        # Containerization
        "Docker", "Kubernetes", "Helm",

        # Cloud
        "AWS", "Google Cloud Platform", "Microsoft Azure", "GCP",
        "Amazon S3", "Lambda", "CloudFormation",

        # IaC
        "Terraform", "Ansible",

        # CI/CD
        "Jenkins", "GitHub Actions", "CircleCI", "GitLab CI", "ArgoCD",

        # Monitoring
        "Prometheus", "Grafana", "Datadog", "ELK Stack", "Splunk",

        # Web Frameworks
        "FastAPI", "Django", "Flask", "Spring Boot",
        "Express.js", "Node.js", "NestJS",

        # Frontend
        "React", "Vue.js", "Angular", "Next.js", "Redux",

        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Cassandra", "DynamoDB", "Oracle", "SQLite",
        "Snowflake", "BigQuery", "Redshift",

        # Data / ML Tools
        "Apache Kafka", "Apache Spark", "Apache Airflow", "dbt",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Keras", "Hugging Face", "LangChain", "OpenCV",
        "Matplotlib", "Seaborn", "Plotly",

        # MLOps Tools
        "MLflow", "Weights and Biases", "DVC", "Kubeflow",
        "SageMaker", "Vertex AI",

        # Dev Tools
        "Jupyter Notebook", "VS Code", "Linux", "Unix",
        "Postman", "Swagger", "JIRA",

        # Security Tools
        "Nmap", "Wireshark", "Burp Suite", "OWASP",

        # Deployment
        "Render", "Heroku", "Vercel", "Nginx",

        # Message Queues
        "RabbitMQ", "Celery",
    ],

    "soft_skills": [
        "Communication", "Technical Communication", "Written Communication",
        "Problem Solving", "Analytical Thinking", "Critical Thinking",
        "Troubleshooting",
        "Teamwork", "Collaboration", "Cross Functional Collaboration",
        "Leadership", "Team Leadership", "Mentoring",
        "Project Management", "Time Management", "Prioritization",
        "Deadline Management",
        "Adaptability", "Fast Learning", "Self Directed Learning",
        "Continuous Learning",
        "Attention to Detail", "Creativity", "Innovation", "Research",
        "Stakeholder Management", "Client Communication",
        "Data Driven Decision Making", "Business Acumen",
        "Ownership", "Accountability", "Initiative",
    ]
}


def load_scraped_taxonomy() -> dict:
    with open(SCRAPED_TAXONOMY_PATH) as f:
        return json.load(f)


def load_frequency_map() -> dict:
    if not FREQUENCY_MAP_PATH.exists():
        return {}
    with open(FREQUENCY_MAP_PATH) as f:
        return json.load(f)


def merge_taxonomies(
    scraped: dict,
    manual: dict,
    frequency_map: dict
) -> list[dict]:
    """
    Merge scraped and manual taxonomies.

    Returns ordered list of skill dicts:
    [{"name": str, "category": str, "frequency_score": int}, ...]

    Sorted by frequency_score descending within each category.
    """
    seen = set()   # lowercase deduplication
    merged = []

    # Priority 1: scraped taxonomy skills (have real frequency scores)
    for category, skills in scraped.items():
        for skill_name in skills:
            key = skill_name.lower().strip()
            if key not in seen:
                seen.add(key)
                freq = frequency_map.get(key, {}).get("count", 1)
                merged.append({
                    "name":            skill_name,
                    "category":        category,
                    "frequency_score": freq,
                    "source":          "scraped"
                })

    scraped_count = len(merged)

    # Priority 2: manual taxonomy skills not in scraped
    for category, skills in manual.items():
        for skill_name in skills:
            key = skill_name.lower().strip()
            if key not in seen:
                seen.add(key)
                # Check frequency map — might exist even if below threshold
                freq = frequency_map.get(key, {}).get("count", 1)
                merged.append({
                    "name":            skill_name,
                    "category":        category,
                    "frequency_score": freq,
                    "source":          "manual"
                })

    manual_count = len(merged) - scraped_count

    print(f"  From scraped taxonomy:  {scraped_count} skills")
    print(f"  From manual taxonomy:   {manual_count} skills")
    print(f"  Total after merge:      {len(merged)} skills")
    print(f"  Duplicates removed:     {scraped_count + sum(len(v) for v in manual.values()) - len(merged)}")

    return merged


async def seed_database(merged_skills: list[dict]) -> list[str]:
    """Clear and reseed taxonomy_skills with merged data."""
    async with AsyncSessionLocal() as session:
        await session.execute(delete(TaxonomySkill))
        await session.commit()
        print("\nCleared existing taxonomy from DB.")

        ordered_names = []

        for skill_data in merged_skills:
            skill = TaxonomySkill(
                skill_name=skill_data["name"],
                normalized_name=skill_data["name"].lower().strip(),
                category=skill_data["category"],
                frequency_score=skill_data["frequency_score"],
            )
            session.add(skill)
            ordered_names.append(skill_data["name"])

        await session.commit()
        print(f"Seeded {len(ordered_names)} skills into taxonomy_skills.")
        return ordered_names


async def main():
    print("=== Merging Scraped + Manual Taxonomy ===\n")

    # Init DB
    print("1. Initializing database...")
    await init_db()
    print("   Done.\n")

    # Load both taxonomies
    print("2. Loading taxonomies...")
    scraped  = load_scraped_taxonomy()
    manual   = MANUAL_TAXONOMY
    freq_map = load_frequency_map()

    scraped_total = sum(len(v) for v in scraped.values())
    manual_total  = sum(len(v) for v in manual.values())
    print(f"   Scraped taxonomy: {scraped_total} skills")
    print(f"   Manual taxonomy:  {manual_total} skills")
    print(f"   Frequency map:    {len(freq_map)} entries\n")

    # Merge
    print("3. Merging...")
    merged_skills = merge_taxonomies(scraped, manual, freq_map)

    # Print category breakdown
    print("\nCategory breakdown:")
    from collections import Counter
    cat_counts = Counter(s["category"] for s in merged_skills)
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count} skills")

    # Print top 20 by frequency
    print("\nTop 20 by market frequency:")
    top = sorted(merged_skills, key=lambda x: x["frequency_score"], reverse=True)[:20]
    for s in top:
        print(f"  [{s['frequency_score']:3d}] {s['name']} ({s['category']}) "
              f"[{s['source']}]")

    # Save merged taxonomy JSON
    merged_json = {
        "technical_skills": sorted(
            [s["name"] for s in merged_skills if s["category"] == "technical_skills"]
        ),
        "tools": sorted(
            [s["name"] for s in merged_skills if s["category"] == "tools"]
        ),
        "soft_skills": sorted(
            [s["name"] for s in merged_skills if s["category"] == "soft_skills"]
        ),
    }
    with open("data/taxonomy/skill_taxonomy.json", "w") as f:
        json.dump(merged_json, f, indent=2)
    print("\nSaved merged taxonomy → data/taxonomy/skill_taxonomy.json")

    # Seed DB
    print("\n4. Seeding database...")
    ordered_names = await seed_database(merged_skills)

    # Generate embeddings
    print("\n5. Generating embeddings...")
    embeddings = embed_skills(ordered_names)
    print(f"   Shape: {embeddings.shape}")

    save_embeddings(embeddings, EMBEDDINGS_PATH)
    save_skill_ids(ordered_names, SKILL_IDS_PATH)

    print("\n=== Merge Complete ===")
    print(f"   Total skills: {len(ordered_names)}")
    print(f"   Embeddings:   {EMBEDDINGS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())