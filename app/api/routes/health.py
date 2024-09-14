from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    """
    health check.
    """
    return {
        "success": True,
        "message": "server is up"
    }
