"""
Curated resource dictionary — verified links only.
LLM outputs resource names, this mapper provides the actual URLs.
No hallucinated links.
"""

# Structure:
# "keyword": [{"title": str, "platform": str, "url": str, "free": bool}]
# Keywords are lowercase for matching

RESOURCE_MAP = {
    # ── MACHINE LEARNING ──
    "machine learning": [
        {"title": "Machine Learning Specialization", "platform": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "free": False},
        {"title": "Practical Machine Learning", "platform": "fast.ai", "url": "https://course.fast.ai", "free": True},
        {"title": "ML Crash Course", "platform": "Google", "url": "https://developers.google.com/machine-learning/crash-course", "free": True},
        {"title": "Hands-On Machine Learning (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/", "free": False},
    ],
    "deep learning": [
        {"title": "Deep Learning Specialization", "platform": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/deep-learning", "free": False},
        {"title": "Practical Deep Learning for Coders", "platform": "fast.ai", "url": "https://course.fast.ai", "free": True},
        {"title": "Deep Learning with Python (Book)", "platform": "Manning", "url": "https://www.manning.com/books/deep-learning-with-python-second-edition", "free": False},
    ],
    "neural networks": [
        {"title": "Neural Networks and Deep Learning", "platform": "Coursera", "url": "https://www.coursera.org/learn/neural-networks-deep-learning", "free": False},
        {"title": "Neural Networks: Zero to Hero", "platform": "Andrej Karpathy (YouTube)", "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "free": True},
    ],
    "natural language processing": [
        {"title": "NLP Specialization", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/specializations/natural-language-processing", "free": False},
        {"title": "Hugging Face NLP Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course", "free": True},
        {"title": "Speech and Language Processing (Book)", "platform": "Stanford (free PDF)", "url": "https://web.stanford.edu/~jurafsky/slp3/", "free": True},
    ],
    "computer vision": [
        {"title": "CS231n: Convolutional Neural Networks", "platform": "Stanford (free)", "url": "http://cs231n.stanford.edu", "free": True},
        {"title": "OpenCV Python Tutorials", "platform": "OpenCV Docs", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "free": True},
        {"title": "Practical Computer Vision", "platform": "fast.ai", "url": "https://course.fast.ai", "free": True},
    ],
    "reinforcement learning": [
        {"title": "Deep RL Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/deep-rl-course", "free": True},
        {"title": "Spinning Up in Deep RL", "platform": "OpenAI", "url": "https://spinningup.openai.com", "free": True},
        {"title": "RL: An Introduction (Book)", "platform": "Sutton & Barto (free PDF)", "url": "http://incompleteideas.net/book/the-book-2nd.html", "free": True},
    ],
    "statistical modeling": [
        {"title": "Statistics with Python Specialization", "platform": "Coursera (UMich)", "url": "https://www.coursera.org/specializations/statistics-with-python", "free": False},
        {"title": "Think Stats (Book)", "platform": "Allen Downey (free)", "url": "https://greenteapress.com/wp/think-stats-2e/", "free": True},
        {"title": "StatQuest with Josh Starmer", "platform": "YouTube", "url": "https://www.youtube.com/@statquest", "free": True},
    ],
    "feature engineering": [
        {"title": "Feature Engineering for ML", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/feature-engineering", "free": True},
        {"title": "Feature Engineering Booklet", "platform": "Alice Zheng (free PDF)", "url": "https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/", "free": False},
    ],
    "data analysis": [
        {"title": "Data Analysis with Python", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "free": True},
        {"title": "Python for Data Analysis (Book)", "platform": "Wes McKinney (O'Reilly)", "url": "https://wesmckinney.com/book/", "free": True},
        {"title": "Kaggle Pandas Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "free": True},
    ],
    "data modeling": [
        {"title": "Database Design Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "free": True},
        {"title": "Data Modeling Fundamentals", "platform": "IBM (Coursera)", "url": "https://www.coursera.org/learn/data-modeling-fundamentals", "free": False},
        {"title": "dbt Learn", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
    ],
    "data visualization": [
        {"title": "Data Visualization with Python", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/data-visualization", "free": True},
        {"title": "Matplotlib Documentation", "platform": "Matplotlib", "url": "https://matplotlib.org/stable/tutorials/index.html", "free": True},
        {"title": "Seaborn Tutorial", "platform": "Seaborn Docs", "url": "https://seaborn.pydata.org/tutorial.html", "free": True},
        {"title": "Fundamentals of Data Visualization (Book)", "platform": "Claus Wilke (free)", "url": "https://clauswilke.com/dataviz/", "free": True},
    ],
    "data warehousing": [
        {"title": "Data Warehousing Fundamentals", "platform": "Coursera", "url": "https://www.coursera.org/learn/data-warehousing", "free": False},
        {"title": "dbt Learn — Analytics Engineering", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
        {"title": "Snowflake Getting Started", "platform": "Snowflake Docs", "url": "https://docs.snowflake.com/en/user-guide-getting-started", "free": True},
    ],
    "data structures": [
        {"title": "Data Structures and Algorithms", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=8hly31xKli0", "free": True},
        {"title": "Visualgo — Algorithm Visualizer", "platform": "NUS (free)", "url": "https://visualgo.net", "free": True},
        {"title": "LeetCode DSA Study Plan", "platform": "LeetCode", "url": "https://leetcode.com/study-plan/data-structure/", "free": True},
    ],
    "algorithms": [
        {"title": "Algorithms Specialization", "platform": "Coursera (Stanford)", "url": "https://www.coursera.org/specializations/algorithms", "free": False},
        {"title": "Introduction to Algorithms (CLRS)", "platform": "MIT Press", "url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/", "free": False},
        {"title": "NeetCode Roadmap", "platform": "NeetCode", "url": "https://neetcode.io/roadmap", "free": True},
    ],
    "system design": [
        {"title": "System Design Primer", "platform": "GitHub (free)", "url": "https://github.com/donnemartin/system-design-primer", "free": True},
        {"title": "Grokking System Design", "platform": "educative.io", "url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers", "free": False},
        {"title": "ByteByteGo Newsletter", "platform": "ByteByteGo", "url": "https://bytebytego.com", "free": False},
    ],
    "generative ai": [
    {"title": "Generative AI for Everyone", "platform": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/learn/generative-ai-for-everyone", "free": False},
    {"title": "Google Generative AI Learning Path", "platform": "Google Cloud (free)", "url": "https://www.cloudskillsboost.google/paths/118", "free": True},
    ],
    "prompt engineering": [
        {"title": "ChatGPT Prompt Engineering for Developers", "platform": "deeplearning.ai (free)", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "free": True},
        {"title": "Prompt Engineering Guide", "platform": "DAIR.AI (free)", "url": "https://www.promptingguide.ai", "free": True},
    ],
    "continuous learning": [
        {"title": "Lifelong Machine Learning", "platform": "Coursera", "url": "https://www.coursera.org/learn/machine-learning", "free": False},
        {"title": "Transfer Learning Guide", "platform": "TensorFlow (free)", "url": "https://www.tensorflow.org/tutorials/images/transfer_learning", "free": True},
    ],
    "mlops": [
        {"title": "MLOps Specialization", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops", "free": False},
        {"title": "Made With ML — MLOps", "platform": "Goku Mohandas (free)", "url": "https://madewithml.com", "free": True},
    ],
    "data driven decision making": [
        {"title": "Data-driven Decision Making", "platform": "Coursera (PwC)", "url": "https://www.coursera.org/learn/decision-making", "free": False},
        {"title": "Making Data-Driven Decisions", "platform": "Google Analytics (free)", "url": "https://analytics.google.com/analytics/academy/", "free": True},
    ],

    # ── PROGRAMMING LANGUAGES ──
    "python": [
        {"title": "Python Documentation Tutorial", "platform": "Python.org", "url": "https://docs.python.org/3/tutorial/", "free": True},
        {"title": "Fluent Python (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/", "free": False},
        {"title": "Real Python Tutorials", "platform": "Real Python", "url": "https://realpython.com", "free": True},
    ],
    "sql": [
        {"title": "SQLZoo", "platform": "SQLZoo", "url": "https://sqlzoo.net", "free": True},
        {"title": "Mode SQL Tutorial", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "free": True},
        {"title": "SQL for Data Science", "platform": "Coursera (UC Davis)", "url": "https://www.coursera.org/learn/sql-for-data-science", "free": False},
    ],
    "javascript": [
        {"title": "The Odin Project", "platform": "The Odin Project", "url": "https://www.theodinproject.com", "free": True},
        {"title": "JavaScript.info", "platform": "javascript.info", "url": "https://javascript.info", "free": True},
        {"title": "MDN JavaScript Guide", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "free": True},
    ],
    "typescript": [
        {"title": "TypeScript Official Handbook", "platform": "TypeScript Docs", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "free": True},
        {"title": "Total TypeScript", "platform": "Matt Pocock", "url": "https://www.totaltypescript.com", "free": True},
    ],

    # ── TOOLS ──
    "docker": [
        {"title": "Docker Getting Started", "platform": "Docker Docs", "url": "https://docs.docker.com/get-started/", "free": True},
        {"title": "Docker and Kubernetes", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=Wf2eSG3owoA", "free": True},
    ],
    "kubernetes": [
        {"title": "Kubernetes Documentation", "platform": "kubernetes.io", "url": "https://kubernetes.io/docs/tutorials/", "free": True},
        {"title": "CKA Study Guide", "platform": "KodeKloud", "url": "https://kodekloud.com/courses/certified-kubernetes-administrator-cka/", "free": False},
    ],
    "aws": [
        {"title": "AWS Cloud Practitioner Essentials", "platform": "AWS Training (free)", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "free": True},
        {"title": "AWS Free Tier", "platform": "AWS", "url": "https://aws.amazon.com/free/", "free": True},
        {"title": "A Cloud Guru AWS Courses", "platform": "A Cloud Guru", "url": "https://acloudguru.com", "free": False},
    ],
    "mlflow": [
        {"title": "MLflow Documentation", "platform": "MLflow", "url": "https://mlflow.org/docs/latest/index.html", "free": True},
        {"title": "MLflow Getting Started Tutorial", "platform": "MLflow", "url": "https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html", "free": True},
    ],
    "tensorflow": [
        {"title": "TensorFlow Tutorials", "platform": "TensorFlow.org", "url": "https://www.tensorflow.org/tutorials", "free": True},
        {"title": "TensorFlow Developer Certificate", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "free": False},
    ],
    "pytorch": [
        {"title": "PyTorch Official Tutorials", "platform": "PyTorch.org", "url": "https://pytorch.org/tutorials/", "free": True},
        {"title": "Deep Learning with PyTorch", "platform": "fast.ai", "url": "https://course.fast.ai", "free": True},
    ],
    "scikit-learn": [
        {"title": "Scikit-learn User Guide", "platform": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/user_guide.html", "free": True},
        {"title": "Scikit-learn Tutorial", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "free": True},
    ],
    "pandas": [
        {"title": "Pandas Getting Started", "platform": "Pandas Docs", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "free": True},
        {"title": "Kaggle Pandas Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "free": True},
    ],
    "git": [
        {"title": "Pro Git (Book)", "platform": "git-scm.com (free)", "url": "https://git-scm.com/book/en/v2", "free": True},
        {"title": "Learn Git Branching", "platform": "Interactive", "url": "https://learngitbranching.js.org", "free": True},
    ],
    "postgresql": [
        {"title": "PostgreSQL Tutorial", "platform": "postgresqltutorial.com", "url": "https://www.postgresqltutorial.com", "free": True},
        {"title": "PostgreSQL Official Documentation", "platform": "postgresql.org", "url": "https://www.postgresql.org/docs/current/tutorial.html", "free": True},
    ],
    "fastapi": [
        {"title": "FastAPI Official Documentation", "platform": "FastAPI", "url": "https://fastapi.tiangolo.com", "free": True},
        {"title": "FastAPI Full Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA", "free": True},
    ],
    "react": [
        {"title": "React Official Documentation", "platform": "react.dev", "url": "https://react.dev/learn", "free": True},
        {"title": "The Odin Project — React", "platform": "The Odin Project", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/react", "free": True},
    ],

    # ── SOFT SKILLS ──
    "system design": [
        {"title": "System Design Primer", "platform": "GitHub (free)", "url": "https://github.com/donnemartin/system-design-primer", "free": True},
    ],
    "communication": [
        {"title": "Technical Writing Courses", "platform": "Google (free)", "url": "https://developers.google.com/tech-writing", "free": True},
    ],
    "database design": [
        {"title": "Database Design Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "free": True},
        {"title": "Database Management Essentials", "platform": "Coursera (CU Boulder)", "url": "https://www.coursera.org/learn/database-management", "free": False},
    ],
    "ci/cd": [
        {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "free": True},
        {"title": "CI/CD Pipeline Tutorial", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "free": True},
    ],
    "devops": [
        {"title": "DevOps Roadmap", "platform": "roadmap.sh", "url": "https://roadmap.sh/devops", "free": True},
        {"title": "The Phoenix Project (Book)", "platform": "IT Revolution Press", "url": "https://itrevolution.com/product/the-phoenix-project/", "free": False},
    ],
    "cybersecurity": [
        {"title": "CS50 Cybersecurity", "platform": "Harvard (free)", "url": "https://cs50.harvard.edu/cybersecurity/", "free": True},
        {"title": "TryHackMe", "platform": "TryHackMe", "url": "https://tryhackme.com", "free": True},
    ],
    "svm": [
        {"title": "Support Vector Machines Explained", "platform": "StatQuest (YouTube)", "url": "https://www.youtube.com/watch?v=efR1C6CvhmE", "free": True},
        {"title": "SVM in Scikit-learn", "platform": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/modules/svm.html", "free": True},
    ],
    "xgboost": [
        {"title": "XGBoost Documentation", "platform": "XGBoost Docs", "url": "https://xgboost.readthedocs.io", "free": True},
        {"title": "XGBoost Tutorial", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intermediate-machine-learning", "free": True},
    ],
    "logistic regression": [
        {"title": "Logistic Regression Explained", "platform": "StatQuest (YouTube)", "url": "https://www.youtube.com/watch?v=yIYKR4sgzI8", "free": True},
        {"title": "Logistic Regression in Scikit-learn", "platform": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression", "free": True},
    ],
    "anomaly detection": [
        {"title": "Anomaly Detection in ML", "platform": "Andrew Ng Coursera", "url": "https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning", "free": False},
        {"title": "PyOD Library Docs", "platform": "PyOD", "url": "https://pyod.readthedocs.io", "free": True},
    ],
    "transformer": [
        {"title": "The Illustrated Transformer", "platform": "Jay Alammar (free)", "url": "https://jalammar.github.io/illustrated-transformer/", "free": True},
        {"title": "Hugging Face Transformers Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course", "free": True},
    ],
    "bert": [
        {"title": "BERT Explained", "platform": "Jay Alammar (free)", "url": "https://jalammar.github.io/illustrated-bert/", "free": True},
        {"title": "Hugging Face BERT Tutorial", "platform": "Hugging Face", "url": "https://huggingface.co/docs/transformers/model_doc/bert", "free": True},
    ],
    "lstm": [
        {"title": "Understanding LSTM Networks", "platform": "Colah's Blog (free)", "url": "https://colah.github.io/posts/2015-08-Understanding-LSTMs/", "free": True},
        {"title": "LSTM with PyTorch Tutorial", "platform": "PyTorch Docs", "url": "https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html", "free": True},
    ],
    "etl": [
        {"title": "Apache Airflow Tutorial", "platform": "Airflow Docs", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "free": True},
        {"title": "dbt Learn", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
    ],
    "research": [
        {"title": "How to Read a Paper", "platform": "S. Keshav (free PDF)", "url": "https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf", "free": True},
        {"title": "Papers With Code", "platform": "paperswithcode.com", "url": "https://paperswithcode.com", "free": True},
    ],
    "object oriented programming": [
        {"title": "OOP in Python", "platform": "Real Python", "url": "https://realpython.com/python3-object-oriented-programming/", "free": True},
        {"title": "Clean Code (Book)", "platform": "Robert C. Martin", "url": "https://www.oreilly.com/library/view/clean-code-a/9780136083238/", "free": False},
    ],
}


def get_resources_for_skill(skill_name: str, max_resources: int = 3) -> list[dict]:
    """
    Look up curated resources for a skill name.
    Falls back to generic learning resources if skill not found.

    Args:
        skill_name: skill name string (e.g. "Machine Learning")
        max_resources: maximum resources to return

    Returns:
        list of resource dicts with title, platform, url, free fields
    """
    key = skill_name.lower().strip()

    # Direct lookup
    if key in RESOURCE_MAP:
        return RESOURCE_MAP[key][:max_resources]

    # Partial match — check if any key is contained in the skill name
    for map_key, resources in RESOURCE_MAP.items():
        if map_key in key or key in map_key:
            return resources[:max_resources]

    # Generic fallback
    return [
        {"title": f"Search '{skill_name}' on Kaggle Learn", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "free": True},
        {"title": f"Search '{skill_name}' on roadmap.sh", "platform": "roadmap.sh", "url": "https://roadmap.sh", "free": True},
    ]


def enrich_roadmap_with_resources(roadmap: dict) -> dict:
    """
    Replace LLM-generated resource strings with verified URLs
    from the curated resource map.

    Modifies roadmap in place and returns it.
    """
    for phase in roadmap.get("phases", []):
        for week in phase.get("weeks", []):
            focus = week.get("focus", "")
            if focus and focus.lower() not in ["consolidation and projects",
                                                "portfolio and interview preparation",
                                                "consolidation"]:
                verified = get_resources_for_skill(focus)
                week["resources"] = [
                    f"{r['title']} — {r['platform']} — {r['url']} {'(Free)' if r['free'] else '(Paid)'}"
                    for r in verified
                ]

    # Also update weekly breakdown
    for week in roadmap.get("weekly_breakdown", []):
        focus = week.get("focus", "")
        if focus and focus.lower() not in ["consolidation and projects",
                                            "portfolio and interview preparation",
                                            "consolidation"]:
            verified = get_resources_for_skill(focus)
            week["resources"] = [
                f"{r['title']} — {r['platform']} — {r['url']}"
                for r in verified
            ]

    return roadmap