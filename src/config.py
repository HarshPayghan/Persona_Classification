import os
from dotenv import load_dotenv

load_dotenv()

# Gemini

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Embedding Model

EMBEDDING_MODEL = "text-embedding-004"

# Generation Model

LLM_MODEL = "gemini-2.5-flash"

# Vector Database

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "support_kb"

# Chunking Settings

CHUNK_SIZE = 400
CHUNK_OVERLAP = 40

# Retrieval Settings

TOP_K_RESULTS = 3

# Escalation Threshold

CONFIDENCE_THRESHOLD = 0.25

# Sensitive Keywords

SENSITIVE_TOPICS = [
"refund",
"billing",
"payment dispute",
"legal",
"chargeback",
"account deletion",
"cancel subscription"
]
