from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import datetime

from api_client import APIClient

admin_router = Router()
client = APIClient('http://127.0.0.1:8000')

ADMIN_ID = {1396686124, 1935591182}


@admin_router.message(Command('new_users'), F.from_user.id.in_(ADMIN_ID))
async def new_users(message: Message):
    if len(message.text.split()) != 3:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /new_users <start_date> <end_date>')
        return

    try:
        start_date = datetime.datetime.strptime(message.text.split()[1], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(message.text.split()[2], '%Y-%m-%d')
    except ValueError:
        await message.answer('Неверный формат даты. Используйте формат даты "ГГГГ-ММ-ДД"')
        return

    await message.answer(f'Количество новых пользователей за период с {start_date.date()} по {end_date.date()}:')


@admin_router.message(Command('users_count'), F.from_user.id.in_(ADMIN_ID))
async def users_count(message: Message):
    await message.answer('Количество пользователей')
    # из бд количество пользователей


@admin_router.message(Command('change_price'), F.from_user.id.in_(ADMIN_ID))
async def change_price(message: Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer(
            'Неверное количество аргументов. Используйте команду в формате: /change_price <model_name> <new_price>')
        return

    model_name = args[1]
    new_price = args[2]

    try:
        new_price = float(new_price)
    except ValueError:
        await message.answer('Новый ценник должен быть числом')
        return

    # Обновляем цену в бд

    await message.answer(f'Цена модели "{model_name}" успешно изменена на {new_price}')


@admin_router.message(Command('change_balance'), F.from_user.id.in_(ADMIN_ID))
async def change_balance(message: Message):
    if len(message.text.split()) != 3:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /change_balance <user_name> <new_balance>')
        return

    user_id = message.text.split()[1]
    new_balance = message.text.split()[2]

    try:
        new_price = float(new_balance)
    except ValueError:
        await message.answer('Новый баланс должен быть числом')
        return

    # Изменяем баланс пользователя в бд

    await message.answer(f'Баланс пользователя с ID {user_id} успешно изменен на {new_balance}')


@admin_router.message(Command('balance_user'))
async def balance(message: Message):
    if len(message.text.split()) != 2:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /balance_user <user_name>')
        return

    user_name = message.text.split()[1]

    user = await client.get_user(user_name)
    token_amount = user['token_amount']
    await message.answer(f'Ваш текущий баланс пользователя {user_name}: {token_amount}')