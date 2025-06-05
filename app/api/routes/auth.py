from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.domain.schemas.auth import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest
from app.domain.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """ユーザー登録"""
    return AuthService.create_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """ログイン"""
    return AuthService.login(db, credentials)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """リフレッシュトークンを使用して新しいアクセストークンを取得"""
    return AuthService.refresh_access_token(db, refresh_request.refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """現在のユーザー情報取得"""
    return current_user
