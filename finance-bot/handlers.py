from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import Request
from middlewares import AddRecord, DeleteRecord

router = Router()


@router.message(Command("start", "help"))
async def proceed_start(message: Message) -> None:
    await message.answer("<b>Bot for financial accounting</b>\n\n"
                         "Add record: 250 cab\n"
                         "Categories: /categories\n"
                         "Current month: /month\n"
                         "Last changes: /changes")


@router.message(Command("categories"))
async def proceed_categories(message: Message, request: Request) -> None:
    content = await request.get_categories()
    await message.answer(f"{content}\n\nAdd record: 250 cab\nLast changes: /changes")


@router.message(Command("changes"))
async def proceed_changes(message: Message, request: Request) -> None:
    content = await request.get_last_changes()
    await message.answer(f"{content}\n\nAdd record: 250 cab\nCategories: /categories")


@router.message(DeleteRecord())
async def proceed_delete(message: Message, id_: int, request: Request) -> None:
    is_delete = await request.delete_change(id_)
    answer = ("<b>No record found so not deleted</b>\n\nLast changes: /changes",
              "<b>Record has been deleted</b>\n\nLast changes: /changes")[is_delete]
    await message.answer(answer)


@router.message(AddRecord())
async def proceed_record(message: Message, amount: float,
                         category: str, raw_text: str, request: Request) -> None:
    res = await request.add_record(amount, category, raw_text)
    answer = ("False", "True")[1 if res else 0]
    await message.answer(answer)


@router.message()
async def proceed_other(message: Message) -> None:
    await message.answer("<b>Not recognized</b>\n\nTo add record: 250 cab\nOr use /help for help")
