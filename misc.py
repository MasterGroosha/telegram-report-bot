import logging
from aiogram import Bot, Dispatcher
from configurator import Config, check_config
from filters import IsAdminFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

ok, error = check_config()
if not ok:
    exit(error)


if not Config.BOT_TOKEN:
    exit("No token provided")


# Initialize bot and dispatcher
bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Activate filters
dp.filters_factory.bind(IsAdminFilter)
