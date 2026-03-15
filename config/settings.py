import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

    VECTOR_DB_PATH = "data/faiss_index"

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100

settings = Settings()