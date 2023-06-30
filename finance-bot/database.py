import asyncio
from typing import NamedTuple

import asyncpg

from config_data import DSN


class Statistics(NamedTuple):
    expenses: float
    savings: float
    incomes: float
    plan_savings: float


class Request:
    def __init__(self, connector: asyncpg.Pool) -> None:
        self.connector = connector

    async def get_categories(self) -> str:
        res = await self.connector.fetch("select * from category")
        expenses = "\n".join(map(lambda x: f"• {x['codename']} ({x['aliases']})",
                                 filter(lambda x: x['is_expense'], res)))
        incomes = "\n".join(map(lambda x: f"• {x['codename']} ({x['aliases']})",
                                 filter(lambda x: not x['is_expense']
                                        and x['codename'] != 'savings', res)))
        return (f"<b>List of expense category</b>\n{expenses}\n\n<b>"
                f"List of income category</b>\n{incomes}")

    async def get_last_records(self) -> str:
        res = await self.connector.fetch("select id, amount, created, codename from record "
                                         "order by created asc limit 5")
        records = "\n".join(map(lambda x: f"• {round(x['amount'], 1)}₽ for {x['codename']} "
                    f"at {x['created'].date()}. Press /del{x['id']} to delete", res))
        return ("No records found", f"<b>List of last records</b>\n\n{records}")[records != ""]

    async def delete_change(self, id_: int) -> int:
        res = await self.connector.execute("delete from record where id = $1", id_)
        return int(res.split()[1])

    async def _parse_category(self, category: str) -> str | None:
        res = await self.connector.fetch("select * from category")
        categories = {x['codename']: x['aliases'].split(", ") for x in res}
        for i in categories:
            if i == category or category in categories[i]:
                return i

    async def add_record(self, amount: float, category: str,
                         raw_text: str) -> tuple[float, str] | None:
        codename = await self._parse_category(category)
        if not codename or amount <= 0:
            return
        await self.connector.execute("insert into record (amount, created, "
                             "codename, raw_text) values ($1, "
                             "current_timestamp, $2, $3)", amount, codename, raw_text)
        return round(amount, 1), codename

    async def get_statistics(self, period: str = "month"):
        """
        Returns expenses, incomes and savings for period

        Params:
        period  One of the periods: "month", "day"
        """
        expenses = await self.connector.fetchrow("select sum(amount) from record join "
                "category on record.codename = category.codename "
                "where is_expense = true and created > "
               f"date_trunc('{period}', now()) and record.codename <> 'savings'")
        savings = await self.connector.fetchrow("select sum(amount) from record join "
                "category on record.codename = category.codename "
                "where is_expense = true and created > "
               f"date_trunc('{period}', now()) and record.codename = 'savings'")
        incomes = await self.connector.fetchrow("select sum(amount), sum(amount) * 0.15 "
                "as \"Plan savings\" from record join category on record.codename = "
                "category.codename where is_expense = false and created > "
                f"date_trunc('{period}', now())")
        return Statistics(round(float(expenses[0]), 1), round(float(savings[0]), 1),
                          round(float(incomes[0]), 1), round(float(incomes[1]), 1))



async def main() -> None:
    """Temporary function to test methods"""
    async with asyncpg.create_pool(DSN) as pool:
        # print(await Request(pool).add_record(200, "business", "200 business"))
        print(await Request(pool).get_last_records())


if __name__ == "__main__":
    asyncio.run(main())
