from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, Command

from pkg.filters import IsGroup, AdminFilter
from pkg.handlers.users.admin_panel import admin_panel, change, text_remake, text_change, get_all
from pkg.handlers.users.handlers import bot_start, registration, check_sub, delete, run, close, stats
from pkg.data import config
from pkg.keyboards.inline.panel import admin_callback, button_callback
from pkg.states.states import ChangeText


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_callback_query_handler(check_sub, text='check')
    dp.register_message_handler(registration, commands=['reg'])
    dp.register_message_handler(delete, commands=['del'])
    dp.register_message_handler(AdminFilter, admin_panel, commands='admin_panel', user_id=config.ADMINS)
    dp.register_callback_query_handler(change, admin_callback.filter(action='change'))
    dp.register_callback_query_handler(get_all, admin_callback.filter(action="check_sub"))
    dp.register_callback_query_handler(close, text='close', state='*')
    dp.register_callback_query_handler(text_remake, button_callback.filter(change="select"))
    dp.register_message_handler(text_change, state=ChangeText.add_text)
    dp.register_message_handler(AdminFilter, stats, commands=["stats"], user_id=config.ADMINS)

    dp.register_message_handler(run, Command(commands='run', prefixes='!'), user_id=config.ADMINS)
