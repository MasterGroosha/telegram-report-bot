#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter, Text
from time import time
from os import getenv
from sys import exit

# Local files
import config
import localization as lang
import utils

token = getenv("BOT_TOKEN")
if not token:
    exit("No token provided")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)


class IsAdminFilter(BoundFilter):
    """
    Custom class to add "is_admin" filter for some handlers below
    """
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(chat_id=config.group_main, content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    """
    Removes "user joined" message
    :param message: Service message "User joined group
    """
    await message.delete()


@dp.message_handler(chat_id=config.group_main, commands=["report"])
async def cmd_report(message: types.Message):
    """
    Handler for /report command in chat.
    Reports to admins are ignored. Reports which are not replies are ignored.
    :param message: Telegram message containing /report command
    :return:
    """
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply(lang.get_string("error_no_reply"))
        return

    # We don't want users to report an admin
    user = await bot.get_chat_member(config.group_main, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(lang.get_string("error_report_admin"))
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
        text=lang.get_string("action_del_msg"),
        callback_data=f"del_{message.reply_to_message.message_id}")
    )
    # Delete message by its id and ban user by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text=lang.get_string("action_del_and_ban"),
        callback_data=f"delban_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))
    # Delete message by its id and mute user for 2 hours by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text=lang.get_string("action_del_and_readonly"),
        callback_data=f"mute_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    await message.reply_to_message.forward(config.group_reports)
    await bot.send_message(config.group_reports,
                           utils.get_report_comment(message.reply_to_message.date,
                                                    message.reply_to_message.message_id,
                                                    report_message),
                           reply_markup=action_keyboard)
    await message.reply(lang.get_string("report_delivered"))


@dp.message_handler(is_admin=True, chat_id=config.group_main, commands=["ro"])
async def cmd_readonly(message: types.Message):
    """
    Handler for /ro command in chat.
    Reports which are not replies are ignored.
    Only admins can use this command. A time period may be set after command, f.ex. /ro 2d,
    anything else is treated as commentary with no effect.
    :param message: Telegram message with /ro command and optional time
    """
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply(lang.get_string("error_no_reply"))
        return

    # Admins cannot be restricted
    user = await bot.get_chat_member(config.group_main, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(lang.get_string("error_restrict_admin"))
        return

    words = message.text.split()
    restriction_time: int = 0
    if len(words) > 1:  # /ro with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(lang.get_string("error_wrong_time_format"))
            return

    await bot.restrict_chat_member(config.group_main,
                                   message.reply_to_message.from_user.id,
                                   types.ChatPermissions(),
                                   until_date=int(time()) + restriction_time
                                   )
    await message.reply(lang.get_string("resolved_readonly").format(restriction_time=words[1] if len(words) > 1
                        else lang.get_string("restriction_forever")))


@dp.message_handler(is_admin=True, chat_id=config.group_main, commands=["nomedia", "textonly", "nm"])
async def cmd_nomedia(message: types.Message):
    """
    Handler for /nomedia or /textonly or /nm command in chat.
    Reports which are not replies are ignored.
    Only admins can use this command. A time period may be set after command, f.ex. /nm 2d,
    anything else is treated as commentary with no effect.
    :param message: Telegram message with /nomedia or /textonly or /nm command and optional time
    """
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply(lang.get_string("error_no_reply"))
        return

    # Admins cannot be restricted
    user = await bot.get_chat_member(config.group_main, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(lang.get_string("error_restrict_admin"))
        return

    words = message.text.split()
    restriction_time: int = 0
    if len(words) > 1:  # /ro with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(lang.get_string("error_wrong_time_format"))
            return

    await bot.restrict_chat_member(config.group_main,
                                   message.reply_to_message.from_user.id,
                                   types.ChatPermissions(can_send_messages=True),
                                   until_date=int(time()) + restriction_time)
    await message.reply(lang.get_string("resolved_nomedia").format(restriction_time=words[1] if len(words) > 1
                        else lang.get_string("restriction_forever")))


@dp.message_handler(Text(startswith="@admin", ignore_case=True), chat_id=config.group_main)
async def calling_all_units(message: types.Message):
    """
    Handler which is triggered when message starts with @admin.
    Honestly any combination will work: @admin, @admins, @adminisshit
    :param message: Telegram message where text starts with @admin
    """
    await bot.send_message(config.group_reports,
                           lang.get_string("need_admins_attention").format(
                               chat_id=utils.get_url_chat_id(config.group_main),
                               msg_id=message.reply_to_message.message_id
                               if message.reply_to_message
                               else message.message_id))


@dp.message_handler(lambda message: message.text and len(message.text.split()) <= 2, chat_id=config.group_main)
async def short_messages(message: types.Message):
    """
    Handler which triggers when there are only 2 or less words in a message.
    If one of the words is considered as "greeting", like "Hello", "Hi" etc, bot kindly
    asks user to express his thoughts without such short useless sentences.
    :param message: Telegram message consisting of 2 or less words
    """
    for word in message.text.lower().split():
        if word.replace(",", "").replace("!", "").replace(".", "") in lang.get_string("greetings_words"):
            await message.reply(lang.get_string("error_message_too_short"))


@dp.callback_query_handler(lambda call: call.data)
async def callback_handler(call: types.CallbackQuery):
    """
    Keyboard buttons handler
    :param call: Callback with action put into call.data field
    """
    if call.data.startswith("del_"):
        await bot.delete_message(config.group_main, int(call.data.split("_")[1]))
        await bot.edit_message_text(chat_id=config.group_reports,
                                    message_id=call.message.message_id,
                                    text=call.message.text + lang.get_string("action_deleted"))
        await bot.answer_callback_query(call.id, "Done")
        return
    elif call.data.startswith("delban_"):
        await bot.delete_message(config.group_main, int(call.data.split("_")[1]))
        await bot.kick_chat_member(chat_id=config.group_main, user_id=call.data.split("_")[2])
        await bot.edit_message_text(chat_id=config.group_reports,
                                    message_id=call.message.message_id,
                                    text=call.message.text + lang.get_string("action_deleted_banned"))
        await bot.answer_callback_query(call.id, "Done")
        return
    elif call.data.startswith("mute_"):
        await bot.delete_message(config.group_main, int(call.data.split("_")[1]))
        await bot.restrict_chat_member(chat_id=config.group_main, user_id=call.data.split("_")[2],
                                       permissions=types.ChatPermissions(),
                                       until_date=int(time()) + 7200)  # 2 hours from now
        await bot.edit_message_text(chat_id=config.group_reports,
                                    message_id=call.message.message_id,
                                    text=call.message.text + lang.get_string("action_deleted_readonly"))
        await bot.answer_callback_query(call.id, "Done")
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
