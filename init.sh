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
    id integer primary key generated always as identity,
    amount numeric(13, 3),
    created timestamptz(3),
    codename varchar(50),
    raw_text text,
    FOREIGN KEY(codename) REFERENCES category(codename)
);
insert into category(codename, aliases, is_expense)
values
    ('food', 'meal, еда, продукты', true),
    ('transport', 'bus, транспорт', true),
    ('pharmacy', 'аптека, лекарства', true),
    ('mobile', 'связь, phone, телефон', true),
    ('internet', 'инет, inet, hosting, server', true),
    ('barber', 'hair, стрижка, барбер', true),
    ('lunch', 'ланч, столовая, ресторан, кафе, cafe', true),
    ('cab', 'такси, taxi', true),
    ('relax', 'прогулка, свидание', true),
    ('clothes', 'шмот, одежда', true),
    ('gift', 'prize, подарки', true),
    ('car', 'машина, авто, auto', true),
    ('housing', 'home, дом, жилье', true),
    ('household', 'быт, уклад, life', true),
    ('electronics', 'technics', true),
    ('subscription', 'подписка, sub', true),
    ('other', 'прочее, другое', true),
    ('salary', 'зп', false),
    ('business', 'dividends, extra', false),
    ('savings', 'подушка, save', true);
create or replace function get_statistics_by_category(period_ varchar default 'month')
	returns table(codename varchar, is_expense boolean, sum_ numeric)
	as
\$\$
	select r.codename, is_expense, sum(amount) as sum_ from record r
		join category c on r.codename = c.codename
		where created >= date_trunc(period_, now())
		group by r.codename, is_expense order by sum_ desc;
\$\$ language sql;
EOF
