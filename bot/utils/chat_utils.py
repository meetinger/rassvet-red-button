import asyncio
import html
from pprint import pprint

import aiogram.utils.markdown as md

from aiogram.exceptions import TelegramMigrateToChat, TelegramBadRequest
from aiogram.types import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot

from core.logs import get_logger
from db.models import Chat as ChatDB

logger = get_logger(__file__)


def error_format(e):
    return f"Произошла ошибка: {md.hblockquote(html.escape(str(e)))}"


async def delete_user_from_all_chats_and_send_alert(user: User, session: AsyncSession, bot: Bot):
    user_link = f"{md.hlink(user.full_name, f'tg://user?id={user.id}')}"
    alert_msg = f"Пользователь {user_link} был {md.hbold("ЗАДЕРЖАН!!!")}"
    user_id = user.id
    query = select(ChatDB)
    chats = (await session.execute(query)).scalars()

    async def get_user_chat_status(_user_id: int, _chat_id: int):
        nonlocal bot
        try:
            chat_member = await bot.get_chat_member(chat_id=_chat_id, user_id=_user_id)
            return chat_member.status
        except:
            raise

    async def process_user(_user_id: int, _chat_id: int):

        logger.debug(f"Processing user {_user_id} in chat {_chat_id}")

        try:
            user_chat_status = await get_user_chat_status(_user_id, _chat_id)
        except TelegramMigrateToChat as e:
            _chat_id = e.migrate_to_chat_id
            user_chat_status = await get_user_chat_status(_user_id, _chat_id)
        except Exception as e:
            logger.error(f"Error sending alert to chat {_chat_id}: {e}")
            await bot.send_message(_chat_id, f"{alert_msg}\nПроизошла ошибка. \n{error_format(e)}",
                                   )
            return

        if user_chat_status == 'creator':
            logger.error(f"Error user banning in chat {_chat_id}: User is creator")
            await bot.send_message(_chat_id,
                                   f"{alert_msg}\nОн является владельцем чата, поэтому его удалить нельзя", )
            return
        if user_chat_status == 'administrator':
            try:
                logger.debug(f"Demoting user {_user_id} in chat {_chat_id}")
                is_user_demoted = await bot.promote_chat_member(
                    chat_id=_chat_id,
                    user_id=_user_id,
                    is_anonymous=False,
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_pin_messages=False,
                    can_manage_topics=False
                )
                if not is_user_demoted:
                    logger.error(f"Error user banning in chat {_chat_id}: User was not demoted")
                    raise TelegramBadRequest
            except TelegramBadRequest as e:
                logger.error(f"User {_user_id} is admin in chat {_chat_id}: {str(e)}")
                await bot.send_message(_chat_id,
                                       f"{alert_msg}\nОн является администратором чата, боты не могут снимать админку, поэтому его удалить нельзя. \n{error_format(e)}",
                                       )
                return
        if user_chat_status in ('left', 'restricted', 'kicked'):
            return

        try:
            await bot.ban_chat_member(chat_id=_chat_id, user_id=_user_id)
            await bot.send_message(_chat_id, f"{alert_msg}.\nОн был удален из чата.")
        except Exception as e:
            logger.error(f"Error sending alert to chat {_chat_id}: {str(e)}")
            await bot.send_message(_chat_id,
                                   f"{alert_msg}\nПроизошла ошибка при удалении пользователя из чата. \n{error_format(e)}",
                                   )
            return

    await asyncio.gather(*[process_user(user_id, _chat.telegram_id) for _chat in chats])
