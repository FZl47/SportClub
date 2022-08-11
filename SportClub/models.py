import sqlite3

_db_path = 'SportClub/database.db'

def create_connection():
    conn = sqlite3.connect(_db_path)
    return conn

def close_connection(conn):
    try:
        conn.close()
    except:pass


# Create Tables

