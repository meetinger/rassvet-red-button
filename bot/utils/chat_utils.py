from aiogram.exceptions import TelegramMigrateToChat, TelegramBadRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot

from core.logs import get_logger
from db.models import Chat as ChatDB
from db.models.users import User as UserDB

logger = get_logger(__file__)

async def delete_user_from_all_chats_and_send_alert(user_db: UserDB, session: AsyncSession, bot: Bot):
    alert_msg = f"Пользователь {user_db.user_link} был ЗАДЕРЖАН!"

    query = select(ChatDB)
    chats = (await session.execute(query)).scalars()
    for chat in chats:
        chat_id = chat.telegram_id
        try:
            await bot.send_message(chat_id=chat_id, text=alert_msg)
        except TelegramMigrateToChat as e:
            chat_id = e.migrate_to_chat_id
            await bot.send_message(chat_id=chat_id, text=alert_msg)
        except Exception as e:
            logger.error(f"Error sending alert to chat {chat_id}: {e}")
        try:
            await bot.promote_chat_member(
                chat_id=chat_id,
                user_id=user_db.telegram_id,
                is_anonymous=False,
                can_manage_chat=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
            )
            is_banned = await bot.ban_chat_member(chat_id=chat_id, user_id=user_db.telegram_id)
            print(f'Ban status: {is_banned} Chat id: {chat_id}')
            # await bot.unban_chat_member(chat_id=chat_id, user_id=user_db.telegram_id)
            await bot.send_message(chat_id=chat_id, text=f'Пользователь {user_db.user_link} удалён из чата')
        except Exception as e:
            try:
                await bot.send_message(chat_id=chat_id, text=f'Ошибка удаления пользователя {user_db.user_link}: {e}')
            except:
                pass