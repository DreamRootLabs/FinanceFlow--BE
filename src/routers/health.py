from fastapi import APIRouter

# Create APIRouter instance
health_router = APIRouter(prefix="", tags=["Health"])

@health_router.get("/")
async def health_check():
    """
    GET health check
    """
    return {"status": "PayFlow backend server is running"}