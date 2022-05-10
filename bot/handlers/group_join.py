from aiogram import types, Router, F

router = Router()


@router.message(F.new_chat_member, F.config.re.is_(True))
async def on_user_join(message: types.Message):
    """
    Delete "user joined" service messages

    :param message: a service message from Telegram "<user> joined the group"
    """
    await message.delete()
