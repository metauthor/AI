from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.settings.config import BOT_TOKEN, OPENAI_TOKEN
from src.database.database import *
from src.handlers.static.generateResponse import *
from states.states import *
from datetime import datetime, timedelta
import openai

storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)
openai.api_key = OPENAI_TOKEN


@dp.message_handler(text=['Новий запит 💡'], state=None)
async def startWayCommand(message):
    if await get_allowedRequests(message.from_user.id) == float('inf') or (await get_allowedRequests(message.from_user.id)) >= 1:
        current_date = datetime.now()
        if await get_allowedRequests(message.from_user.id) == float('inf') and str(current_date.strftime('%d.%m.%Y %H:%M:%S')) <= str(await get_expiryDate(message.from_user.id)):
            button = KeyboardButton('Відміна 🔴')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
            await message.answer(f"""*Запитів доступно:* `{await get_allowedRequests(message.from_user.id)}`

Відправ боту повідомлення зі своїм запитом, щоб отримати результат:""", reply_markup=keyboard)
            await extraQuestions.q.set()
            await update_totalRequested(message.from_user.id, 1)
        elif (await get_allowedRequests(message.from_user.id)) >= 1:
            button = KeyboardButton('Відміна 🔴')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
            await message.answer(f"""*Запитів доступно:* `{await get_allowedRequests(message.from_user.id)}`

Відправ боту повідомлення зі своїм запитом, щоб отримати результат:""", reply_markup=keyboard)
            await extraQuestions.q.set()
            await update_totalRequested(message.from_user.id, 1)
        elif await get_allowedRequests(message.from_user.id) != float('inf') and str(current_date.strftime('%d.%m.%Y %H:%M:%S')) >= str(await get_expiryDate(message.from_user.id)):
            button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
            button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            await message.answer("""*Схоже твоя підписка закінчилась 😢*
        
Щоб продовжити користування ботом, обери тариф підписки:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)
        else:
            button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
            button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            await message.answer("""*Друзі, підтримувати роботу цього боту досить дорого 🫠*

Для того, щоб проект міг продовжити своє існування і ми покрили хоча б частину розходів подальше користування здійснюється за тарифами:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)
    else:
        button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
        button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
        await message.answer("""*Друзі, підтримувати роботу цього боту досить дорого 🫠*

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


@dp.message_handler(state=extraQuestions.q)
async def extraQuestion(message, state: FSMContext):
    if message.text == 'Відміна 🔴':
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
    else:
        if (await get_allowedRequests(message.from_user.id)) >= 1:   
            await message.answer("Зачекай, відповідь генерується...")
            response = await generate_response(message.text, message.from_user.id)
            button_1 = InlineKeyboardButton('На головну', callback_data='main')
            button_2 = InlineKeyboardButton('Запитати ще 🎯', callback_data='start_way')
            button_3 = InlineKeyboardButton('Виникла помилка 🙁', callback_data='error')

            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_2).add(button_1).add(button_3)
            
            if len(response) < 500:
                await increment_allowedRequests(message.from_user.id)
                await bot.send_message(-1001861498963, text=f"*🟢 НОВИЙ ЛОГ*\n\n*Користувач:* `{message.from_user.full_name}`\n\n*Питання користувача:* `{message.text}`\n\n*Відпоідь боту:* `{response}`", parse_mode='Markdown')
                await message.answer(f"Відповідь:\n\n{response}\n\n", parse_mode='None', reply_markup=keyboard)
            else:
                await increment_allowedRequests(message.from_user.id)
                await bot.send_document(-1001861498963, open(f"outs/{message.from_user.id}.txt", 'rb'), caption = f"*Користувач:* `{message.from_user.full_name}`\n\n*Питання користувача:* `{message.text}`"  ,parse_mode='Markdown')
                await bot.send_document(message.from_user.id, open(f"outs/{message.from_user.id}.txt", 'rb'), caption = "*Ваша відповідь виявилась довгою, тому для зручності ми розмістили її в текстовому файлі 😊*", reply_markup=keyboard)
            button = InlineKeyboardButton('Профіль користувача 🔗', url=f"tg://user?id={message.from_user.id}")
            keyboard_2 = InlineKeyboardMarkup(resize_keyboard=True).add(button)

            await state.update_data(text=response)
            
            await state.finish()
        else:
            button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
            button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
            await message.answer("""*Досягнуто ліміту запитів 😢*
            
    Щоб продовжити користування ботом, обери тариф підписки:
    
    *Лімітована* 5 запитів = 50грн.
    *Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='error')
async def error(call):
    button_1 = InlineKeyboardButton('На головну', callback_data='main')
    button_2 = InlineKeyboardButton('Запитати ще 🎯', callback_data='start_way')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_2).add(button_1)
    await call.message.answer("*Нам дуже шкода 🙁*\n\nНіхто не застрахований від будь-яких помилок. Ми усіма силами стараємось покращити дієздатність та ефективність боту.\n\nМаєте пропозиції та побажання? Розкажіть це в розділі 'Підтримка 📢'", reply_markup=keyboard)


def register_handlers_newRequestMenu(dp: Dispatcher):
    dp.register_message_handler(startWayCommand, text=['Новий запит 💡'], state=None)
    dp.register_message_handler(extraQuestion, state=extraQuestions.q)
    dp.register_message_handler(cancel, text=['Відміна 🔴'])
    dp.register_callback_query_handler(error, text='error')
