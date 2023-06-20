#!/bin/sh

psql << EOF
create user ${DB_USER} with password '${DB_PASSWORD}';
alter role ${DB_USER} with createdb createrole;
create database ${DB_NAME};
grant all on database ${DB_NAME} to ${DB_USER};
\c ${DB_NAME}
grant all on schema public to ${DB_USER};
\c ${DB_NAME} ${DB_USER}
create table if not exists expense_category(
    codename varchar(50) primary key,
    is_base_expense boolean,
    aliases text
);
create table if not exists expense(
    expense_id integer primary key generated always as identity,
    amount numeric(13, 3),
    created timestamptz(3),
    codename varchar(50),
    raw_text text,
    FOREIGN KEY(codename) REFERENCES expense_category(codename)
);
create table if not exists income_category(
    codename varchar(50) primary key,
    aliases text
);
create table if not exists income(
    income_id integer primary key generated always as identity,
    amount numeric(13, 2),
    created timestamptz(3),
    codename varchar(50),
    raw_text text,
    FOREIGN KEY(codename) REFERENCES income_category(codename)
);
insert into expense_category(codename, is_base_expense, aliases)
values
    ('food', true, 'food,meal,еда,продукты'),
    ('transport', true, 'bus,транспорт'),
    ('pharmacy', true, 'аптека,лекарства'),
    ('mobile', true, 'связь,phone,телефон'),
    ('internet', true, 'инет,inet'),
    ('barber', true, 'hair,стрижка,барбер'),
    ('lunch', false, 'ланч,столовая,ресторан,кафе,cafe'),
    ('cab', false, 'такси,taxi,cab'),
    ('relax', false, 'прогулка,свидание'),
    ('clothes', false, 'шмот,одежда'),
    ('gift', false, 'подарки'),
    ('car', false, 'машина,авто,auto'),
    ('subscription', false, 'подписка,sub'),
    ('other',  true, 'прочее,другое');
insert into income_category(codename, aliases) values
    ('salary', 'зп'), ('business', 'dividends,extra'), ('gift', 'from other');
EOF
