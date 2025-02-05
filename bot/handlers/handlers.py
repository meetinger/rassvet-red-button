from aiogram import types, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ChatMemberUpdated, User
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.decorators import inject_user
from bot.keyboards.keyboards import get_bot_keyboard_jail, get_bot_keyboard_confirm_jail
from bot.utils.chat_utils import delete_user_from_all_chats_and_send_alert
from core.logs import get_logger
from db.db_loader import get_session
from bot.cruds import chats as chats_cruds

router = Router()

logger = get_logger(__file__)

class JailStates(StatesGroup):
    confirm_await = State()
    confirmed = State()


@router.message(lambda message: (message.text or "").lower() == "МЕНЯ ЗАДЕРЖАЛИ".lower()
                                and message.chat.type == "private")
@inject_user
async def jail_handler(user: User, message: types.Message, state: FSMContext):
    logger.info(f'User {user.id} pressed "МЕНЯ ЗАДЕРЖАЛИ"')
    await state.set_state(JailStates.confirm_await)
    await message.answer("Попробуй еще раз, может в следующий раз задержат)0)))", reply_markup=get_bot_keyboard_confirm_jail())

@router.message(JailStates.confirm_await)
@inject_user
async def jail_handler(user: User, message: types.Message, state: FSMContext):
    logger.info(f'User {user.id} pressed "{message.text}"')
    if (message.text or "").lower() == "МЕНЯ ПРАВДА ЗАДЕРЖАЛИ".lower():
        await state.set_state(JailStates.confirmed)
        await message.answer("Вас поняли...", reply_markup=get_bot_keyboard_jail())
        async with get_session() as session:
            await delete_user_from_all_chats_and_send_alert(user, session, message.bot)
    else:
        await message.answer("Попробуй еще раз, может в следующий раз задержат)0)))", reply_markup=get_bot_keyboard_jail())


@router.message(lambda message: message.chat.type in ["group", "supergroup"])
@inject_user
async def track_users_messages_in_chat(user: User, message: types.Message):
    logger.info(f'Tracked message in chat: {message.chat.id}')
    async with get_session() as session:
        chat_db = await chats_cruds.get_or_create_chat(message.chat, session)
        # await chat_db.add_user(user_db.telegram_id, session)


@router.chat_member(lambda event: event.chat.type in ["group", "supergroup"])
@inject_user
async def track_chat_members(user: User, event: ChatMemberUpdated):
    logger.info(f'Tracked chat member in chat: {event.chat.id}')
    async with get_session() as session:
        chat_db = await chats_cruds.get_or_create_chat(event.chat, session)
        # await chat_db.add_user(user_db.telegram_id, session)

@router.message()
@inject_user
async def start_handler(user: User, message: types.Message):
    logger.info(f'User {user.id} pressed "{message.text}"')
    await message.answer("""Привет""", reply_markup=get_bot_keyboard_jail())