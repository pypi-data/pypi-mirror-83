import datetime

def get_date(date=None):
    date = date or datetime.datetime.now()
    return date.strftime('%Y-%m-%d')


def get_current_time(date=None):
    date = date or datetime.datetime.now()
    return date.strftime('%H:%M:%S')


def get_datetime(date=None):
    date = date or datetime.datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')

def get_yesterday():
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def get_tomorrow():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
