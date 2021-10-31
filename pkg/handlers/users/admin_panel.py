import csv

from aiogram import types
from aiogram.dispatcher import FSMContext

from pkg.keyboards.inline.panel import panel, generate_kb, cancel_kb
from pkg.states.states import ChangeText
from pkg.utils.db_api.db_func import get_users_status


async def admin_panel(message: types.Message):
    await message.answer("Выберите действие", reply_markup=await panel())


async def get_all(callback: types.CallbackQuery):
    await callback.answer()
    users = await get_users_status()
    fied_names = ["user_id", "username", "fullname"]
    with open("new.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fied_names)
        writer.writeheader()

    count = 0
    for user in users:
        with open("new.csv", "a", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow((user.user_id, user.username, user.fullname,))
            count += 1

    await callback.bot.send_document(caption=f"Общее количество учасников: {count}",
                                     chat_id=callback.message.chat.id,
                                     document=open("new.csv", "rb"))


async def change(callback: types.CallbackQuery):
    await callback.answer()
    with open("text_on_message.txt", "r", encoding="utf-8") as f:
        text = f.readlines()

    encoded_string = ""
    for index, value in enumerate(text):
        if index + 1 <= 6:
            encoded_string += f"Сообщение №{index + 1}:\n{value}\n"

    await callback.message.answer(f"Выберите какое сообщение поменять:\n\n{encoded_string}",
                                  reply_markup=await generate_kb())


async def text_remake(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    index = int(callback_data.get("index"))
    await callback.message.edit_text("Введите текст...", reply_markup=await cancel_kb())
    await ChangeText.add_text.set()
    await state.update_data(index=index)


async def text_change(message: types.Message, state: FSMContext):
    await state.update_data(add_text=message.text)
    async with state.proxy() as data:
        index = int(data.get("index"))
        add_text = data.get("add_text")
    with open("text_on_message.txt", "r", encoding="utf-8") as f:
        text = f.read()
    text = text.split("\n")
    text[index] = add_text
    with open("text_on_message.txt", "w", encoding="utf-8"):
        pass
    with open("text_on_message.txt", "a", encoding="utf-8") as f:
        for item in text:
            f.write("%s\n" % item)
    await message.answer("Сообщение успешно изменено")
    await state.finish()
