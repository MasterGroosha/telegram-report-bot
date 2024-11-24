from aiogram.filters import BaseFilter
from aiogram.types import ChatMemberUpdated
from aiogram.utils.chat_member import ADMINS


class AdminAdded(BaseFilter):
    async def __call__(self, event: ChatMemberUpdated) -> bool:
        return isinstance(event.new_chat_member, ADMINS)

class AdminRemoved(BaseFilter):
    async def __call__(self, event: ChatMemberUpdated) -> bool:
        return (
            isinstance(event.old_chat_member, ADMINS)
            and
            not isinstance(event.new_chat_member, ADMINS)
        )
