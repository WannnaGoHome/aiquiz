from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from sqlalchemy import select

from app.common.db import get_async_session
from app.users.models import User


async def init_admin(telegram_id: int, nickname: str, session: AsyncSession):

    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=telegram_id,
            nickname=nickname,
            is_admin=True,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        print(f"✅ Админ {nickname} создан")
    else:
        if not user.is_admin:
            user.is_admin = True
            await session.commit()
            print(f"⚡ Пользователь {nickname} получил права админа")
        else:
            print(f"ℹ️ Админ {nickname} уже существует")

class CurrentUser:
    def __init__(self, require_admin: bool = False):
        self.require_admin = require_admin

    async def __call__(self, session: AsyncSession = Depends(get_async_session), telegram_id: int = 0):
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(401, "User not found")
        if self.require_admin and not user.is_admin:
            raise HTTPException(403, "Admin rights required")
        return user
