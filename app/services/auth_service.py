from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import JWTError
from app.domain.models.user import User
from app.domain.schemas.auth import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest
from app.utils.crypt import PasswordHasher
from app.utils.auth import AuthUtils
from app.core.config import settings


class AuthService:
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        # メールアドレスの重複チェック
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # パスワードハッシュ化
        hashed_password = PasswordHasher.hash_password(user_data.password)
        
        # ユーザー作成
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def login(db: Session, credentials: UserLogin) -> TokenResponse:
        user = db.query(User).filter(
            User.email == credentials.email,
            User.is_deleted == False
        ).first()
        
        if not user or not PasswordHasher.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        payload = {
            "email": user.email,
            "name": user.name
        }
        
        access_token = AuthUtils.create_access_token(
            sub=str(user.id), 
            exp_minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES, 
            payload=payload
        )
        
        refresh_token = AuthUtils.create_refresh_token(
            sub=str(user.id), 
            exp_days=AuthService.REFRESH_TOKEN_EXPIRE_DAYS, 
            payload=payload
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            expires_in=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        try:
            decoded = AuthUtils.decode_jwt(refresh_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = decoded.get("sub")
        token_type = decoded.get("type")
        
        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        payload = {
            "email": user.email,
            "name": user.name
        }
        
        new_access_token = AuthUtils.create_access_token(
            sub=str(user.id), 
            exp_minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES, 
            payload=payload
        )
        
        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            expires_in=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
