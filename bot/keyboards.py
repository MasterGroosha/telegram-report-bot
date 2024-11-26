import structlog
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization
from structlog.types import FilteringBoundLogger

from bot.callback_factories import AdminActionCallbackV1, AdminAction

logger: FilteringBoundLogger = structlog.get_logger()


def get_report_keyboard(
        user_or_chat_id: int,
        reported_message_id: int,
        l10n: FluentLocalization,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    delete_callback = AdminActionCallbackV1(
        action=AdminAction.DELETE,
        user_or_chat_id=user_or_chat_id,
        reported_message_id=reported_message_id,
    )
    logger.debug(f"Generated delete button with callback {delete_callback.pack()}")
    builder.button(
        text=l10n.format_value("report-button-delete"),
        callback_data=delete_callback,
    )

    ban_callback = AdminActionCallbackV1(
        action=AdminAction.BAN,
        user_or_chat_id=user_or_chat_id,
        reported_message_id=reported_message_id,
    )
    logger.debug(f"Generated delete+ban button with callback {ban_callback.pack()}")
    builder.button(
        text=l10n.format_value("report-button-delete-and-ban"),
        callback_data=ban_callback,
    )

    builder.adjust(1)
    return builder.as_markup()
