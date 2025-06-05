from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.user import User
from app.domain.schemas.auth import UserCreate, UserLogin, Token
from app.utils.crypt import PasswordHasher
from app.utils.auth import AuthUtils
from app.core.config import settings


class AuthService:
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
    def authenticate_user(db: Session, user_data: UserLogin) -> Token:
        user = db.query(User).filter(
            User.email == user_data.email,
            User.is_deleted == False
        ).first()
        
        if not user or not PasswordHasher.verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthUtils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
