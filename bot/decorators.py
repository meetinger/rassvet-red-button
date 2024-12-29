import functools


def inject_user(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        telegram_user = args[0].from_user
        return await func(telegram_user, *args, **kwargs)

    return wrapper
