from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.settings.config import BOT_TOKEN, TARGET_CHANNEL_1, SUCCESS_SUB_TEXT
from src.database.database import *
from states.states import *
from datetime import datetime

storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def startCommand(message):
    search_user_id_global = db["global"].find_one({"_id": message.from_user.id})
    channel_1 = await bot.get_chat_member(chat_id=TARGET_CHANNEL_1, user_id=message.from_user.id)
    if not search_user_id_global:
        await add_userGlobal(message.from_user.id, message.from_user.full_name, message.from_user.username)
        if channel_1["status"] == 'left':
            button_link_1 = InlineKeyboardButton('Підписатись ✅', url=f'https://t.me/{TARGET_CHANNEL_1[1:]}')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_link_1)
            await bot.send_message(message.from_user.id, text=f"*🎉 ChatGPT тепер доступний в Україні. Ви можете використовувати всім відомий AI за допомогою цього боту.*\n\n_Для цього підпишіться на канал_ та натисність /start", reply_markup=keyboard, disable_web_page_preview=True)
        else:
            if (await get_isPaid(message.from_user.id)) == True:
                if (await get_userPosition(message.from_user.id)) == 'User':
                    button_1 = KeyboardButton('Новий запит 💡')
                    button_2 = KeyboardButton('Мій кабінет 🏦')
                    button_3 = KeyboardButton('Як користуватись ⁉️')
                    button_4 = KeyboardButton('Підтримка 📢')
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
                    await message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
                elif (await get_userPosition(message.from_user.id)) == 'Admin':
                    button_1 = KeyboardButton('Новий запит 💡')
                    button_2 = KeyboardButton('Мій кабінет 🏦')
                    button_3 = KeyboardButton('Як користуватись ⁉️')
                    button_4 = KeyboardButton('Підтримка 📢')
                    button_5 = KeyboardButton('Адмін-панель 👮')
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
                    await message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
            elif (await get_isPaid(message.from_user.id)) == False:
                button_1 = InlineKeyboardButton('Як користуватись ⁉️', callback_data='how_to_use')
                button_2 = InlineKeyboardButton('Почати 🎯', callback_data='start_way')
                keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
                await message.answer(text=SUCCESS_SUB_TEXT, reply_markup=keyboard)  
    else:
        if channel_1["status"] == 'left':
            button_link_1 = InlineKeyboardButton('Підписатись ✅', url=f'https://t.me/{TARGET_CHANNEL_1[1:]}')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_link_1)
            await bot.send_message(message.from_user.id, text=f"*🎉 ChatGPT тепер доступний в Україні. Ви можете використовувати всім відомий AI за допомогою цього боту.*\n\n_Для цього підпишіться на канал_ та натисність /start", reply_markup=keyboard, disable_web_page_preview=True)
        else:
            button_1 = InlineKeyboardButton('Як користуватись ⁉️', callback_data='how_to_use')
            button_2 = InlineKeyboardButton('Почати 🎯', callback_data='start_way')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            if (await get_isPaid(message.from_user.id)) == True:
                if (await get_userPosition(message.from_user.id)) == 'User':
                    button_1 = KeyboardButton('Новий запит 💡')
                    button_2 = KeyboardButton('Мій кабінет 🏦')
                    button_3 = KeyboardButton('Як користуватись ⁉️')
                    button_4 = KeyboardButton('Підтримка 📢')
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
                    await message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
                elif (await get_userPosition(message.from_user.id)) == 'Admin':
                    button_1 = KeyboardButton('Новий запит 💡')
                    button_2 = KeyboardButton('Мій кабінет 🏦')
                    button_3 = KeyboardButton('Як користуватись ⁉️')
                    button_4 = KeyboardButton('Підтримка 📢')
                    button_5 = KeyboardButton('Адмін-панель 👮')
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
                    await message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
            elif (await get_isPaid(message.from_user.id)) == False:
                await message.answer(text=SUCCESS_SUB_TEXT, reply_markup=keyboard)



