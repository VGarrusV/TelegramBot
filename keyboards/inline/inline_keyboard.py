from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Исполнитель", callback_data="performer"),
            InlineKeyboardButton(text="Заказчик", callback_data="customer"),
        ]
    ]
)

cats = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Снегурочка", callback_data="cust_снегурочка"),
            InlineKeyboardButton(text="Дед Мороз", callback_data="cust_дед мороз"),
        ],
        [
            InlineKeyboardButton(text="Тамада", callback_data="cust_тамада"),
            InlineKeyboardButton(text="Ведущий на выпускной", callback_data="cust_ведущий на выпускной")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]

    ]
)

# возможно стоит написать более продвинутый класс кнопок, чтобы можно было упростить хендлеры, а в дальнейшем это можно
# использовать при создании каких угодно ботов.
def create_button(txt, state):
    if state == "True":
        button = InlineKeyboardButton(text='\u2611 ' + txt, callback_data=f"{txt}:False")
    else:
        button = InlineKeyboardButton(text=txt, callback_data=f"{txt}:True")
    return button


def create_keyboard(txts, states):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = create_button(txts[0], states[0])
    button2 = create_button(txts[1], states[1])
    button3 = create_button(txts[2], states[2])
    button4 = create_button(txts[3], states[3])
    keyboard.insert(button1)
    keyboard.insert(button2)
    keyboard.insert(button3)
    keyboard.insert(button4)
    keyboard.insert(InlineKeyboardButton(text="Готово", callback_data="done"))
    keyboard.insert(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    return keyboard
