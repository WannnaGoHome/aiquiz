from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


# ---------- User ----------
async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User(**data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_telegram(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def list_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def update_user(session: AsyncSession, telegram_id: int, data: UserUpdate) -> User:
    user = await get_user(session, telegram_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user


# async def delete_user(session: AsyncSession, telegram_id: int) -> None:
#     user = await session.execute(select(User).where(User.telegram_id == telegram_id))
#     await session.delete(user)
#     await session.commit()

async def delete_user(session: AsyncSession, telegram_id: int) -> None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()  # Получаем объект User
    
    if user:
        await session.delete(user)  # Удаляем объект, а не результат запроса
        await session.commit()