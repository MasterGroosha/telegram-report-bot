import datetime
from aiogram import types
from configurator import config
from misc import dp
import localization


@dp.message_handler(chat_id=config.groups.main, content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    """
    Removes "user joined" message

    :param message: Service message "User joined group
    """
    await message.delete()


@dp.message_handler(lambda message: 0 < len(message.text.split()) <= 2, chat_id=config.groups.main)
async def short_messages(message: types.Message):
    """
    Handler which triggers when there are only 2 or less words in a message.
    If one of the words is considered as "greeting", like "Hello", "Hi" etc, bot kindly
    asks user to express his thoughts without such short useless sentences.

    :param message: Telegram message consisting of 2 or less words
    """
    # Не будем это использовать по воскресеньям
    now = datetime.datetime.now()+datetime.timedelta(hours=3)
    if now.weekday() == 6:  # 6 — это воскресенье
        return

    for word in message.text.lower().split():
        if word.replace(",", "").replace("!", "").replace(".", "") in localization.get_string("greetings_words"):
            await message.reply(localization.get_string("error_message_too_short"))