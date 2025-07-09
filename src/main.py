import asyncio
import sys

import uvicorn
from fastapi import FastAPI

from src.core.settings import settings
from src.routers import admin
from src.routers import auth
from src.routers import note
from src.scripts.init_users import init_users

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(note.router, prefix="/note", tags=["note"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "runserver"

    if command == "runserver":
        uvicorn.run(
            "src.main:app", host=settings.HOST_APP, port=settings.PORT_APP, reload=True
        )
    elif command == "init":
        asyncio.run(init_users())
    else:
        print(f"[!] Неизвестная команда: {command}")


if __name__ == "__main__":
    main()
