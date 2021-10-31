from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino

from pkg.data import config

db = Gino()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), unique=True)
    username = db.Column(db.Unicode())
    fullname = db.Column(db.Unicode())
    status = db.Column(db.Boolean(), default=False)


class Logs(db.Model):
    __tablename__ = 'logs'
    user_id = db.Column(db.Integer(), unique=True)
    count_of_wins = db.Column(db.Integer())


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(config.POSTGRES_URI)


def setup(executor: Executor):
    executor.on_startup(on_startup)
