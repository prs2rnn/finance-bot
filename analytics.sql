/*
returns stitstics by all categories in specified period: week, day, month, year
or none, i.e. 0 rows
*/
create or replace function get_statistics_by_category(period_ varchar default 'month')
	returns table(codename varchar, is_expense boolean, sum_ numeric)
	as
$$
	select r.codename, is_expense, sum(amount) as sum_ from record r
		join category c on r.codename = c.codename
		where created >= date_trunc(period_, now())
		group by r.codename, is_expense order by sum_ desc;
$$ language sql;

/*
returns summary statistics for current specified period: year, month ...
or none
*/
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

----------------------------------------------------------------------------------

-- 1
/*
PARAMS: year, period_: 'month', 'week', 'day'
OUT:
period_|year_|expenses |incomes |savings|planned_savings|
-------+-----+---------+--------+-------+---------------+
      1| 2023|34300.000|        |       |               |
*/
select * from get_dynamic_statistics();

-- 2
