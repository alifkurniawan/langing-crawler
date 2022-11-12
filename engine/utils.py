from datetime import datetime, timedelta


def get_now():
    return str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


def get_time_minutes_ago(minutes: int):
    return (datetime.now() - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
