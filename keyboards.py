from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2')],
                                     [KeyboardButton(text='выбрать все варианты')]],
                           resize_keyboard=True)