@dp.callback_query_handler(text=['start_way'], state=None)
async def startWayCommand(call):
    if await get_allowedRequests(call.from_user.id) == float('inf') or (await get_allowedRequests(call.from_user.id)) >= 1:
        current_date = datetime.now()
        if await get_allowedRequests(call.from_user.id) == float('inf') and str(current_date.strftime('%d.%m.%Y %H:%M:%S')) <= str(await get_expiryDate(call.from_user.id)):
            button = KeyboardButton('Відміна 🔴')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
            await call.message.answer(f"""*Запитів доступно:* `{await get_allowedRequests(call.from_user.id)}`

Відправ боту повідомлення зі своїм запитом, щоб отримати результат:""", reply_markup=keyboard)
            await extraQuestions.q.set()
        elif (await get_allowedRequests(call.from_user.id)) >= 1:
            button = KeyboardButton('Відміна 🔴')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
            await call.message.answer(f"""*Запитів доступно:* `{await get_allowedRequests(call.from_user.id)}`

Відправ боту повідомлення зі своїм запитом, щоб отримати результат:""", reply_markup=keyboard)
            await extraQuestions.q.set()
        elif await get_allowedRequests(call.from_user.id) != float('inf') and str(current_date.strftime('%d.%m.%Y %H:%M:%S')) >= str(await get_expiryDate(call.from_user.id)):
            button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
            button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            await call.message.answer("""*Схоже твоя підписка закінчилась 😢*
        
Щоб продовжити користування ботом, обери тариф підписки:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)
        else:
            button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
            button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            await call.message.answer("""*Друзі, підтримувати роботу цього боту досить дорого 🫠*

Для того, щоб проект міг продовжити своє існування і ми покрили хоча б частину розходів подальше користування здійснюється за тарифами:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)
    else:
        button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
        button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
        await call.message.answer("""*Друзі, підтримувати роботу цього боту досить дорого 🫠*

Для того, щоб проект міг продовжити своє існування і ми покрили хоча б частину розходів подальше користування здійснюється за тарифами:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)

@dp.message_handler(text=['Відміна 🔴'])
async def cancel(message, state: FSMContext):
    await state.finish()
    if (await get_userPosition(message.from_user.id)) == 'User':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
        await message.answer('Відмінено, ви повернулись в головноме меню 🏠', reply_markup=keyboard)
    elif (await get_userPosition(message.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await message.answer('Відмінено, ви повернулись в головноме меню 🏠', reply_markup=keyboard)

@dp.message_handler(text='Мій кабінет 🏦')
async def myCabinet(message):
    if str(await get_currentTariff(message.from_user.id)) == 'Limited':
        await message.answer(f"""*Ваш кабінет 🏦*
        
*Мій тариф:* `{await get_currentTariff(message.from_user.id)}`
*Залишок запитів:* `{await get_allowedRequests(message.from_user.id)}`

*Ви з нами з:* `{await get_joiningDateGlobal(message.from_user.id)}`
""")
    elif str(await get_currentTariff(message.from_user.id)) == 'Unlimited':
        await message.answer(f"""*Ваш кабінет 🏦*
        
*Мій тариф:* `{await get_currentTariff(message.from_user.id)}`
*Залишок запитів:* `{await get_allowedRequests(message.from_user.id)}`
*Дата закінчення тарифу:* `{await get_expiryDate(message.from_user.id)}`

*Ви з нами з:* `{await get_joiningDateGlobal(message.from_user.id)}`
""")
    else:
        await message.answer("Схоже сталася якась помилка 😢\n\nЗверністься в Підтримку")


def register_handlers_authMenu(dp: Dispatcher):
    dp.register_message_handler(startCommand, commands='start')
    dp.register_message_handler(cancel, text=['Відміна 🔴'])
    dp.register_callback_query_handler(startWayCommand, text=['start_way'], state=None)
    dp.register_message_handler(myCabinet, text='Мій кабінет 🏦')
