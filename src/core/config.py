import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
DEMO_TOKEN_TTL_HOURS = int(os.getenv("DEMO_TOKEN_TTL_HOURS", "24"))

def get_demo_ttl() -> timedelta:
    return timedelta(hours=DEMO_TOKEN_TTL_HOURS)