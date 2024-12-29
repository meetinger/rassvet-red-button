from aiogram.types import Chat
from sqlalchemy import select

from core.logs import get_logger
from db.models.chats import Chat as ChatDB

from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__file__)

async def get_or_create_chat(chat: Chat, session: AsyncSession) -> ChatDB:
    chat_db = await get_chat_or_none_by_telegram_id(chat.id, session)
    if chat_db is None:
        logger.info(f"Creating chat: {chat.model_dump()}")
        chat_db = ChatDB(
            telegram_id=chat.id,
            title=chat.title,
            description=chat.description,
            # owner_user_id=chat.owner_user_id,
        )
        session.add(chat_db)
        await session.flush()
    logger.info(f"Chat: {chat_db.to_dict()}")
    return chat_db

async def get_chat_or_none_by_telegram_id(telegram_id: int, session: AsyncSession) -> ChatDB:
    return (await session.execute(select(ChatDB).where(ChatDB.telegram_id == telegram_id))).scalars().one_or_none()