from aiogram import F, Router
from . import changing_admins, reporting_to_admins, reacting_to_reports, restricting_users, additional_features

def get_routers(
        main_group_id: tuple[int, ...],
        reports_group_id: int,
) -> list[Router]:
    main_group_router = Router()
    main_group_router.message.filter(F.chat.id.in_(main_group_id))
    main_group_router.chat_member.filter(F.chat.id.in_(main_group_id))
    main_group_router.include_routers(
        changing_admins.router,
        restricting_users.router,
        reporting_to_admins.router,
        additional_features.router,
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
