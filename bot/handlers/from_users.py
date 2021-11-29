import logging

from aiogram import types, Bot
from aiogram import html
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.exceptions import TelegramAPIError
from magic_filter import F

from bot.config_reader import Config
from bot.localization import Lang
from bot.callback_factories import DeleteMsgCallback

logger = logging.getLogger("report_bot")


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


async def cmd_report(message: types.Message, config: Config, lang: Lang, bot: Bot):
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

    # Get list of recipients.
    # If report mode is "group", then only report group is used
    # Otherwise, all admins who can delete messages and ban users
    if config.report_mode == "group":
        recipients = [config.group.reports]
    else:
        recipients = []
        for admin_id, permissions in config.admins.items():
            if admin_id != bot.id and permissions.get("can_restrict_members", False) is True:
                recipients.append(admin_id)

    for chat in recipients:
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


async def calling_all_units(message: types.Message, config: Config, lang: Lang, bot: Bot):
    """
    Handle messages starting with "@admin". No additional checks are done, so
    "@admin", "@admin!!!", "@administrator" and other are valid

    :param message: Telegram message with /report command
    :param config: config instance
    :param lang: locale instance
    :param bot: bot instance
    """
    await bot.send_message(
        config.group.reports,
        lang.get("need_admins_attention").format(msg_url=message.get_url(force_private=True))
    )


def register_from_users_handlers(router: Router):
    router.message.register(cmd_report, Command(commands="report"), F.reply_to_message)
    router.message.register(calling_all_units, F.text.startswith("@admin"))
