from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
import matplotlib.pyplot as plt
import datetime

from api_client import APIClient
from model_enum import CVModelEnum

admin_router = Router()
client = APIClient('http://127.0.0.1:8000')


@admin_router.message(Command('new_users'))
async def new_users(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    if len(message.text.split()) != 3:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /new_users <start_date> <end_date>')
        return

    try:
        start_date = datetime.datetime.strptime(message.text.split()[1], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(message.text.split()[2], '%Y-%m-%d')
    except ValueError:
        await message.answer('Неверный формат даты. Используйте формат даты "ГГГГ-ММ-ДД"')
        return

    users = await client.get_all_user()

    dates = [d['registration_date'] for d in users]
    users_count = [len([d for d in users if d['registration_date'] == date]) for date in dates]

    dates_in_range = [date for date in dates if start_date <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date]
    users_count_in_range = [users_count[dates.index(date)] for date in dates_in_range]

    # Создаем график
    plt.plot(dates_in_range, users_count_in_range)
    plt.ylabel('Количество пользователей')
    plt.xlabel('Дата регистрации')
    plt.title('График количества пользователей по дате регистрации')
    plt.gcf().autofmt_xdate()
    min_y = min(users_count)
    max_y = max(users_count)
    plt.yticks(range(min_y, max_y + 1))

    # Сохраняем график в файл
    plt.savefig('chart.png')

    # Отправляем график в чат
    with open('chart.png', 'rb') as f:
        await message.bot.send_photo(message.chat.id, photo=BufferedInputFile(f.read(), filename='chart.png'))


@admin_router.message(Command('users_count'))
async def users_count(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    users = await client.get_all_user()

    dates = [d['registration_date'] for d in users]
    users_count = [len([d for d in users if d['registration_date'] == date]) for date in dates]

    # Создаем график
    plt.plot(dates, users_count)
    plt.ylabel('Количество пользователей')
    plt.xlabel('Дата регистрации')
    plt.title('График количества пользователей по дате регистрации')
    min_y = min(users_count)
    max_y = max(users_count)
    plt.yticks(range(min_y, max_y + 1))

    # Сохраняем график в файл
    plt.savefig('chart.png')

    # Отправляем график в чат
    with open('chart.png', 'rb') as f:
        await message.bot.send_photo(message.chat.id, photo=BufferedInputFile(f.read(), filename='chart.png'))


@admin_router.message(Command('change_price'))
async def change_price(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    args = message.text.split()
    if len(args) != 3:
        await message.answer(
            'Неверное количество аргументов. Используйте команду в формате: /change_price <model_name> <new_price>')
        return

    model_name = args[1]
    new_price = args[2]

    if model_name not in CVModelEnum:
        await message.answer('Такой модели не существует')
        return

    try:
        new_price = int(new_price)
    except ValueError:
        await message.answer('Новый ценник должен быть числом')
        return

    await client.change_model_cost(model_name, new_price)

    await message.answer(f'Цена модели "{model_name}" успешно изменена на {new_price}')


@admin_router.message(Command('change_balance'))
async def change_balance(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    if len(message.text.split()) != 3:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /change_balance <user_name> <new_balance>')
        return

    user_name = message.text.split()[1]
    new_balance = message.text.split()[2]

    try:
        new_price = int(new_balance)
    except ValueError:
        await message.answer('Новый баланс должен быть целым числом')
        return

    await client.change_token(user_name, new_price)

    await message.answer(f'Баланс пользователя {user_name} успешно изменен на {new_balance}')


@admin_router.message(Command('balance_user'))
async def balance(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    if len(message.text.split()) != 2:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /balance_user <user_name>')
        return

    user_name = message.text.split()[1]

    user = await client.get_user(user_name)
    token_amount = user['token_amount']
    await message.answer(f'Ваш текущий баланс пользователя {user_name}: {token_amount}')


@admin_router.message(Command('change_role'))
async def change_balance(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] == 'client':
        return

    if len(message.text.split()) != 3:
        await message.answer('Неверное количество аргументов. Используйте команду в формате /change_role <user_name> <new_role>')
        return

    user_name = message.text.split()[1]
    new_row = message.text.split()[2]

    if new_row != 'client' or new_row != 'manager':
        await message.answer(f'Неправильна введена роль')

    await client.change_role(user_name, new_row)
    await message.answer(f'Роль пользователя {user_name} успешно изменена на {new_row}')

