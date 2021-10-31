from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

admin_callback = CallbackData("admin", "name", "action")
button_callback = CallbackData("button", "change", "index")


async def panel():
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton(text="Посмотреть всех участвующих 📣",
                                callback_data=admin_callback.new(name="panel", action="check_sub"))).add(
        InlineKeyboardButton(text="Изменить текст сообщений 🎺",
                             callback_data=admin_callback.new(name="panel", action="change"))

    )
    return kb


async def generate_kb():
    kb = InlineKeyboardMarkup()
    with open("text_on_message.txt", "r", encoding="utf-8") as f:
        text = f.readlines()

    for index, value in enumerate(text):
        if index + 1 <= 6:
            kb.add(
                InlineKeyboardButton(text=f"Изменить №{index + 1}",
                                     callback_data=button_callback.new(change="select", index=index)))

    return kb


async def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='close'))
    return kb
