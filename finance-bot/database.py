import asyncio

import asyncpg

from config_data import DSN


class Request:
    def __init__(self, connector: asyncpg.Pool) -> None:
        self.connector = connector

    async def _check_user(self, id_: int) -> bool:
        res = await self.connector.fetchrow("select exists (select 1 from users where "
                                            "telegram_id = $1)", id_)
        # extract from Record as column named "exists", or res[0] as first column
        return res["exists"]

    async def _add_user(self, id_: int, name: str | None) -> None:
        await self.connector.execute("insert into users(telegram_id, telegram_name) "
                                     "values ($1, $2)", id_, name)


async def main() -> None:
    """Temporary function to test methods"""
    async with asyncpg.create_pool(DSN) as pool:
        await Request(pool)._check_user(123456789)


if __name__ == "__main__":
    asyncio.run(main())
