from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
import time


import keyboards as kb
from admin_handlers import ADMIN_ID
from api_client import APIClient

router = Router()

HELP_COMMAND = """
Список доступных команд:
1. /balance - текущий баланс
2. /history - история операций
3. /favorites - избранные запросы
"""

HELP_COMMAND_ADMIN = """
Список доступных команд для администратора:
1. /balance - текущий баланс
2. /history - история операций
3. /favorites - избранные запросы
4. /new_users <start_date> <end_date> - количество новых пользователей за период 
5. /users_count - количество пользователей 
6. /change_price <model_name> <new_price> - изменить стоимость модели 
7. /change_balance <user_id> <new_balance> - изменить баланс пользователя 
"""

MODEL = ''
client = APIClient('http://127.0.0.1:8000')

@router.message(CommandStart())
async def cmd_start(message: Message):
    await client.add_user(message.from_user.username, 'client', 100)
    await message.answer('Добро пожаловать! Чтобы начать подсчет монет введите команду /count_coins')

@router.message(Command('count_coins'))
async def help(message: Message):
    await message.answer('Выберите модель для обработки фотографии',
                         reply_markup=kb.main)

@router.message(Command('help'))
async def help(message: Message):
    if F.from_user.id.in_(ADMIN_ID):
        await message.answer(text=HELP_COMMAND_ADMIN)
        return
    await message.answer(text=HELP_COMMAND)

@router.message(Command('balance'))
async def balance(message: Message):
    user = await client.get_user(message.from_user.username)
    token_amount = user['token_amount']
    await message.answer(f'Ваш текущий баланс: {token_amount}')

@router.message(Command('history'))
async def cmd_help(message: Message):
    await message.answer('Ваша история операций:')
    # из бд получаем историю пользователя

@router.message(Command('favorites'))
async def cmd_help(message: Message):
    await message.answer('Ваши избранные запросы:')
    # из бд получаем избранные вопросы

@router.message(F.text.in_({'yolo8s', 'yolo8m', 'yolo8n'}))
async def check(message: Message):
    global MODEL
    await message.answer('Cделай фотографию для подсчета монет', reply_markup=ReplyKeyboardRemove())
    MODEL = message.text

@router.message(F.photo)
async def image(message: Message):
    file_id = message.photo[-1].file_id
    file = await message.download_file(file_id)

    task_id = await client.send_img_to_api(message.from_user.username, file, MODEL)
    if task_id == 1:
        await message.answer('Произошла ошибка, попробуйте еще раз')

    while True:
        result = await client.get_img_to_api(task_id)
        if result == 0:
            time.sleep(5)
        elif result == 1:
            await message.answer('Произошла ошибка, попробуйте еще раз')
            break
        else:
            await message.send_photo(result['result'])
            break