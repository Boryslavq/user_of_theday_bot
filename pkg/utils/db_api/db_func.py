from asyncpg import UniqueViolationError
import fileinput
from pkg.data.config import ADMINS
from pkg.utils.db_api.database import User, db, Logs


async def add_user(user_id: int, username: str, full_name: str):
    try:
        await User.create(user_id=user_id, username=username,
                          fullname=full_name)
    except UniqueViolationError:
        await User.update.values(username=username, fullname=full_name).where(
            'user_id' == user_id).gino.status()


async def get_all_users():
    all_users = await User.query.gino.all()
    return all_users


async def get_users_status() -> [tuple]:
    return await User.select('user_id', 'username', 'fullname').where(User.status == True).gino.all()


async def add_user_to_log(user_id: int):
    try:
        await Logs.create(user_id=user_id, count_of_wins=1)
    except UniqueViolationError:
        num = await get_count(user_id)
        await Logs.update.values(count_of_wins=num + 1).where(Logs.user_id == user_id).gino.status()


async def get_logs():
    return await Logs.select('user_id', 'count_of_wins').gino.all()


async def get_count(user_id: int) -> int:
    return await Logs.select('count_of_wins').where(Logs.user_id == user_id).gino.scalar()


async def delete_user(user_id: int):
    await User.delete.where(User.user_id == user_id).gino.status()


async def get_status(user_id: int) -> bool:
    return await User.select('status').where(User.user_id == user_id).gino.scalar()


async def reg_status(user_id: int):
    if not await get_status(user_id):
        status = True
        await User.update.values(status=status).where(User.user_id == user_id).gino.status()


async def del_status(user_id: int):
    if await get_status(user_id):
        status = False
        await User.update.values(status=status).where(User.user_id == user_id).gino.status()
