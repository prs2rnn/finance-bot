select * from record r;
select * from category c ;

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

-- month category expenses
select r.codename, sum(amount) as expenses from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('month', now())
	and is_expense = true and r.codename <> 'savings'
	group by r.codename order by expenses desc;

-- month category incomes
select r.codename, sum(amount) as incomes from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('month', now()) and is_expense = false
	group by r.codename order by incomes desc;

-- month category incomes, savings and planned
select incomes, savings, incomes * 0.15 as planned_savings from
(select to_char(created, 'month') as month_, sum(amount) as savings from record r
	join category c on r.codename = c.codename
	where created > date_trunc('month', now()) and r.codename = 'savings'
	group by month_) as savings
full join
(select to_char(created, 'month') as month_, sum(amount) as incomes from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('month', now())
	and is_expense = false
	group by month_) as planned_savings
on savings.month_ = planned_savings.month_;
