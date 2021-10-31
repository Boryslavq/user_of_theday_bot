from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher

from pkg.utils.db_api.db_func import del_status, get_users_status


async def change_status():
    users = await get_users_status()
    for user in users:
        await del_status(user.user_id)
