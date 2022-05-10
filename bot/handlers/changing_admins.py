from aiogram import types, Router

from bot.filters.changing_admins import AdminAdded, AdminRemoved
from bot.config_reader import config

router = Router()


@router.chat_member(AdminAdded())
async def admin_added(event: types.ChatMemberUpdated):
    """
    Handle "new admin was added" event and update config.admins dictionary

    :param event: ChatMemberUpdated event
    :param config: config instance
    """
    new = event.new_chat_member
    if new.status == "creator":
        config.admins[new.user.id] = {"can_restrict_members": True}
    else:
        config.admins[new.user.id] = {"can_restrict_members": new.can_restrict_members}


@router.chat_member(AdminRemoved())
async def admin_removed(event: types.ChatMemberUpdated):
    """
    Handle "user was demoted from admins" event and update config.admins dictionary

    :param event: ChatMemberUpdated event
    """
    new = event.new_chat_member
    if new.user.id in config.admins.keys():
        del config.admins[new.user.id]
