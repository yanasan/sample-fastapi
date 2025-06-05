from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.api.dependencies.database import get_db
from app.utils.auth import AuthUtils
from app.domain.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = AuthUtils.decode_jwt(credentials.credentials)
    except JWTError:
        raise credentials_exception
    
    user_id = payload.get("sub")
    token_type = payload.get("type")
    
    if user_id is None or token_type != "access":
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if user is None:
        raise credentials_exception
    return user
