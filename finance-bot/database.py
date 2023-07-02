import asyncio
from typing import NamedTuple

import asyncpg

from config_data import DSN
from vocabulary import VOCABULARY

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
        expenses = "\n".join(map(lambda x: VOCABULARY["db_category"].format(
                                codename=x["codename"], aliases=x["aliases"]),
                                 filter(lambda x: x['is_expense'], res)))
        incomes = "\n".join(map(lambda x: VOCABULARY["db_category"].format(
                                codename=x["codename"], aliases=x["aliases"]),
                                 filter(lambda x: not x['is_expense']
                                        and x['codename'] != 'savings', res)))
        return VOCABULARY["db_categories"].format(expenses=expenses, incomes=incomes)

    async def get_last_records(self) -> str:
        res = await self.connector.fetch("select * from (select id, amount, created, "
                                         "codename from record order by created desc limit 5) "
                                         "as first order by created asc")
        records = "\n".join(map(lambda x: VOCABULARY["db_records"].format(
                            amount=round(x["amount"], 1), codename=x["codename"],
                            created=x["created"].date(), id_=x["id"]), res))
        return (VOCABULARY["db_records_false"],
                VOCABULARY["db_records_true"].format(records=records))[records != ""]

    async def delete_record(self, id_: int) -> int:
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

    async def get_statistics(self, period: str = "month") -> Statistics:
        """
        Returns expenses, incomes and savings for period

        Params:
        period  One of the periods: "month", "day", "week"
        """
        expenses = await self.connector.fetchrow("select sum(amount) from record join "
                "category on record.codename = category.codename "
                "where is_expense = true and created >= "
               f"date_trunc('{period}', now()) and record.codename <> 'savings'")
        savings = await self.connector.fetchrow("select sum(amount) from record join "
                "category on record.codename = category.codename "
                "where is_expense = true and created >= "
               f"date_trunc('{period}', now()) and record.codename = 'savings'")
        incomes = await self.connector.fetchrow("select sum(amount), sum(amount) * 0.15 "
                "as \"Plan savings\" from record join category on record.codename = "
                "category.codename where is_expense = false and created >= "
                f"date_trunc('{period}', now())")
        return Statistics(round(float(expenses[0]) if expenses[0] is not None else 0.0, 1),
                          round(float(savings[0]) if savings[0] is not None else 0.0, 1),
                          round(float(incomes[0]) if incomes[0] is not None else 0.0, 1),
                          round(float(incomes[1] if incomes[1] is not None else 0.0), 1))



async def main() -> None:
    """Temporary function to test methods"""
    async with asyncpg.create_pool(DSN) as pool:
        # print(await Request(pool).add_record(200, "business", "200 business"))
        print(await Request(pool).get_statistics())


if __name__ == "__main__":
    asyncio.run(main())
