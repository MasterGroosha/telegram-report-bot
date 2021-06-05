import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot.config_reader import load_config
from bot.handlers.main_group_admin import register_main_group_admin
from bot.handlers.main_group_user import register_main_group_user
from bot.handlers.main_group_events import register_group_events
from bot.handlers.callbacks_reports import register_callbacks_reports

logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="report", description="Report message to group admins"),
    ]
    await bot.set_my_commands(commands)


def get_handled_updates_list(dp: Dispatcher) -> list:
    """
    Here we collect only the needed updates for bot based on already registered handlers types.
    This way Telegram doesn't send unwanted updates and bot doesn't have to proceed them.

    :param dp: Dispatcher
    :return: a list of registered handlers types
    """
    available_updates = (
        "callback_query_handlers", "channel_post_handlers", "chat_member_handlers",
        "chosen_inline_result_handlers", "edited_channel_post_handlers", "edited_message_handlers",
        "inline_query_handlers", "message_handlers", "my_chat_member_handlers", "poll_answer_handlers",
        "poll_handlers", "pre_checkout_query_handlers", "shipping_query_handlers"
    )
    return [item.replace("_handlers", "") for item in available_updates
            if len(dp.__getattribute__(item).handlers) > 0]


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Reading config from env vars
    config = load_config()

    bot = Bot(token=config.token, parse_mode="HTML")
    bot["config"] = config
    dp = Dispatcher(bot)

    # Register handlers
    register_main_group_admin(dp, main_group_id=config.group.main)
    register_main_group_user(dp, main_group_id=config.group.main)
    register_group_events(dp, main_group_id=config.group.main)
    register_callbacks_reports(dp)

    # Register /-commands in UI
    await set_bot_commands(bot)

    logger.info("Starting bot")

    # Start polling
    # await dp.skip_updates()  # skip pending updates (optional)
    try:
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
