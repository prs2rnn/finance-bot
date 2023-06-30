import asyncio

import asyncpg
from config_data import DSN


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
        return f"<b>List of expense category</b>\n{expenses}\n\n<b>List of income category</b>\n{incomes}"

    async def get_last_changes(self) -> str:
        res = await self.connector.fetch("select id, created, raw_text from record "
                                         "order by created asc limit 5")
        changes = "\n".join(map(lambda x: f"• \"{x['raw_text']}\" "
                    f"at {x['created'].date()}. Press /del{x['id']} to delete", res))
        return ("No changes", f"<b>List of last changes</b>\n\n{changes}")[changes != ""]

    async def delete_change(self, id_: int) -> int:
        res = await self.connector.execute("delete from record where id = $1", id_)
        return int(res.split()[1])

    async def _parse_category(self, category: str) -> str | None:
        res = await self.connector.fetch("select * from category")
        categories = {x['codename']: x['aliases'].split(",") for x in res}
        for i in categories:
            if i == category or category in categories[i]:
                return i

    async def add_record(self, amount: float, category: str, raw_text: str) -> str | None:
        codename = await self._parse_category(category)
        if not codename or amount <= 0:
            return
        res = await self.connector.execute("insert into record (amount, created, "
                    "codename, raw_text) values ($1, current_timestamp, $2, $3)",
                                           amount, codename, raw_text)
        return res




async def main() -> None:
    """Temporary function to test methods"""
    async with asyncpg.create_pool(DSN) as pool:
        print(await Request(pool).add_record(100, "22", "100 зп"))
        print(await Request(pool).get_last_changes())
        # print(await Request(pool).delete_change(1))


if __name__ == "__main__":
    asyncio.run(main())
