import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from pkg.keyboards.inline.check_button import check_kb
from pkg.utils.db_api.db_func import add_user, reg_status, get_status, del_status, get_users_status, add_user_to_log, \
    get_logs, get_all_users
from pkg.utils.mics.change_status import change_status
from pkg.utils.mics.subscription import check
from pkg.data.config import CHANNEL_ID, CHAT_ID
from aiogram.utils.exceptions import BadRequest


async def bot_start(message: types.Message):
    if message.chat.id > 0:
        chat = await message.bot.get_chat(CHANNEL_ID)
        invite_link = await chat.export_invite_link()
        msg = f"<a href='{invite_link}'>{chat.title}</a>"
        await message.answer(f"<b>Здравствуйте!</b> для того что бы сыграть подпишись на наш канал\n{msg}",
                             reply_markup=await check_kb(), disable_web_page_preview=True)
        await add_user(message.from_user.id, message.from_user.username,
                       message.from_user.full_name)


async def check_sub(callback: types.CallbackQuery):
    if callback.message.chat.id > 0:
        status = await check(user_id=callback.from_user.id, channel=CHANNEL_ID)
        await callback.bot.get_chat(CHANNEL_ID)
        if status:
            await callback.message.edit_text("Ты подписалсьа!")
        else:
            await callback.answer("Ты не подписалсьа")


async def registration(message: types.Message):
    if message.chat.id > 0:
        get_sub = await check(user_id=message.from_user.id, channel=CHANNEL_ID)
        if get_sub:
            status = await get_status(message.from_user.id)
            msg = "Результаты объявит администратор в чате <a href='https://t.me/BlefachChat'>Блефачечная</a>\n" \
                  "Ждём тебя там!"
            await message.answer("Ты в игре!") if status else await message.answer(
                f"Отлично ты в игре!\n{msg}", disable_web_page_preview=True)
            await reg_status(message.from_user.id)
        else:
            await message.answer("Подпишись не ленись")


async def delete(message: types.Message):
    if message.chat.id > 0:
        get_sub = await check(user_id=message.from_user.id, channel=CHANNEL_ID)
        if get_sub:
            await message.answer("Ты не в игре ну и ладно")
            await del_status(message.from_user.id)
        else:
            await message.answer("Подпишись не ленись")


async def run(message: types.Message):
    global rand_num
    with open("text_on_message.txt", "r", encoding="utf-8") as f:
        text = f.readlines()
    text = list(text)
    for i in text[:6]:
        await message.answer(i)
        await asyncio.sleep(1)

    all_users = []
    users = await get_users_status()
    for user in users:
        all_users.append(user.user_id)
    try:
        rand_num = random.randint(0, len(all_users) - 1)
    except ValueError:
        await message.answer("Учасников нету")
        return

    try:
        chat_member_info = await message.bot.get_chat_member(user_id=all_users[rand_num], chat_id=message.chat.id)
        member = {chat_member_info.user.get_mention(as_html=True)}
        encodedstr = f"Поздравляю " + "".join(member) + " вы выиграли!"
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=encodedstr, parse_mode="HTML")
        await add_user_to_log(all_users[rand_num])
        await asyncio.sleep(10)
        users = await get_all_users()
        await change_status()
        for user in users:
            try:
                await message.bot.send_message(chat_id=user.user_id,
                                               text="Розыгрыш окончен, жми /reg"
                                                    " что бы принять участие в следующей игре!")

                await asyncio.sleep(0.3)
            except Exception:
                pass
    except BadRequest:
        await message.answer("Похоже,пользователя нету в этом чате:(\nЗначит переигрываем!")
        await del_status(all_users[rand_num])


async def close(callback: types.CallbackQuery, state: FSMContext):
    await state.reset_state()

    await callback.message.delete()


async def stats(message: types.Message):
    get_sub = await check(user_id=message.from_user.id, channel=CHANNEL_ID)
    if get_sub:
        winners = await get_logs()
        encodedstr = ""
        count = 0
        for user in winners:
            chat_member_info = await message.bot.get_chat_member(user_id=user.user_id, chat_id=message.chat.id)
            member = {chat_member_info.user.get_mention(as_html=True)}
            encodedstr += f"" + "".join(member) + f" выиграл {user.count_of_wins} раз(а)\n"
            count += 1
        if count > 0:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text=f"🎉 Наши победители!\n\n{encodedstr}", parse_mode="HTML")
        else:
            await message.bot.send_message(chat_id=message.chat.id, text="Увы, но пока победителей нету:(")
