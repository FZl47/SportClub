import sqlite3

_db_path = 'db.sqlite'

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
    _LIST_FUNC_SQL_COMMANDS.append(func)
    def wrapper(*args):
        return func(*args)
    return wrapper

@sql_command
def create_table_info():
    sql = """
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            about_us TEXT,
            emails TEXT,
            phones TEXT
        );
    """
    return sql


@sql_command
def create_table_time_available():
    sql = """
        CREATE TABLE IF NOT EXISTS time_available (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time_start time NOT NULL,
            time_end time NOT NULL
        );
    """
    return sql


# Get Data Records
def get_data_info():
    sql = """
        SELECT * FROM info;
    """
    conn = create_connection()
    curs = conn.cursor()
    data = curs.execute(sql).fetchone()
    close_connection(conn)
    return data




def _migrate():
    conn = create_connection()
    cursor = conn.cursor()
    for handler_sql in _LIST_FUNC_SQL_COMMANDS:
        sql = handler_sql()
        cursor.execute(sql)
    conn.commit()
    close_connection(conn)
    print('----------- Migrate Successfully ------------')




