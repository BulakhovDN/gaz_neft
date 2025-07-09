from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.models.user import User
from src.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.get_current_user_by_token(token)


def admin_required(user: User = Depends(get_current_user)):
    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Требуется роль администратора")
    return user


async def require_user_role(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("User", "Admin"):
        raise HTTPException(
            status_code=403, detail="Требуется роль пользователя или администратора"
        )
    return current_user
