from typing import Dict

from aiogram import Bot
from aiogram.types import ChatMemberAdministrator

from bot.config_reader import config


async def fetch_admins(bot: Bot) -> Dict:
    result = {}
    admins = await bot.get_chat_administrators(config.group.main)
    for admin in admins:
        if admin.status == "creator":
            result[admin.user.id] = {"can_restrict_members": True}
        else:
            result[admin.user.id] = {"can_restrict_members": admin.can_restrict_members}
    return result


async def check_rights_and_permissions(bot: Bot, chat_id: int):
    chat_member_info = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
    if not isinstance(chat_member_info, ChatMemberAdministrator):
        raise PermissionError("Bot is not an administrator")
    if not chat_member_info.can_restrict_members or not chat_member_info.can_delete_messages:
        raise PermissionError("Bot needs 'restrict participants' and 'delete messages' permissions to work properly")

