# Installation

Rename `.env.example` to `.env` and fill the variables

```shell
mv .env.example .env
```

Change DSN variable in `config_data.py` file depending the way you wish to launch bot

```python
# localhost
DSN = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@localhost:5434/{getenv('DB_NAME')}"
# docker
DSN = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@postgres:5432/{getenv('DB_NAME')}"
```

The default way

```shell
docker-compose up -d
```

Or modify as you want. Note that docker-compose.yml file uses `db.sh` script to init database

Database volume is being created in `../db/` directory

# Technical specification

Implement a simple program using telegram bot api for personal finance management and subsequent analytical research.

### Dependencies

- aiogram3.x
- postgresql as data base (asyncpg)
- docker (Dockerfile, docker-compose.yml)

### Requirements

- Implementation of exclusively necessary functionality, without excessive work opportunities such as ORM or inline keyboards.

- Ensuring the security of interaction through the required interface. The bot responds to incoming updates exclusively for the specified id.

- Both expenses and income are accounted for.

- Ensuring the convenience and speed of making changes to the database.

- Neat and maintainable code and modular project structure.

- Secure information is stored in environments variables.

- The possibility of deducting 10-20% of income in the form of an amount going as an airbag.
