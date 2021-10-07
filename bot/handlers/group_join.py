from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.content_types import ContentTypesFilter


async def on_user_join(message: types.Message):
    """
    Delete "user joined" service messages

    :param message: a service message from Telegram "<user> joined the group"
    """
    await message.delete()


def register_group_join_handler(router: Router):
    router.message.register(
        on_user_join, ContentTypesFilter(content_types="new_chat_members")
    )
