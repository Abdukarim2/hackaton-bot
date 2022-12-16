from aiogram import types
from loader import dp
from utils.db import get_user
from utils.state import UserRegistration
from messages.message import MESSAGES as MS
from buttons.button import sign_up, get_contact, menu


@dp.message_handler()
async def messages(message: types.Message):
    msg = message.text
    user = message.chat
    us = get_user(user.id)
    if us:
        if msg.lower() == "✅ asosiy qoidalar":
            for text in MS.get("rules"):
                await message.answer(f"{text}")
        elif msg.lower() == "🧑‍💻 kimlar uchun":
            for text in MS.get("for"):
                await message.answer(f"{text}")
        elif msg.lower() == "📄 shartlar":
            for text in MS.get("conditions"):
                await message.answer(f"{text}")
        elif msg.lower() == "🗓 hakaton tartibi":
            for text in MS.get("hackathon"):
                await message.answer(f"{text}")
        elif msg.lower() == "🎁 sovrin":
            for text in MS.get("gift"):
                await message.answer(f"{text}")
        else:
            await message.answer(f"Siz Hakatonga ro’yhatdan o’tgansiz. Sizning <b>ID’ingiz : {us[0]}</b>", reply_markup=menu())
    else:
        if msg.lower() == "/start":
            for text in MS.get("start"):
                await message.answer(f"{text}")
            await message.answer(MS.get("sign_up")[0], reply_markup=sign_up())
        elif msg.lower() == "ro'yhatdan o'tish":
            await UserRegistration.number.set()
            await message.answer("Raqamingizni tasdiqlating yoki kiritin:",
                                 reply_markup=get_contact())
        else:
            await message.answer(MS.get("sign_up")[0], reply_markup=sign_up())

