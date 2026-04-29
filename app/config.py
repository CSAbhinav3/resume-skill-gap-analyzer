from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:         str   = "sqlite+aiosqlite:///./dev.db"
    GEMINI_API_KEY:       str                                        # ← renamed
    GEMINI_MODEL:         str   = "gemini-2.0-flash"                # ← fast + cheap
    EMBEDDING_MODEL:      str   = "all-MiniLM-L6-v2"               # unchanged
    TAXONOMY_EMB_PATH:    str   = "data/taxonomy/embeddings.npy"
    TAXONOMY_IDS_PATH:    str   = "data/taxonomy/skill_ids.json"
    SIMILARITY_THRESHOLD: float = 0.75
    MAX_MISSING_SKILLS:   int   = 15
    DEBUG:                bool  = False

    class Config:
        env_file = ".env"


settings = Settings()