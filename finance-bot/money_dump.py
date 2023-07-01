import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from config_data import DSN
import asyncpg

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
    values = ({k: float(row[k]) if k == "amount" else row[k] for k in row}  # pyright: ignore
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


def load_csv() -> Iterable[dict[str, Any]]:
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="	")
        return parse_csv(reader)


async def import_csv(data: Iterable[dict[str, Any]]) -> None:
    async with asyncpg.create_pool(DSN) as pool:
        await pool.execute("insert into record")


if __name__ == "__main__":
    load_csv()
