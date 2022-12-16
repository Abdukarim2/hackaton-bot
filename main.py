from aiogram import executor
from loader import dp
from utils.db import init
from handlers import message_handler, state_handler


async def on_start(_):
    init()
    print("bot is runing...")


async def on_shutdown(_):
    print("bot is stoped")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown)
