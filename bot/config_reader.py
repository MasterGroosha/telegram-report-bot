from dataclasses import dataclass
from os import getenv
from typing import Dict


@dataclass
class Group:
    main: int
    reports: int


@dataclass
class Config:
    token: str
    lang: str
    group: Group
    admins: Dict


def load_config():
    return Config(
        token=getenv("BOT_TOKEN"),
        lang=getenv("BOT_LANGUAGE"),
        group=Group(
            main=int(getenv("GROUP_MAIN")),
            reports=int(getenv("GROUP_REPORTS"))
        ),
        admins={}
    )
