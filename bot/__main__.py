import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BotCommand
from aiogram.dispatcher.router import Router
from magic_filter import F

from bot.config_reader import load_config
from bot.before_start import fetch_admins, check_rights_and_permissions
from bot.handlers.not_replies import register_no_replies_handler
from bot.handlers.from_users import register_from_users_handlers
from bot.handlers.from_admins import register_from_admins_handlers
from bot.handlers.group_join import register_group_join_handler
from bot.handlers.callbacks import register_callbacks
from bot.handlers.changing_admins import register_admin_changes_handlers
from bot.localization import Lang


async def set_bot_commands(bot: Bot):
    # TODO: set narrower scopes
    commands = [
        BotCommand(command="report", description="Report message to group admins"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Reading config from env vars
    config = load_config()

    # Define the only router
    main_group_router = Router()

    # Define bot, dispatcher and include routers to dispatcher
    bot = Bot(token=config.token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(main_group_router)

    # Check that bot is admin in "main" group and has necessary permissions
    try:
        await check_rights_and_permissions(bot, config.group.main)
    except (TelegramAPIError, PermissionError) as error:
        error_msg = f"Error with main group: {error}"
        try:
            await bot.send_message(config.group.reports, error_msg)
        finally:
            print(error_msg)
            return

    # Collect admins so that we don't have to fetch them every time
    try:
        result = await fetch_admins(config, bot)
    except TelegramAPIError as error:
        error_msg = f"Error fetching main group admins: {error}"
        try:
            await bot.send_message(config.group.reports, error_msg)
        finally:
            print(error_msg)
            return
    config.admins = result

    try:
        lang = Lang(config.lang)
    except ValueError:
        print(f"Error no localization found for language code: {config.lang}")
        return

    # Restrict routers to corresponding chats
    main_group_router.message.filter(F.chat.id == config.group.main)

    # Register handlers
    register_no_replies_handler(main_group_router, config)
    register_from_users_handlers(main_group_router)
    register_from_admins_handlers(main_group_router, config)
    register_group_join_handler(main_group_router, config.remove_joins)
    register_admin_changes_handlers(main_group_router)
    register_callbacks(main_group_router)

    # Register /-commands in UI
    await set_bot_commands(bot)

    logging.info("Starting bot")

    # Start polling
    # await bot.get_updates(offset=-1)  # skip pending updates (optional)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),
                           config=config, lang=lang)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
