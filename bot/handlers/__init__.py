from aiogram import Router, F

from bot.config_reader import config


def setup_routers() -> Router:
    from . import callbacks, changing_admins, from_admins, from_users, group_join, not_replies

    router = Router()
    router.message.filter(F.chat.id == config.group_main)

    router.include_router(not_replies.router)
    router.include_router(from_users.router)
    router.include_router(from_admins.router)
    router.include_router(group_join.router)
    router.include_router(changing_admins.router)
    router.include_router(callbacks.router)

    return router
