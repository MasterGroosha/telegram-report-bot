from aiogram import types
from aiogram.dispatcher.router import Router

from bot.filters.changing_admins import AdminAdded, AdminRemoved
from bot.config_reader import Config


async def admin_added(event: types.ChatMemberUpdated, config: Config):
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


async def admin_removed(event: types.ChatMemberUpdated, config: Config):
    """
    Handle "user was demoted from admins" event and update config.admins dictionary

    :param event: ChatMemberUpdated event
    :param config: config instance
    """
    new = event.new_chat_member
    if new.user.id in config.admins.keys():
        del config.admins[new.user.id]


def register_admin_changes_handlers(router: Router):
    router.chat_member.register(admin_added, AdminAdded())
    router.chat_member.register(admin_removed, AdminRemoved())
