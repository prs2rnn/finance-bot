import asyncio
import functools
import logging
from typing import Callable

import httpx

from config_data import TELEGRAM_BOT_TOKEN, ALLOWED_TELEGRAM_USER_IDS


async def send_log(url: str, chat_id: int | str, text: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        )


class TelegramLoggingHandler(logging.Handler):
    def __init__(self, token: str, chat_id: int | str) -> None:
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord) -> None:
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        # asyncio.run(send_log(url, self.chat_id, self.format(record)))
        loop = asyncio.get_running_loop()
        loop.create_task(send_log(url, self.chat_id, self.format(record)))


telegram_logger = logging.getLogger(__file__)
telegram_logger.setLevel(logging.ERROR)
handler = TelegramLoggingHandler(TELEGRAM_BOT_TOKEN,
                                 ALLOWED_TELEGRAM_USER_IDS.split(",")[0])
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
telegram_logger.addHandler(handler)


def exception_logger(logger: logging.Logger):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as err:
                logger.exception(err)

        return wrapper

    return decorator

if __name__ == "__main__":
    @exception_logger(telegram_logger)
    def main() -> None:
        raise FileNotFoundError("shit")
