import re
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from aiogram.types.message import Message
import asyncpg

from database import Request
from vocabulary import VOCABULARY_EN


class AccessMiddleware(BaseMiddleware):
    """Authentication to use bot for incoming user"""

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


class DbSession(BaseMiddleware):
    """Establishes database connection for incoming updates"""

    def __init__(self, connector: asyncpg.Pool) -> None:
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.connector.acquire() as connection:
            data["request"] = Request(connection)
            return await handler(event, data)


class DeleteRecord(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, int | str] | None:
        match = re.fullmatch(r"(/del)_(expense)_(\d+)|(/del)_(income)_\d+",
                             message.text if message.text else "")
        if match:
            return {"table_name": match.group(2), "id_": int(match.group(3))}
