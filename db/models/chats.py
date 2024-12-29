import uuid

from sqlalchemy import BigInteger, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped

from core.logs import get_logger
from db.db_loader import Base
from db.models.users_chats import UserChat

logger = get_logger(__file__)

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    async def add_user(self, user_telegram_id: int, session: AsyncSession):
        logger.info(f"Adding user {user_telegram_id} to chat {self.telegram_id}")
        if (await session.execute(
            select(UserChat).
                    where(UserChat.user_telegram_id == user_telegram_id,
                          UserChat.chat_telegram_id == self.telegram_id))).scalars().one_or_none() is None:

            logger.info(f"User {user_telegram_id} added to chat {self.telegram_id}")
            user_chat = UserChat(user_telegram_id=user_telegram_id, chat_telegram_id=self.telegram_id)
            session.add(user_chat)
            return await session.flush()