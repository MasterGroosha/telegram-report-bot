import re
from datetime import timedelta

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from fluent.runtime import FluentLocalization

from bot.config_reader import BotConfig
from bot.utils import get_formatted_datetime

restriction_time_regex = re.compile(r'(\b[1-9][0-9]*)([mhd]\b)')

router = Router()


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


@router.message(Command("ro", prefix="!"), F.reply_to_message)
async def cmd_ro(
        message: Message,
        bot: Bot,
        bot_config: BotConfig,
        l10n: FluentLocalization,
        admins: dict,
):
    # Prohibit non-admins from using this command
    if message.from_user.id not in admins:
        return
    # Prohibit from restricting admins
    if message.reply_to_message.from_user.id in admins.keys():
        await message.reply(l10n.format_value("error-restricting-admin"))
        return
    # Do not allow admin with no restrict permissions from restricting other users
    if admins.get(message.from_user.id, {}).get("can_restrict_members", False) is False:
        await message.reply(l10n.format_value("error-no-restrict-permissions"))
        return
    # If a message is sent on behalf of channel, then we can only ban it
    if message.reply_to_message.sender_chat and not message.reply_to_message.is_automatic_forward:
        await bot.ban_chat_sender_chat(message.chat.id, message.reply_to_message.sender_chat.id)
        await message.reply(l10n.format_value("channel-banned"))
        return

    restriction_period = get_restriction_period(message.text)
    restriction_end_date = message.date + timedelta(seconds=restriction_period)

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(),
        until_date=restriction_end_date
    )

    if restriction_period == 0:
        await message.reply(l10n.format_value("readonly-forever"))
    else:
        formatted_date_time_offset = get_formatted_datetime(bot_config, restriction_end_date)
        await message.reply(
            l10n.format_value("readonly-temporary", {
                "msg_date": formatted_date_time_offset.date,
                "msg_time": formatted_date_time_offset.time,
                "msg_utc": formatted_date_time_offset.offset,
            })
        )
