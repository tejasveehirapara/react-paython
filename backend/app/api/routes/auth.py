from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginData, LoginRequest, UserCreate
from app.schemas.response import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse[None], status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, database: Session = Depends(get_db)) -> ApiResponse[None]:
    try:
        AuthService.create_user(database, payload)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return ApiResponse(message="User registered successfully.")


@router.post("/login", response_model=ApiResponse[LoginData])
def login(payload: LoginRequest, database: Session = Depends(get_db)) -> ApiResponse[LoginData]:
    user = AuthService.authenticate(database, str(payload.email), payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    session, access_token = AuthService.create_session(database, user)
    return ApiResponse(message="Login successful.", data=LoginData(session_id=session.id, access_token=access_token, expires_at=session.expires_at))
