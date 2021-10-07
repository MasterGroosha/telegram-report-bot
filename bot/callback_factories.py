from aiogram.dispatcher.filters.callback_data import CallbackData


class DeleteMsgCallback(CallbackData, prefix="delmsg"):
    option: str
    user_id: int
    message_ids: str  # Lists are not supported =(
