
DEBUG = True

DB_PATH = 'db.sqlite'
STATIC_URL = '/static'


# Note! The order should be like thi

WEEKDAYS = {
    1 : 'شنبه',
    2 : 'یکشنبه',
    3 : 'دوشنبه',
    4 : 'سه شنبه',
    5 : 'چهارشنبه',
    6 : 'پنجشنبه',
    7 : 'جمعه',
}

# Conversion of days of the week in Iran
# Weekday 6 == Weekday 1 in iran
# ...
# ...
# ...
# Weekday 1 == Weekday 3 in iran
WEEKDAYS_ORDER_BY_PERSIAN = {
    6 : 1,
    7 : 2,
    1 : 3,
    2 : 4,
    3 : 5,
    4 : 6,
    5 : 7
}

def CONVERT_DAY_TO_DAY_PERSIAN(day):
    return WEEKDAYS_ORDER_BY_PERSIAN.get(day)