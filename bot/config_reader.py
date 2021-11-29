from dataclasses import dataclass
from os import getenv
from typing import Dict, Optional


@dataclass
class Group:
    main: int
    reports: Optional[int]


@dataclass
class Config:
    token: str
    lang: str
    group: Group
    admins: Dict
    report_mode: str
    remove_joins: bool


def load_config():
    return Config(
        token=getenv("BOT_TOKEN"),
        lang=getenv("BOT_LANGUAGE"),
        group=Group(
            main=int(getenv("GROUP_MAIN")),
            reports=int(getenv("GROUP_REPORTS"))
        ),
        admins={},
        report_mode=getenv("REPORT_MODE", "private"),
        remove_joins=getenv("REMOVE_JOINS", "no") in ("1", "yes", "True")
    )
