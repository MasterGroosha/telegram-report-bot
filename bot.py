from aiogram import executor
from misc import dp
import handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
