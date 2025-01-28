from enum import StrEnum, auto
from functools import lru_cache
from os import getenv
from tomllib import load
from typing import Type, TypeVar, Union

from pydantic import BaseModel, SecretStr, field_validator

ConfigType = TypeVar("ConfigType", bound=BaseModel)


class LogRenderer(StrEnum):
    JSON = auto()
    CONSOLE = auto()


class BotConfig(BaseModel):
    token: SecretStr
    main_group_id: tuple[int, ...]
    reports_group_id: int
    utc_offset: int
    date_format: str
    time_format: str
    remove_joins: bool
    auto_ban_channels: bool

    @field_validator("main_group_id", mode="before")
    @classmethod
    def main_group_id_transform(cls, raw: Union[int, tuple[int, ...]]) -> tuple[int, ...]:
        if isinstance(raw, list):
            return tuple(raw)
        return (raw,)


class LogConfig(BaseModel):
    show_datetime: bool
    datetime_format: str
    show_debug_logs: bool
    time_in_utc: bool
    use_colors_in_console: bool
    renderer: LogRenderer
    allow_third_party_logs: bool

    @field_validator('renderer', mode="before")
    @classmethod
    def log_renderer_to_lower(cls, v: str):
        return v.lower()


@lru_cache
def parse_config_file() -> dict:
    file_path = getenv("CONFIG_FILE_PATH")
    if file_path is None:
        error = "Could not find settings file"
        raise ValueError(error)
    with open(file_path, "rb") as file:
        config_data = load(file)
    return config_data


@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = parse_config_file()
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)
    return model.model_validate(config_dict[root_key])
