from typing import Optional

from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    bot_token: SecretStr
    lang: str
    report_mode: str
    group_main: int
    group_reports: Optional[int]
    admins: dict = {}
    remove_joins: bool
    ban_channels: bool

    @validator("lang")
    def validate_lang(cls, v):
        if v not in ("en", "ru"):
            raise ValueError("Incorrect value. Must be one of: en, ru")
        return v

    @validator("report_mode")
    def validate_report_mode(cls, v):
        if v not in ("group", "private"):
            raise ValueError("Incorrect value. Must be one of: group, private")
        return v

    @validator("group_reports")
    def validate_group_reports(cls, v, values):
        if values.get("report_mode") == "group" and v is None:
            raise ValueError("Reports group ID not set")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()
