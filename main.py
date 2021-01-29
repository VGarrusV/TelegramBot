from aiogram import executor
from config.config import admin_id
from loader import bot


async def on_startup(dp):
    # await asyncio.sleep(10)
    await bot.send_message(admin_id, "I'm running")


async def on_shutdown(dp):
    await bot.send_message(admin_id, "Powering down")
    await bot.close()


if __name__ == "__main__":
    from handlers.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

# @dp.message_handler(Command("start"))
# async def greeting(message: Message):
#     await message.answer("Добрый день! Этот бот предназначен для простого и быстрого поиска исполнителя для любого "
#                          "интересующего вас события. Если вы заказчик - выберете интересующую вас категорию "
#                          "праздника или события. Если вы исполнитель - пожалуйста, зарегестрируйтесь в нашей базе "
#                          "данных, чтобы клиенты могли легче находить вас.", reply_markup=choice)
#
#
# @dp.callback_query_handler(text="customer")
# async def customer_choice(call: CallbackQuery):
#     await bot.answer_callback_query(callback_query_id=call.id)
#     await call.message.answer("Примерные варианты", reply_markup=customer_button)
#
#
# @dp.callback_query_handler(text="performer")
# async def performer_input(call: CallbackQuery):
#     await bot.answer_callback_query(callback_query_id=call.id)
#     await call.message.answer("Пожалуйста, введите электронную почту:")
#     await Performer_data.D1.set()
#
#
# @dp.message_handler(state=Performer_data.D1)
# async def answer_d1(message: Message, state: FSMContext):
#     answer = message.text
#     # print(answer)
#     await state.update_data(answer1=answer)
#     await message.answer("Пожалуйста, введите ссылку на ваш Instagram:")
#     await Performer_data.next()
#
#
# @dp.message_handler(state=Performer_data.D2)
# async def answer_d2(message: Message, state: FSMContext):
#     data = await state.get_data()
#     answer1 = data.get("answer1")
#     answer2 = message.text
#     print(f"email: {answer1}, Instagram: {answer2}")
#
#     # chat_id = message.from_user.id
#     id = await database.add_new_user(answer1, answer2)
#
#     if not id:
#         id = await database.get_id()
#     else:
#         text = "Added to database"
#
#     await message.answer("Спасибо, вы зарегестрированы!")
#     await state.finish()
#
#
# @dp.callback_query_handler(text="cancel")
# async def cancel_chat(call: CallbackQuery):
#     await call.answer("Ну вот :(", show_alert=True)
#     await call.message.edit_reply_markup(reply_markup=None)
