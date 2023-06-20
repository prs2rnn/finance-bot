#!/bin/sh

source ./.env

echo \
"create user $DB_USER with password '$DB_PASSWORD';
alter role $DB_USER with createdb createrole;
create database $DB_NAME;
grant all on database $DB_NAME to $DB_USER;
\c $DB_NAME
grant all on schema public to $DB_USER;
\c $DB_NAME $DB_USER

create table if not exists users(
  telegram_id bigint unique not null,
  telegram_name varchar(30)
);

create or replace function insert_values_from_env(env_var text)
returns void as \$\$
declare
  values_arr bigint[];
  value bigint;
begin
  -- split env var value into array of bigints:
  select string_to_array(env_var, ',')::bigint[] into values_arr;
  -- iteratively insert each value into the table:
  foreach value in array values_arr loop
    insert into users (telegram_id) values (value);
  end loop;
end;
\$\$ language plpgsql;
select insert_values_from_env('$ALLOWED_TELEGRAM_USER_IDS');" > init.sql

sudo docker-compose up -d
rm init.sql
