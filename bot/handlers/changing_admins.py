import structlog
from aiogram import types, Router
from aiogram.types import ChatMemberOwner
from structlog.typing import FilteringBoundLogger

from bot.filters import AdminAdded, AdminRemoved

logger: FilteringBoundLogger = structlog.get_logger()
router = Router()


@router.chat_member(AdminAdded())
async def admin_added(
        event: types.ChatMemberUpdated,
        admins: dict[int, dict[int, object]]
):
    """
    Handle "new admin was added" event and update admins dictionary

    :param event: ChatMemberUpdated event
    :param admins: dictionary of admins before handling this event
    """
    new = event.new_chat_member
    if isinstance(new, ChatMemberOwner):
        can_restrict_members = True
    else:
        can_restrict_members = new.can_restrict_members
    admins[event.chat.id][new.user.id] = {"can_restrict_members": can_restrict_members}
    await logger.ainfo(f"Added new admin with id={new.user.id} and {can_restrict_members=} to chat {event.chat.id}")



@router.chat_member(AdminRemoved())
async def admin_removed(
        event: types.ChatMemberUpdated,
        admins: dict[int, dict[int, object]],
):
    """
    Handle "user was demoted from admins" event and update admins dictionary

    :param event: ChatMemberUpdated event
    :param admins: dictionary of admins before handling this event
    """
    new = event.new_chat_member
    if new.user.id in admins[event.chat.id].keys():
        del admins[event.chat.id][new.user.id]
    await logger.ainfo(f"Removed user with id={new.user.id} from admins of chat {event.chat.id}")
