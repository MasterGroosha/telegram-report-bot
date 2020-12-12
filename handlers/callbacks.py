from time import time
from aiogram import types
from configurator import Config
from misc import dp
import localization


@dp.callback_query_handler()
async def callback_handler(call: types.CallbackQuery):
    """
    Keyboard buttons handler

    :param call: Callback with action put into call.data field
    """
    if call.data.startswith("del_"):
        await call.message.bot.delete_message(Config.GROUP_MAIN, int(call.data.split("_")[1]))
        await call.message.bot.edit_message_text(chat_id=Config.GROUP_REPORTS,
                                                 message_id=call.message.message_id,
                                                 text=call.message.text + localization.get_string("action_deleted"))
        await call.answer(text="Done")

    elif call.data.startswith("delban_"):
        await call.message.bot.delete_message(Config.GROUP_MAIN, int(call.data.split("_")[1]))
        await call.message.bot.kick_chat_member(chat_id=Config.GROUP_MAIN, user_id=call.data.split("_")[2])
        await call.message.bot.edit_message_text(chat_id=Config.GROUP_REPORTS,
                                                 message_id=call.message.message_id,
                                                 text=call.message.text + localization.get_string(
                                                     "action_deleted_banned"))
        await call.answer(text="Done")

    elif call.data.startswith("mute_"):
        await call.message.bot.delete_message(Config.GROUP_MAIN, int(call.data.split("_")[1]))
        await call.message.bot.restrict_chat_member(chat_id=Config.GROUP_MAIN, user_id=call.data.split("_")[2],
                                                    permissions=types.ChatPermissions(),
                                                    until_date=int(time()) + 7200)  # 2 hours from now
        await call.message.bot.edit_message_text(chat_id=Config.GROUP_REPORTS,
                                                 message_id=call.message.message_id,
                                                 text=call.message.text + localization.get_string(
                                                     "action_deleted_readonly"))
        await call.answer(text="Done")
