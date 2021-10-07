from typing import Union, Tuple, Optional, Dict

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner

from bot.config_reader import Config


async def fetch_admins(config: Config, bot: Bot) -> Tuple[bool, Union[Dict, str]]:
    result = {}
    try:
        admins = await bot.get_chat_administrators(config.group.main)
        for admin in admins:
            if admin.status == "creator":
                result[admin.user.id] = {"can_restrict_members": True}
            else:
                result[admin.user.id] = {"can_restrict_members": admin.can_restrict_members}
        return True, result
    except TelegramAPIError as ex:
        return False, str(ex)


async def check_rights_and_permissions(bot: Bot, chat_id: int) -> Tuple[bool, Optional[str]]:
    try:
        chat_member_info = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
    except TelegramAPIError as ex:
        return False, str(ex)
    if not isinstance(chat_member_info, ChatMemberAdministrator):
        return False, "Bot is not an administrator"
    if not chat_member_info.can_restrict_members or not chat_member_info.can_delete_messages:
        return False, "Bot needs 'restrict participants' and 'delete messages' permissions to work properly"
    return True, None
