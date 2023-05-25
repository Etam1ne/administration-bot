import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import signIn, signUp

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class AuthStates(StatesGroup):
    usernameState = State()
    passwordState = State()
    authenticatedState = State()

@dp.message_handler(commands=['signIn'])
async def start_auth_handler(message: types.Message): 
    await message.reply('Напишите имя пользователя')
    await AuthStates.usernameState.set()

@dp.message_handler(state=AuthStates.usernameState)
async def handle_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Теперь введите пароль")
    await AuthStates.passwordState.set()

@dp.message_handler(state=AuthStates.passwordState)
async def handle_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    if await signIn(username, password):
        await message.reply(f"Здравствуйте, {username}, Вы успешно вошли в аккаунт")
    else:
        await message.reply("Имя пользователя или пароль неверные, попробуйте еще раз или /leave закройте окно входа")

    await state.finish()

class SignUpStates(StatesGroup):
    usernameState = State()
    passwordState = State()

@dp.message_handler(commands=['signUp'])
async def start_sign_up_handler(message: types.Message, state: FSMContext):
    await message.reply("Введите имя пользователя")
    await SignUpStates.usernameState.set()

@dp.message_handler(state=SignUpStates.usernameState)
async def handle_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Теперь введите пароль")
    await SignUpStates.passwordState.set()

@dp.message_handler(state=SignUpStates.passwordState)
async def handle_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    if await signUp(username, password):
        await message.reply(f"Здравствуйте, {username}, Вы успешно создали аккаунт")
    else:
        await message.reply("Имя пользователя или пароль неверные, попробуйте еще раз или /leave закройте окно регистрации")
        await SignUpStates.usernameState.set()

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)