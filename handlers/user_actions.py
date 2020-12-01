from aiogram import types
from aiogram.dispatcher.filters import Text
from configurator import Config
from misc import dp
import localization
import utils


@dp.message_handler(chat_id=Config.GROUP_MAIN, commands="report")
async def cmd_report(message: types.Message):
    """
    Handler for /report command in chat.
    Reports to admins are ignored. Reports which are not replies are ignored.

    :param message: Telegram message containing /report command
    """
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply(localization.get_string("error_no_reply"))
        return

    # We don't want users to report an admin
    user = await message.bot.get_chat_member(Config.GROUP_MAIN, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(localization.get_string("error_report_admin"))
        return

    # Check for report message (anything sent after /report command)
    msg_parts = message.text.split()
    report_message = None
    if len(msg_parts) > 1:
        report_message = message.text.replace("/report", "")

    # Generate keyboard with some actions
    action_keyboard = types.InlineKeyboardMarkup()
    # Delete message by its id
    action_keyboard.add(types.InlineKeyboardButton(
        text=localization.get_string("action_del_msg"),
        callback_data=f"del_{message.reply_to_message.message_id}")
    )
    # Delete message by its id and ban user by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text=localization.get_string("action_del_and_ban"),
        callback_data=f"delban_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))
    # Delete message by its id and mute user for 2 hours by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text=localization.get_string("action_del_and_readonly"),
        callback_data=f"mute_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    await message.reply_to_message.forward(Config.GROUP_REPORTS)
    await message.bot.send_message(
        Config.GROUP_REPORTS,
        utils.get_report_comment(
            message.reply_to_message.date,
            message.reply_to_message.message_id,
            report_message
        ),
        reply_markup=action_keyboard)
    await message.reply(localization.get_string("report_delivered"))


@dp.message_handler(Text(startswith="@admin", ignore_case=True), chat_id=Config.GROUP_MAIN)
async def calling_all_units(message: types.Message):
    """
    Handler which is triggered when message starts with @admin.
    Honestly any combination will work: @admin, @admins, @adminisshit

    :param message: Telegram message where text starts with @admin
    """
    await message.bot.send_message(
        Config.GROUP_REPORTS,
        localization.get_string("need_admins_attention").format(
            chat_id=utils.get_url_chat_id(Config.GROUP_MAIN),
            msg_id=message.reply_to_message.message_id
            if message.reply_to_message
            else message.message_id
        )
    )
