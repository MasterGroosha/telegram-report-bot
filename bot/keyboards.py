from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

from bot.callback_factories import AdminActionCallbackV1, AdminAction


def get_report_keyboard(
        user_or_chat_id: int,
        reported_message_id: int,
        l10n: FluentLocalization,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=l10n.format_value("report-button-delete"),
        callback_data=AdminActionCallbackV1(
            action=AdminAction.DELETE,
            user_or_chat_id=user_or_chat_id,
            reported_message_id=reported_message_id,
        )
    )
    builder.button(
        text=l10n.format_value("report-button-delete-and-ban"),
        callback_data=AdminActionCallbackV1(
            action=AdminAction.BAN,
            user_or_chat_id=user_or_chat_id,
            reported_message_id=reported_message_id,
        )
    )

    builder.adjust(1)
    return builder.as_markup()
