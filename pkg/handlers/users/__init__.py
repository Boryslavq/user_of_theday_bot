from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from pkg.handlers.users.start import bot_start


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
