from datetime import datetime, timezone, timedelta
from bot.config_reader import BotConfig

from typing import NamedTuple


class FormattedDateTimeOffset(NamedTuple):
    date: str
    time: str
    offset: str

def get_formatted_datetime(
        bot_config: BotConfig,
) -> FormattedDateTimeOffset:
    offset = bot_config.utc_offset
    now_in_tz = datetime.now(tz=timezone.utc) + timedelta(hours=offset)
    if offset == 0:
        offset_str = "UTC"
    elif offset > 0:
        offset_str = f"UTC+{offset}"
    else:
        offset_str = f"UTC-{abs(offset)}"

    return FormattedDateTimeOffset(
        date=now_in_tz.strftime(bot_config.date_format),
        time=now_in_tz.strftime(bot_config.time_format),
        offset=offset_str,
    )
