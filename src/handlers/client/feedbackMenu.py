from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.settings.config import BOT_TOKEN
from src.database.database import *
from states.states import *


storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(text='Підтримка 📢')
async def feedbackCommand(message):
    await message.answer("*Служба Підтримки 📢*\n\nОпиши суть своєї пропозиції/питання повідомленням та відправ боту!", reply_markup=types.ReplyKeyboardRemove())
    await feedback.text.set()


@dp.message_handler(state=feedback.text)
async def feedbackText(message, state: FSMContext):
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
        await feedback.state.set()



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


@dp.callback_query_handler(text='next', state=feedback.state)
async def feedback_n(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await bot.send_message(call.from_user.id, text=f"*‼️ Нове повідомлення*\n\n*Від:* [{call.from_user.full_name}](tg://user?id={call.from_user.id})\n*ID:* `{call.from_user.id}`\n*Текст:* `{text}`")
    if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer('Відправлено, очікуйте на відповідь!', reply_markup=keyboard)
    elif (await get_userPosition(call.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await call.message.answer('Відправлено, очікуйте на відповідь!', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='add_photo', state=feedback.state)
async def feedback_add_photo(call):
    await call.message.answer('Пришли фото')
    await feedback.photo.set()


@dp.message_handler(state=feedback.photo, content_types=types.ContentType.PHOTO)
async def feedback_photo(message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    btnNext = InlineKeyboardButton('Відправити 📢', callback_data='next')
    btnQuit = InlineKeyboardButton('Відміна 🚫', callback_data='quit')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(btnNext).add(btnQuit)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


@dp.callback_query_handler(text='next', state=feedback.photo)
async def feedbackm(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await bot.send_photo(call.from_user.id, photo=photo, caption=f"*‼️ Нове повідомлення*\n\n*Від:* [{call.from_user.full_name}](tg://user?id={call.from_user.id})\n*ID:* `{call.from_user.id}`\n*Текст:* `{text}`")
    if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer('Відправлено, очікуйте на відповідь!', reply_markup=keyboard)
    elif (await get_userPosition(call.from_user.id)) == 'Admin':
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        button_5 = KeyboardButton('Адмін-панель 👮')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
        await call.message.answer('Відправлено, очікуйте на відповідь!', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='quit', state=[feedback.text, feedback.photo, feedback.state])
async def feedback_quit(call, state: FSMContext):
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


@dp.callback_query_handler(text='main')
async def toMain(call):
    if str(await get_isPaid(call.from_user.id)) == "False":
        button_1 = InlineKeyboardButton('Тарифи 📲', callback_data='tariffs')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1)
        await call.message.answer("Нажаль, ця функція вам недоступна, адже ви не обрали тариф 😢\n\nЩоб продовжити користування ботом, натисніть на кнопку нижче", reply_markup=keyboard)
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
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Вітаємо в головному меню 🏠", reply_markup=keyboard)

def register_handlers_feedbackMenu(dp: Dispatcher):
    dp.register_message_handler(feedbackCommand, text='Підтримка 📢')
    dp.register_message_handler(cancel, text=['Відміна 🔴'])
    dp.register_message_handler(feedbackText, state=feedback.text)
    dp.register_callback_query_handler(feedback_n, text='next', state=feedback.state)
    dp.register_callback_query_handler(feedback_add_photo, text='add_photo', state=feedback.state)
    dp.register_message_handler(feedback_photo, state=feedback.photo, content_types=types.ContentType.PHOTO)
    dp.register_callback_query_handler(feedbackm, text='next', state=feedback.photo)
    dp.register_callback_query_handler(feedback_quit, text='quit', state=[feedback.text, feedback.photo, feedback.state])
    dp.register_callback_query_handler(toMain, text='main')