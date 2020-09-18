import datetime
import typing
import localization
from configurator import config


def get_restriction_time(string: str) -> typing.Optional[int]:
    """
    Get user restriction time in seconds

    :param string: string to check for multiplier. The last symbol should be one of:
        "m" for minutes, "h" for hours and "d" for days
    :return: number of seconds to restrict or None if error
    """
    if len(string) < 2:
        return None
    letter = string[-1]
    try:
        number = int(string[:-1])
    except TypeError:
        return None
    else:
        if letter == "m":
            return 60 * number
        elif letter == "h":
            return 3600 * number
        elif letter == "d":
            return 86400 * number
        else:
            return None


def get_report_comment(message_date: datetime.datetime, message_id: int, report_message: typing.Optional[str]) -> str:
    """
    Generates a report message for admins

    :param message_date: Datetime when reported message was sent
    :param message_id: ID of that message
    :param report_message: An optional note for admins so that they can understand what's wrong
    :return: A report message for admins in report chat
    """
    msg = localization.get_string("report_message").format(
        date=message_date.strftime(localization.get_string("report_date_format")),
        chat_id=get_url_chat_id(config.groups.main),
        msg_id=message_id)

    if report_message:
        msg += localization.get_string("report_note").format(note=report_message)
    return msg


def get_url_chat_id(chat_id: int) -> int:
    """
    Well, this value is a "magic number", so I have to explain it a bit.
    I don't want to use hardcoded chat username, so I just take its ID (see "group_main" variable above),
    add id_compensator and take a positive value. This way I can use https://t.me/c/{chat_id}/{msg_id} links,
    which don't rely on chat username.

    :param chat_id: chat_id to apply magic number to
    :return: chat_id for t.me links
    """
    return abs(chat_id+1_000_000_000_000)
