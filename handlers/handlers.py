from loader import bot, dp
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from keyboards.default.default_keyboard import phone
from keyboards.inline.inline_keyboard import create_keyboard, choice, cats
from states.performer_states import PerformerData
from aiogram.dispatcher import FSMContext
from aiogram import types
import database


# txt = ["Cнегурочка", "Дед Мороз", "Тамада", "Ведущий на выпускной"]
# init_states = ["False", "False", "False", "False"]

# Общие комментарии по будущим изменениям: попробовать ужать хэндлеры до минимального размера, уменьшить их кол-во.
# Возможно раскидать хэндлеры по разным файлам, разделить структуру на две ветки - Заказчик и исполнитель.
# По внешнему виду - написать нормальный текст ко всем кнопкам, описание и т.д. Возможно сделать пару отдельных
# Хендлеров, которые будут в самом начале выводить общую информацию о боте. Далее по каждому хендрелу кокренто.

# Тут более менее, надо Добавить более общее описание, и возможно отвязать кнопку choice от команды start, чтобы опи-
# сание не выскакивало каждый раз.
@dp.message_handler(Command("start"), state="*")
async def greeting(message: Message, state=FSMContext):
    await state.finish()
    await message.answer("Добрый день! Этот бот предназначен для простого и быстрого поиска исполнителя для любого "
                         "интересующего вас события. Если вы заказчик - выберете интересующую вас категорию "
                         "праздника или события. Если вы исполнитель - пожалуйста, зарегистрируйтесь в нашей базе "
                         "данных, чтобы клиенты могли легче находить вас.", reply_markup=choice)


@dp.callback_query_handler(text="customer")
async def categories(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.edit_reply_markup(reply_markup=cats)

# Хороший пример генерализации хендлера, здесь 4 кнопки сразу обрабатывается.
@dp.callback_query_handler(text_contains="cust")
async def categories(call: CallbackQuery):
    string = call.data.split("cust_")

    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.answer(text=f'Чтобы вывести список исполнителей в категории {string[1]}, введите команду "'
                                   f'@Tesovii_bot {string[1]}".')


@dp.callback_query_handler(text="performer")
async def categories(call: CallbackQuery):
    global txt
    txt = ["Cнегурочка", "Дед Мороз", "Тамада", "Ведущий на выпускной"]
    global init_states
    init_states = ["False", "False", "False", "False"]
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.edit_reply_markup(reply_markup=create_keyboard(txt, init_states))


# Тут идут 4 хендлера на все 4 категории. Думаю возможно придумать способ генерализации.
@dp.callback_query_handler(text_contains="Cнегурочка")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    string = call.data
    split = string.split(":")
    init_states[0] = split[1]
    await call.message.edit_reply_markup(reply_markup=create_keyboard(txt, init_states))


@dp.callback_query_handler(text_contains="Дед Мороз")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    string = call.data
    split = string.split(":")
    init_states[1] = split[1]
    await call.message.edit_reply_markup(reply_markup=create_keyboard(txt, init_states))


@dp.callback_query_handler(text_contains="Тамада")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    string = call.data
    split = string.split(":")
    init_states[2] = split[1]
    await call.message.edit_reply_markup(reply_markup=create_keyboard(txt, init_states))


@dp.callback_query_handler(text_contains="Ведущий на выпускной")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    string = call.data
    split = string.split(":")
    init_states[3] = split[1]
    await call.message.edit_reply_markup(reply_markup=create_keyboard(txt, init_states))


@dp.callback_query_handler(text="done")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    print(init_states)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Поделитесь своим номером телефона, если хотите пропустить этот шаг, нажмите \n /next.",
                              reply_markup=phone)
    await PerformerData.D1.set()


@dp.message_handler(content_types=['contact'], state=PerformerData.D1)
async def read_contact(message: Message, state=FSMContext):
    answer = message.contact.phone_number
    if answer[0] == '7':
        answer = '+' + answer
    print(answer)
    await state.update_data(answer1=answer)
    await message.answer("Пожалуйста, введите электронную почту. Если хотите пропустить этот шаг, нажмите \n /next.",
                         reply_markup=ReplyKeyboardRemove())
    await PerformerData.next()


@dp.message_handler(Command("next"), state=PerformerData.D1)
async def get_email(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer1=answer)
    await message.answer(text="После отмены; Пожалуйста, введите электронную почту. Если хотите пропустить этот шаг, "
                              "нажмите \n /next.",
                         reply_markup=ReplyKeyboardRemove())
    await PerformerData.next()


