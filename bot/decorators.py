from bot.cruds import users as users_cruds

import functools

from db.db_loader import get_session


def inject_user(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        telegram_user = args[0].from_user
        async with get_session() as session:
            user_db = await users_cruds.get_or_create_user(telegram_user, session)
        return await func(user_db, *args, **kwargs)

    return wrapper
