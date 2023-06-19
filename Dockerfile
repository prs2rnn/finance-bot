FROM python:3.11.3-alpine3.18

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN apk add --update curl libc-dev gcc
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN mkdir -p /finance-bot
WORKDIR /finance-bot
COPY . /finance-bot

RUN poetry install

CMD [ "poetry", "run", "python", "finance-bot/bot.py" ]
