import smtplib
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, executor
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked, RetryAfter
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime
from email.message import EmailMessage
from pymongo import MongoClient
from src.settings.config import *
from src.settings.keep_alive import keep_alive
from src.handlers.admin.adminMenu import *
from src.handlers.client.feedbackMenu import *
from src.handlers.static.auth import *
from src.handlers.static.help import *
from src.handlers.client.newRequest import *
from src.handlers.static.buyMenu import *
from src.handlers.admin.mailingMenu import *

keep_alive()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)

register_handlers_authMenu(dp)
register_handlers_adminMenu(dp)
register_handlers_feedbackMenu(dp)

register_handlers_helpMenu(dp)
register_handlers_newRequestMenu(dp)

register_handlers_BotMailing(dp)
register_handlers_buyMenu(dp)

@dp.callback_query_handler(text='toMain')
async def toMain(call):
    if str(await get_isPaid(call.from_user.id)) == "False":
        button_1 = InlineKeyboardButton('Тарифи 📲', callback_data='tariffs')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1)
        await call.message.answer(
            "Нажаль, ця функція вам недоступна, адже ви не обрали тариф 😢\n\nЩоб продовжити користування ботом, натисніть на кнопку нижче",
            reply_markup=keyboard)
    else:
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2,
                                                                                                 button_4).add(button_3)
            await call.message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)


@dp.callback_query_handler(text='main')
async def toMain(call):
    if str(await get_isPaid(call.from_user.id)) == "False":
        button_1 = InlineKeyboardButton('Тарифи 📲', callback_data='tariffs')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1)
        await call.message.answer(
            "Нажаль, ця функція вам недоступна, адже ви не обрали тариф 😢\n\nЩоб продовжити користування ботом, натисніть на кнопку нижче",
            reply_markup=keyboard)
    else:
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2,
                                                                                                 button_4).add(button_3)
            await call.message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)

@dp.callback_query_handler(text='limitedTariff')
async def limitedTariff(call):
    current_date = datetime.now()
    await call.message.answer(f"""<b>#USEREXTRACT</b>
    
<b>Вартість:</b> <code>50грн.</code>
<b>Запитів до зарахування:</b> <code>5</code>
<b>Ваш ID:</b> <code>{call.from_user.id}</code>

Для здійснення покупки здійсни грошовий переказ за реквізитами (<i>Ти можеш скопіювати, натиснувши на текст</i>):
💳 <b>Номер картки:</b> <code>{CARD}</code>


<i>Після успішної транзакції, перешли ЦЕ повідомлення та квитанцію менеджеру</i> — {MANAGER}
""", parse_mode='html')
# ⚠️ <b>Призначення:</b> <code>ult: ID{call.from_user.id} {current_date.strftime('%H%M%S')}</code>
    

@dp.callback_query_handler(text='unlimitedTariff')
async def unlimitedTariff(call):
    current_date = datetime.now()
    await call.message.answer(f"""<b>#USEREXTRACT</b>
    
<b>Вартість:</b> <code>300грн.</code>
<b>Запитів до зарахування:</b> <code>Безліміт на місяць (30днів)</code>
<b>Ваш ID:</b> <code>{call.from_user.id}</code>

Для здійснення покупки здійсни грошовий переказ за реквізитами (<i>Ти можеш скопіювати, натиснувши на текст</i>):
💳 <b>Номер картки:</b> <code>{CARD}</code>

<i>Після успішної транзакції, перешли ЦЕ повідомлення та квитанцію менеджеру</i> — {MANAGER}
""", parse_mode='html')
# ⚠️ <b>Призначення:</b> <code>ult: ID{call.from_user.id} {current_date.strftime('%H%M%S')}</code>

@dp.callback_query_handler(text='tariffs')
async def tariffs(call):
    button_1 = InlineKeyboardButton('Лімітована', callback_data='limitedTariff')
    button_2 = InlineKeyboardButton('Безліміт', callback_data='unlimitedTariff')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
    await call.message.answer("""Щоб продовжити користування ботом, обери тариф підписки:

*Лімітована* 5 запитів = 50грн.
*Безліміт* на 1 місяць = 300грн.""", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
