from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import Request
from vocabulary import VOCABULARY_EN

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message, request: Request) -> None:
    id_, name = (
        message.from_user.id,  # pyright: ignore
        message.from_user.username if message.from_user.username  # pyright: ignore
        is not None else message.from_user.full_name)  # pyright: ignore
    if not await request._check_user(id_):
        await request._add_user(id_, name)
    await message.answer(VOCABULARY_EN["/start"])
