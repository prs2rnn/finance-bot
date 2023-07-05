"""I used this script to import own expenses from MoneyOK IOS app"""
import asyncio
import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import asyncpg

from config_data import DSN

path = Path(__file__).parent.joinpath("MoneyOK.csv")


def parse_csv(rows: csv.DictReader) -> Iterable[dict[str, Any]]:
    cols = {
        "Date": "created",
        "Amount": "amount",
        "Category": "codename",
        "Note": "raw_text",
    }
    values = ({cols[k]: v for k, v in row.items() if k in cols} for row in rows)
    values = ({k: datetime.strptime(row[k], "%Y.%m.%d") if k == "created" else row[k]
        for k in row}for row in values)
    values = ({k: abs(float(row[k])) if k == "amount" else row[k] for k in row}  # pyright: ignore
             for row in values)
    codenames = {
        "From others": "business",
        "Salary": "salary",
        "Dividends": "business",
        "Business": "business",
        "Food": "food",
        "Transport": "transport",
        "Extra expenses": "other",
        "Internet": "internet",
        "Pharmacy": "pharmacy",
        "Mobile": "mobile",
        "Lunches": "lunch",
        "Barbershop": "barber",
        "Relaxation": "relax",
        "Clothes": "clothes",
        "For people": "gift",
        "House": "house",
        "Car": "car",
        "Music": "subscription",
    }
    values = ({k: codenames[row[k]] if k == "codename" else row[k]  # pyright: ignore
               for k in row} for row in values)
    return values


async def import_db(data: Iterable[dict[str, Any]]) -> None:
    async with asyncpg.create_pool(DSN) as pool:
        tasks = (asyncio.create_task(pool.execute("insert into record (created, "
            "amount, codename, raw_text) values ($1, $2, $3, $4)", *raw.values()))
            for raw in data)
        await asyncio.gather(*tasks)


async def main() -> None:
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="	")
        data = parse_csv(reader)
        await import_db(data)
        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
