ROLE_SKILL_MAP = {

    # =========================================================
    # DATA SCIENCE / AI
    # =========================================================

    "Data Scientist": {
        "Python": 1.0,
        "Machine Learning": 1.0,
        "Deep Learning": 0.95,
        "Pandas": 0.95,
        "NumPy": 0.95,
        "Scikit-learn": 0.9,
        "TensorFlow": 0.85,
        "PyTorch": 0.85,
        "Statistical Analysis": 0.95,
        "Feature Engineering": 0.9,
        "SQL": 0.9,
        "Data Visualization": 0.85,
        "Model Evaluation": 0.9,
        "Natural Language Processing": 0.8,
        "Time Series Analysis": 0.75,
    },

    "ML Engineer": {
        "Python": 1.0,
        "TensorFlow": 0.95,
        "PyTorch": 0.95,
        "Docker": 0.9,
        "Kubernetes": 0.85,
        "MLflow": 0.9,
        "FastAPI": 0.85,
        "AWS": 0.9,
        "MLOps": 1.0,
        "CI/CD": 0.85,
        "Model Deployment": 1.0,
        "Model Serving": 0.9,
        "Feature Store": 0.75,
    },

    "AI Engineer": {
        "Python": 1.0,
        "LLMs": 1.0,
        "Prompt Engineering": 0.95,
        "RAG": 0.95,
        "Vector Databases": 0.9,
        "LangChain": 0.9,
        "Transformers": 0.9,
        "PyTorch": 0.85,
        "FastAPI": 0.8,
        "OpenAI API": 0.85,
        "Fine-Tuning": 0.8,
    },

    "Data Analyst": {
        "SQL": 1.0,
        "Excel": 0.95,
        "Power BI": 0.95,
        "Tableau": 0.9,
        "Python": 0.85,
        "Pandas": 0.85,
        "Statistical Analysis": 0.8,
        "Data Visualization": 0.95,
        "Dashboarding": 0.9,
        "Business Analysis": 0.8,
    },

    "Data Engineer": {
        "Python": 1.0,
        "SQL": 1.0,
        "Spark": 0.95,
        "Hadoop": 0.85,
        "ETL": 1.0,
        "Airflow": 0.9,
        "Kafka": 0.9,
        "AWS": 0.9,
        "Data Warehousing": 0.9,
        "Snowflake": 0.8,
        "BigQuery": 0.8,
    },

    # =========================================================
    # SOFTWARE ENGINEERING
    # =========================================================

    "Backend Engineer": {
        "Python": 0.9,
        "FastAPI": 1.0,
        "REST APIs": 1.0,
        "SQL": 0.95,
        "PostgreSQL": 0.9,
        "Redis": 0.8,
        "Docker": 0.85,
        "System Design": 1.0,
        "Authentication": 0.85,
        "Linux": 0.8,
        "Caching": 0.75,
        "Microservices": 0.9,
    },

    "Frontend Engineer": {
        "JavaScript": 1.0,
        "TypeScript": 0.95,
        "React": 1.0,
        "Next.js": 0.9,
        "HTML": 1.0,
        "CSS": 1.0,
        "Tailwind CSS": 0.9,
        "Redux": 0.8,
        "Responsive Design": 0.9,
        "UI/UX": 0.75,
    },

    "Full Stack Engineer": {
        "JavaScript": 1.0,
        "TypeScript": 0.9,
        "React": 1.0,
        "Node.js": 0.95,
        "Express.js": 0.9,
        "MongoDB": 0.85,
        "SQL": 0.85,
        "REST APIs": 0.9,
        "Authentication": 0.85,
        "Docker": 0.8,
        "Git": 0.8,
    },

    "Software Engineer": {
        "Data Structures": 1.0,
        "Algorithms": 1.0,
        "System Design": 0.95,
        "OOP": 0.9,
        "Git": 0.85,
        "SQL": 0.8,
        "Problem Solving": 1.0,
        "Testing": 0.75,
        "Linux": 0.7,
    },

    # =========================================================
    # DEVOPS / CLOUD
    # =========================================================

    "DevOps Engineer": {
        "Docker": 1.0,
        "Kubernetes": 1.0,
        "CI/CD": 0.95,
        "Linux": 0.95,
        "AWS": 0.9,
        "Terraform": 0.9,
        "Monitoring": 0.85,
        "Jenkins": 0.85,
        "GitHub Actions": 0.85,
        "Ansible": 0.8,
    },

    "Cloud Engineer": {
        "AWS": 1.0,
        "Azure": 0.9,
        "GCP": 0.9,
        "Terraform": 0.9,
        "Docker": 0.85,
        "Kubernetes": 0.85,
        "Networking": 0.8,
        "Linux": 0.8,
        "Cloud Security": 0.75,
    },

    "MLOps Engineer": {
        "MLflow": 1.0,
        "Docker": 0.95,
        "Kubernetes": 0.95,
        "CI/CD": 0.9,
        "AWS": 0.9,
        "Model Deployment": 1.0,
        "Monitoring": 0.85,
        "Airflow": 0.8,
        "Feature Store": 0.75,
    },

    # =========================================================
    # CYBERSECURITY
    # =========================================================

    "Cyber Security Engineer": {
        "Network Security": 1.0,
        "Penetration Testing": 1.0,
        "Threat Modeling": 0.95,
        "SIEM": 0.95,
        "Linux": 0.9,
        "Cryptography": 0.85,
        "Incident Response": 0.9,
        "Firewalls": 0.9,
        "Vulnerability Assessment": 0.95,
        "Wireshark": 0.9,
        "Burp Suite": 0.85,
        "OWASP": 0.9,
        "SOC": 0.85,
        "IAM": 0.8,
        "Security Auditing": 0.8,
    },

    "SOC Analyst": {
        "SIEM": 1.0,
        "Incident Response": 0.95,
        "Threat Intelligence": 0.9,
        "Log Analysis": 0.9,
        "Linux": 0.8,
        "Network Security": 0.85,
        "Splunk": 0.9,
        "SOC": 1.0,
    },

    # =========================================================
    # DATABASE / INFRA
    # =========================================================

    "Database Administrator": {
        "SQL": 1.0,
        "PostgreSQL": 0.95,
        "MySQL": 0.95,
        "Database Optimization": 0.9,
        "Backup Recovery": 0.85,
        "Replication": 0.8,
        "Performance Tuning": 0.9,
    },

    "Site Reliability Engineer": {
        "Linux": 1.0,
        "Monitoring": 0.95,
        "Kubernetes": 0.9,
        "Docker": 0.9,
        "AWS": 0.85,
        "CI/CD": 0.85,
        "Incident Response": 0.8,
        "System Reliability": 1.0,
    },
}