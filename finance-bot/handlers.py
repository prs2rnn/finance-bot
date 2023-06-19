from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import Request
from vocabulary import VOCABULARY_EN

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message, request: Request) -> None:
    await message.answer(VOCABULARY_EN["/start"])
