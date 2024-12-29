from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_bot_keyboard_jail():
    buttons = [[KeyboardButton(text="МЕНЯ ЗАДЕРЖАЛИ")]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return keyboard

def get_bot_keyboard_confirm_jail():
    buttons = [[KeyboardButton(text="МЕНЯ ПРАВДА ЗАДЕРЖАЛИ")], [KeyboardButton(text="Отмена")]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return keyboard