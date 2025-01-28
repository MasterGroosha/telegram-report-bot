from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.config_reader import BotConfig
from bot.filters import AdminsCalled
from bot.keyboards import get_report_keyboard
from bot.utils import get_formatted_datetime

router = Router()

REPORT_COMMAND = Command("report", prefix="!/")

@router.message(REPORT_COMMAND, F.reply_to_message.as_("replied_msg"))
async def cmd_report(
        message: Message,
        command: CommandObject,
        bot: Bot,
        admins: dict[int, dict[int, object]],
        bot_config: BotConfig,
        l10n: FluentLocalization,
        replied_msg: Message,
):
    # If message sent by user who is admin
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        await message.reply(l10n.format_value("error-cannot-report-admins"))
        return
    # If message sent by anonymous group admin
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        await message.reply(l10n.format_value("error-cannot-report-admins"))
        return
    # If message is automatic forward from linked channel
    if message.is_automatic_forward:
        await message.reply(l10n.format_value("error-cannot-report-linked"))
        return

    # Gather all report message parameters
    chat_id = replied_msg.chat.id
    offender_id = replied_msg.sender_chat.id if replied_msg.sender_chat else replied_msg.from_user.id
    offender_message_id = replied_msg.message_id
    formatted_date_time_offset = get_formatted_datetime(bot_config)
    params = {
        "msg_date": formatted_date_time_offset.date,
        "msg_time": formatted_date_time_offset.time,
        "msg_utc": formatted_date_time_offset.offset,
        "msg_url": replied_msg.get_url(force_private=True, include_thread_id=True),
    }
    if command.args is None:
        locale_key = "report-info"
    else:
        locale_key = "report-info-with-comment"
        params.update(msg_comment=command.args)

    # Send 3 messages: forwarded replied message, report info message and acknowledgement
    await replied_msg.forward(chat_id=bot_config.reports_group_id)
    await bot.send_message(
        chat_id=bot_config.reports_group_id,
        text=l10n.format_value(locale_key, params),
        reply_markup=get_report_keyboard(
            chat_id=chat_id,
            user_or_chat_id=offender_id,
            reported_message_id=offender_message_id,
            l10n=l10n,
        ),
    )
    await message.reply(l10n.format_value("report-sent"))


@router.message(REPORT_COMMAND, ~F.reply_to_message)
async def cmd_report(
        message: Message,
        l10n: FluentLocalization,
):
    await message.reply(l10n.format_value("error-must-be-reply"))


@router.message(AdminsCalled())
async def calling_all_units(
        message: Message,
        bot: Bot,
        bot_config: BotConfig,
        l10n: FluentLocalization,
):
    msg_url = message.get_url(force_private=True, include_thread_id=True)
    message_text = l10n.format_value("need-admins-attention", {"msg_url": msg_url})
    await bot.send_message(
        chat_id=bot_config.reports_group_id,
        text=message_text,
    )
