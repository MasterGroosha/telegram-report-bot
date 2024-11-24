import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.before_start import fetch_admins, check_rights_and_permissions
from bot.config_reader import config
from bot.handlers import setup_routers
from bot.localization import Lang


async def set_bot_commands(bot: Bot, main_group_id: int):
    commands = [
        BotCommand(command="report", description="Report message to group admins"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=main_group_id))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Define bot, dispatcher and include routers to dispatcher
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    # Check that bot is admin in "main" group and has necessary permissions
    try:
        await check_rights_and_permissions(bot, config.group_main)
    except (TelegramAPIError, PermissionError) as error:
        error_msg = f"Error with main group: {error}"
        try:
            await bot.send_message(config.group_reports, error_msg)
        finally:
            print(error_msg)
            return

    # Collect admins so that we don't have to fetch them every time
    try:
        result = await fetch_admins(bot)
    except TelegramAPIError as error:
        error_msg = f"Error fetching main group admins: {error}"
        try:
            await bot.send_message(config.group_reports, error_msg)
        finally:
            print(error_msg)
            return
    config.admins = result

    try:
        lang = Lang(config.lang)
    except ValueError:
        print(f"Error no localization found for language code: {config.lang}")
        return

    # Register handlers
    router = setup_routers()
    dp.include_router(router)

    # Register /-commands in UI
    await set_bot_commands(bot, config.group_main)

    logging.info("Starting bot")

    # Start polling
    # await bot.get_updates(offset=-1)  # skip pending updates (optional)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), lang=lang)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
