import asyncio

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from structlog.typing import FilteringBoundLogger

from bot.before_start import check_bot_rights_main_group, check_bot_rights_reports_group, fetch_admins, set_bot_commands
from bot.config_reader import get_config, LogConfig, BotConfig
from bot.fluent_loader import get_fluent_localization
from bot.handlers import get_routers
from bot.logs import get_structlog_config


async def main():
    log_config: LogConfig = get_config(model=LogConfig, root_key="logs")
    structlog.configure(**get_structlog_config(log_config))

    bot_config: BotConfig = get_config(model=BotConfig, root_key="bot")
    bot = Bot(
        token=bot_config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    logger: FilteringBoundLogger = structlog.get_logger()

    # Check that bot can run properly
    try:
        await check_bot_rights_main_group(bot, bot_config.main_group_id)
    except (TelegramAPIError, PermissionError) as ex:
        await logger.aerror(f"Cannot use bot in main group, because {ex.__class__.__name__}: {str(ex)}")
        await bot.session.close()
        return

    try:
        await check_bot_rights_reports_group(bot, bot_config.reports_group_id)
    except (TelegramAPIError, PermissionError) as ex:
        await logger.aerror(f"Cannot use bot in reports group, because {ex.__class__.__name__}: {str(ex)}")
        await bot.session.close()
        return

    await set_bot_commands(bot, bot_config.main_group_id)

    main_group_admins: dict = await fetch_admins(bot, bot_config.main_group_id)

    l10n = get_fluent_localization()

    dp = Dispatcher(
        admins=main_group_admins,
        bot_config=bot_config,
        l10n=l10n,
    )
    dp.include_routers(*get_routers(
        main_group_id=bot_config.main_group_id,
        reports_group_id=bot_config.reports_group_id,
    ))


    await logger.ainfo("Program started...")
    await dp.start_polling(bot)

asyncio.run(main())
