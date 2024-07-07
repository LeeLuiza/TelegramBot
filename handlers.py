from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile
from aiogram.filters import CommandStart, Command
import aiohttp
import asyncio
import base64

import keyboards as kb
from api_client import APIClient
from model_enum import CVModelEnum

router = Router()
MODEL = ''
queue = []
client = APIClient('http://127.0.0.1:8000')
user_photos = {}

HELP_COMMAND = """
Список доступных команд:
1. /count_coins - подсчет монет
2. /balance - текущий баланс
3. /history - история операций
4. /photo_by_id <id_task>- просмотреть фотографию, связанную с определенной задачей по id
5. /model_price - стоимость моделей
"""

HELP_COMMAND_ADMIN = """
Список доступных команд для администратора:
1. /count_coins - подсчет монет
2. /balance - текущий баланс
3. /history - история операций
4. /photo_by_id <id_task>- просмотреть фотографию, связанную с определенной задачей по id
5. /model_price - стоимость моделей
6. /new_users <start_date> <end_date> - количество новых пользователей за период
7. /users_count - количество пользователей
8. /change_price <model_name> <new_price> - изменить стоимость модели
9. /change_balance <user_name> <new_balance> - изменить баланс пользователя
10. /balance_user <user_name> - посмотреть баланс пользователя
"""


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await client.check_user(message.from_user.username)
    if user:
        if message.from_user.username == 'Lu_i_z_a' or message.from_user.username == 'evan_kirk':
            await client.add_user(message.from_user.username, 'manager', 100)
        else:
            await client.add_user(message.from_user.username, 'client', 100)
    await message.answer('Добро пожаловать! Чтобы начать подсчет монет введите команду /count_coins')


@router.message(Command('count_coins'))
async def help(message: Message):
    await message.answer('Выберите модель для обработки фотографии',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def help(message: Message):
    user = await client.get_user(message.from_user.username)
    if user['role'] != 'client':
        await message.answer(text=HELP_COMMAND_ADMIN)
        return
    await message.answer(text=HELP_COMMAND)


@router.message(Command('balance'))
async def balance(message: Message):
    user = await client.get_user(message.from_user.username)
    token_amount = user['token_amount']
    await message.answer(f'Ваш текущий баланс: {token_amount}')


@router.message(Command('model_price'))
async def model_price(message: Message):
    msg = ''
    for model in CVModelEnum:
        cost_model = await client.get_cost_model(model)
        msg = msg + f'Стоимость модели {model}: {cost_model['cost']} токенов\n'
    await message.answer(msg)


@router.message(Command('photo_by_id'))
async def cmd_help(message: Message):
    if len(message.text.split()) != 2:
        await message.answer(
            'Неверное количество аргументов. Используйте команду в формате /photo_by_id <id_task>')
        return

    id_task = message.text.split()[1]

    try:
        new_id_task = int(id_task)
    except ValueError:
        await message.answer('id задачи должно быть целым числом')
        return

    # ищем в бд id определенной задачи


@router.message(Command('history'))
async def cmd_help(message: Message):
    history = client.get_history(message.from_user.username)
    #
    await message.answer('Ваша история операций:\n')


@router.message(F.text.in_(CVModelEnum))
async def check(message: Message):
    global MODEL
    await message.answer('Cделай фотографию для подсчета монет', reply_markup=ReplyKeyboardRemove())
    MODEL = message.text


@router.message(F.photo)
async def image(message: Message):

    # user_id = message.from_user.id
    # if user_id not in user_photos:
    #     user_photos[user_id] = message.photo[-1].file_id
    # else:
    #     await message.answer("Извините, вы уже отправили фотографию ранее.")

    if MODEL == 'Выбрать все модели':
        await all_models(message)
        return
    elif MODEL == '':
        await message.answer(f'Вы не выбрали модель', reply_markup=kb.main)
        return

    if await check_balance(message, False):
        return

    await download_photo(message)

    task_id = await client.use_yolo8(message.from_user.username,'photo.jpg', MODEL)
    if task_id == 1:
        await message.answer('Произошла ошибка, попробуйте еще раз')
        return

    await processing_result(message, task_id)


async def processing_result(message: Message, task_id):
    queue.append(message.from_user.id)
    position = queue.index(message.from_user.id) + 1
    previous_position = position

    msg = await message.answer(f'Запрос в обработке. Вы {position} в очереди')
    result = await client.get_result(task_id)
    while result == 0:
        position = queue.index(message.from_user.id) + 1
        if position != previous_position:
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                                text=f'Запрос в обработке. Вы {position} в очереди')
        await asyncio.sleep(5)
        result = await client.get_result(task_id)

    await message.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

    if result == 1:
        queue.remove(message.from_user.id)
        await message.answer('Произошла ошибка, попробуйте еще раз')
        return
    else:
        image_data = base64.b64decode(result['image'])
        msg = result['total']
        with open('result.jpeg', 'wb') as img_result:
            img_result.write(image_data)

        await message.bot.send_photo(chat_id=message.chat.id, photo=BufferedInputFile(result, 'result.jpeg'),
                                     caption=msg)

    queue.remove(message.from_user.id)


async def all_models(message: Message):
    if await check_balance(message, True):
        return

    await download_photo(message)

    for model in CVModelEnum:
        task_id = await client.use_yolo8(message.from_user.username, 'photo.jpg', model)
        if task_id == 1:
            await message.answer('Произошла ошибка, попробуйте еще раз')
            return
        await message.answer(f'Результат модели - {model}')
        await processing_result(message, task_id)


async def download_photo(message: Message):
    photo_file_id = message.photo[-1].file_id

    # Скачиваем изображение с сервера Telegram
    file = await message.bot.get_file(photo_file_id)

    # Загрузка фотографии с помощью aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}') as response:
            response.raise_for_status()
            photo_data = await response.read()

        with open('photo.jpg', 'wb') as f:
            f.write(photo_data)


async def check_balance(message: Message, all_model: bool):
    user = await client.get_user(message.from_user.username)
    token_amount = user['token_amount']
    price = 0
    if all_model:
        for model in CVModelEnum:
            price = price + await client.get_cost_model(model)
    else:
        price = await client.get_cost_model(MODEL)
    if token_amount - price['cost'] < 0:
        await message.answer('Недостаточно токенов. Выберите другую модель, либо пополните счет')
        return True
    else:
        return False
