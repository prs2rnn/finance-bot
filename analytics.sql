-- returns summary statistics for current specified period: year, month ...
-- or none
create or replace function get_statistics(period_ varchar default 'month')
	returns table(expenses numeric, incomes numeric, savings numeric, planned_savings numeric)
	as
$$
	select coalesce(expenses, 0) as expenses, coalesce(incomes, 0) as incomes,
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
select * from get_statistics('day');

-- returns stitstics by all categories in specified period: week, day, month, year
-- or none, i.e. 0 rows
create or replace function get_statistics_by_category(period_ varchar default 'month')
	returns table(codename varchar, sum_ numeric)
	as
$$
	select r.codename, sum(amount) as sum_ from record r
		join category c on r.codename = c.codename
		where created >= date_trunc(period_, now())
		group by r.codename order by sum_ desc;
$$ language sql;
select * from get_expenses_by_category('week');

-----------------------------------------------------------------------------------------

-- all month categories
select codename, coalesce(sum_, 0) as sum_ from category left join
(select codename, sum(amount) as sum_ from record r
	where created >= date_trunc('month', now())
	group by codename) as cat
using(codename) order by sum_ desc;

-- prev month
select codename, (case when sum_ is not null then sum_ else 0 end) as month_ from category left join
(select codename, sum(amount) as sum_ from record r
	where created >= date_trunc('month', now()) - interval '1 month'
	and created < date_trunc('month', now())
	group by codename) as cat
using(codename) order by month_ desc;

-- year by month group stat
select month_, expenses, incomes, savings, incomes * 0.15 as planned_savings from
(select month_, expenses from
	(select to_char(date_trunc('month', created), 'month') as month_, sum(amount) as expenses,
		date_trunc('month', created) as sorted_col
		from record r
		join category c using(codename)
		where extract(year from created) = extract(year from now()) and c.is_expense = true
		and r.codename <> 'savings'
		group by month_, sorted_col order by sorted_col) as total) as expenses
full join
(select month_, incomes from
	(select to_char(date_trunc('month', created), 'month') as month_, sum(amount) as incomes,
		date_trunc('month', created) as sorted_col
		from record r
		join category c using(codename)
		where extract(year from created) = extract(year from now()) and c.is_expense = false
		group by month_, sorted_col order by sorted_col) as total) as incomes
using(month_)
full join
(select month_, savings from
	(select to_char(date_trunc('month', created), 'month') as month_, sum(amount) as savings,
		date_trunc('month', created) as sorted_col
		from record r
		join category c using(codename)
		where extract(year from created) = extract(year from now()) and r.codename = 'savings'
		group by month_, sorted_col order by sorted_col) as total) as savings
using(month_);

-- dynamic get_statistics old
select week_, expenses, incomes, savings, incomes * 0.15 as planned_savings from
(select extract(week from created) as week_, sum(amount) as savings from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('week', now()) - interval '1 week'
    and created < date_trunc('week', now())
    and r.codename = 'savings'
	group by week_) as savings
full join
(select extract(week from created) as week_, sum(amount) as incomes from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('week', now()) - interval '1 week'
    and created < date_trunc('week', now())
	and is_expense = false
	group by week_) as planned_savings
using(week_)
full join
(select extract(week from created) as week_, sum(amount) as expenses from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('week', now()) - interval '1 week'
    and created < date_trunc('week', now())
    and is_expense = true and r.codename <> 'savings'
	group by week_) as expenses
using(week_);
