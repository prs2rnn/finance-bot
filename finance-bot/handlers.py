from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters import Command

from vocabulary import VOCABULARY_EN

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(VOCABULARY_EN["/start"])
