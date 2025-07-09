from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.core.settings import settings
from src.db.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def authenticate_user(self, email: str, password: str) -> str:
        async with self.db.begin():
            result = await self.db.execute(select(User).filter(User.email == email))
            user = result.scalars().first()

            if not user or not self.verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=400, detail="Неверное имя пользователя или пароль"
                )

            access_token_expires = timedelta(minutes=self.token_expire_minutes)
            return self.create_access_token(
                data={"sub": str(user.id)}, expires_delta=access_token_expires
            )

    async def get_current_user_by_token(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: int = int(payload.get("sub"))
        except (JWTError, TypeError, ValueError):
            raise credentials_exception

        async with self.db.begin():
            result = await self.db.execute(select(User).filter(User.id == user_id))
            user = result.scalars().first()
            if user is None:
                raise credentials_exception
            return user
