from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.common.db import get_async_session
from sqlalchemy.orm import selectinload
import logging

from app.users.models import User
from app.users.schemas import UserCreate
from app.events.models import Event, EventStatus
from app.users import schemas, crud

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

# @router.post("/register")
# async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):

#     result = await session.execute(select(User).where(User.telegram_id == user_data.telegram_id))

#     existing_user = result.scalar_one_or_none()

#     if existing_user:
#         raise HTTPException(status_code=400, detail={ "status": "error", "code": "NICKNAME_TAKEN", "message": "Этот никнейм уже занят" })

#     new_user = User(telegram_id=user_data.telegram_id, nickname=user_data.nickname)

#     result = await session.execute(select(Event).where(Event.status == EventStatus.REGISTRATION))

#     active_event = result.scalar_one_or_none()

#     if not active_event:
#         raise HTTPException(status_code=400, detail={ "status": "error", "code": "GAME_ALREADY_STARTED", "message": "Регистрация уже завершена либо игра ещё не начата" })

#     active_event.players.append(new_user)

#     session.add(new_user)
#     await session.commit()
#     await session.refresh(new_user)

#     return { "status": "success" }

@router.post("/register")
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Запрос на регистрацию: telegram_id={user_data.telegram_id}, nickname={user_data.nickname}")
        
        result = await session.execute(select(User).where(User.telegram_id == user_data.telegram_id))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "code": "NICKNAME_TAKEN",
                "message": "Этот никнейм уже занят"
            })

        new_user = User(telegram_id=user_data.telegram_id, nickname=user_data.nickname)

        result = await session.execute(select(Event).where(Event.status == EventStatus.REGISTRATION))
        active_event = result.scalar_one_or_none()
        if not active_event:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "code": "GAME_ALREADY_STARTED",
                "message": "Регистрация уже завершена либо игра ещё не начата"
            })

        active_event.players.append(new_user)
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        logger.info(f"Успешная регистрация пользователя {new_user.nickname}")
        return {"status": "success"}

    except Exception as e:
        logger.exception("Ошибка при регистрации пользователя")
        raise


# @router.post("/check_admin")
# async def check_admin(telegram_id: int, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(User).where(User.telegram_id == telegram_id))
#     user = result.scalar_one_or_none()
#     if not user or not user.is_admin:
#         raise HTTPException(status_code=403, detail="Admin rights required")
#     return {"status": "success"}
@router.post("/check_admin")
async def check_admin(telegram_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"is_admin": False}  # или 404
    return {"is_admin": user.is_admin}


# @router.post("/", response_model=schemas.UserRead)
# async def create_user(data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
#     return await crud.create_user(session, data)


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    return await crud.list_users(session)


@router.get("/{telegram_id}", response_model=schemas.UserRead)
async def get_user(telegram_id: int, session: AsyncSession = Depends(get_async_session)):
    return await crud.get_user(session, telegram_id=telegram_id)


# @router.put("/{user_id}", response_model=schemas.UserRead)
# async def update_user(user_id: int, data: schemas.UserUpdate, session: AsyncSession = Depends(get_async_session)):
#     return await crud.update_user(session, user_id, data)


@router.delete("/{telegram_id}")
async def delete_user(telegram_id: int, session: AsyncSession = Depends(get_async_session)):
    await crud.delete_user(session, telegram_id=telegram_id)
    return {"detail": "User deleted"}
