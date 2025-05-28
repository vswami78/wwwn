import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUBMISSION_DEADLINE = os.getenv("SUBMISSION_DEADLINE")

if not DB_URL:
    raise RuntimeError("DB_URL environment variable not set.")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set.")
if not SUBMISSION_DEADLINE:
    raise RuntimeError("SUBMISSION_DEADLINE environment variable not set.")

# You might also want to add type casting or further validation if necessary
