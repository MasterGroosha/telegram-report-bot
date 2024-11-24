from aiogram import types, Router, F

from bot.config_reader import config

router = Router()


@router.message(F.new_chat_members, lambda x: config.remove_joins is True)
async def on_user_join(message: types.Message):
    """
    Delete "user joined" service messages

    :param message: a service message from Telegram "<user> joined the group"
    """
    await message.delete()
