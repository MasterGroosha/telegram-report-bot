import logging
from typing import List

from aiogram import types, Bot
from aiogram import html
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.exceptions import TelegramAPIError
from magic_filter import F

from bot.config_reader import config
from bot.localization import Lang
from bot.callback_factories import DeleteMsgCallback

logger = logging.getLogger("report_bot")


def get_report_chats(bot_id: int) -> List[int]:
    """
    Get list of recipients to send report message to.
    If report mode is "group", then only report group is used
    Otherwise, all admins who can delete messages and ban users (except this bot)

    :param bot_id: this bot's ID
    :return: list of chat IDs to send messages to
    """
    if config.report_mode == "group":
        return [config.group.reports]
    else:
        recipients = []
        for admin_id, permissions in config.admins.items():
            if admin_id != bot_id and permissions.get("can_restrict_members", False) is True:
                recipients.append(admin_id)
        return recipients


def make_report_message(message: types.Message, lang: Lang):
    """
    Prepare report message format. This includes original (reported) message datetime,
    message private URL (even for public groups) and optional notes from user who made the report

    :param message: Telegram message with /report command
    :param lang: locale instance
    :return: formatted report message text
    """
    msg = lang.get("report_message").format(
        time=message.reply_to_message.date.strftime(lang.get("report_date_format")),
        msg_url=message.reply_to_message.get_url(force_private=True)
    )
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        msg += lang.get("report_note").format(note=html.quote(parts[1]))
    return msg


def make_report_keyboard(user_id: int, message_ids: str, lang: Lang):
    """
    Prepare report message keyboard. Currently it includes two buttons:
    one simply deletes original message, report message and report confirmation message,
    the other also bans author of original message which was reported

    :param user_id: Telegram ID of user who may be banned from group chat
    :param message_ids: IDs of original message, report message and report confirmation message
    :param lang: locale instance
    :return: inline keyboard with these two buttons
    """
    markup = [
        [types.InlineKeyboardButton(
            text=lang.get("action_del_msg"),
            callback_data=DeleteMsgCallback(
                option="del", user_id=user_id, message_ids=message_ids
            ).pack()
        )],
        [types.InlineKeyboardButton(
            text=lang.get("action_del_and_ban"),
            callback_data=DeleteMsgCallback(
                option="ban", user_id=user_id, message_ids=message_ids
            ).pack()
        )],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=markup)


async def cmd_report(message: types.Message, lang: Lang, bot: Bot):
    """
    Handle /report command in main group

    :param message: Telegram message with /report command
    :param config: config instance
    :param lang: locale instance
    :param bot: bot instance
    """
    if message.reply_to_message.from_user.id in config.admins.keys():
        await message.reply(lang.get("error_report_admin"))
        return
    msg = await message.reply(lang.get("report_sent"))

    for chat in get_report_chats(bot.id):
        try:
            await bot.forward_message(
                chat_id=chat, from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id
            )
            await bot.send_message(
                chat, text=make_report_message(message, lang),
                reply_markup=make_report_keyboard(
                    user_id=message.reply_to_message.from_user.id,
                    message_ids=f"{message.message_id},{message.reply_to_message.message_id},{msg.message_id}",
                    lang=lang
                )
            )
        except TelegramAPIError as ex:
            logger.error(f"[{type(ex).__name__}]: {str(ex)}")


async def calling_all_units(message: types.Message, lang: Lang, bot: Bot):
    """
    Handle messages starting with "@admin". No additional checks are done, so
    "@admin", "@admin!!!", "@administrator" and other are valid

    :param message: Telegram message with /report command
    :param config: config instance
    :param lang: locale instance
    :param bot: bot instance
    """
    for chat in get_report_chats(bot.id):
        await bot.send_message(
            chat, lang.get("need_admins_attention").format(msg_url=message.get_url(force_private=True))
        )


async def any_message_from_channel(message: types.Message, lang: Lang, bot: Bot):
    """
    Handle messages sent on behalf of some channels
    Read more: https://telegram.org/blog/protected-content-delete-by-date-and-more#anonymous-posting-in-public-groups

    :param message: Telegram message send on behalf of some channel
    :param lang: locale instance
    :param bot: bot instance
    """

    # If is_automatic_forward is not None, then this is post from linked channel, which shouldn't be banned
    # If message.sender_chat.id == message.chat.id, then this is an anonymous admin, who shouldn't be banned either
    if message.is_automatic_forward is None and message.sender_chat.id != message.chat.id:
        await message.answer(lang.get("channels_not_allowed"))
        await bot.ban_chat_sender_chat(message.chat.id, message.sender_chat.id)
        await message.delete()


def register_from_users_handlers(router: Router):
    router.message.register(cmd_report, Command(commands="report"), F.reply_to_message)
    router.message.register(calling_all_units, F.text.startswith("@admin"))
    router.message.register(any_message_from_channel, F.sender_chat, magic_data=F.config.ban_channels.is_(True))
