current_date = datetime.date.now()
days_between_start_date = (current_date.weekday() - 0) % 7
start_date = current_date - datetime.timedelta(days=days_between_start_date)
print(start_date)