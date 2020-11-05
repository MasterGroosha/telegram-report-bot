from time import time
from aiogram import types
from configurator import config
from misc import dp
import localization
import utils


@dp.message_handler(is_admin=True, chat_id=config.groups.main, commands="ro")
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
        await message.reply(localization.get_string("error_no_reply"))
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(config.groups.main, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(localization.get_string("error_restrict_admin"))
        return

    words = message.text.split()
    restriction_time: int = 0
    if len(words) > 1:  # /ro with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(localization.get_string("error_wrong_time_format"))
            return

    await message.bot.restrict_chat_member(config.groups.main,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(),
                                           until_date=int(time()) + restriction_time
                                           )
    await message.reply(localization.get_string("resolved_readonly").format(restriction_time=words[1] if len(words) > 1
    else localization.get_string("restriction_forever")))


@dp.message_handler(is_admin=True, chat_id=config.groups.main, commands=["nomedia", "textonly", "nm"])
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
        await message.reply(localization.get_string("error_no_reply"))
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(config.groups.main, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(localization.get_string("error_restrict_admin"))
        return

    words = message.text.split()
    restriction_time: int = 0
    if len(words) > 1:  # /ro with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(localization.get_string("error_wrong_time_format"))
            return

    await message.bot.restrict_chat_member(
        config.groups.main,
        message.reply_to_message.from_user.id,
        types.ChatPermissions(can_send_messages=True),
        until_date=int(time()) + restriction_time)
    await message.reply(localization.get_string("resolved_nomedia").format(
        restriction_time=words[1] if len(words) > 1 else localization.get_string("restriction_forever"))
    )
