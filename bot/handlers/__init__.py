from aiogram import F, Router
from . import changing_admins, reporting_to_admins, reacting_to_reports

def get_routers(
        main_group_id: int,
        reports_group_id: int,
) -> list[Router]:
    main_group_router = Router()
    main_group_router.message.filter(F.chat.id == main_group_id)
    main_group_router.chat_member.filter(F.chat.id == main_group_id)
    main_group_router.include_routers(
        changing_admins.router,
        reporting_to_admins.router,
    )

    reports_group_router = Router()
    reports_group_router.message.filter(F.chat.id == reports_group_id)
    reports_group_router.callback_query.filter(F.message.chat.id == reports_group_id)
    reports_group_router.include_routers(
        reacting_to_reports.router,
    )

    return [
        main_group_router,
        reports_group_router,
    ]


# from aiogram import Router, F
#
# from bot.config_reader import config
#
#
# def setup_routers() -> Router:
#     from . import callbacks, changing_admins, from_admins, from_users, group_join, not_replies
#
#     router = Router()
#     router.message.filter(F.chat.id == config.group_main)
#
#     router.include_router(not_replies.router)
#     router.include_router(from_users.router)
#     router.include_router(from_admins.router)
#     router.include_router(group_join.router)
#     router.include_router(changing_admins.router)
#     router.include_router(callbacks.router)
#
#     return router
