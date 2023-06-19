from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types.message import Message

from vocabulary import VOCABULARY_EN


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: str) -> None:
        self.allowed_ids = list(map(int, allowed_ids.split(",")))

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.allowed_ids:
            return await handler(event, data)
        await event.answer(VOCABULARY_EN["deny"])
