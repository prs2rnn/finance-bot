import asyncio
import csv
from pathlib import Path
from typing import Any

import asyncpg
import httpx

from config_data import ALLOWED_TELEGRAM_USER_IDS, DSN, TELEGRAM_BOT_TOKEN
from database import Request, Statistics
from vocabulary import VOCABULARY

backup_path = Path(__file__).parent.joinpath("backup.csv")


def save_to_csv(cols: list[str], data: list[dict[str, Any]]) -> None:
    with open(backup_path, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, cols, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(data)


async def backup_db() -> Statistics:
    async with asyncpg.create_pool(DSN) as pool:
        res = await pool.fetch("select * from record")
        cols = list(res[0].keys())
        data = [dict(row.items()) for row in res]
        save_to_csv(cols, data)
        return await Request(pool).get_statistics("week")


async def notify(client: httpx.AsyncClient, id_: str, text: str) -> None:
    url = (f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
           f"sendMessage")
    await client.post(url, headers={"Content-Type": "application/json"},
                      json={"chat_id": id_, "text": text, "parse_mode": "HTML"})
    if backup_path.stat().st_size < 2097152:
        with open(backup_path, "rb") as file:
            url = (f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
                   f"sendDocument?chat_id={id_}&document=attach://file")
            await client.post(url, files={"file": file})
    else:
        await client.get("url", params={"chat_id": id_,
                                        "text": VOCABULARY["backup_error"]})


async def main() -> None:
    statistics = await backup_db()
    text = VOCABULARY["notify_week"].format(
            expenses=statistics.expenses, incomes=statistics.incomes,
            savings=statistics.savings, plan_savings=statistics.plan_savings)
    async with httpx.AsyncClient() as client:
        tasks = (asyncio.create_task(notify(client, id_, text))
                 for id_ in ALLOWED_TELEGRAM_USER_IDS.split(","))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
