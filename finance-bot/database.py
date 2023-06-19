import asyncio

import asyncpg

from config_data import DSN


async def main() -> None:
    async with asyncpg.create_pool(DSN) as pool:
        res = await pool.fetchrow("select current_timestamp;")
        print(res)


if __name__ == "__main__":
    asyncio.run(main())
