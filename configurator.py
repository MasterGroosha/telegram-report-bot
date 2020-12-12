from os import getenv
from typing import Tuple, Optional


class Config:
    BOT_TOKEN = None
    BOT_LANGUAGE = None
    GROUP_MAIN = None
    GROUP_REPORTS = None


def check_config() -> Tuple[bool, Optional[str]]:
    for key in ("BOT_TOKEN", "BOT_LANGUAGE", "GROUP_MAIN", "GROUP_REPORTS"):
        env_value = getenv(key)
        if not env_value:
            return False, f'Error: environment variable {key} is not defined. Exiting.'
        setattr(Config, key, env_value)
    return True, None
