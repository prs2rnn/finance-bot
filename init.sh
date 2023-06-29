#!/bin/sh

psql << EOF
create user ${DB_USER} with password '${DB_PASSWORD}';
alter role ${DB_USER} with createdb createrole;
create database ${DB_NAME};
grant all on database ${DB_NAME} to ${DB_USER};
\c ${DB_NAME}
grant all on schema public to ${DB_USER};
\c ${DB_NAME} ${DB_USER}
create table if not exists category(
    codename varchar(50) primary key,
    aliases text,
    is_expense boolean
);
create table if not exists record(
    expense_id integer primary key generated always as identity,
    amount numeric(13, 3),
    created timestamptz(3),
    codename varchar(50),
    raw_text text,
    FOREIGN KEY(codename) REFERENCES expense_category(codename)
);
insert into category(codename, aliases, is_expense)
values
    ('food', 'food,meal,еда,продукты', true),
    ('transport', 'bus,транспорт', true),
    ('pharmacy', 'аптека,лекарства', true),
    ('mobile', 'связь,phone,телефон', true),
    ('internet', 'инет,inet', true),
    ('barber', 'hair,стрижка,барбер', true),
    ('lunch', 'ланч,столовая,ресторан,кафе,cafe', true),
    ('cab', 'такси,taxi,cab', true),
    ('relax', 'прогулка,свидание', true),
    ('clothes', 'шмот,одежда', true),
    ('gift', 'подарки', true),
    ('car', 'машина,авто,auto', true),
    ('subscription', 'подписка,sub', true),
    ('other', 'прочее,другое', true);
    ('salary', 'зп', false),
    ('business', 'dividends,extra', false),
    ('gift', 'from other', false);
EOF
