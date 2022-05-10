import logging

from aiogram import types, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.dispatcher.router import Router

from bot.config_reader import config
from bot.localization import Lang
from bot.callback_factories import DeleteMsgCallback

logger = logging.getLogger("report_bot")


async def delmsg_callback(call: types.CallbackQuery, callback_data: DeleteMsgCallback,
                          lang: Lang, bot: Bot):
    delete_ok = True
    for msg_id in callback_data.message_ids.split(","):
        try:
            await bot.delete_message(config.group.main, int(msg_id))
        except TelegramAPIError as ex:
            # Todo: better pointer at message which caused this error
            logger.error(f"[{type(ex).__name__}]: {str(ex)}")
            delete_ok = False

    if callback_data.option == "del":
        await call.message.edit_text(call.message.html_text + lang.get("action_deleted"))
    elif callback_data.option == "ban":
        try:
            await bot.ban_chat_member(config.group.main, callback_data.user_id)
            await call.message.edit_text(call.message.html_text + lang.get("action_deleted_banned"))
        except TelegramAPIError as ex:
            logger.error(f"[{type(ex).__name__}]: {str(ex)}")

    if delete_ok:
        await call.answer()
    else:
        await call.answer(show_alert=True, text=lang.get("action_deleted_partially"))


def register_callbacks(router: Router):
    router.callback_query.register(delmsg_callback, DeleteMsgCallback.filter())
