from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:         str   = "sqlite+aiosqlite:///./dev.db"
    GROQ_API_KEY:         str
    GROQ_MODEL:           str   = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL:      str   = "all-MiniLM-L6-v2"
    TAXONOMY_EMB_PATH:    str   = "data/taxonomy/embeddings.npy"
    TAXONOMY_IDS_PATH:    str   = "data/taxonomy/skill_ids.json"
    SIMILARITY_THRESHOLD: float = 0.65
    MAX_MISSING_SKILLS:   int   = 15
    ADZUNA_APP_ID:        str   = ""
    ADZUNA_APP_KEY:       str   = ""
    DEBUG:                bool  = False

    class Config:
        env_file = ".env"


settings = Settings()