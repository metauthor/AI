from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from states.states import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.settings.config import BOT_TOKEN, ADMIN_ID

from src.database.database import *


storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)


@dp.callback_query_handler(text='BotMailingSMS', state=None)
async def BotMailingSMS(call):
        button = KeyboardButton('Відміна 🔴')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
        await call.message.answer("Введи текст, який хочеш відправити користувачам", reply_markup=keyboard)
        await BotMailing.text.set()


@dp.message_handler(state=BotMailing.text)
async def BotMailingText(message, state: FSMContext):
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
        answer = message.text
        await state.update_data(text=answer)
        btnAddPhoto = InlineKeyboardButton('📸 Додати фото', callback_data='add_photo')
        btnNext = InlineKeyboardButton('Відправити 📢', callback_data='next')
        btnQuit = InlineKeyboardButton('Відміна 🚫', callback_data='quit')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(btnAddPhoto, btnNext).add(btnQuit)
        await message.answer(text=answer, reply_markup=keyboard)
        await BotMailing.state.set()


@dp.callback_query_handler(text='next', state=BotMailing.state)
async def BotMailing_n(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    for user in db["global"].find({"DATA": "global"}):
        try:
            await bot.send_message(user['_id'], text=f'{text}')
        except Exception:
            pass
    if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer('Відправлено!', reply_markup=keyboard)
    elif (await get_userPosition(call.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await call.message.answer('Відправлено!', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='add_photo', state=answerTo.state)
async def BotMailing_add_photo(call):
    await call.message.answer('Пришли фото')
    await answerTo.photo.set()


@dp.message_handler(state=answerTo.photo, content_types=types.ContentType.PHOTO)
async def BotMailing_photo(message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    btnNext = InlineKeyboardButton('Відправити 📢', callback_data='next')
    btnQuit = InlineKeyboardButton('Відміна 🚫', callback_data='quit')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(btnNext).add(btnQuit)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


@dp.callback_query_handler(text='next', state=answerTo.photo)
async def BotMailingm(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in db["global"].find({"DATA": "global"}):
        try:
            await bot.send_photo(user['_id'], photo=photo, caption=f'{text}')
        except Exception:
            pass
    if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer('Відправлено!', reply_markup=keyboard)
    elif (await get_userPosition(call.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await call.message.answer('Відправлено!', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='quit', state=[answerTo.text, answerTo.photo, answerTo.state])
async def BotMailing_quit(call, state: FSMContext):
    await state.finish()
    if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer('Відмінено, ви повернулись в головноме меню 🏠', reply_markup=keyboard)
    elif (await get_userPosition(call.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await call.message.answer('Відмінено, ви повернулись в головноме меню 🏠', reply_markup=keyboard)


def register_handlers_BotMailing(dp: Dispatcher):
    dp.register_callback_query_handler(BotMailingSMS, text='BotMailingSMS', state=None)
    dp.register_message_handler(BotMailingText, state=BotMailing.text)
    dp.register_callback_query_handler(BotMailing_n, text='next', state=BotMailing.state)
    dp.register_callback_query_handler(BotMailing_add_photo,text='add_photo', state=BotMailing.state)
    dp.register_message_handler(BotMailing_photo, state=BotMailing.photo, content_types=types.ContentType.PHOTO)
    dp.register_callback_query_handler(BotMailingm, text='next', state=BotMailing.photo)
    dp.register_callback_query_handler(BotMailing_quit, text='quit', state=[BotMailing.text, BotMailing.photo, BotMailing.state])
