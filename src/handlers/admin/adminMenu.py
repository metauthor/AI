from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.settings.config import BOT_TOKEN
from src.database.database import *
from states.states import *
from datetime import datetime, timedelta


storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(text=['/admin', 'Адмін-панель 👮'])
async def adminMenu(message):
    if str(await get_userPosition(message.from_user.id)) == 'Admin':
        button = InlineKeyboardButton('Розсилка 📨', callback_data='BotMailingSMS')
        button_0 = InlineKeyboardButton('Написати повідомлення 📝', callback_data='writeSMS')
        button_1 = InlineKeyboardButton('Змінити тариф 📐', callback_data='changeTariff')
        button_2 = InlineKeyboardButton('Надати тариф 🎯', callback_data='setTariff')
        button_3 = InlineKeyboardButton('Додати адміністратора 🟢', callback_data='addAdmin')
        button_4 = InlineKeyboardButton('Видалити адміністратора 🔴', callback_data='removeAdmin')
        button_5 = InlineKeyboardButton('На головну 🏠', callback_data='main')
        keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button).add(button_0).add(button_2, button_1).add(button_3).add(button_4).add(button_5)

        usersINDB = db["global"].distinct("_id", {"DATA": "global"})
        paidUsers = db["global"].distinct("_id", {"isPaid": True})
        adminsReq = db["global"].distinct("_id", {"userPosition": "Admin"})
        await message.answer(f"""*Вітаємо в Адмін-панелі 👮*

*Статистика боту 📊*

👥 *Користувачів в Базі Даних:* `{len(usersINDB)}`
💰 *Придбали підписку:* `{len(paidUsers)}`
👮 *Адміністраторів:* `{len(adminsReq)}`
    
Оберіть дію, натиснувши на одну з кнопок""", reply_markup=keyboard)
    else:
        button_1 = KeyboardButton('Новий запит 💡')
        button_2 = KeyboardButton('Мій кабінет 🏦')
        button_3 = KeyboardButton('Як користуватись ⁉️')
        button_4 = KeyboardButton('Підтримка 📢')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
        await message.answer('Нажаль у вас немає прав доступу!')
        await message.answer("Ви в головному меню 🏠", reply_markup=keyboard)


@dp.callback_query_handler(text='addAdmin', state=None)
async def addAdmin(call):
    button = KeyboardButton('Відміна 🔴')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await call.message.answer("Введи ID користувача", reply_markup=keyboard)
    await addAdmins.ids.set()


