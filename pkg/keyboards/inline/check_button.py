from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def check_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Я подписался!", callback_data="check"))
    return kb
