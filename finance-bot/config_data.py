from os import getenv

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_TELEGRAM_USER_IDS = getenv("ALLOWED_TELEGRAM_USER_IDS", "")
DSN = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@postgres:5432/{getenv('DB_NAME')}"
