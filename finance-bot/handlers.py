from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import Request
from middlewares import DeleteRecord
from vocabulary import VOCABULARY_EN

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(VOCABULARY_EN["/start"])


@router.message(Command("categories"))
async def proceed_categories(message: Message, request: Request) -> None:
    content = await request.get_categories()
    await message.answer(VOCABULARY_EN["/categories"] + content)


@router.message(Command("changes"))
async def proceed_changes(message: Message, request: Request) -> None:
    content = await request.get_last_changes()
    await message.answer(VOCABULARY_EN["/changes"] + content)


@router.message(DeleteRecord())
async def proceed_delete(message: Message, table_name: str,
                         id_: int, request: Request) -> None:
    is_delete = await request.delete_change(table_name, id_)
    if is_delete:
        await message.answer(VOCABULARY_EN["/del"])
