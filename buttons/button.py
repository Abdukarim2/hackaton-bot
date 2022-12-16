from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from messages.message import MESSAGES as MS

def sign_up():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(
        KeyboardButton("Ro'yhatdan o'tish")
    )
    return kb


def get_contact():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.insert(
        KeyboardButton("Tasdiqlash ☎", request_contact=True)
    )
    kb.insert(
        KeyboardButton("Orqaga ➡")
    )
    return kb


def check():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(
        KeyboardButton("Tekshirish")
    )
    return kb


def back():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(
        KeyboardButton("Orqaga ➡")
    )
    return kb


def regions():
    kb = InlineKeyboardMarkup(row_width=1)
    for region in MS.get("regions"):
        kb.insert(
            InlineKeyboardButton(f"{region.title()}", callback_data=f"region_{region}")
        )
    return kb


def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for text in MS.get("menu"):
        kb.insert(
            KeyboardButton(f"{text}")
        )
    return kb
