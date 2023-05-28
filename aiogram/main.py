import os
from dotenv import load_dotenv
import logging
import redis
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import ContentTypeFilter
from auth import auth_message_handlers
from aiogram.dispatcher.middlewares import BaseMiddleware

load_dotenv()

class AllMessagesMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Print the text of the message
        print(f'[{message.date}] Received message from {message.from_user.username} ({message.from_user.full_name}): {message.text}')
 
API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AllMessagesMiddleware())

@dp.message_handler(commands=['userInfo'])
async def get_user_data(message: types.Message):
    stored_data = r.get(f'user:{message.from_user.id}:username')
    await message.reply(f"Ваше имя: {stored_data}")

auth_message_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)