#!/bin/sh

psql << EOF
create user ${DB_USER} with password '${DB_PASSWORD}';
alter role ${DB_USER} with createdb createrole;
create database ${DB_NAME};
grant all on database ${DB_NAME} to ${DB_USER};
\c ${DB_NAME}
grant all on schema public to ${DB_USER};
\c ${DB_NAME} ${DB_USER}
create table if not exists users(
  telegram_id int unique not null,
  telegram_name varchar(30)
);
EOF
