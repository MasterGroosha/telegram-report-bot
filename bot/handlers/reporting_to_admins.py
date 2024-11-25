from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.filters import AdminsCalled

router = Router()

REPORT_COMMAND = Command("report", prefix="!/")

@router.message(REPORT_COMMAND, F.reply_to_message)
async def cmd_report(
        message: Message,
        bot: Bot,
        admins: dict,
        reports_group_id: int,
        l10n: FluentLocalization,
):
    if message.reply_to_message.from_user.id in admins:
        await message.reply(l10n.format_value("error-cannot-report-admins"))
        return
    await bot.send_message(
        chat_id=reports_group_id,
        text=f"[todo] New report! {message.get_url(force_private=True, include_thread_id=True)}"
    )


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
        reports_group_id: int,
        l10n: FluentLocalization,
):
    msg_url = message.get_url(force_private=True, include_thread_id=True)
    message_text = l10n.format_value("need-admins-attention", {"msg_url": msg_url})
    await bot.send_message(
        chat_id=reports_group_id,
        text=message_text,
    )
