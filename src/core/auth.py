from datetime import datetime, timezone
from typing import Dict, Any

import jwt  # pyjwt

from src.core.config import SECRET_KEY, get_demo_ttl

ALGORITHM = "HS256"

def create_demo_token(owner_id: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    exp = now + get_demo_ttl()

    payload = {
        "sub": owner_id,    # subject = owner_id (demo_id)
        "is_demo": True,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "token": token,
        "expires_at": exp
    }

def decode_token(token: str) -> Dict[str, Any]:
    # Raises jwt exceptions if invalid/expired – you can catch in dependency
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])