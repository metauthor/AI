import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = 787080961
MANAGER = "@mary_ITmanager"
CARD = '5366 3911 5640 1416'
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

EMAIL_ADDRESS = 'chatgptlogs@gmail.com'
TO_EMAIL_ADRESS = 'ioleksandr.panashchuk@gmail.com'
EMAIL_PASSWORD = 'qzdlreluasutlszv'

DB_USER_KEY = os.getenv("DB_USER_KEY")
DB_PASS_KEY = os.getenv("DB_PASS_KEY")

TARGET_CHANNEL_1 = os.getenv("TARGET_CHANNEL_1")

SUCCESS_SUB_TEXT = """*Підписку на канал підтверджено!*

Нижче можеш ознайомитись із рекомендаціями по користуванню або одразу розпочати роботу."""
