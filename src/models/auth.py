from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated


class DemoAuthResponse(BaseModel):
    user_id: str
    token: str
    expires_at: datetime


class AuthResponse(BaseModel):
    user_id: str
    token: str
    expires_at: datetime
    is_demo: bool


class RegisterRequest(BaseModel):
    email: EmailStr
    # enforce min/max length to avoid bcrypt error
    password: Annotated[str, StringConstraints(min_length=8, max_length=72)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str