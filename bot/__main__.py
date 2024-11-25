import asyncio

import structlog
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
# from aiogram.types import BotCommand, BotCommandScopeChat
from structlog.typing import FilteringBoundLogger

from bot.before_start import check_bot_rights_main_group, check_bot_rights_reports_group, fetch_admins
from bot.config_reader import get_config, LogConfig, BotConfig
from bot.handlers import get_routers
from bot.logs import get_structlog_config


# async def set_bot_commands(bot: Bot, main_group_id: int):
#     commands = [
#         BotCommand(command="report", description="Report message to group admins"),
#     ]
#     await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=main_group_id))


async def main():
    log_config: LogConfig = get_config(model=LogConfig, root_key="logs")
    structlog.configure(**get_structlog_config(log_config))

    bot_config: BotConfig = get_config(model=BotConfig, root_key="bot")
    bot = Bot(bot_config.token.get_secret_value())

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

    main_group_admins: dict = await fetch_admins(bot, bot_config.main_group_id)

    dp = Dispatcher(
        admins=main_group_admins,
        main_group_id=bot_config.main_group_id,
        reports_group_id=bot_config.reports_group_id,
    )
    dp.include_routers(*get_routers(
        main_group_id=bot_config.main_group_id,
        reports_group_id=bot_config.reports_group_id,
    ))


    await logger.ainfo("Program started...")
    await dp.start_polling(bot)


    # # Define bot, dispatcher and include routers to dispatcher
    # bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    # dp = Dispatcher()
    #
    # # Check that bot is admin in "main" group and has necessary permissions
    # try:
    #     await check_rights_and_permissions(bot, config.group_main)
    # except (TelegramAPIError, PermissionError) as error:
    #     error_msg = f"Error with main group: {error}"
    #     try:
    #         await bot.send_message(config.group_reports, error_msg)
    #     finally:
    #         print(error_msg)
    #         return
    #
    # # Collect admins so that we don't have to fetch them every time
    # try:
    #     result = await fetch_admins(bot)
    # except TelegramAPIError as error:
    #     error_msg = f"Error fetching main group admins: {error}"
    #     try:
    #         await bot.send_message(config.group_reports, error_msg)
    #     finally:
    #         print(error_msg)
    #         return
    # config.admins = result
    #
    # try:
    #     lang = Lang(config.lang)
    # except ValueError:
    #     print(f"Error no localization found for language code: {config.lang}")
    #     return
    #
    # # Register handlers
    # router = setup_routers()
    # dp.include_router(router)
    #
    # # Register /-commands in UI
    # await set_bot_commands(bot, config.group_main)
    #
    # logging.info("Starting bot")
    #
    # # Start polling
    # # await bot.get_updates(offset=-1)  # skip pending updates (optional)
    # await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), lang=lang)


asyncio.run(main())
