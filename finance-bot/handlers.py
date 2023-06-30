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
                         "Last records: /records")


@router.message(Command("categories"))
async def proceed_categories(message: Message, request: Request) -> None:
    content = await request.get_categories()
    await message.answer(f"{content}\n\nAdd record: 250 cab\nLast records: /records"
                         "\n\n<b>Warning</b>: savings are added manually and not included "
                         "in expenses when calculating. Planned savings - 15%")


@router.message(Command("records"))
async def proceed_records(message: Message, request: Request) -> None:
    content = await request.get_last_records()
    await message.answer(f"{content}\n\nAdd record: 250 cab\nCategories: /categories")


@router.message(DeleteRecord())
async def proceed_delete(message: Message, id_: int, request: Request) -> None:
    is_delete = await request.delete_change(id_)
    answer = ("<b>No record found so not deleted</b>\n\nLast records: /records",
              "<b>Delete record</b>\n\nAdd record: 250 cab\nLast records: /records\n"
              "Current month: /month")[is_delete]
    await message.answer(answer)


@router.message(AddRecord())
async def proceed_record(message: Message, amount: float, category: str,
                         raw_text: str, request: Request) -> None | Message:
    res = await request.add_record(amount, category, raw_text)
    if not res:
        return await message.answer(
         "<b>Not recognized</b>\n\nTo add record: 250 cab\nOr use /help for help")
    amount, codename = res
    statistics = await request.get_statistics("day")
    await message.answer(
        f"Add new record: {round(amount, 1)}₽ for {codename}\n\n"
        f"Today statistics:\nExpenses\t{statistics.expenses}₽\nIncomes\t"
        f"{statistics.incomes}₽\nSavings\t{statistics.savings}₽ from planned "
        f"{statistics.plan_savings}₽\n\n"
        f"Current month: /month\nLast records: /records\nCategories: /categories"
)


@router.message(Command("month"))
async def proceed_month(message: Message, request: Request) -> None:
    statistics = await request.get_statistics()
    await message.answer(f"<b>Month statistics</b>\n\nExpenses\t{statistics.expenses}₽"
        f"\nIncomes\t{statistics.incomes}₽\n"
        f"Savings\t{statistics.savings}₽ from planned {statistics.plan_savings}₽"
        "\n\nAdd record: 250 bus\nCategories: /categories\nLast records: /records"
)


@router.message()
async def proceed_other(message: Message) -> None:
    await message.answer(
        "<b>Not recognized</b>\n\nAdd record: 250 cab\nOr use /help for help")
