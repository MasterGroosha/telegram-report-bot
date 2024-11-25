from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filters import AdminsCalled

router = Router()

REPORT_COMMAND = Command("report", prefix="!/")

@router.message(REPORT_COMMAND, F.reply_to_message)
async def cmd_report(
        message: Message,
        bot: Bot,
        admins: dict,
        reports_group_id: int,
):
    if message.reply_to_message.from_user.id in admins:
        await message.reply("Cannot report admins!")
        return
    await bot.send_message(
        chat_id=reports_group_id,
        text=f"[todo] New report! {message.get_url(force_private=True, include_thread_id=True)}"
    )


@router.message(REPORT_COMMAND, ~F.reply_to_message)
async def cmd_report(
        message: Message
):
    await message.reply("This command must be reply to other message!")


@router.message(AdminsCalled())
async def calling_all_units(
        message: Message,
        bot: Bot,
        reports_group_id: int
):
    await bot.send_message(
        chat_id=reports_group_id,
        text=f"[todo] Need your attention! {message.get_url(force_private=True, include_thread_id=True)}"
    )
