from aiogram import types, Dispatcher


async def on_user_join(message: types.Message):
    """
    Delete service messages about users joining the group

    :param message: service message from Telegram about user joining the group
    """
    await message.delete()


def register_group_events(dp: Dispatcher, main_group_id: int):
    dp.register_message_handler(on_user_join, chat_id=main_group_id, content_types="new_chat_members")
