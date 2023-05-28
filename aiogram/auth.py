from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import redis
from database import sign_in, sign_up

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

async def check_login(userId: int) -> bool:
    stored_data = r.get(f'user:{userId}:username')
    if (stored_data is None): return False
    return True

# LEAVE

async def leave_command(message: types.Message):
    r.delete(f'user:{message.from_user.id}:username')
    await message.reply('Вы вышли из аккаунта')

# SIGN IN

class SignInStates(StatesGroup):
    usernameState = State()
    passwordState = State()
    authenticatedState = State()

async def start_sign_in_handler(message: types.Message):
    if(await check_login(message.from_user.id)): 
        await message.reply('Вы уже вошли')
        return
    
    await message.reply('Напишите имя пользователя')
    await SignInStates.usernameState.set()

async def handle_username_sign_in(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Теперь введите пароль")
    await SignInStates.passwordState.set()

async def handle_password_sign_in(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    if await sign_in(username, password):
        r.set(f'user:{message.from_user.id}:username', username)
        stored_data = r.get(f'user:{message.from_user.id}:username')
        await message.reply(f"Здравствуйте, {stored_data}, Вы успешно вошли в аккаунт")
    else:
        await message.reply("Имя пользователя или пароль неверные, попробуйте еще раз /signIn")

    await state.finish()

# SIGN UP

class SignUpStates(StatesGroup):
    usernameState = State()
    passwordState = State()

async def start_sign_up_handler(message: types.Message, state: FSMContext):
    if(await check_login(message.from_user.id)): 
        await message.reply('Вы уже вошли')
        await state.finish()
    
    await message.reply("Введите имя пользователя")
    await SignUpStates.usernameState.set()

async def handle_username_sign_up(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Теперь введите пароль")
    await SignUpStates.passwordState.set()

async def handle_password_sign_up(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    if await sign_up(username, password):
        r.set(f'user:{message.from_user.id}:username', username)
        stored_data = r.get(f'user:{message.from_user.id}:username')
        await message.reply(f"Здравствуйте, {stored_data}, Вы успешно создали аккаунт")
    else:
        await message.reply("Имя пользователя или пароль неверные, попробуйте еще раз /signUp")

    await state.finish()
def auth_message_handlers(dp: Dispatcher):
    dp.register_message_handler(leave_command, commands=['leave'])
    dp.register_message_handler(start_sign_in_handler, commands=['signIn'])
    dp.register_message_handler(handle_username_sign_in, state=SignInStates.usernameState)
    dp.register_message_handler(handle_password_sign_in, state=SignInStates.passwordState)
    dp.register_message_handler(start_sign_up_handler, commands=['signUp'])
    dp.register_message_handler(handle_username_sign_up, state=SignUpStates.usernameState)
    dp.register_message_handler(handle_password_sign_up, state=SignUpStates.passwordState)