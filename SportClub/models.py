import sqlite3
import config
import datetime

_db_path = 'db.sqlite'


def create_connection():
    conn = sqlite3.connect(_db_path)
    return conn


def close_connection(conn):
    try:
        conn.close()
    except:
        pass


# Create Tables

_LIST_FUNC_SQL_COMMANDS = []


def sql_command(func):
    _LIST_FUNC_SQL_COMMANDS.append(func)

    def wrapper(*args):
        return func(*args)

    return wrapper


# @sql_command
# def create_table_info():
#     sql = """
#         CREATE TABLE IF NOT EXISTS info (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             about_us TEXT,
#             emails TEXT,
#             phones TEXT
#         );
#     """
#     return sql


@sql_command
def create_table_times():
    sql = """
        CREATE TABLE IF NOT EXISTS time(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time_start time NOT NULL,
            time_end time NOT NULL,
            price DECIMAL NOT NULL
        );
    """
    return sql


@sql_command
def create_table_days():
    """
        day is day number like (
            1 : Saturday
            2 : Sunday
            3 : Monday
            4 : Tuesday
            5 : Wednesday
            6 : Thursday
            7 : Friday
        )
    """
    sql = """
        CREATE TABLE IF NOT EXISTS day(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL
        );        
    """
    return sql

@sql_command
def create_table_day_times_ManyToMany():
    """
        ManyToMany
        every day can have multi time for reserve
    """
    sql = """
            CREATE TABLE IF NOT EXISTS day_time(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            day_id INTEGER NOT NULL,
            time_id INTEGER NOT NULL,
            FOREIGN KEY (day_id) REFERENCES day(id),
            FOREIGN KEY (time_id) REFERENCES time(id)
        );
    """
    return sql



def _migrate():
    conn = create_connection()
    cursor = conn.cursor()
    for handler_sql in _LIST_FUNC_SQL_COMMANDS:
        sql = handler_sql()
        cursor.execute(sql)
    conn.commit()
    close_connection(conn)
    print('----------- Migrate Successfully ------------')






def test_get():


    sql = """
            SELECT day.day, time.*
            FROM day
            INNER JOIN day_time 
                ON day.id = day_time.day_id
            INNER JOIN time
                ON time.id = day_time.time_id
  
    """
    conn = create_connection()
    cursor = conn.cursor()
    data = cursor.execute(sql).fetchall()
    print(data)
    close_connection(conn)


class Time:
    def __init__(self,data):
        data = self._convert_data_tuple_to_dict(data)
        self.id = data.get('id')
        self.time_start = data.get('time_start')
        self.time_end = data.get('time_end')
        self.price = data.get('price')

    def __repr__(self):
        return 'time_obj'

    def _convert_data_tuple_to_dict(self,data):
        return {
            'day':data[0],
            'id':data[1],
            'time_start':data[2],
            'time_end':data[3],
            'price':data[4],
        }

class Day:


    def __init__(self,data):
        data = self._convert_data_tuple_to_dict(data)
        self.id = data.get('id')
        self.day = data.get('day')

    def __repr__(self):
        return 'day_obj'

    @classmethod
    def all(cls):
        """
            get all record table "day"
        :return => list days object => [day_obj,day_obj,...]
        """
        results = []
        sql = f"""
                SELECT * FROM day
        """
        conn = create_connection()
        cursor = conn.cursor()
        days_data = cursor.execute(sql).fetchall()
        for day in days_data:
            results.append(Day(day))
        close_connection(conn)

        return results


    def _convert_data_tuple_to_dict(self,data):
        return {
            'id':data[0],
            'day':data[1]
        }

    def get_times(self):
        """
            get all record table "time"
            :return => list times object => [time_obj,time_obj,...]
          """
        results = []
        sql = f"""
                SELECT day.day , time.*
                FROM day
                INNER JOIN day_time 
                    ON day.id = day_time.day_id
                INNER JOIN time
                    ON time.id = day_time.time_id
                WHERE day.id = '{self.id}'
        """
        conn = create_connection()
        cursor = conn.cursor()
        times_data = cursor.execute(sql).fetchall()
        for time in times_data:
            results.append(Time(time))
        close_connection(conn)
        return results

    def get_day_name(self):
        return config.WEEKDAYS.get(self.day)

    def is_today(self):
        today_num = datetime.datetime.now().isoweekday()
        today_num = config.CONVERT_DAY_TO_DAY_PERSIAN(today_num)
        if today_num  == self.day:
            return True
        return False