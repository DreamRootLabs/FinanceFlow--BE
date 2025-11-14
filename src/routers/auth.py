from fastapi import APIRouter

from src.models.auth import DemoAuthResponse
from src.services.demo_auth_service import DemoAuthService

router = APIRouter(prefix="/auth", tags=["auth"])

_demo_service = DemoAuthService()

@router.post("/demo", response_model=DemoAuthResponse)
def create_demo():
    """
    Start a new demo session:
    - Creates demo_sessions/{demo_id}
    - Seeds default categories
    - Returns demo_id + token + expires_at
    """
    return _demo_service.create_demo()