@dp.message_handler(state=PerformerData.D2)
async def get_insta(message: Message, state=FSMContext):
    answer = message.text
    if answer == '/next':
        answer = ''
    await state.update_data(answer2=answer)
    await message.answer(text="Пожалуйста, введите имя пользователя Instagram. Если хотите пропустить этот шаг, "
                              "нажмите \n /next.")
    await PerformerData.next()

# Главный хэндлер записывающий в базу. Тут можно скорее всего поменять способ который составляет отчет report, больно
# много там if и так далее. Скорее всего есть хороший питоновский способ таких операций.
@dp.message_handler(state=PerformerData.D3)
async def answer_d2(message: Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = message.text
    if answer3 == '/next':
        answer3 = ''
    else:
        answer3 = 'https://www.instagram.com/' + answer3 + '/'
    print(f"phone: {answer1}, email: {answer2}, Instagram: {answer3}")

    user = types.User.get_current()
    chat_id = user.id
    # username = user.username
    full_name = user.full_name

    # chat_id = message.from_user.id
    tables = ['snow_maidens', 'santas', 'toastmasters', 'prom_presenters']
    ls = []
    try:
        for i in range(len(init_states)):
            if init_states[i] == 'True':
                existence = database.add_user(tables[i], chat_id, full_name, answer1, answer2, answer3)
                if not existence:
                    ls.append(txt[i])
        report = ''
        if ls:
            length = len(ls)
            report = 'Вы зарегистрированы в'
            if length > 1:
                report += ' категориях '
                for i in range(length):
                    if i < length - 1:
                        report += f'"{ls[i]}", '
                    else:
                        report += f'"{ls[i]}".'
            else:
                report += f' категории "{ls[0]}".'
        else:
            report += 'Вы уже были зарегистрированы.'
        report += ' Для возвращения в начало, нажмите /start.'
        await message.answer(report)
    except Exception as e:
        print(e)
        await message.answer(
            text='К сожалению, на данный момент база данных не доступна. Пожалуйста, попробуйте позже.')
    await state.finish()


@dp.callback_query_handler(text="cancel")
async def customer_choice(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.edit_reply_markup(reply_markup=choice)

# Этот хендлер относится только ко второй ветке, то есть к стороне потребителя. Возможно выделить его в отдельный модуль
# но не знаю правильно ли будет диспатчер приходить в main.
# Здесь нужно добавить некоторым образом картинки в инлайн меню, например, если пользователь оставляет ссылку на инста-
# грам, через его апи скачивать аватарку и пихать в тамб сюда.
@dp.inline_handler()
async def query_text(query: types.InlineQuery):
    tables = ['snow_maidens', 'santas', 'toastmasters', 'prom_presenters']
    cat = ["Снегурочка".lower(), "Дед Мороз".lower(), "Тамада".lower(), "Ведущий на выпускной".lower()]
    if query.query.lower() in cat:
        idx = cat.index(query.query)
        offset = int(query.offset) if query.offset else 0
        print("offset = ", offset)
        info = database.retrieve_users_offset(tables[idx], offset)
        # if len(info) is 0:
        #     try:
        #         result = types.InlineQueryResultArticle(id='1',
        #                                                 title=('В базе пока ничего нет'),
        #                                                 description=('Извините!'),
        #                                                 input_message_content=types.InputTextMessageContent(
        #                                                     message_text="(текст)"))
        #         await query.answer(switch_pm_text="Вернуться к Боту", switch_pm_parameter="_", results=[result],
        #                            cache_time=120,
        #                            is_personal=True)
        #     except Exception as e:
        #         print(e)
        #     return
        results_array = []
        try:
            m_next_offset = str(offset + 5) if len(info) == 5 else None
            for index, info in enumerate(info):
                try:
                    results_array.append(
                        types.InlineQueryResultArticle(id=str(index),
                                                       title=(info[0]),
                                                       description=(info[2]),
                                                       url=info[3],
                                                       input_message_content=types.InputTextMessageContent(
                                                           message_text=('Информация об исполнителе: \n'
                                                                         'Телефон: ' + info[1] + '\n'
                                                                                                 'Email: ' + info[
                                                                             2] + '\n'
                                                                                  'Ссылка: ' + info[3])),
                                                       )
                    )
                except Exception as e:
                    print(e)
            await query.answer(switch_pm_text="Вернуться к Боту", switch_pm_parameter="_", results=results_array,
                               cache_time=120,
                               is_personal=True, next_offset=m_next_offset if m_next_offset else "")
        except Exception as e:
            print(e)
