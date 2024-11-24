from aiogram.dispatcher.filters.callback_data import CallbackData


class DeleteMsgCallback(CallbackData, prefix="delmsg"):
    # action to perform: "del" to simply delete a message or "ban" to ban chat/user as well
    action: str
    # the ID of chat or user to perform action on
    entity_id: int
    # string-formatted list of message IDs to delete
    message_ids: str  # Lists are not supported =(
