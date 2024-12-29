from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bot.decorators import inject_user
from bot.keyboards.keyboards import get_bot_keyboard_jail, get_bot_keyboard_confirm_jail
from bot.utils.chat_utils import delete_user_from_all_chats_and_send_alert
from core.logs import get_logger
from db.db_loader import get_session
from db.models import User as UserDB
from bot.cruds import chats as chats_cruds

router = Router()

logger = get_logger(__file__)

class JailStates(StatesGroup):
    confirm_await = State()
    confirmed = State()


@router.message(CommandStart())
@inject_user
async def start_handler(user_db: UserDB, message: types.Message):
    await message.answer("""Привет""", reply_markup=get_bot_keyboard_jail())

@router.message(lambda message: (message.text or "").lower() == "МЕНЯ ЗАДЕРЖАЛИ".lower())
@inject_user
async def jail_handler(user_db: UserDB, message: types.Message, state: FSMContext):
    await state.set_state(JailStates.confirm_await)
    await message.answer("Тебя точно задержали?", reply_markup=get_bot_keyboard_confirm_jail())

# @router.message(lambda message: message.text.lower() == "МЕНЯ ПРАВДА ЗАДЕРЖАЛИ".lower())
@router.message(JailStates.confirm_await)
@inject_user
async def jail_handler(user_db: UserDB, message: types.Message, state: FSMContext):
    if message.text.lower() == "МЕНЯ ПРАВДА ЗАДЕРЖАЛИ".lower():
        await state.set_state(JailStates.confirmed)
        await message.answer("Дропаем базу...", reply_markup=get_bot_keyboard_jail())
        async with get_session() as session:
            await delete_user_from_all_chats_and_send_alert(user_db, session, message.bot)
    else:
        await message.answer("Попробуй еще раз", reply_markup=get_bot_keyboard_jail())


@router.message(lambda message: message.chat.type in ["group", "supergroup"])
@inject_user
async def track_users_messages_in_chat(user_db: UserDB, message: types.Message):
    logger.info(f'Tracked message in chat: {message.chat.id}')
    async with get_session() as session:
        chat_db = await chats_cruds.get_or_create_chat(message.chat, session)
        # await chat_db.add_user(user_db.telegram_id, session)


@router.chat_member(lambda event: event.chat.type in ["group", "supergroup"])
@inject_user
async def track_chat_members(user_db: UserDB, event: ChatMemberUpdated):
    async with get_session() as session:
        chat_db = await chats_cruds.get_or_create_chat(event.chat, session)
        # await chat_db.add_user(user_db.telegram_id, session)