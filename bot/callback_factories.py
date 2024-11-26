from enum import Enum

from aiogram.filters.callback_data import CallbackData


class AdminAction(str, Enum):
    DELETE = "del"
    BAN = "ban"

class AdminActionCallbackV1(CallbackData, prefix="v1"):
    action: AdminAction
    user_or_chat_id: int
    reported_message_id: int
