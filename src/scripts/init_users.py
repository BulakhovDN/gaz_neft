from passlib.context import CryptContext
from sqlalchemy import select

from src.db.database import async_session
from src.db.models.user import User
from src.models.emums import RoleEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(username: str, email: str, password: str, role: RoleEnum):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        if result.scalars().first():
            print(f"[!] User '{username}' уже существует.")
            return

        user = User(
            username=username,
            email=email,
            hashed_password=pwd_context.hash(password),
            role=role,
        )
        session.add(user)
        await session.commit()
        print(f"[+] Пользователь '{username}' с ролью '{role.value}' создан.")


async def init_users():
    await create_user("user", "user@mail.ru", "user123", RoleEnum.user)
    await create_user("user1", "user1@mail.ru", "user1231", RoleEnum.user)
    await create_user("admin", "admin@mail.ru", "admin123", RoleEnum.admin)
