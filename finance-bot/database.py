import asyncio

import asyncpg
from datetime import datetime
from config_data import DSN


class Request:
    def __init__(self, connector: asyncpg.Pool) -> None:
        self.connector = connector

    async def get_categories(self) -> str:
        res = await self.connector.fetch("select * from category")
        expenses = "\n".join(map(lambda x: f"• {x['codename']} ({x['aliases']})",
                                 filter(lambda x: x['is_expense'], res)))
        incomes = "\n".join(map(lambda x: f"• {x['codename']} ({x['aliases']})",
                                 filter(lambda x: not x['is_expense'], res)))
        return f"List of expense category\n{expenses}\n\nList of income category\n{incomes}"

    async def get_last_changes(self) -> str:
        res = await self.connector.fetch("select expense_id as id, amount, codename, "
                        "created, table_name from (select *, 'expense' as table_name "
                        "from expense union select *, 'income' as table_name from "
                        "income order by created desc limit 5) as a order by created asc")
        changes = "\n".join(map(lambda x: f"{res.index(x) + 1}) "
                                f"{round(x['amount'], 1)} rub, {x['codename']}, "
            f"{datetime.strftime(x['created'], '%d-%m-%y')}\n"
            f"(/del_{x['table_name']}_{x['id']})", res))
        return changes

    async def delete_change(self, table_name: str, id_: int) -> int:
        res = await self.connector.execute(f"delete from {table_name} where "
                                           f"{table_name}_id = $1", id_)
        return int(res.split()[1])

    async def add_record(self, amount: float, category: str, raw_text: str) -> None:
        table_name = ("expense", "income")[amount > 0]
        await self.connector.execute(f"insert into {table_name} ()")


async def main() -> None:
    """Temporary function to test methods"""
    async with asyncpg.create_pool(DSN) as pool:
        print(await Request(pool).get_categories())


if __name__ == "__main__":
    asyncio.run(main())
