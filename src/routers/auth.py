from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
import uuid

import jwt
from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from db.db_connector import get_firestore

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")
DEMO_TOKEN_TTL_HOURS = int(os.getenv("DEMO_TOKEN_TTL_HOURS", "24"))


class DemoAuthResponse(BaseModel):
    user_id: str
    token: str
    expires_at: datetime


# -------- handler --------

def _create_demo_user(request: Request) -> DemoAuthResponse:
    db = get_firestore()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=DEMO_TOKEN_TTL_HOURS)

    # You can also use db.collection("users").document() for Firestore auto-id
    user_id = f"demo_{uuid.uuid4().hex[:12]}"

    user_doc = {
        "is_demo": True,
        "email": None,
        "created_at": now,
        "expires_at": expires_at,
    }

    db.collection("users").document(user_id).set(user_doc)

    payload = {
        "sub": user_id,
        "is_demo": True,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return DemoAuthResponse(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )


# -------- route registration --------

router.add_api_route(
    "/demo",
    endpoint=_create_demo_user,
    methods=["POST"],
    response_model=DemoAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
