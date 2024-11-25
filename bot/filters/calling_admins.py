from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminsCalled(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
                message.text in ("@admin", "@admins")
                or
                message.text.startswith("@admin ")
                or
                message.text.startswith("@admins ")
        )
