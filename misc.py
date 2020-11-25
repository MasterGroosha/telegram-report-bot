import logging
from aiogram import Bot, Dispatcher
from configurator import config, check_config_file
from filters import IsAdminFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

if not check_config_file("config/config.ini"):
    exit("Errors while parsing config file. Exiting.")

if not config.bot.token:
    exit("No token provided")


# Initialize bot and dispatcher
bot = Bot(token=config.bot.token, parse_mode="HTML")
dp = Dispatcher(bot)

# Activate filters
dp.filters_factory.bind(IsAdminFilter)
