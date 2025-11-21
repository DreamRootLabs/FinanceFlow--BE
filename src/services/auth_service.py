from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from db.db_connector import get_firestore
from src.models.auth import (
    DemoAuthResponse,
    AuthResponse,
    RegisterRequest,
    LoginRequest,
)

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")
ALGORITHM = "HS256"

DEMO_TOKEN_TTL_HOURS = int(os.getenv("DEMO_TOKEN_TTL_HOURS", "24"))
ACCESS_TOKEN_TTL_HOURS = int(os.getenv("ACCESS_TOKEN_TTL_HOURS", "168"))

# Use pbkdf2_sha256 (no 72-byte limit like bcrypt)
_pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def _hash_password(password: str) -> str:
    # Length limits are already enforced by Pydantic (min/max),
    # so just hash here.
    return _pwd_context.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


class AuthService:
    def __init__(self, db=None):
        self.db = db or get_firestore()

    def _create_token(
        self,
        user_id: str,
        is_demo: bool,
        expires_delta: timedelta,
    ) -> AuthResponse:
        now = datetime.now(timezone.utc)
        expires_at = now + expires_delta

        payload = {
            "sub": user_id,
            "is_demo": is_demo,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return AuthResponse(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_demo=is_demo,
        )

    # -------- Demo auth --------
    def create_demo_user(self) -> DemoAuthResponse:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=DEMO_TOKEN_TTL_HOURS)

        user_id = f"demo_{uuid.uuid4().hex[:12]}"

        self.db.collection("users").document(user_id).set(
            {
                "is_demo": True,
                "email": None,
                "created_at": now,
                "expires_at": expires_at,
            }
        )

        token = jwt.encode(
            {
                "sub": user_id,
                "is_demo": True,
                "iat": int(now.timestamp()),
                "exp": int(expires_at.timestamp()),
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        return DemoAuthResponse(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

    # -------- Real auth: register --------
    def register(self, body: RegisterRequest) -> AuthResponse:
        email = _normalize_email(body.email)

        # Check if email already exists
        docs = (
            self.db.collection("users")
            .where("email", "==", email)
            .limit(1)
            .stream()
        )
        for _ in docs:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        now = datetime.now(timezone.utc)
        doc_ref = self.db.collection("users").document()
        user_id = doc_ref.id

        doc_ref.set(
            {
                "email": email,
                "password_hash": _hash_password(body.password),
                "is_demo": False,
                "created_at": now,
                "expires_at": None,
            }
        )

        return self._create_token(
            user_id=user_id,
            is_demo=False,
            expires_delta=timedelta(hours=ACCESS_TOKEN_TTL_HOURS),
        )

    # -------- Real auth: login --------
    def login(self, body: LoginRequest) -> AuthResponse:
        email = _normalize_email(body.email)

        docs = (
            self.db.collection("users")
            .where("email", "==", email)
            .limit(1)
            .stream()
        )

        user_doc = None
        user_id = None

        for doc in docs:
            user_doc = doc.to_dict() or {}
            user_id = doc.id
            break

        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if user_doc.get("is_demo"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This is a demo user. Use /auth/demo instead.",
            )

        hashed = user_doc.get("password_hash")
        if not hashed or not _verify_password(body.password, hashed):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return self._create_token(
            user_id=user_id,
            is_demo=False,
            expires_delta=timedelta(hours=ACCESS_TOKEN_TTL_HOURS),
        )
