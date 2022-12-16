from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegistration(StatesGroup):
    number = State()
    status = State()
    name = State()
    surname = State()
    age = State()
    address = State()
