import re
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from aiogram.types.message import Message
import asyncpg

from database import Request


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
    async def __call__(self, message: Message) -> dict[str, int] | None:
        match = re.fullmatch(r"(/del)(\d+)",
                             message.text if message.text else "")
        if match:
            return {"id_": int(match.group(2))}


class AddRecord(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, float | str | None] | None:
        match = re.fullmatch(r"(\d+\.?\d*) ([A-Za-zА-Яа-я]+) ?[^\n]*",
                             message.text if message.text else "")
        if match:
            return {"amount": float(match.group(1)),
                    "category": match.group(2).lower(),
                    "raw_text": message.text}
