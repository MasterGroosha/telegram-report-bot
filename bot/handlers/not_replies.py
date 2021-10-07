from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.command import Command
from magic_filter import F

from bot.localization import Lang
from bot.config_reader import Config


async def no_reply(message: types.Message, lang: Lang):
    """
    Show an error if specific commands were not sent as replies to other messages

    :param message: message which is not a reply to other message
    :param lang: locale instance
    """
    await message.reply(lang.get("error_no_reply"))


def register_no_replies_handler(router: Router, config: Config):
    router.message.register(no_reply, Command(commands=["report"]), ~F.reply_to_message)
    router.message.register(no_reply, Command(commands=["ro", "nm"]),
                            F.from_user.id.in_(config.admins.keys()), ~F.reply_to_message)
