from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from typing import Dict, Any


class ConfigMiddleware(BaseMiddleware):
    """
    This is middleware to push 'config' and 'lang' values further in handlers
    """
    def __init__(self, config):
        super(ConfigMiddleware, self).__init__()
        self.config = config

    async def on_pre_process_message(self, message: types.Message, data: Dict[str, Any]):
        data["config"] = self.config
        data["lang"] = self.config.lang

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: Dict[str, Any]):
        data["config"] = self.config
        data["lang"] = self.config.lang
