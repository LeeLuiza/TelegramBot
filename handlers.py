from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command

import keyboards as kb
from admin_handlers import ADMIN_ID

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


@router.message(CommandStart())
async def cmd_start(message: Message):
    # добавляем в бд нового пользователя и указываем роль
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
    # из бд получаем баланс текущего пользователя
    balance = 100
    await message.answer(f'Ваш текущий баланс: {balance}')

@router.message(Command('history'))
async def cmd_help(message: Message):
    await message.answer('Ваша история операций:')
    # из бд получаем историю пользователя

@router.message(Command('favorites'))
async def cmd_help(message: Message):
    await message.answer('Ваши избранные запросы:')
    # из бд получаем избранные вопросы

@router.message(Command('id'))
async def id(message: Message):
    await message.answer(f'{message.from_user.id}')

@router.message(F.photo)
async def image(message: Message):
    # по определенной модели обработываем фотографию
    # вычитаем из баланса некоторую стоимость
    # сохраняем в историю его фотографию
    await message.reply('На фотографии ...')


@router.message(F.text.in_({'1', '2', 'выбрать все варианты'}))
async def check(message: Message):
    if message.text == 'выбрать все варианты':
        await message.answer('Вы выбрали все варианты', reply_markup=ReplyKeyboardRemove())
    elif message.text == '1':
        await message.answer('Вы выбрали модель "1"', reply_markup=ReplyKeyboardRemove())
    elif message.text == '2':
        await message.answer('Вы выбрали модель "2"', reply_markup=ReplyKeyboardRemove())
    await message.answer('Cделай фотографию для подсчета монет')









