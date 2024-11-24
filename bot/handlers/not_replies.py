from aiogram import types, Router, F
from aiogram.dispatcher.filters.command import Command

from bot.config_reader import config
from bot.localization import Lang

router = Router()
router.message.filter(~F.reply_to_message)


@router.message(Command(commands=["report"]))
@router.message(Command(commands=["ro", "nm"]), F.from_user.id.in_(config.admins.keys()))
async def no_reply(message: types.Message, lang: Lang):
    """
    Show an error if specific commands were not sent as replies to other messages

    :param message: message which is not a reply to other message
    :param lang: locale instance
    """
    await message.reply(lang.get("error_no_reply"))