@dp.message_handler(state=addAdmins.ids)
async def addAdmins2(message, state: FSMContext):
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
        try:
            user_id = int(message.text)
            await state.update_data(ids=user_id)
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await update_userPosition(user_id, 'Admin')
            await bot.send_message(user_id, text='📢 *Ваш статус оновлено*\n\nВам доступна оновлена *Адмін-панель* 👮', reply_markup=keyboard)
            await message.answer('Успішно додано нового адміністратора!')
            await message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        except ValueError:
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await update_userPosition(user_id, 'Admin')
            await message.answer("Невірний ID користувача. Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='removeAdmin', state=None)
async def removeAdmin(call):
    button = KeyboardButton('Відміна 🔴')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await call.message.answer("Введи ID користувача", reply_markup=keyboard)
    await removeAdmins.ids.set()


@dp.message_handler(state=removeAdmins.ids)
async def removeAdmins2(message, state: FSMContext):
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
        try:
            user_id = int(message.text)
            await state.update_data(ids=user_id)
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await update_userPosition(user_id, 'User')
            await bot.send_message(user_id, text='📢 *Ваш статус оновлено*\n\nВам більше недоступна *Адмін-панель* 👮', reply_markup=keyboard)
            await message.answer('Успішно забрано адміністратора!')
            await message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        except ValueError:
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await update_userPosition(user_id, 'User')
            await message.answer("Невірний ID користувача. Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='changeTariff', state=None)
async def changeTariff(call):
    button = KeyboardButton('Відміна 🔴')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await call.message.answer("Введи ID користувача", reply_markup=keyboard)
    await changeUserTariff.ids.set()


@dp.message_handler(state=changeUserTariff.ids)
async def changeTariff2(message, state: FSMContext):
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
        user_id = int(message.text)
        await state.update_data(ids=user_id)
        if (await get_currentTariff(user_id)) == 'Non Paid':
            await message.answer("Схоже що користувач, не має оформленого Тарифу. Спершу скористайтесь функцією '*Надати тариф 🎯*'")
            await state.finish()
        else:
            button_1 = InlineKeyboardButton('Limited', callback_data='LimitedTariff')
            button_2 = InlineKeyboardButton('Unlimited', callback_data='UnlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1, button_2)
            if await get_currentTariff(user_id) == "Limited":
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await changeUserTariff.t.set()
            elif await get_currentTariff(user_id) == "Unlimited":
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Дата закінчення тарифу:* `{await get_expiryDate(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await changeUserTariff.t.set()
            else:
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await changeUserTariff.t.set()


@dp.callback_query_handler(state=changeUserTariff.t)
async def changeTariff3(call, state: FSMContext):
    await state.update_data(t=call.data)
    if call.data == 'LimitedTariff':
        user_data = await state.get_data()
        await update_allowedRequests(user_data['ids'], 5)
        await update_isPaid(user_data['ids'], True)
        await update_expiryDate(user_data['ids'], " ")
        await update_currentTariff(user_data['ids'], 'Limited')
        await bot.send_message(user_data['ids'], text=f"*Ваш тариф оновлено 🎯*\n\n*Новий тариф:* `{await get_currentTariff(user_data['ids'])}`\n*Залишилось запитів:* `{await get_allowedRequests(user_data['ids'])}`\n\nДякуємо, що ви з нами 🧑‍💻")
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
    if call.data == 'UnlimitedTariff':
        user_data = await state.get_data()
        current_date = datetime.now()
        end_date = current_date + timedelta(days=30)
        await update_allowedRequests(user_data['ids'], float('inf'))
        await update_isPaid(user_data['ids'], True)
        await update_expiryDate(user_data['ids'], str(end_date.strftime('%d.%m.%Y %H:%M:%S')))
        await update_currentTariff(user_data['ids'], 'Unlimited')
        await bot.send_message(user_data['ids'], text=f"*Ваш тариф оновлено 🎯*\n\n*Новий тариф:* `{await get_currentTariff(user_data['ids'])}`\n*Дата закінчення тарифу:* `{await get_expiryDate(user_data['ids'])}`\n*Залишилось запитів:* `{await get_allowedRequests(user_data['ids'])}`\n\nДякуємо, що ви з нами 🧑‍💻")
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='setTariff', state=None)
async def setTariff(call):
    button = KeyboardButton('Відміна 🔴')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await call.message.answer("Введи ID користувача", reply_markup=keyboard)
    await setUserTariff.ids.set()


@dp.message_handler(state=setUserTariff.ids)
async def setTariff2(message, state: FSMContext):
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
        user_id = int(message.text)
        await state.update_data(ids=user_id)
        if (await get_currentTariff(user_id)) == 'Limited' or (await get_currentTariff(user_id)) == 'Unlimited':
            await message.answer("Схоже що користувач, вже має оформлений Тариф. Скористайтесь функцією '*Змінити тариф 📐*'")
            await state.finish()
        else:
            button_1 = InlineKeyboardButton('Limited', callback_data='LimitedTariff')
            button_2 = InlineKeyboardButton('Unlimited', callback_data='UnlimitedTariff')
            keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1, button_2)
            if await get_currentTariff(user_id) == "Limited":
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await setUserTariff.t.set()
            elif await get_currentTariff(user_id) == "Unlimited":
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Дата закінчення тарифу:* `{await get_expiryDate(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await setUserTariff.t.set()
            else:
                await message.answer(f"*Про користувача 📖*\n\n*Тариф*: `{await get_currentTariff(user_id)}`\n*Залишок запитів:* `{await get_allowedRequests(user_id)}`\n*З нами з:* `{await get_joiningDateGlobal(user_id)}`\n\nОберіть тариф _(Наявний {await get_currentTariff(user_id)})_", reply_markup=keyboard)
                await changeUserTariff.t.set()
    

@dp.callback_query_handler(state=setUserTariff.t)
async def setTariff3(call, state: FSMContext):
    typeTariff = call.data
    await state.update_data(t=call.data)
    if call.data == 'LimitedTariff':
        user_data = await state.get_data()
        await update_allowedRequests(user_data['ids'], 5)
        await update_isPaid(user_data['ids'], True)
        await update_expiryDate(user_data['ids'], " ")
        await update_currentTariff(user_data['ids'], 'Limited')
        await bot.send_message(user_data['ids'], text=f"*Ваш тариф оновлено 🎯*\n\n*Новий тариф:* `{await get_currentTariff(user_data['ids'])}`\n*Залишилось запитів:* `{await get_allowedRequests(user_data['ids'])}`\n\nДякуємо, що ви з нами 🧑‍💻")
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
    if call.data == 'UnlimitedTariff':
        current_date = datetime.now()
        end_date = current_date + timedelta(days=30)
        user_data = await state.get_data()
        await update_allowedRequests(user_data['ids'], float('inf'))
        await update_isPaid(user_data['ids'], True)
        await update_expiryDate(user_data['ids'], str(end_date.strftime('%d.%m.%Y %H:%M:%S')))
        await update_currentTariff(user_data['ids'], 'Unlimited')
        await bot.send_message(user_data['ids'], text=f"*Ваш тариф оновлено 🎯*\n\n*Новий тариф:* `{await get_currentTariff(user_data['ids'])}`\n*Дата закінчення тарифу:* `{await get_expiryDate(user_data['ids'])}`\n*Залишилось запитів:* `{await get_allowedRequests(user_data['ids'])}`\n\nДякуємо, що ви з нами 🧑‍💻")
        if (await get_userPosition(call.from_user.id)) == 'User':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()
        elif (await get_userPosition(call.from_user.id)) == 'Admin':
            button_1 = KeyboardButton('Новий запит 💡')
            button_2 = KeyboardButton('Мій кабінет 🏦')
            button_3 = KeyboardButton('Як користуватись ⁉️')
            button_4 = KeyboardButton('Підтримка 📢')
            button_5 = KeyboardButton('Адмін-панель 👮')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_5).add(button_1).add(button_2, button_4).add(button_3)
            await call.message.answer("Ви в головному меню 🏠", reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='writeSMS', state=None)
async def writeSMS(call):
    button = KeyboardButton('Відміна 🔴')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await call.message.answer("Введи ID користувача", reply_markup=keyboard)
    await answerTo.ids.set()


@dp.message_handler(state=answerTo.ids)
async def answerToCommand(message, state: FSMContext):
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
        user_id = int(message.text)
        await state.update_data(ids=user_id)
        await message.answer("Введи текст, який хочеш відправити користувачу", reply_markup=types.ReplyKeyboardRemove())
        await answerTo.text.set()

@dp.message_handler(state=answerTo.text)
async def answerToText(message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    btnAddPhoto = InlineKeyboardButton('📸 Додати фото', callback_data='add_photo')
    btnNext = InlineKeyboardButton('Відправити 📢', callback_data='next')
    btnQuit = InlineKeyboardButton('Відміна 🚫', callback_data='quit')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(btnAddPhoto, btnNext).add(btnQuit)
    await message.answer(text=answer, reply_markup=keyboard)
    await answerTo.state.set()


@dp.callback_query_handler(text='next', state=answerTo.state)
async def answerTo_n(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await bot.send_message(data['ids'], text=f'*‼️ Відповідь служби підтримки*\n\n`{text}`')
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


@dp.callback_query_handler(text='add_photo', state=answerTo.state)
async def answerTo_add_photo(call):
    await call.message.answer('Пришли фото')
    await answerTo.photo.set()


@dp.message_handler(state=answerTo.photo, content_types=types.ContentType.PHOTO)
async def answerTo_photo(message, state: FSMContext):
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
async def answerTom(call, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await bot.send_photo(data['ids'], photo=photo, caption=f'*‼️ Відповідь служби підтримки*\n\n`{text}`')
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


@dp.callback_query_handler(text='quit', state=[answerTo.text, answerTo.photo, answerTo.state])
async def answerTo_quit(call, state: FSMContext):
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


def register_handlers_adminMenu(dp: Dispatcher):
    dp.register_message_handler(adminMenu, text=['/admin', 'Адмін-панель 👮'])
    dp.register_callback_query_handler(addAdmin, text='addAdmin', state=None)
    dp.register_message_handler(addAdmins2, state=addAdmins.ids)
    dp.register_callback_query_handler(removeAdmin, text='removeAdmin', state=None)
    dp.register_message_handler(removeAdmins2, state=removeAdmins.ids)
    dp.register_callback_query_handler(changeTariff, text='changeTariff', state=None)
    dp.register_message_handler(changeTariff2, state=changeUserTariff.ids)
    dp.register_callback_query_handler(changeTariff3, state=changeUserTariff.t)
    dp.register_callback_query_handler(setTariff, text='setTariff', state=None)
    dp.register_message_handler(setTariff2, state=setUserTariff.ids)
    dp.register_callback_query_handler(setTariff, state=setUserTariff.t)
    dp.register_callback_query_handler(writeSMS, text='writeSMS', state=None)
    dp.register_message_handler(answerToCommand, state=answerTo.ids)
    dp.register_message_handler(answerToText, state=answerTo.text)
    dp.register_callback_query_handler(answerTo_n, text='next', state=answerTo.state)
    dp.register_callback_query_handler(answerTo_add_photo, text='add_photo', state=answerTo.state)
    dp.register_message_handler(answerTo_photo, state=answerTo.photo, content_types=types.ContentType.PHOTO)
    dp.register_callback_query_handler(answerTom, text='next', state=answerTo.photo)
    dp.register_message_handler(cancel, text=['Відміна 🔴'])
    dp.register_callback_query_handler(answerTo_quit, text='quit', state=[answerTo.text, answerTo.photo, answerTo.state])

