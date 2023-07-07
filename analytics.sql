create or replace function get_statistics_by_category(period_ varchar default 'month')
	returns table(codename varchar, is_expense boolean, sum_ numeric)
	as
$$
	select r.codename, is_expense, sum(amount) as sum_ from record r
		join category c on r.codename = c.codename
		where created >= date_trunc(period_, now())
		group by r.codename, is_expense order by sum_ desc;
$$ language sql;

create or replace function get_statistics(period_ varchar default 'month')
	returns table(period_ varchar, expenses numeric, incomes numeric,
                savings numeric, planned_savings numeric)
	as
$$
	select period_, coalesce(expenses, 0) as expenses, coalesce(incomes, 0) as incomes,
		   coalesce(savings, 0) as savings, coalesce(incomes * 0.15, 0) as planned_savings from
		(select to_char(created, period_) as period_, sum(amount) as savings from record r
			join category c on r.codename = c.codename
			where created >= date_trunc(period_, now()) and r.codename = 'savings'
			group by period_
		) as savings
	full join
		(select to_char(created, period_) as period_, sum(amount) as incomes from record r
			join category c on r.codename = c.codename
			where created >= date_trunc(period_, now())
			and is_expense = false
			group by period_
		) as incomes
	using(period_)
	full join
		(select to_char(created, period_) as period_, sum(amount) as expenses from record r
			join category c on r.codename = c.codename
			where created > date_trunc(period_, now()) and is_expense = true
			and r.codename <> 'savings'
			group by period_
		) as expenses
	using(period_);
$$ language sql;

create function get_dynamic_statistics(year_ integer default date_part('year', now()), period_ varchar default 'month')
	returns table(period_ integer, year_ integer, expenses numeric, incomes numeric, savings numeric, planned_savings numeric)
	as
$$
	select period_, year_, expenses, incomes, savings, incomes * 0.15 as planned_savings from
	(select date_part(period_, created) as period_, year_, sum(amount) as expenses
		   from record r join category c using (codename)
		where date_part('year', created) = year_
		and is_expense = true and codename <> 'savings'
		group by period_ order by period_
	) as expenses
	full join
	(select date_part(period_, created) as period_, year_, sum(amount) as incomes
		   from record r join category c using (codename)
		where date_part('year', created) = year_  and is_expense = false
		group by period_ order by period_
	) as incomes
	using (period_, year_)
	full join
	(select date_part(period_, created) as period_, year_, sum(amount) as savings
			from record r join category c using (codename)
		where date_part('year', created) = year_  and codename = 'savings'
		group by period_ order by period_
	) as savings
	using (period_, year_);
$$ language sql;

create or replace function compare_cur_prev_by_categories
	(year_ int default date_part('year', now()), period__ varchar default 'month')
	returns table (codename_ varchar, prev numeric, cur numeric)
	as
$$
begin
	return query
	with cur_prev as
		(select * from get_categories_dynamic_statistics(year_, period__)
			where period_ = date_part(period__, now())
			or period_ = date_part(period__, now()) - 1 order by period_)
	select codename, coalesce(prev.sum_, 0) as prev, coalesce(cur.sum_, 0) as cur from
		(select * from cur_prev where period_ = (select min(period_) from cur_prev)) as prev
	full join
		(select * from cur_prev where period_ = (select max(period_) from cur_prev)) as cur
	using(codename);
end;
$$ language plpgsql;

----------------------------------------------------------------------------------

-- 1
/*
PARAMS: year, period_: 'month', 'week', 'day', 'quarter'
OUT:
period_|year_|expenses |incomes |savings|planned_savings|
-------+-----+---------+--------+-------+---------------+
      1| 2023|34300.000|        |       |               |
*/
select * from get_dynamic_statistics();

-- 2
/*
OUT:
period_|year_|codename |sum_     |
-------+-----+---------+---------+
      1| 2023|barber   |  450.000|
      2| 2023|barber   |  450.000|
      1| 2023|business | 9390.000|
*/
select * from get_categories_dynamic_statistics();

-- 3
/*
OUT:
codename_|prev    |cur     |
---------+--------+--------+
mobile   | 300.000|       0|
other    | 370.000|       0|
pharmacy |2080.000|1400.000|
*/
select * from compare_cur_prev_by_categories(2023, 'month');
