import structlog
from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization
from structlog.types import FilteringBoundLogger

from bot.callback_factories import AdminActionCallbackV1, AdminAction
from bot.config_reader import BotConfig

router = Router()
logger: FilteringBoundLogger = structlog.get_logger()


@router.callback_query(AdminActionCallbackV1.filter())
async def reacting_to_reports(
        callback: CallbackQuery,
        bot: Bot,
        bot_config: BotConfig,
        callback_data: AdminActionCallbackV1,
        l10n: FluentLocalization,
):
    await logger.adebug(f"Received callback query: {callback.data}")

    message_delete_success: bool = True

    # First, try to delete message
    try:
        await bot.delete_message(
            chat_id=callback_data.chat_id,
            message_id=callback_data.reported_message_id,
        )
    except TelegramAPIError as ex:
        await logger.aerror(f"Failed to delete message, because {ex.__class__.__name__}: {str(ex)} ")
        message_delete_success = False

    if message_delete_success:
        message_delete_lang_key = "message-deleted-successfully"
        show_alert = False
    else:
        message_delete_lang_key = "failed-to-delete-message"
        show_alert = True

    # If we only had to delete message, we can stop here
    if callback_data.action == AdminAction.DELETE:
        await callback.message.edit_text(
            text=callback.message.html_text + "\n\n" + l10n.format_value(message_delete_lang_key),
        )
        await callback.answer(show_alert=show_alert, text=l10n.format_value(message_delete_lang_key))
        return

    # If action was delete and ban, let's try to ban user as well
    offender_ban_success: bool = True
    args = {"chat_id": callback_data.chat_id}
    if callback_data.user_or_chat_id > 0:
        func = bot.ban_chat_member
        args.update(user_id=callback_data.user_or_chat_id)
    else:
        func = bot.ban_chat_sender_chat
        args.update(sender_chat_id=callback_data.user_or_chat_id)

    try:
        await func(**args)
    except TelegramAPIError as ex:
        await logger.aerror(f"Failed to ban user, because {ex.__class__.__name__}: {str(ex)} ")
        offender_ban_success = False

    if offender_ban_success:
        offender_ban_lang_key = "user-or-channel-banned-successfully"
    else:
        offender_ban_lang_key = "failed-to-ban-user-or-channel"
        show_alert = True

    additional_text = f"{l10n.format_value(message_delete_lang_key)} {l10n.format_value(offender_ban_lang_key)}"
    await callback.message.edit_text(
        text=callback.message.html_text + "\n\n" + additional_text,
    )
    await callback.answer(show_alert=show_alert, text=additional_text)
    return
