from datetime import datetime
from pydantic import BaseModel

class DemoAuthResponse(BaseModel):
    demo_id: str
    token: str
    expires_at: datetime