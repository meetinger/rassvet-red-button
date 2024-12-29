from aiogram.types import User as TelegramUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logs import get_logger
from db.models import User as UserDB

logger = get_logger(__file__)

async def get_or_create_user(telegram_user: TelegramUser, session: AsyncSession) -> UserDB:
    user_db = await get_user_or_none_by_telegram_id(telegram_user.id, session)
    if user_db is None:
        logger.info(f"Creating user: {telegram_user.model_dump()}")
        user_db = UserDB(
            telegram_id=telegram_user.id,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            telegram_username=telegram_user.username,
        )
        session.add(user_db)
        await session.flush()
    logger.info(f"User: {user_db.to_dict()}")
    return user_db

async def get_user_or_none_by_telegram_id(telegram_id: int, session: AsyncSession) -> UserDB:
    return (await session.execute(select(UserDB).where(UserDB.telegram_id == telegram_id))).scalars().one_or_none()