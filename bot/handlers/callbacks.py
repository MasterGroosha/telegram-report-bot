import logging

from aiogram import types, Bot, Router
from aiogram.exceptions import TelegramAPIError

from bot.config_reader import config
from bot.localization import Lang
from bot.callback_factories import DeleteMsgCallback

logger = logging.getLogger("report_bot")
router = Router()


@router.callback_query(DeleteMsgCallback.filter())
async def delmsg_callback(call: types.CallbackQuery, callback_data: DeleteMsgCallback,
                          lang: Lang, bot: Bot):
    delete_ok: bool = True
    for msg_id in callback_data.message_ids.split(","):
        try:
            await bot.delete_message(config.group_main, int(msg_id))
        except TelegramAPIError as ex:
            # Todo: better pointer at message which caused this error
            logger.error(f"[{type(ex).__name__}]: {str(ex)}")
            delete_ok = False

    if callback_data.action == "del":
        await call.message.edit_text(call.message.html_text + lang.get("action_deleted"))
    elif callback_data.action == "ban":
        try:
            # if a channel was reported
            if callback_data.entity_id < 0:
                await bot.ban_chat_sender_chat(config.group_main, callback_data.entity_id)
            # if a user was reported
            else:
                await bot.ban_chat_member(config.group_main, callback_data.entity_id)
            await call.message.edit_text(call.message.html_text + lang.get("action_deleted_banned"))
        except TelegramAPIError as ex:
            logger.error(f"[{type(ex).__name__}]: {str(ex)}")
            delete_ok = False

    if delete_ok:
        await call.answer()
    else:
        await call.answer(show_alert=True, text=lang.get("action_deleted_partially"))
