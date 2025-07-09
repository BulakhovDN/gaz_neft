from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.models.user import Token
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    service = AuthService(db)
    access_token = await service.authenticate_user(
        form_data.username, form_data.password
    )
    return {"access_token": access_token, "token_type": "bearer"}
