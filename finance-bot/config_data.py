from os import getenv

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_TELEGRAM_USER_IDS = getenv("ALLOWED_TELEGRAM_USER_IDS", "")
