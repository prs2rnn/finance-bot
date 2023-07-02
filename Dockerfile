FROM python:3.11.3-alpine3.18

ENV TZ Europe/Moscow

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN apk add --update curl libc-dev gcc openrc
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN mkdir -p /finance-bot
WORKDIR /finance-bot
COPY . /finance-bot

RUN poetry install

ADD crontab /etc/cron.d/finance-bot-cron
RUN chmod 0644 /etc/cron.d/finance-bot-cron
RUN crontab /etc/cron.d/finance-bot-cron
RUN touch /var/log/cron.log

CMD ["sh", "-c", "crond && poetry run python finance-bot/bot.py"]
