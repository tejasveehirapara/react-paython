from fastapi import APIRouter

from app.schemas.response import ApiResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=ApiResponse[None])
async def health_check() -> ApiResponse[None]:
    return ApiResponse(message="API is running")
