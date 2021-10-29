from aiogram import types


async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
