VOCABULARY = {
    "notify_week": "<b>Weekly backup and statistics here</b>\n\nExpenses: "
                   "{expenses}₽\nIncomes\t{incomes}₽\n"
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
    "month": "<b>Month statistics</b>\n\nExpenses\t{expenses}₽"
             "\nIncomes\t{incomes}₽\n"
             "Savings\t{savings}₽ from planned {plan_savings}₽"
             "\n\nAdd record: 250 bus\nCategories: /categories\nLast records: /records",
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
}