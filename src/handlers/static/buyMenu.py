from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.settings.config import BOT_TOKEN, MANAGER, CARD
from datetime import datetime, timedelta

storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot, storage=storage)


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


def register_handlers_buyMenu(dp: Dispatcher):
    dp.register_callback_query_handler(limitedTariff, text='limitedTariff')
    dp.register_callback_query_handler(unlimitedTariff, text='unlimitedTariff')