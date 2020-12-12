from configurator import Config

strings = {
    "en": {
        "error_no_reply": "This command must be sent as a reply to one's message!",
        "error_report_admin": "Whoa! Don't report admins 😈",
        "error_restrict_admin": "You cannot restrict an admin.",
        "error_wrong_time_format": "Wrong time format. Use a number + symbols 'h', 'm' or 'd'. F.ex. 4h",
        "error_message_too_short": "Please avoid short useless greetings. "
                                   "If you have a question or some information, put it in one message. Thanks in "
                                   "advance! 🤓",

        "report_date_format": "%d.%m.%Y at %H:%M (server time)",
        "report_message": '👆 Sent {date}\n'
                          '<a href="https://t.me/c/{chat_id}/{msg_id}">Go to message</a>',
        "report_note": "\n\nNote:{note}",
        "report_delivered": "<i>Report sent</i>",

        "action_del_msg": "Delete message",
        "action_del_and_ban": "Delete and ban",
        "action_del_and_readonly": "Delete and set RO for 2 hours",

        "action_deleted": "\n\n🗑 <b>Deleted</b>",
        "action_deleted_banned": "\n\n🗑❌ <b>Deleted, user banned</b>",
        "action_deleted_readonly": "\n\n🗑🙊 <b>Deleted, set readonly for 2 hours</b>",

        "resolved_readonly": "<i>User set to read-only mode ({restriction_time})</i>",
        "resolved_nomedia": "<i>User set to text-only mode ({restriction_time})</i>",

        "restriction_forever": "forever",
        "need_admins_attention": 'Dear admins, your presence in chat is needed!\n\n'
                                 '<a href="https://t.me/c/{chat_id}/{msg_id}">Go to message</a>',

        "greetings_words": ["hi", "q", "hello", "hey"]  # Bot will react to short messages with these words
    },
    "ru": {
        "error_no_reply": "Эта команда должна быть ответом на какое-либо сообщение!",
        "error_report_admin": "Админов репортишь? Ай-ай-ай 😈",
        "error_restrict_admin": "Невозможно ограничить администратора.",
        "error_wrong_time_format": "Неправильный формат времени. Используйте число + символ h, m или d. Например, 4h",
        "error_message_too_short": "Пожалуйста, избегайте бессмысленных коротких приветствий. "
                                   "Если у Вас есть вопрос или информация, напишите всё в одном сообщении. Заранее "
                                   "спасибо! 🤓",

        "report_date_format": "%d.%m.%Y в %H:%M (серверное время)",
        "report_message": '👆 Отправлено {date}\n'
                          '<a href="https://t.me/c/{chat_id}/{msg_id}">Перейти к сообщению</a>',
        "report_note": "\n\nПримечание:{note}",
        "report_delivered": "<i>Жалоба отправлена администраторам</i>",

        "action_del_msg": "Удалить сообщение",
        "action_del_and_ban": "Удалить и забанить",
        "action_del_and_readonly": "Удалить и дать RO на 2 часа",

        "action_deleted": "\n\n🗑 <b>Удалено</b>",
        "action_deleted_banned": "\n\n🗑❌ <b>Удалено, юзер забанен</b>",
        "action_deleted_readonly": "\n\n🗑🙊 <b>Удалено, юзер в режиме «только чтение» на 2 часа</b>",

        "resolved_readonly": "<i>Пользователь переведён в режим «только чтение» ({restriction_time})</i>",
        "resolved_nomedia": "<i>Пользователь переведён в режим «только текст» ({restriction_time})</i>",

        "restriction_forever": "навсегда",
        "need_admins_attention": 'Товарищи админы, в чате нужно ваше присутствие!\n\n'
                                 '<a href="https://t.me/c/{chat_id}/{msg_id}">Перейти к сообщению</a>',

        "greetings_words": ["привет", "хай", "ку", "здарова"]  # Бот среагирует на короткие сообщения с этими словами
    },
}


def get_string(key):
    """
    Get localized string. First, try language as set in config. Then, try English locale. Else - raise an exception.

    :param key: string name
    :return: localized string
    """
    lang = strings.get(Config.BOT_LANGUAGE)
    if not lang:
        if not strings.get("en"):
            raise KeyError(f'Neither "{Config.BOT_LANGUAGE}" nor "en" locales found')
        else:
            lang = strings.get("en")
    try:
        return lang[key]
    except KeyError:
        try:
            return strings.get("en")[key]
        except Exception:
            raise
