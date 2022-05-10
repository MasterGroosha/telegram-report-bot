class Lang:
    strings = {
        "en": {
            "error_no_reply": "This command must be sent as a reply to one's message!",
            "error_report_admin": "Whoa! Don't report admins 😈",
            "error_restrict_admin": "You cannot restrict an admin.",
            "error_cannot_restrict": "You are not allowed to restrict users",
            "error_cannot_report_linked": "You cannot report messages from linked channel",

            "report_date_format": "%d.%m.%Y at %H:%M",
            "report_message": '👆 Sent {time} (server time)\n'
                              '<a href="{msg_url}">Go to message</a>',
            "report_note": "\n\nNote: {note}",
            "report_sent": "<i>Report sent</i>",

            "action_del_msg": "Delete message",
            "action_del_and_ban": "Delete and ban",

            "action_deleted": "\n\n🗑 <b>Deleted</b>",
            "action_deleted_banned": "\n\n🗑❌ <b>Deleted, user or chat banned</b>",
            "action_deleted_partially": "Some messages couldn't be found or deleted. "
                                        "Perhaps they were deleted by another admin.",

            "readonly_forever": "🙊 <i>User set to read-only mode forever</i>",
            "readonly_temporary": "🙊 <i>User set to read-only mode until {time} (server time)</i>",
            "nomedia_forever": "🖼 <i>User set to text-only mode forever</i>",
            "nomedia_temporary": "🖼 <i>User set to text-only mode until {time} (server time)</i>",
            "channel_banned_forever": "📛 <i>Channel banned forever</i>",

            "need_admins_attention": 'Dear admins, your presence in chat is needed!\n\n'
                                     '<a href="{msg_url}">Go to chat</a>',

            "channels_not_allowed": "Sending messages on behalf of channels is not allowed in this group. Channel banned."
        },
        "ru": {
            "error_no_reply": "Эта команда должна быть ответом на какое-либо сообщение!",
            "error_report_admin": "Админов репортишь? Ай-ай-ай 😈",
            "error_restrict_admin": "Невозможно ограничить администратора.",
            "error_cannot_restrict": "У вас нет права ограничивать пользователей",
            "error_cannot_report_linked": "Нельзя жаловаться на сообщения из привязанного канала",

            "report_date_format": "%d.%m.%Y в %H:%M",
            "report_message": '👆 Отправлено {time} (время серверное)\n'
                              '<a href="{msg_url}">Перейти к сообщению</a>',
            "report_note": "\n\nПримечание: {note}",
            "report_sent": "<i>Жалоба отправлена администраторам</i>",

            "action_del_msg": "Удалить сообщение",
            "action_del_and_ban": "Удалить и забанить",

            "action_deleted": "\n\n🗑 <b>Удалено</b>",
            "action_deleted_banned": "\n\n🗑❌ <b>Удалено, юзер или чат забанен</b>",
            "action_deleted_partially": "Не удалось найти или удалить некоторые сообщения. "
                                        "Возможно, они уже были удалены другим админом.",

            "readonly_forever": "🙊 <i>Пользователь переведён в режим «только чтение» навсегда</i>",
            "readonly_temporary": "🙊 <i>Пользователь переведён в режим «только чтение» до {time} (время серверное)</i>",
            "nomedia_forever": "🖼 <i>Пользователю запрещено отправлять медиафайлы навсегда</i>",
            "nomedia_temporary": "🖼 <i>Пользователю запрещено отправлять медиафайлы до {time} (время серверное)</i>",
            "channel_banned_forever": "📛 <i>Канал забанен навсегда</i>",

            "need_admins_attention": 'Уважаемые админы, в чате нужно ваше присутствие!\n\n'
                                     '<a href="{msg_url}">Перейти к чату</a>',

            "channels_not_allowed": "В этой группе запрещено отправлять сообщения от имени канала. Сам канал забанен."
        },
    }

    def __init__(self, language_key: str):
        if language_key in self.strings.keys():
            self.chosen_lang = language_key
        else:
            raise ValueError(f"No such language: {language_key}")

    def get(self, key):
        return self.strings.get(self.chosen_lang, {}).get(key, "%MISSING STRING%")
