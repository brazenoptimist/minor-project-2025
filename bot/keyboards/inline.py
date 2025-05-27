from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

start_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="Bupyc", url="https://t.me/Not_Bupyc"),
            InlineKeyboardButton(text="Template", url="https://github.com/NotBupyc/aiogram-bot-template"),
        ]
    ]
).as_markup()

def build_initial_survey_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Пройти опрос"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)