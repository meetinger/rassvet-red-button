import uuid
import datetime as dt
from sqlalchemy import BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.db_loader import Base


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))
    action: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    datetime: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True),
                                                  default=lambda: dt.datetime.now(dt.timezone.utc))