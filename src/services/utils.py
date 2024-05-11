from datetime import datetime, timedelta
import calendar


def generate_date_range(date: datetime, end_date: datetime, group_type: str):
    match group_type:
        case 'month':
            if date.day != datetime.min.day:
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)
                days = calendar.monthrange(date.year, date.month)[1]
                date += timedelta(days=days - date.day)
            while date <= end_date:
                yield date
                days = calendar.monthrange(date.year, date.month)[1]
                date += timedelta(days=days)
        case 'week':
            delta = timedelta(days=7)
            if date.weekday() != datetime.min.weekday():
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)
                date += timedelta(days=7 - date.weekday())
            while date <= end_date:
                yield date
                date += delta
        case 'day':
            delta = timedelta(days=1)
            if date.time() != datetime.min.time():
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)
                date += delta
            while date <= end_date:
                yield date
                date += delta
        case 'hour':
            delta = timedelta(hours=1)
            if date.minute != datetime.min.minute or date.second != datetime.min.second or date.microsecond != datetime.min.microsecond:
                date = date.replace(minute=0, second=0, microsecond=0)
                date += delta
            while date <= end_date:
                yield date
                date += delta