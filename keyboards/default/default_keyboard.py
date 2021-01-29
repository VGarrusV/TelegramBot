from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться телефонным номером', request_contact=True)
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
