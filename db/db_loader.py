from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, DeclarativeMeta, class_mapper

from core.settings import settings

class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self, include_relationships=False):

        columns = class_mapper(self.__class__).columns
        result = {column.key: getattr(self, column.key) for column in columns}

        if not include_relationships:
            return result

        for relation in class_mapper(self.__class__).relationships:
            related_value = getattr(self, relation.key)
            if related_value is not None:
                if relation.uselist:
                    result[relation.key] = [self.model_to_dict(item) for item in related_value]
                else:
                    result[relation.key] = self.model_to_dict(related_value)

        return result

engine = create_async_engine(settings.db_url, echo=False)

session_maker = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        async with session.begin():
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()