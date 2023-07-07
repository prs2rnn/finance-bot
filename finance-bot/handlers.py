from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import Request
from middlewares import AddRecord, DeleteRecord
from telegram_logger import exception_logger, telegram_logger
from vocabulary import VOCABULARY

router = Router()


@router.message(Command("start", "help"))
async def proceed_start(message: Message) -> None:
    await message.answer(VOCABULARY["start"])


@router.message(Command("categories"))
@exception_logger(telegram_logger)
async def proceed_categories(message: Message, request: Request) -> None:
    content = await request.get_categories()
    await message.answer(VOCABULARY["categories"].format(content=content))


@router.message(Command("records"))
@exception_logger(telegram_logger)
async def proceed_records(message: Message, request: Request) -> None:
    content = await request.get_last_records()
    await message.answer(VOCABULARY["records"].format(content=content))


@router.message(DeleteRecord())
@exception_logger(telegram_logger)
async def proceed_delete(message: Message, id_: int, request: Request) -> None:
    is_delete = await request.delete_record(id_)
    answer = (VOCABULARY["delete_false"], VOCABULARY["delete_true"])[is_delete]
    await message.answer(answer)


@router.message(AddRecord())
@exception_logger(telegram_logger)
async def proceed_record(message: Message, amount: float, category: str,
                         raw_text: str, request: Request) -> None | Message:
    res = await request.add_record(amount, category, raw_text)
    if not res:
        return await message.answer(VOCABULARY["other"])
    amount, codename = res
    statisics, categories = await request.get_statistics("day")
    await message.answer(VOCABULARY["add_record"].format(
            codename=codename, amount=round(amount, 1),
            expenses=statisics.expenses, incomes=statisics.incomes,
            savings=statisics.savings, plan_savings=statisics.planned_savings,
            categories=categories))


@router.message(Command("month"))
@exception_logger(telegram_logger)
async def proceed_month(message: Message, request: Request) -> None:
    statisics, categories = await request.get_statistics()
    await message.answer(VOCABULARY["month"].format(
            expenses=statisics.expenses, incomes=statisics.incomes,
            savings=statisics.savings, plan_savings=statisics.planned_savings,
            categories=categories))


@router.message()
async def proceed_other(message: Message) -> None:
    await message.answer(VOCABULARY["other"])
