from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.logs import get_logger
from core.settings import settings
from bot.handlers.handlers import router as start_router

logger = get_logger(__file__)
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def register_handlers():
    dp.include_router(start_router)


async def run_bot():
    logger.info("Starting bot...")

    register_handlers()

    logger.info("Starting polling...")
    await dp.start_polling(bot)