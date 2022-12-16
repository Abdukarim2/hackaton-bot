import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils.state import UserRegistration
from buttons.button import sign_up, check, back, regions
from messages.message import MESSAGES as MS
from utils.db import create_user


@dp.message_handler(lambda message: message.text.lower() == "orqaga ➡", state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Ro'yhatdan o'tish bekor qilindi", reply_markup=sign_up())


async def check_status(message):
    user = message.chat
    chanel1 = await bot.get_chat_member("@robocode_andijan", user.id)
    chanel2 = await bot.get_chat_member("@pybloguz", user.id)
    if chanel1.status == "member" and chanel2.status == "member":
        await message.answer("Ismingizni kiritin:", reply_markup=back())
        await UserRegistration.next()
    else:
        await message.answer("Ro’yhatdan o’tishda davom etish uchun iltimos @robocode_andijan va @pybloguz kanallariga obuna bo’ling va <b>Tekshirish</b> tugmasini bosing", reply_markup=check())


@dp.message_handler(state=UserRegistration.number)
async def rg_number_text(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        if msg.strip("+").isdigit() and len(msg.strip("+")) == 9 or len(msg.strip("+")) == 12 and "." not in msg.strip("+"):
            data['number'] = int(msg)
            await UserRegistration.next()
            await check_status(message)
        else:
            await message.answer("Iltimos raqamingizni to'g'ri tasdiqlang yoki kiritin:")


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegistration.number)
async def rg_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = int(message.contact.phone_number)
        await UserRegistration.next()
        await check_status(message)


@dp.message_handler(state=UserRegistration.status)
async def rg_status(message: types.Message):
    await check_status(message)


@dp.message_handler(state=UserRegistration.name)
async def rg_name(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        if len(msg.lower()) >= 3 and msg.isalpha():
            data['name'] = msg
            await UserRegistration.next()
            await message.answer("Familyangizni kiritin:")
        else:
            await message.answer("Ismingizni to'g'ri kiritin:")


@dp.message_handler(state=UserRegistration.surname)
async def rg_surname(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        if len(msg.lower()) >= 3 and msg.isalpha():
            data['surname'] = msg
            await UserRegistration.next()
            await message.answer("Yoshingizni kiritin:")
        else:
            await message.answer("Familyangizni to'g'ri kiritin:")


@dp.message_handler(state=UserRegistration.age)
async def rg_age(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        if msg.isdigit() and 18 >= int(msg) > 12:
            data['age'] = int(msg)
            await UserRegistration.next()
            await message.answer("Yashash manzilingizni kiritin:", reply_markup=regions())
        else:
            await message.answer("Yosh oralig'i 12 yoshdan 18 yoshgacha bo'lishi kerak")


@dp.message_handler(state=UserRegistration.address)
async def rg_address_text(message: types.Message, state: FSMContext):
    date = datetime.datetime.now()
    username = message.chat.username if message.chat.username else 'none'
    msg = message.text
    regs = MS.get("regions")
    async with state.proxy() as data:
        if msg.lower() in regs:
            data['address'] = msg.title()
            data['user_id'] = message.chat.id
            data['username'] = username
            data['date'] = date.strftime("%Y-%m-%d %H:%M:%S")
            await state.finish()
            new_user = create_user(data.as_dict())
            if new_user:
                success = f"Tabriklaymiz siz Hakatonga ro’yhatdan o’tdingiz !\n<b>ID: AB{new_user.lastrowid}</b>\nYuqorida ko’rsatilgan kanallar orqali yangiliklarni kuzatib boring. Omad !"
                await message.answer(success)
            else:
                await message.answer("Nimadur hato ketdi iltimos boshqatdan urinib ko'rin")
        else:
            await message.answer("Yashash manzilingizni to'g'ri kiritin:", reply_markup=regions())


@dp.callback_query_handler(lambda call: call.data.startswith("region"), state=UserRegistration.address)
async def rg_address_call(callback: types.CallbackQuery, state: FSMContext):
    date = datetime.datetime.now()
    username = callback.from_user.username if callback.from_user.username else 'none'
    msg = callback.data[7:]
    async with state.proxy() as data:
        data['address'] = msg.title()
        data['user_id'] = callback.from_user.id
        data['username'] = username
        data['date'] = date.strftime("%Y-%m-%d %H:%M:%S")
        await state.finish()
        new_user = create_user(data.as_dict())
        if new_user:
            success = f"Tabriklaymiz siz Hakatonga ro’yhatdan o’tdingiz !\n<b>ID: AB{new_user.lastrowid}</b>\nYuqorida ko’rsatilgan kanallar orqali yangiliklarni kuzatib boring. Omad !"
            await bot.send_message(callback.from_user.id, success)
        else:
            await bot.send_message(callback.from_user.id, "Nimadur hato ketdi iltimos boshqatdan urinib ko'rin")

