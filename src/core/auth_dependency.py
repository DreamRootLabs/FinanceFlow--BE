from __future__ import annotations

import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")

def get_current_owner_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extracts user_id (owner_id) from the JWT `sub` claim.
    Works for both demo and future real users.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    owner_id = payload.get("sub")  # this IS your user_id
    if not owner_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return owner_id