from contextlib import suppress
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageToDeleteNotFound
from bot.common import report_msg_cb
from bot.config_reader import Config
from bot.localization import get_string


async def callbacks_on_report_msg(call: types.CallbackQuery, callback_data: dict):
    """
    Handle callback button taps on report message in admin group

    :param call: callback coming from Telegram
    :param callback_data: callback data parsed by aiogram
    :param config: bot config
    :param lang: preferred bot language
    """
    config = call.bot.get("config")
    option = callback_data.get("option", "del")
    user_id = callback_data.get("user_id")
    message_ids = callback_data.get("message_ids")

    for msg_id in message_ids.split(","):
        with suppress(MessageToDeleteNotFound):
            await call.bot.delete_message(config.group.main, msg_id)

    if option == "del":
        await call.message.edit_text(
            call.message.html_text + get_string(config.lang, "action_deleted"))
    elif option == "ban":
        await call.bot.kick_chat_member(config.group.main, user_id)
        await call.message.edit_text(call.message.html_text + get_string(config.lang, "action_deleted_banned"))
    await call.answer()


def register_callbacks_reports(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_on_report_msg, report_msg_cb.filter())
