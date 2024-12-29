import uuid

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from db.db_loader import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    telegram_username: Mapped[str] = mapped_column(nullable=True)

    login: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)

    @property
    def full_name(self):
        return f'{self.first_name}{" " + self.last_name if self.last_name else ""}'

    @property
    def user_link(self):
        return f'<a href="tg://user?id={self.telegram_id}">{self.full_name}</a>'