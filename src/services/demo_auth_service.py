import uuid
from datetime import datetime, timezone

from src.core.auth import create_demo_token
from src.models.auth import DemoAuthResponse
from src.repos.demo_session_repo import DemoSessionRepo

class DemoAuthService:
    def __init__(self, repo: DemoSessionRepo | None = None):
        self.repo = repo or DemoSessionRepo()

    def create_demo(self) -> DemoAuthResponse:
        # 1) generate demo_id (also used as owner_id)
        demo_id = f"demo_{uuid.uuid4().hex[:12]}"

        # 2) create token (gives us token + expires_at)
        token_info = create_demo_token(demo_id)
        token = token_info["token"]
        expires_at = token_info["expires_at"]

        # 3) write demo_sessions doc
        self.repo.create_demo_session(demo_id, expires_at)

        # 4) seed default categories
        self.repo.seed_default_categories(demo_id)

        # 5) (optional) seed_example_transactions(demo_id)

        # 6) return response
        return DemoAuthResponse(
            demo_id=demo_id,
            token=token,
            expires_at=expires_at,
        )