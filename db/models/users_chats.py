import uuid

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db_loader import Base


class UserChat(Base):
    __tablename__ = "users_chats"

    # id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(ForeignKey("chats.telegram_id"), primary_key=True)