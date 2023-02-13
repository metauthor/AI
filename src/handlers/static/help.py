from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.settings.config import BOT_TOKEN


bot = Bot(BOT_TOKEN, parse_mode='markdown')
dp = Dispatcher(bot)


@dp.callback_query_handler(text='how_to_use')
async def howToUseCommand(call):
    button_1 = InlineKeyboardButton('Почати 🎯', callback_data='start_way')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1)
    await call.message.answer("""*Як користуватись ботом ⁉️*

Добре подумайте перед тим, як запитувати щось у бота. ChatGPT вимагає чітких конкретизованих запитів, наприклад:
- `Вкажи українською мовою плюси та мінуси бути програмістом`
- `Надішли шлях для вивчення Front-End розробки`
- `Як створити милі стікери для Telegram?`

Пропонуємо ознайомитись із більш детальною [статтею-керівництвом](https://telegra.ph/ChatGPT--pravila-koristuvannya-01-16) по використанню бота.

Пам'ятайте, вам відповідає штучний інтелект, тому результат завжди залежить напряму від того, наскільки якісний та конкретизований запит.""", reply_markup=keyboard, disable_web_page_preview=True)

@dp.message_handler(text='Як користуватись ⁉️')
async def howToUseCommand2(message):
    button_1 = InlineKeyboardButton('Почати 🎯', callback_data='start_way')
    # button_2 = InlineKeyboardButton('На головну', callback_data='main')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(button_1)#.add(button_2)
    await message.answer("""*Як користуватись ботом ⁉️*

Добре подумайте перед тим, як запитувати щось у бота. ChatGPT вимагає чітких конкретизованих запитів, наприклад:
- `Вкажи українською мовою плюси та мінуси бути програмістом`
- `Надішли шлях для вивчення Front-End розробки`
- `Як створити милі стікери для Telegram?`

Пропонуємо ознайомитись із більш детальною [статтею-керівництвом](https://telegra.ph/ChatGPT--pravila-koristuvannya-01-16) по використанню бота.

Пам'ятайте, вам відповідає штучний інтелект, тому результат завжди залежить напряму від того, наскільки якісний та конкретизований запит.""", reply_markup=keyboard, disable_web_page_preview=True)

def register_handlers_helpMenu(dp: Dispatcher):
    dp.register_callback_query_handler(howToUseCommand, text='how_to_use')
    dp.register_message_handler(howToUseCommand2, text='Як користуватись ⁉️')
