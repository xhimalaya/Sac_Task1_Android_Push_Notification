import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/pushdb"
)

# VAPID (Web Push)
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_EMAIL = os.getenv("VAPID_EMAIL", "mailto:himalayamandal@gmail.com")

# Basic sanity checks (fail fast)
if not VAPID_PRIVATE_KEY:
    print("WARNING: VAPID_PRIVATE_KEY is not set")

if not VAPID_PUBLIC_KEY:
    print("WARNING: VAPID_PUBLIC_KEY is not set")
