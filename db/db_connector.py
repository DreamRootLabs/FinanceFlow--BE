import os
import json
import base64
from functools import lru_cache
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
from loguru import logger

ENV_PROJECT_ID = "FIREBASE_PROJECT_ID"
ENV_CRED_FILE = "FIREBASE_CREDENTIALS_FILE"      
ENV_CRED_B64 = "FIREBASE_CREDENTIALS_BASE64"

# 1) Try base64 env 
def _build_credentials() -> credentials.Certificate:
    """
    Build Firebase credentials either from base64 env or a JSON file path.
    """
    b64 = os.getenv(ENV_CRED_B64)
    if b64:
        try:
            decoded = base64.b64decode(b64)
            data = json.loads(decoded)
            logger.info("Using Firebase credentials from {}", ENV_CRED_B64)
            return credentials.Certificate(data)
        except Exception as e:
            raise RuntimeError(f"Failed to decode Firebase credentials from {ENV_CRED_B64}: {e}")

# 2) Try file path (good for local development)
    path = os.getenv(ENV_CRED_FILE)
    if not path:
        raise RuntimeError(f"Set {ENV_CRED_FILE} or {ENV_CRED_B64}")

    p = Path(path)
    if not p.exists():
        raise RuntimeError(f"Credential file not found at {p}")

    logger.info("Using Firebase credentials file at {}", p)
    return credentials.Certificate(str(p))

@lru_cache(maxsize=1)
def get_firestore() -> firestore.Client:
    """
    Lazily initialize and return a shared Firestore client.

    Priority:
    - If FIREBASE_CREDENTIALS_BASE64 or FIREBASE_CREDENTIALS_FILE is set:
        use explicit Firebase credentials.
    - Otherwise:
        rely on default GCP credentials (Cloud Run / GCE service account).
    """
    project_id = os.getenv(ENV_PROJECT_ID)
    if not project_id:
        raise RuntimeError(f"{ENV_PROJECT_ID} is not set")

    try:
        try:
            # Reuse existing app if initialized
            app = firebase_admin.get_app()
            logger.debug("Reusing existing Firebase app: {}", app.name)
        except ValueError:
            # Not initialized yet → choose credentials strategy
            if os.getenv(ENV_CRED_B64) or os.getenv(ENV_CRED_FILE):
                cred = _build_credentials()
                logger.info("Initializing Firebase app with explicit credentials")
                firebase_admin.initialize_app(cred, {"projectId": project_id})
            else:
                # Cloud Run / GCP mode: use default application credentials
                logger.info(
                    "Initializing Firebase app with default application credentials "
                    "(no {} or {} set)", ENV_CRED_FILE, ENV_CRED_B64
                )
                firebase_admin.initialize_app(options={"projectId": project_id})

        return firestore.client()
    except Exception as e:
        logger.exception("Failed to initialize Firestore")
        raise RuntimeError(f"Failed to initialize Firestore: {e}")