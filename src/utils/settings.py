import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "../db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
IONOS_API_BASE_URL = os.getenv("IONOS_API_BASE_URL", "")
IONOS_API_TOKEN = SecretStr(os.getenv("IONOS_API_TOKEN", ""))
LLM_MODEL = os.getenv("LLM_MODEL", "")
