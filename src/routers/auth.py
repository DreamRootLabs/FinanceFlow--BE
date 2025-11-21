from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status

from src.models.auth import (
    DemoAuthResponse,
    AuthResponse,
    RegisterRequest,
    LoginRequest,
)
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


# -------- dependency --------

def get_auth_service() -> AuthService:
    return AuthService()


# -------- handlers --------

def _create_demo_user(
    request: Request,
    service: AuthService = Depends(get_auth_service),
) -> DemoAuthResponse:
    return service.create_demo_user()


def _register(
    request: Request,
    body: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return service.register(body)


def _login(
    request: Request,
    body: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return service.login(body)


# -------- route registration --------

router.add_api_route(
    "/demo",
    endpoint=_create_demo_user,
    methods=["POST"],
    response_model=DemoAuthResponse,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    "/register",
    endpoint=_register,
    methods=["POST"],
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    "/login",
    endpoint=_login,
    methods=["POST"],
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
