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

_LIST_FUNC_SQL_COMMANDS_CREATE_TABLE = []


def sql_command_create_table(func):
    _LIST_FUNC_SQL_COMMANDS_CREATE_TABLE.append(func)
    def wrapper(*args):
        return func(*args)

    return wrapper





@sql_command_create_table
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


@sql_command_create_table
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

@sql_command_create_table
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


@sql_command_create_table
def create_table_order():
    """
        Create table for reserve time and payment
    """
    sql = """
                CREATE TABLE IF NOT EXISTS `order`(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL ,
                phone VARCHAR (20) NOT NULL ,
                date_submit DATETIME NOT NULL ,
                datetime_reserve DATETIME NOT NULL ,
                price_pay DECIMAL NOT NULL ,
                day_id INTEGER NOT NULL,
                time_id INTEGER NOT NULL,
                FOREIGN KEY (day_id) REFERENCES day(id),
                FOREIGN KEY (time_id) REFERENCES time(id)
            );
        """
    return sql


@sql_command_create_table
def create_table_contactus():
    """
        Create table for reserve time and payment
    """
    sql = """
                CREATE TABLE IF NOT EXISTS contact_us(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL ,
                phone VARCHAR (20) NOT NULL ,
                message TEXT NOT NULL 
            );
        """
    return sql


def _migrate():
    conn = create_connection()
    cursor = conn.cursor()
    for handler_sql in _LIST_FUNC_SQL_COMMANDS_CREATE_TABLE:
        sql = handler_sql()
        cursor.execute(sql)
    conn.commit()
    close_connection(conn)
    print('----------- Migrate Successfully ------------')



class Time:
    def __init__(self,data):
        data = self._convert_data_tuple_to_dict(data)
        self.id = data.get('id')
        self.day = data.get('day')
        self.time_start = data.get('time_start')
        self.time_end = data.get('time_end')
        self.price = data.get('price')
        self.available = data.get('available')


    def __repr__(self):
        return 'time_obj'

    def _convert_data_tuple_to_dict(self,data):
        available = True if data[5] == None else False
        return {
            'day':data[0],
            'id':data[1],
            'time_start':data[2],
            'time_end':data[3],
            'price':data[4],
            'available':available,
        }

    @classmethod
    def get(cls,time_id,day_id):
        today_time = datetime.datetime.now()
        datetime_range = (
            today_time,
            today_time + datetime.timedelta(weeks=1)
        )
        sql = f"""
                SELECT day.day , time.*, `order`.id
                FROM day
                INNER JOIN day_time
                    ON day.id = day_time.day_id AND time.id = day_time.time_id
                INNER JOIN time
                    ON time.id = '{time_id}'
                LEFT JOIN `order`
                    ON `order`.day_id = day_time.day_id AND `order`.time_id = day_time.time_id  AND `order`.datetime_reserve <= '{datetime_range[1]}'
                WHERE day.id = '{day_id}'
        """
        conn = create_connection()
        cursor = conn.cursor()
        time = cursor.execute(sql).fetchone()
        time_obj = None
        if time:
            time_obj = Time(time)
        close_connection(conn)
        return time_obj

    def reserve_time(self,name,phone,day_id):
        today_time = datetime.datetime.now()
        days_delta = self.day - config.CONVERT_DAY_TO_DAY_PERSIAN(today_time.isoweekday())
        if days_delta < 1:
            days_delta += 7
        datetime_reserve = (today_time + datetime.timedelta(days=days_delta)).strftime('%Y-%m-%d')

        sql = f"""
                INSERT INTO `order` (`name`,phone,date_submit,datetime_reserve,price_pay,day_id,time_id)
                VALUES (
                    '{name}',
                    '{phone}',
                    '{today_time}',
                    '{datetime_reserve}',
                    '{self.price}',
                    '{day_id}',
                    '{self.id}'
                );       
        """
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        close_connection(conn)
        return 200

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
        today_time = datetime.datetime.now()
        results = []
        sql = f"""
                SELECT day.day , time.*, `order`.id 
                FROM day
                INNER JOIN day_time 
                    ON day.id = day_time.day_id
                INNER JOIN time
                    ON time.id = day_time.time_id
                LEFT JOIN `order`
                    ON `order`.day_id = day_time.day_id AND `order`.time_id = day_time.time_id AND `order`.datetime_reserve > '{today_time}'
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



class ContactUs:

    @classmethod
    def add(self,name,phone,message):
        sql = f"""
              INSERT INTO contact_us (name,phone,message)
              VALUES(
                    '{name}',
                    '{phone}',
                    '{message}'
              );    
              """
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        close_connection(conn)
        return 200