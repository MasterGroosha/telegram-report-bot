from aiogram import Bot
from aiogram.types import (
    ChatMemberAdministrator, ChatMemberOwner, ChatMemberBanned, ChatMemberLeft, ChatMemberRestricted
)


async def check_bot_rights_main_group(
        bot: Bot,
        main_group_id: int,
):
    chat_member_info = await bot.get_chat_member(
        chat_id=main_group_id, user_id=bot.id
    )
    if not isinstance(chat_member_info, ChatMemberAdministrator):
        raise PermissionError("bot is not an administrator")
    if not chat_member_info.can_restrict_members or not chat_member_info.can_delete_messages:
        raise PermissionError("bot needs 'restrict participants' and 'delete messages' permissions to work properly")

async def check_bot_rights_reports_group(
        bot: Bot,
        reports_group_id: int,
):
    chat_member_info = await bot.get_chat_member(
        chat_id=reports_group_id, user_id=bot.id
    )
    if isinstance(chat_member_info, (ChatMemberLeft, ChatMemberBanned)):
        raise PermissionError("bot is banned from the group")
    if isinstance(chat_member_info, ChatMemberRestricted) and not chat_member_info.can_send_messages:
        raise PermissionError("bot is not allowed to send messages")


async def fetch_admins(
        bot: Bot,
        main_group_id: int,
) -> dict:
    result = {}
    admins: list[ChatMemberOwner | ChatMemberAdministrator] = await bot.get_chat_administrators(main_group_id)
    for admin in admins:
        if admin.user.is_bot:
            continue
        if isinstance(admin, ChatMemberOwner):
            result[admin.user.id] = {"can_restrict_members": True}
        else:
            result[admin.user.id] = {"can_restrict_members": admin.can_restrict_members}
    return result
