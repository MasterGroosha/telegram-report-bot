import re
from datetime import timedelta
from aiogram import types, Dispatcher
from bot.localization import get_string

restriction_time_regex = re.compile(r'(\b[1-9][0-9]*)([mhd]\b)')


async def error_no_reply(message: types.Message):
    lang = message.bot.get("config").get("lang")
    await message.reply(get_string(lang, "error_no_reply"))


def get_restriction_period(text: str) -> int:
    """
    Extract restriction period (in seconds) from text using regex search

    :param text: text to parse
    :return: restriction period in seconds (0 if nothing found, which means permanent restriction)
    """
    multipliers = {"m": 60, "h": 3600, "d": 86400}
    if match := re.search(restriction_time_regex, text):
        time, modifier = match.groups()
        return int(time) * multipliers[modifier]
    return 0


async def cmd_ro(message: types.Message):
    """
    Handle /ro command in main group

    :param message: Telegram message starting with /ro
    """
    lang = message.bot.get("config").get("lang")
    readonly_to = await message.chat.get_member(message.reply_to_message.from_user.id)
    if readonly_to.is_chat_admin():
        await message.reply(get_string(lang, "error_restrict_admin"))
        return
    user = await message.chat.get_member(message.from_user.id)
    if not user.is_chat_admin() or user.can_restrict_members is False:
        return
    ro_period = get_restriction_period(message.text)
    ro_end_date = message.date+timedelta(seconds=ro_period)
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(),
        until_date=ro_end_date
    )
    if ro_period == 0:
        await message.reply(get_string(lang, "readonly_forever"))
    else:
        await message.reply(
            get_string(lang, "readonly_temporary").format(time=ro_end_date.strftime("%d.%m.%Y %H:%M"))
        )


async def cmd_nomedia(message: types.Message):
    """
    Handle /nomedia command in main group

    :param message: Telegram message starting with /nomedia
    """
    lang = message.bot.get("config").get("lang")
    nomedia_to = await message.chat.get_member(message.reply_to_message.from_user.id)
    if nomedia_to.is_chat_admin():
        await message.reply(get_string(lang, "error_restrict_admin"))
        return
    user = await message.chat.get_member(message.from_user.id)
    if not user.is_chat_admin() or user.can_restrict_members is False:
        return
    nomedia_period = get_restriction_period(message.text)
    nomedia_end_date = message.date + timedelta(seconds=nomedia_period)
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(can_send_messages=True),
        until_date=nomedia_end_date
    )
    if nomedia_period == 0:
        await message.reply(get_string(lang, "nomedia_forever"))
    else:
        await message.reply(
            get_string(lang, "nomedia_temporary").format(time=nomedia_end_date.strftime("%d.%m.%Y %H:%M"))
        )


def register_main_group_admin(dp: Dispatcher, main_group_id: int):
    dp.register_message_handler(error_no_reply, chat_id=main_group_id, is_reply=False, commands=["ro", "nomedia"])
    dp.register_message_handler(cmd_ro, chat_id=main_group_id, is_reply=True, commands="ro")
    dp.register_message_handler(cmd_nomedia, chat_id=main_group_id, is_reply=True, commands="nomedia")
