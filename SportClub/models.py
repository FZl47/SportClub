import sqlite3

_db_path = 'database.sqlite3'

def create_connection():
    conn = sqlite3.connect(_db_path)
    return conn

def close_connection(conn):
    try:
        conn.close()
    except:pass


# Create Tables

_LIST_FUNC_SQL_COMMANDS = []
def sql_command(func):
    def wrapper(*args):
        _LIST_FUNC_SQL_COMMANDS.append(func)
        return func(*args)
    return wrapper

@sql_command
def create_table_info(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            about_us TEXT,
            emails TEXT,
            phones TEXT
        )
    """
    return sql


@sql_command
def create_table_time_available(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS time_available(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time_start time NOT NULL,
            time_end time NOT NULL,
        )
    """
    return sql



def get_data_info():
    sql = """
        SELECT * FROM info
    """ 
    conn = create_connection()
    curs = conn.cursor()
    data = curs.execute(sql)
    data = data.fetchone() 
    close_connection(conn)
    return data

get_data_info()



def _migrate():
    conn = create_connection()
    for handler_sql in _LIST_FUNC_SQL_COMMANDS:
        sql = handler_sql()
        cursor = conn.cursor()
        cursor.execute(sql)
    conn.commit()
    close_connection(conn)
    print('----------- Migrate Successfully ------------')




def test():
    sql = """
        SELECT * FROM info
    """
    conn = create_connection()
    curs = conn.cursor()
    x = curs.execute(sql).fetchone()
    print(x)

