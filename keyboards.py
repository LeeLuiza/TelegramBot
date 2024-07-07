from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from model_enum import CVModelEnum


keyboard_buttons = []
button = []
for model in CVModelEnum:
    keyboard_buttons.append(KeyboardButton(text=model.value))
button.append(KeyboardButton(text='Выбрать все модели'))

main = ReplyKeyboardMarkup(keyboard=[keyboard_buttons, button], resize_keyboard=True)