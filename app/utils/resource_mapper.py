"""
Curated resource dictionary — verified links only.
LLM outputs resource names, this mapper provides the actual URLs.
No hallucinated links.
Covers all 15 engineering roles scraped from Adzuna.
"""

RESOURCE_MAP = {

    # ══════════════════════════════════════════
    # ML / AI / DATA SCIENCE
    # ══════════════════════════════════════════
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
        {"title": "Feature Engineering for Machine Learning (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/", "free": False},
    ],
    "model evaluation": [
        {"title": "Evaluating Machine Learning Models", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "free": True},
        {"title": "ML Evaluation Metrics", "platform": "Google ML Guides", "url": "https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc", "free": True},
    ],
    "hyperparameter tuning": [
        {"title": "Hyperparameter Tuning in Practice", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intermediate-machine-learning", "free": True},
        {"title": "Optuna Documentation", "platform": "Optuna", "url": "https://optuna.readthedocs.io", "free": True},
    ],
    "transfer learning": [
        {"title": "Transfer Learning Guide", "platform": "TensorFlow (free)", "url": "https://www.tensorflow.org/tutorials/images/transfer_learning", "free": True},
        {"title": "Transfer Learning with Hugging Face", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course/chapter3/1", "free": True},
    ],
    "generative ai": [
        {"title": "Generative AI for Everyone", "platform": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/learn/generative-ai-for-everyone", "free": False},
        {"title": "Google Generative AI Learning Path", "platform": "Google Cloud (free)", "url": "https://www.cloudskillsboost.google/paths/118", "free": True},
        {"title": "Generative AI with LLMs", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/learn/generative-ai-with-llms", "free": False},
    ],
    "llm": [
        {"title": "LLM University", "platform": "Cohere (free)", "url": "https://docs.cohere.com/docs/llmu", "free": True},
        {"title": "Building LLM Applications", "platform": "deeplearning.ai (free)", "url": "https://www.deeplearning.ai/short-courses/", "free": True},
    ],
    "prompt engineering": [
        {"title": "ChatGPT Prompt Engineering for Developers", "platform": "deeplearning.ai (free)", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "free": True},
        {"title": "Prompt Engineering Guide", "platform": "DAIR.AI (free)", "url": "https://www.promptingguide.ai", "free": True},
    ],
    "mlops": [
        {"title": "MLOps Specialization", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops", "free": False},
        {"title": "Made With ML", "platform": "Goku Mohandas (free)", "url": "https://madewithml.com", "free": True},
        {"title": "Full Stack Deep Learning", "platform": "UC Berkeley (free)", "url": "https://fullstackdeeplearning.com", "free": True},
    ],
    "continuous learning": [
        {"title": "Transfer Learning Guide", "platform": "TensorFlow (free)", "url": "https://www.tensorflow.org/tutorials/images/transfer_learning", "free": True},
        {"title": "Continual Learning Papers", "platform": "Papers With Code", "url": "https://paperswithcode.com/task/continual-learning", "free": True},
    ],
    "anomaly detection": [
        {"title": "Anomaly Detection Course", "platform": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning", "free": False},
        {"title": "PyOD Library Docs", "platform": "PyOD", "url": "https://pyod.readthedocs.io", "free": True},
    ],
    "time series analysis": [
        {"title": "Time Series Forecasting", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/time-series", "free": True},
        {"title": "Forecasting: Principles and Practice (Book)", "platform": "Rob Hyndman (free)", "url": "https://otexts.com/fpp3/", "free": True},
    ],
    "data analysis": [
        {"title": "Data Analysis with Python", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "free": True},
        {"title": "Python for Data Analysis (Book)", "platform": "Wes McKinney (free)", "url": "https://wesmckinney.com/book/", "free": True},
        {"title": "Kaggle Pandas Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "free": True},
    ],
    "data visualization": [
        {"title": "Data Visualization with Python", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/data-visualization", "free": True},
        {"title": "Matplotlib Documentation", "platform": "Matplotlib", "url": "https://matplotlib.org/stable/tutorials/index.html", "free": True},
        {"title": "Seaborn Tutorial", "platform": "Seaborn Docs", "url": "https://seaborn.pydata.org/tutorial.html", "free": True},
        {"title": "Fundamentals of Data Visualization (Book)", "platform": "Claus Wilke (free)", "url": "https://clauswilke.com/dataviz/", "free": True},
    ],
    "data modeling": [
        {"title": "Database Design Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "free": True},
        {"title": "Data Modeling Fundamentals", "platform": "IBM (Coursera)", "url": "https://www.coursera.org/learn/data-modeling-fundamentals", "free": False},
        {"title": "dbt Learn", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
    ],
    "data warehousing": [
        {"title": "Data Warehousing Fundamentals", "platform": "Coursera", "url": "https://www.coursera.org/learn/data-warehousing", "free": False},
        {"title": "dbt Learn — Analytics Engineering", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
        {"title": "Snowflake Getting Started", "platform": "Snowflake Docs", "url": "https://docs.snowflake.com/en/user-guide-getting-started", "free": True},
    ],
    "data pipelines": [
        {"title": "Apache Airflow Tutorial", "platform": "Airflow Docs", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "free": True},
        {"title": "Data Engineering Zoomcamp", "platform": "DataTalks.Club (free)", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "free": True},
    ],
    "etl": [
        {"title": "Apache Airflow Tutorial", "platform": "Airflow Docs", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "free": True},
        {"title": "dbt Learn", "platform": "dbt Labs", "url": "https://learn.getdbt.com", "free": True},
        {"title": "Data Engineering Zoomcamp", "platform": "DataTalks.Club (free)", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "free": True},
    ],
    "data science": [
        {"title": "Data Science Specialization", "platform": "Coursera (Johns Hopkins)", "url": "https://www.coursera.org/specializations/jhu-data-science", "free": False},
        {"title": "Kaggle Learn", "platform": "Kaggle", "url": "https://www.kaggle.com/learn", "free": True},
        {"title": "Data Science Roadmap", "platform": "roadmap.sh", "url": "https://roadmap.sh/ai-data-scientist", "free": True},
    ],
    "predictive modeling": [
        {"title": "Intermediate Machine Learning", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intermediate-machine-learning", "free": True},
        {"title": "Applied Predictive Modeling (Book)", "platform": "Springer", "url": "https://link.springer.com/book/10.1007/978-1-4614-6849-3", "free": False},
    ],

    # ── ML ALGORITHMS ──
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
    "random forest": [
        {"title": "Random Forests Explained", "platform": "StatQuest (YouTube)", "url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ", "free": True},
        {"title": "Random Forest in Scikit-learn", "platform": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees", "free": True},
    ],
    "gradient boosting": [
        {"title": "Gradient Boosting Explained", "platform": "StatQuest (YouTube)", "url": "https://www.youtube.com/watch?v=3CC4N4z3GJc", "free": True},
        {"title": "XGBoost Documentation", "platform": "XGBoost Docs", "url": "https://xgboost.readthedocs.io", "free": True},
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
    "cnn": [
        {"title": "CS231n: Convolutional Neural Networks", "platform": "Stanford (free)", "url": "http://cs231n.stanford.edu", "free": True},
        {"title": "CNN Tutorial", "platform": "TensorFlow Docs", "url": "https://www.tensorflow.org/tutorials/images/cnn", "free": True},
    ],

    # ══════════════════════════════════════════
    # PROGRAMMING LANGUAGES
    # ══════════════════════════════════════════
    "python": [
        {"title": "Python Documentation Tutorial", "platform": "Python.org", "url": "https://docs.python.org/3/tutorial/", "free": True},
        {"title": "Fluent Python (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/", "free": False},
        {"title": "Real Python Tutorials", "platform": "Real Python", "url": "https://realpython.com", "free": True},
    ],
    "java": [
        {"title": "Java Programming and Software Engineering", "platform": "Coursera (Duke)", "url": "https://www.coursera.org/specializations/java-programming", "free": False},
        {"title": "Java Tutorial for Beginners", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=eIrMbAQSU34", "free": True},
        {"title": "Effective Java (Book)", "platform": "Joshua Bloch", "url": "https://www.oreilly.com/library/view/effective-java/9780134686097/", "free": False},
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
    "sql": [
        {"title": "SQLZoo", "platform": "SQLZoo", "url": "https://sqlzoo.net", "free": True},
        {"title": "Mode SQL Tutorial", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "free": True},
        {"title": "SQL for Data Science", "platform": "Coursera (UC Davis)", "url": "https://www.coursera.org/learn/sql-for-data-science", "free": False},
    ],
    "go": [
        {"title": "Go Tour", "platform": "Go.dev (free)", "url": "https://go.dev/tour/welcome/1", "free": True},
        {"title": "Go by Example", "platform": "gobyexample.com (free)", "url": "https://gobyexample.com", "free": True},
        {"title": "Learning Go (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/learning-go/9781492077206/", "free": False},
    ],
    "rust": [
        {"title": "The Rust Book", "platform": "Rust Docs (free)", "url": "https://doc.rust-lang.org/book/", "free": True},
        {"title": "Rustlings", "platform": "GitHub (free)", "url": "https://github.com/rust-lang/rustlings", "free": True},
    ],
    "scala": [
        {"title": "Scala Documentation", "platform": "Scala Docs", "url": "https://docs.scala-lang.org/getting-started/index.html", "free": True},
        {"title": "Functional Programming in Scala", "platform": "Coursera (EPFL)", "url": "https://www.coursera.org/specializations/scala", "free": False},
    ],
    "r": [
        {"title": "R for Data Science (Book)", "platform": "Hadley Wickham (free)", "url": "https://r4ds.had.co.nz", "free": True},
        {"title": "Statistics and R", "platform": "Harvard (free)", "url": "https://pll.harvard.edu/course/statistics-and-r", "free": True},
    ],
    "bash": [
        {"title": "The Linux Command Line (Book)", "platform": "William Shotts (free)", "url": "https://linuxcommand.org/tlcl.php", "free": True},
        {"title": "Bash Scripting Tutorial", "platform": "Ryan's Tutorials (free)", "url": "https://ryanstutorials.net/bash-scripting-tutorial/", "free": True},
    ],
    "shell scripting": [
        {"title": "Shell Scripting Tutorial", "platform": "shellscript.sh (free)", "url": "https://www.shellscript.sh", "free": True},
        {"title": "The Linux Command Line (Book)", "platform": "William Shotts (free)", "url": "https://linuxcommand.org/tlcl.php", "free": True},
    ],

    # ══════════════════════════════════════════
    # BACKEND / SYSTEM DESIGN
    # ══════════════════════════════════════════
    "system design": [
        {"title": "System Design Primer", "platform": "GitHub (free)", "url": "https://github.com/donnemartin/system-design-primer", "free": True},
        {"title": "Grokking System Design", "platform": "educative.io", "url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers", "free": False},
        {"title": "ByteByteGo", "platform": "ByteByteGo", "url": "https://bytebytego.com", "free": False},
    ],
    "rest apis": [
        {"title": "REST API Design Best Practices", "platform": "freeCodeCamp (free)", "url": "https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/", "free": True},
        {"title": "FastAPI Official Documentation", "platform": "FastAPI", "url": "https://fastapi.tiangolo.com", "free": True},
    ],
    "graphql": [
        {"title": "GraphQL Official Documentation", "platform": "graphql.org", "url": "https://graphql.org/learn/", "free": True},
        {"title": "How to GraphQL", "platform": "howtographql.com (free)", "url": "https://www.howtographql.com", "free": True},
    ],
    "microservices": [
        {"title": "Microservices Patterns (Book)", "platform": "Chris Richardson", "url": "https://microservices.io/book", "free": False},
        {"title": "Microservices with Docker and Kubernetes", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=h0efzp8LC8s", "free": True},
    ],
    "api design": [
        {"title": "REST API Design Rulebook (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/rest-api-design/9781449317904/", "free": False},
        {"title": "API Design Guide", "platform": "Google Cloud (free)", "url": "https://cloud.google.com/apis/design", "free": True},
    ],
    "grpc": [
        {"title": "gRPC Documentation", "platform": "grpc.io (free)", "url": "https://grpc.io/docs/", "free": True},
        {"title": "gRPC Crash Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=Yw4rkaTc0f8", "free": True},
    ],
    "algorithms": [
        {"title": "Algorithms Specialization", "platform": "Coursera (Stanford)", "url": "https://www.coursera.org/specializations/algorithms", "free": False},
        {"title": "Introduction to Algorithms (CLRS)", "platform": "MIT Press", "url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/", "free": False},
        {"title": "NeetCode Roadmap", "platform": "NeetCode", "url": "https://neetcode.io/roadmap", "free": True},
    ],
    "data structures": [
        {"title": "Data Structures and Algorithms", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=8hly31xKli0", "free": True},
        {"title": "Visualgo — Algorithm Visualizer", "platform": "NUS (free)", "url": "https://visualgo.net", "free": True},
        {"title": "LeetCode DSA Study Plan", "platform": "LeetCode", "url": "https://leetcode.com/study-plan/data-structure/", "free": True},
    ],
    "object oriented programming": [
        {"title": "OOP in Python", "platform": "Real Python (free)", "url": "https://realpython.com/python3-object-oriented-programming/", "free": True},
        {"title": "Clean Code (Book)", "platform": "Robert C. Martin", "url": "https://www.oreilly.com/library/view/clean-code-a/9780136083238/", "free": False},
    ],
    "functional programming": [
        {"title": "Functional Programming in Python", "platform": "Real Python (free)", "url": "https://realpython.com/python-functional-programming/", "free": True},
        {"title": "Mostly Adequate Guide to FP", "platform": "GitHub (free)", "url": "https://github.com/MostlyAdequate/mostly-adequate-guide", "free": True},
    ],
    "distributed systems": [
        {"title": "Designing Data-Intensive Applications (Book)", "platform": "Martin Kleppmann", "url": "https://dataintensive.net", "free": False},
        {"title": "MIT 6.824 Distributed Systems", "platform": "MIT (free)", "url": "https://pdos.csail.mit.edu/6.824/", "free": True},
    ],
    "database design": [
        {"title": "Database Design Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "free": True},
        {"title": "Database Management Essentials", "platform": "Coursera (CU Boulder)", "url": "https://www.coursera.org/learn/database-management", "free": False},
    ],
    "query optimization": [
        {"title": "Use the Index, Luke", "platform": "use-the-index-luke.com (free)", "url": "https://use-the-index-luke.com", "free": True},
        {"title": "PostgreSQL Query Optimization", "platform": "PostgreSQL Docs", "url": "https://www.postgresql.org/docs/current/performance-tips.html", "free": True},
    ],
    "agile": [
        {"title": "Agile Manifesto", "platform": "agilemanifesto.org (free)", "url": "https://agilemanifesto.org", "free": True},
        {"title": "Agile Fundamentals", "platform": "Coursera", "url": "https://www.coursera.org/learn/agile-fundamentals", "free": False},
        {"title": "Scrum Guide", "platform": "Scrum.org (free)", "url": "https://scrumguides.org/scrum-guide.html", "free": True},
    ],
    "test driven development": [
        {"title": "Test-Driven Development with Python (Book)", "platform": "Harry Percival (free)", "url": "https://www.obeythetestinggoat.com", "free": True},
        {"title": "pytest Documentation", "platform": "pytest Docs", "url": "https://docs.pytest.org", "free": True},
    ],

    # ══════════════════════════════════════════
    # WEB FRAMEWORKS
    # ══════════════════════════════════════════
    "fastapi": [
        {"title": "FastAPI Official Documentation", "platform": "FastAPI", "url": "https://fastapi.tiangolo.com", "free": True},
        {"title": "FastAPI Full Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA", "free": True},
    ],
    "django": [
        {"title": "Django Official Documentation", "platform": "Django Docs", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "free": True},
        {"title": "Django for Beginners (Book)", "platform": "William S. Vincent", "url": "https://djangoforbeginners.com", "free": False},
    ],
    "flask": [
        {"title": "Flask Official Documentation", "platform": "Flask Docs", "url": "https://flask.palletsprojects.com/en/stable/quickstart/", "free": True},
        {"title": "Flask Mega-Tutorial", "platform": "Miguel Grinberg (free)", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "free": True},
    ],
    "spring boot": [
        {"title": "Spring Boot Getting Started", "platform": "Spring Docs", "url": "https://spring.io/guides/gs/spring-boot/", "free": True},
        {"title": "Spring Boot Tutorial", "platform": "Amigoscode (YouTube)", "url": "https://www.youtube.com/watch?v=9SGDpanrc8U", "free": True},
    ],
    "node.js": [
        {"title": "Node.js Official Documentation", "platform": "Node.js Docs", "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs", "free": True},
        {"title": "The Odin Project — NodeJS", "platform": "The Odin Project", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/nodejs", "free": True},
    ],
    "express.js": [
        {"title": "Express.js Official Documentation", "platform": "Express Docs", "url": "https://expressjs.com/en/starter/installing.html", "free": True},
        {"title": "Express.js Crash Course", "platform": "Traversy Media (YouTube)", "url": "https://www.youtube.com/watch?v=L72fhGm1tfE", "free": True},
    ],

    # ══════════════════════════════════════════
    # FRONTEND
    # ══════════════════════════════════════════
    "react": [
        {"title": "React Official Documentation", "platform": "react.dev", "url": "https://react.dev/learn", "free": True},
        {"title": "The Odin Project — React", "platform": "The Odin Project", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/react", "free": True},
    ],
    "vue.js": [
        {"title": "Vue.js Official Documentation", "platform": "Vue Docs", "url": "https://vuejs.org/guide/introduction.html", "free": True},
        {"title": "Vue.js Crash Course", "platform": "Traversy Media (YouTube)", "url": "https://www.youtube.com/watch?v=qZXt1Aom3Cs", "free": True},
    ],
    "angular": [
        {"title": "Angular Official Documentation", "platform": "Angular Docs", "url": "https://angular.io/docs", "free": True},
        {"title": "Angular — The Complete Guide", "platform": "Udemy (Maximilian)", "url": "https://www.udemy.com/course/the-complete-guide-to-angular-2/", "free": False},
    ],
    "next.js": [
        {"title": "Next.js Official Documentation", "platform": "Next.js Docs", "url": "https://nextjs.org/docs", "free": True},
        {"title": "Next.js Learn", "platform": "Vercel (free)", "url": "https://nextjs.org/learn", "free": True},
    ],
    "html": [
        {"title": "MDN HTML Docs", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "free": True},
        {"title": "The Odin Project — Foundations", "platform": "The Odin Project", "url": "https://www.theodinproject.com/paths/foundations", "free": True},
    ],
    "css": [
        {"title": "MDN CSS Docs", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "free": True},
        {"title": "CSS Tricks", "platform": "css-tricks.com (free)", "url": "https://css-tricks.com", "free": True},
    ],
    "responsive design": [
        {"title": "Responsive Web Design", "platform": "freeCodeCamp (free)", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "free": True},
        {"title": "MDN Responsive Design Guide", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design", "free": True},
    ],

    # ══════════════════════════════════════════
    # DATABASES
    # ══════════════════════════════════════════
    "postgresql": [
        {"title": "PostgreSQL Tutorial", "platform": "postgresqltutorial.com (free)", "url": "https://www.postgresqltutorial.com", "free": True},
        {"title": "PostgreSQL Official Documentation", "platform": "postgresql.org", "url": "https://www.postgresql.org/docs/current/tutorial.html", "free": True},
    ],
    "mysql": [
        {"title": "MySQL Tutorial", "platform": "mysqltutorial.org (free)", "url": "https://www.mysqltutorial.org", "free": True},
        {"title": "MySQL Documentation", "platform": "MySQL Docs", "url": "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html", "free": True},
    ],
    "mongodb": [
        {"title": "MongoDB University", "platform": "MongoDB (free)", "url": "https://learn.mongodb.com", "free": True},
        {"title": "MongoDB Documentation", "platform": "MongoDB Docs", "url": "https://www.mongodb.com/docs/manual/tutorial/getting-started/", "free": True},
    ],
    "redis": [
        {"title": "Redis University", "platform": "Redis (free)", "url": "https://university.redis.com", "free": True},
        {"title": "Redis Documentation", "platform": "Redis Docs", "url": "https://redis.io/docs/getting-started/", "free": True},
    ],
    "elasticsearch": [
        {"title": "Elasticsearch Getting Started", "platform": "Elastic Docs", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html", "free": True},
        {"title": "Elasticsearch: The Definitive Guide", "platform": "Elastic (free)", "url": "https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html", "free": True},
    ],
    "cassandra": [
        {"title": "Apache Cassandra Documentation", "platform": "Cassandra Docs", "url": "https://cassandra.apache.org/doc/latest/cassandra/getting-started/", "free": True},
        {"title": "Cassandra Course", "platform": "DataStax Academy (free)", "url": "https://academy.datastax.com", "free": True},
    ],
    "snowflake": [
        {"title": "Snowflake Getting Started", "platform": "Snowflake Docs", "url": "https://docs.snowflake.com/en/user-guide-getting-started", "free": True},
        {"title": "Snowflake University", "platform": "Snowflake (free)", "url": "https://learn.snowflake.com", "free": True},
    ],
    "bigquery": [
        {"title": "BigQuery Getting Started", "platform": "Google Cloud (free)", "url": "https://cloud.google.com/bigquery/docs/quickstarts", "free": True},
        {"title": "BigQuery for Data Analysts", "platform": "Coursera (Google)", "url": "https://www.coursera.org/learn/preparing-data-for-analysis-with-google-cloud", "free": False},
    ],
    "database administration": [
        {"title": "Database Administration Fundamentals", "platform": "Microsoft Learn (free)", "url": "https://learn.microsoft.com/en-us/training/paths/azure-sql-fundamentals/", "free": True},
        {"title": "PostgreSQL DBA Tutorial", "platform": "postgresqltutorial.com (free)", "url": "https://www.postgresqltutorial.com", "free": True},
    ],
    "high availability": [
        {"title": "Designing Distributed Systems (Book)", "platform": "O'Reilly (free)", "url": "https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/", "free": True},
        {"title": "Site Reliability Engineering (Book)", "platform": "Google (free)", "url": "https://sre.google/sre-book/table-of-contents/", "free": True},
    ],

    # ══════════════════════════════════════════
    # DEVOPS / CLOUD / SRE
    # ══════════════════════════════════════════
    "docker": [
        {"title": "Docker Getting Started", "platform": "Docker Docs", "url": "https://docs.docker.com/get-started/", "free": True},
        {"title": "Docker and Kubernetes Full Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=Wf2eSG3owoA", "free": True},
    ],
    "kubernetes": [
        {"title": "Kubernetes Documentation", "platform": "kubernetes.io", "url": "https://kubernetes.io/docs/tutorials/", "free": True},
        {"title": "Kubernetes for Beginners", "platform": "KodeKloud (YouTube)", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "free": True},
        {"title": "CKA Study Guide", "platform": "KodeKloud", "url": "https://kodekloud.com/courses/certified-kubernetes-administrator-cka/", "free": False},
    ],
    "aws": [
        {"title": "AWS Cloud Practitioner Essentials", "platform": "AWS Training (free)", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "free": True},
        {"title": "AWS Free Tier", "platform": "AWS", "url": "https://aws.amazon.com/free/", "free": True},
        {"title": "AWS Solutions Architect", "platform": "A Cloud Guru", "url": "https://acloudguru.com/course/aws-certified-solutions-architect-associate-saa-c03", "free": False},
    ],
    "google cloud platform": [
        {"title": "Google Cloud Skills Boost", "platform": "Google Cloud (free)", "url": "https://www.cloudskillsboost.google", "free": True},
        {"title": "GCP Associate Cloud Engineer", "platform": "A Cloud Guru", "url": "https://acloudguru.com/course/google-certified-associate-cloud-engineer", "free": False},
    ],
    "gcp": [
        {"title": "Google Cloud Skills Boost", "platform": "Google Cloud (free)", "url": "https://www.cloudskillsboost.google", "free": True},
        {"title": "GCP Fundamentals", "platform": "Coursera (Google)", "url": "https://www.coursera.org/learn/gcp-fundamentals", "free": False},
    ],
    "microsoft azure": [
        {"title": "Azure Fundamentals", "platform": "Microsoft Learn (free)", "url": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "free": True},
        {"title": "AZ-900 Study Guide", "platform": "Microsoft Learn (free)", "url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/", "free": True},
    ],
    "terraform": [
        {"title": "Terraform Getting Started", "platform": "HashiCorp (free)", "url": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started", "free": True},
        {"title": "Terraform Documentation", "platform": "HashiCorp Docs", "url": "https://developer.hashicorp.com/terraform/docs", "free": True},
    ],
    "ansible": [
        {"title": "Ansible Documentation", "platform": "Ansible Docs", "url": "https://docs.ansible.com/ansible/latest/getting_started/index.html", "free": True},
        {"title": "Ansible for Beginners", "platform": "KodeKloud (YouTube)", "url": "https://www.youtube.com/watch?v=1id6ERvfozo", "free": True},
    ],
    "ci/cd": [
        {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "free": True},
        {"title": "CI/CD Pipeline Tutorial", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "free": True},
    ],
    "github actions": [
        {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "free": True},
        {"title": "GitHub Actions Tutorial", "platform": "TechWorld with Nana (YouTube)", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "free": True},
    ],
    "jenkins": [
        {"title": "Jenkins Documentation", "platform": "Jenkins Docs", "url": "https://www.jenkins.io/doc/tutorials/", "free": True},
        {"title": "Jenkins Tutorial", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=FX322RVNGj4", "free": True},
    ],
    "devops": [
        {"title": "DevOps Roadmap", "platform": "roadmap.sh", "url": "https://roadmap.sh/devops", "free": True},
        {"title": "DevOps Prerequisites", "platform": "KodeKloud (free)", "url": "https://kodekloud.com/courses/devops-pre-requisite-course/", "free": True},
        {"title": "The Phoenix Project (Book)", "platform": "IT Revolution Press", "url": "https://itrevolution.com/product/the-phoenix-project/", "free": False},
    ],
    "infrastructure as code": [
        {"title": "Terraform Getting Started", "platform": "HashiCorp (free)", "url": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started", "free": True},
        {"title": "Pulumi Documentation", "platform": "Pulumi Docs", "url": "https://www.pulumi.com/docs/get-started/", "free": True},
    ],
    "prometheus": [
        {"title": "Prometheus Getting Started", "platform": "Prometheus Docs", "url": "https://prometheus.io/docs/prometheus/latest/getting_started/", "free": True},
        {"title": "Prometheus and Grafana Tutorial", "platform": "TechWorld with Nana (YouTube)", "url": "https://www.youtube.com/watch?v=QoDqxm7ybLc", "free": True},
    ],
    "grafana": [
        {"title": "Grafana Getting Started", "platform": "Grafana Docs", "url": "https://grafana.com/docs/grafana/latest/getting-started/", "free": True},
        {"title": "Grafana Fundamentals", "platform": "Grafana (free)", "url": "https://grafana.com/tutorials/grafana-fundamentals/", "free": True},
    ],
    "site reliability": [
        {"title": "Site Reliability Engineering (Book)", "platform": "Google (free)", "url": "https://sre.google/sre-book/table-of-contents/", "free": True},
        {"title": "SRE Workbook", "platform": "Google (free)", "url": "https://sre.google/workbook/table-of-contents/", "free": True},
    ],
    "load balancing": [
        {"title": "Load Balancing Explained", "platform": "NGINX (free)", "url": "https://www.nginx.com/resources/glossary/load-balancing/", "free": True},
        {"title": "System Design — Load Balancers", "platform": "System Design Primer (free)", "url": "https://github.com/donnemartin/system-design-primer#load-balancer", "free": True},
    ],
    "linux": [
        {"title": "The Linux Command Line (Book)", "platform": "William Shotts (free)", "url": "https://linuxcommand.org/tlcl.php", "free": True},
        {"title": "Linux Fundamentals", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=ROjZy1WbCIA", "free": True},
    ],

    # ══════════════════════════════════════════
    # DATA / ML TOOLS
    # ══════════════════════════════════════════
    "pandas": [
        {"title": "Pandas Getting Started", "platform": "Pandas Docs", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "free": True},
        {"title": "Kaggle Pandas Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "free": True},
    ],
    "numpy": [
        {"title": "NumPy Getting Started", "platform": "NumPy Docs", "url": "https://numpy.org/doc/stable/user/quickstart.html", "free": True},
        {"title": "NumPy Tutorial", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=QUT1VHiLmmI", "free": True},
    ],
    "scikit-learn": [
        {"title": "Scikit-learn User Guide", "platform": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/user_guide.html", "free": True},
        {"title": "Intro to Machine Learning", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "free": True},
    ],
    "tensorflow": [
        {"title": "TensorFlow Tutorials", "platform": "TensorFlow.org", "url": "https://www.tensorflow.org/tutorials", "free": True},
        {"title": "TensorFlow Developer Certificate", "platform": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "free": False},
    ],
    "pytorch": [
        {"title": "PyTorch Official Tutorials", "platform": "PyTorch.org", "url": "https://pytorch.org/tutorials/", "free": True},
        {"title": "Deep Learning with PyTorch", "platform": "fast.ai", "url": "https://course.fast.ai", "free": True},
    ],
    "hugging face": [
        {"title": "Hugging Face NLP Course", "platform": "Hugging Face (free)", "url": "https://huggingface.co/learn/nlp-course", "free": True},
        {"title": "Hugging Face Documentation", "platform": "Hugging Face Docs", "url": "https://huggingface.co/docs", "free": True},
    ],
    "langchain": [
        {"title": "LangChain Documentation", "platform": "LangChain Docs", "url": "https://python.langchain.com/docs/get_started/introduction", "free": True},
        {"title": "LangChain Crash Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=lG7Uxts9SXs", "free": True},
    ],
    "mlflow": [
        {"title": "MLflow Documentation", "platform": "MLflow", "url": "https://mlflow.org/docs/latest/index.html", "free": True},
        {"title": "MLflow Getting Started Tutorial", "platform": "MLflow", "url": "https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html", "free": True},
    ],
    "apache kafka": [
        {"title": "Apache Kafka Documentation", "platform": "Kafka Docs", "url": "https://kafka.apache.org/documentation/", "free": True},
        {"title": "Kafka Crash Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/watch?v=R873BlNVUB4", "free": True},
    ],
    "apache spark": [
        {"title": "Apache Spark Documentation", "platform": "Spark Docs", "url": "https://spark.apache.org/docs/latest/quick-start.html", "free": True},
        {"title": "Spark and Python for Big Data", "platform": "Udemy (Jose Portilla)", "url": "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/", "free": False},
    ],
    "apache airflow": [
        {"title": "Apache Airflow Documentation", "platform": "Airflow Docs", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "free": True},
        {"title": "Airflow Tutorial", "platform": "Marc Lamberti (YouTube)", "url": "https://www.youtube.com/watch?v=K9AnJ9_ZAXE", "free": True},
    ],
    "dbt": [
        {"title": "dbt Learn", "platform": "dbt Labs (free)", "url": "https://learn.getdbt.com", "free": True},
        {"title": "dbt Documentation", "platform": "dbt Docs", "url": "https://docs.getdbt.com", "free": True},
    ],
    "git": [
        {"title": "Pro Git (Book)", "platform": "git-scm.com (free)", "url": "https://git-scm.com/book/en/v2", "free": True},
        {"title": "Learn Git Branching", "platform": "Interactive (free)", "url": "https://learngitbranching.js.org", "free": True},
    ],

    # ══════════════════════════════════════════
    # CYBERSECURITY
    # ══════════════════════════════════════════
    "cybersecurity": [
        {"title": "CS50 Cybersecurity", "platform": "Harvard (free)", "url": "https://cs50.harvard.edu/cybersecurity/", "free": True},
        {"title": "TryHackMe", "platform": "TryHackMe", "url": "https://tryhackme.com", "free": True},
        {"title": "Cybersecurity Roadmap", "platform": "roadmap.sh", "url": "https://roadmap.sh/cyber-security", "free": True},
    ],
    "network security": [
        {"title": "Network Security Course", "platform": "Cybrary (free)", "url": "https://www.cybrary.it/course/comptia-network-plus/", "free": True},
        {"title": "CompTIA Security+ Study Guide", "platform": "Professor Messer (free)", "url": "https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-plus-course/", "free": True},
    ],
    "penetration testing": [
        {"title": "TryHackMe", "platform": "TryHackMe", "url": "https://tryhackme.com", "free": True},
        {"title": "Hack The Box", "platform": "Hack The Box", "url": "https://www.hackthebox.com", "free": True},
        {"title": "Penetration Testing with Kali Linux", "platform": "Offensive Security", "url": "https://www.offsec.com/courses/pen-200/", "free": False},
    ],
    "owasp": [
        {"title": "OWASP Top 10", "platform": "OWASP (free)", "url": "https://owasp.org/www-project-top-ten/", "free": True},
        {"title": "OWASP Testing Guide", "platform": "OWASP (free)", "url": "https://owasp.org/www-project-web-security-testing-guide/", "free": True},
    ],
    "cryptography": [
        {"title": "Cryptography I", "platform": "Coursera (Stanford)", "url": "https://www.coursera.org/learn/crypto", "free": False},
        {"title": "Crypto 101 (Book)", "platform": "crypto101.io (free)", "url": "https://www.crypto101.io", "free": True},
    ],

    # ══════════════════════════════════════════
    # SOFT SKILLS
    # ══════════════════════════════════════════
    "communication": [
        {"title": "Technical Writing Courses", "platform": "Google (free)", "url": "https://developers.google.com/tech-writing", "free": True},
    ],
    "technical communication": [
        {"title": "Technical Writing Courses", "platform": "Google (free)", "url": "https://developers.google.com/tech-writing", "free": True},
        {"title": "Writing in the Sciences", "platform": "Coursera (Stanford)", "url": "https://www.coursera.org/learn/sciwrite", "free": False},
    ],
    "leadership": [
        {"title": "Inspiring and Motivating Individuals", "platform": "Coursera (Michigan)", "url": "https://www.coursera.org/learn/motivate-people-teams", "free": False},
        {"title": "The Manager's Path (Book)", "platform": "Camille Fournier", "url": "https://www.oreilly.com/library/view/the-managers-path/9781491973882/", "free": False},
    ],
    "problem solving": [
        {"title": "Think Like a Programmer (Book)", "platform": "No Starch Press", "url": "https://nostarch.com/thinklikeaprogrammer", "free": False},
        {"title": "LeetCode Problems", "platform": "LeetCode (free)", "url": "https://leetcode.com/problemset/all/", "free": True},
    ],
    "project management": [
        {"title": "Google Project Management Certificate", "platform": "Coursera (Google)", "url": "https://www.coursera.org/professional-certificates/google-project-management", "free": False},
        {"title": "Project Management Fundamentals", "platform": "PMI (free)", "url": "https://www.pmi.org/learning/training-development/onlinecourses/online-courses-the-fundamentals", "free": True},
    ],
    "research": [
        {"title": "How to Read a Paper", "platform": "S. Keshav (free PDF)", "url": "https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf", "free": True},
        {"title": "Papers With Code", "platform": "paperswithcode.com", "url": "https://paperswithcode.com", "free": True},
    ],
    "data driven decision making": [
        {"title": "Data-driven Decision Making", "platform": "Coursera (PwC)", "url": "https://www.coursera.org/learn/decision-making", "free": False},
        {"title": "Google Analytics Academy", "platform": "Google (free)", "url": "https://analytics.google.com/analytics/academy/", "free": True},
    ],
    "analytical thinking": [
        {"title": "Critical Thinking and Problem Solving", "platform": "Coursera (Rochester)", "url": "https://www.coursera.org/learn/critical-thinking-problem-solving", "free": False},
        {"title": "Think Bayes (Book)", "platform": "Allen Downey (free)", "url": "https://www.greenteapress.com/thinkbayes/html/index.html", "free": True},
    ],
    "stakeholder management": [
        {"title": "Stakeholder Management", "platform": "Coursera (UC Irvine)", "url": "https://www.coursera.org/learn/project-management-capstone", "free": False},
        {"title": "Google Project Management Certificate", "platform": "Coursera (Google)", "url": "https://www.coursera.org/professional-certificates/google-project-management", "free": False},
    ],
    "innovation": [
        {"title": "Design Thinking", "platform": "IDEO (free)", "url": "https://www.ideou.com/blogs/inspiration/what-is-design-thinking", "free": True},
        {"title": "Innovation and Creativity", "platform": "Coursera (Penn)", "url": "https://www.coursera.org/learn/creativity-innovation", "free": False},
    ],
    "ownership": [
        {"title": "Extreme Ownership (Book)", "platform": "Jocko Willink", "url": "https://www.amazon.com/Extreme-Ownership-U-S-Navy-SEALs/dp/1250183863", "free": False},
        {"title": "The Staff Engineer's Path (Book)", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/", "free": False},
    ],
    "collaboration": [
        {"title": "Teamwork Skills", "platform": "Coursera (Boulder)", "url": "https://www.coursera.org/learn/teamwork-skills", "free": False},
        {"title": "Team Topologies (Book)", "platform": "IT Revolution Press", "url": "https://teamtopologies.com/book", "free": False},
    ],
}


def get_resources_for_skill(skill_name: str, max_resources: int = 3) -> list[dict]:
    """
    Look up curated resources for a skill name.
    Falls back to generic learning resources if skill not found.
    """
    key = skill_name.lower().strip()

    # Direct lookup
    if key in RESOURCE_MAP:
        return RESOURCE_MAP[key][:max_resources]

    # Partial match — check if any map key is contained in the skill name or vice versa
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
    """
    consolidation_keywords = [
        "consolidation and projects",
        "portfolio and interview preparation",
        "consolidation",
        "portfolio development",
    ]

    for phase in roadmap.get("phases", []):
        for week in phase.get("weeks", []):
            focus = week.get("focus", "")
            if focus and focus.lower() not in consolidation_keywords:
                verified = get_resources_for_skill(focus)
                week["resources"] = [
                    f"{r['title']} — {r['platform']} — {r['url']} {'(Free)' if r['free'] else '(Paid)'}"
                    for r in verified
                ]

    for week in roadmap.get("weekly_breakdown", []):
        focus = week.get("focus", "")
        if focus and focus.lower() not in consolidation_keywords:
            verified = get_resources_for_skill(focus)
            week["resources"] = [
                f"{r['title']} — {r['platform']} — {r['url']}"
                for r in verified
            ]

    return roadmap