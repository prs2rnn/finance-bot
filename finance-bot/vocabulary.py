from datetime import datetime
from zoneinfo import ZoneInfo

VOCABULARY = {
    "notify_week": f"<b>{datetime.now(ZoneInfo('Europe/Moscow')).strftime('%W')} "
                   "week backup and statistics "
                   "here</b>\n\nExpenses: {expenses}₽\nIncomes\t{incomes}₽\n"
                   "Savings\t{savings}₽ from planned {plan_savings}₽",
    "backup_error": "Backup file is more than 20MB",
    "start": "<b>Bot for financial accounting</b>\n\n"
             "Add record: 250 cab\n"
             "Categories: /categories\n"
             "Current month: /month\n"
             "Last records: /records",
    "categories": "{content}\n\nAdd record: 250 cab\nLast records: /records"
                  "\nCurrent month: /month"
                  "\n\n<b>Warning</b>: savings are added manually and not included "
                  "in expenses when calculating. Planned savings - 15%",
    "content": "{content}\n\nAdd record: 250 cab\nCategories: /categories"
               "\nCurrent month: /month",
    "delete_false": "<b>No record found</b>\n\nLast records: /records",
    "delete_true": "<b>Delete record</b>\n\nAdd record: 250 cab\nLast records: /records\n"
                   "Current month: /month",
    "other": "<b>Not recognized</b>\n\nTo add record: 250 cab\nOr use /help for help",
    "month": f"<b>Month statistics for {datetime.now(ZoneInfo('Europe/Moscow')).strftime('%B')}</b>\n\n"
             "Expenses\t{expenses}₽\nIncomes\t{incomes}₽\n"
             "Savings\t{savings}₽ from planned {plan_savings}₽"
             "\n\nAdd record: 250 cab\nCategories: /categories\nLast records: /records",
    "records": "{content}\n\nAdd record: 250 cab\nCategories: /categories"
               "\nCurrent month: /month",
    "add_record": "<b>Add new record</b>: {amount}₽ for {codename}\n\n"
                  "Today statistics:\nExpenses\t{expenses}₽\nIncomes\t"
                  "{incomes}₽\nSavings\t{savings}₽ from planned "
                  "{plan_savings}₽\n\n"
                  "Current month: /month\nLast records: /records\nCategories: /categories",
    "db_records_false": "No records found",
    "db_records_true": "<b>List of last records</b>\n\n{records}",
    "db_records": "• {amount}₽ for {codename} at {created}. Press /del{id_} to delete",
    "db_categories": "<b>List of expense category</b>\n{expenses}\n\n<b>"
                     "List of income category</b>\n{incomes}",
    "db_category": "• {codename} ({aliases})",
    "deny": "Access denied!"
}

SQL_STATISTICS_CUR = """
select expenses, incomes, savings, incomes * 0.15 as planned_savings from
(select extract({period} from created) as {period}_, sum(amount) as savings from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now()) and r.codename = 'savings'
	group by {period}_) as savings
full join
(select extract({period} from created) as {period}_, sum(amount) as incomes from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now())
	and is_expense = false
	group by {period}_) as planned_savings
using({period}_)
full join
(select extract({period} from created) as {period}_, sum(amount) as expenses from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now()) and is_expense = true
	and r.codename <> 'savings'
	group by {period}_) as expenses
using({period}_);
"""


SQL_STATISTICS_PREV = """
select incomes, savings, incomes * 0.15 as planned_savings from
(select extract({period} from created) as {period}_, sum(amount) as savings from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now()) - interval '1 {period}'
    and created < date_trunc('{period}', now())
    and r.codename = 'savings'
	group by {period}_) as savings
full join
(select extract({period} from created) as {period}_, sum(amount) as incomes from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now()) - interval '1 {period}'
    and created < date_trunc('{period}', now())
	and is_expense = false
	group by {period}_) as planned_savings
using({period}_)
full join
(select extract({period} from created) as {period}_, sum(amount) as expenses from record r
	join category c on r.codename = c.codename
	where created >= date_trunc('{period}', now()) - interval '1 {period}'
    and created < date_trunc('{period}', now())
    and is_expense = true and r.codename <> 'savings'
	group by {period}_) as expenses
using({period}_);
"""
