from dotenv import load_dotenv
import pymysql
import logging
import os

load_dotenv(dotenv_path="./config/.env")

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_DBNAME = os.environ.get('MYSQL_DBNAME')

def get_db_connection():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=MYSQL_DBNAME,
        charset='utf8mb4'
    )
    return conn

def setting_db(message, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(message, params)
        else:
            cursor.execute(message)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_note(title, content, mood, year, month, day):
    message = f"INSERT INTO {MYSQL_DBNAME}.notes (title, content, mood, year, month, day) VALUES (%s, %s, %s, %s, %s, %s)"
    setting_db(message, params=(title, content, mood, year, month, day))
    
    return {"msg": "Note created successfully"}

def modify_note(title, content, mood, year, month, day):
    message = f"UPDATE {MYSQL_DBNAME}.notes SET title = %s, content = %s, mood = %s WHERE year = %s AND month = %s AND day = %s"
    setting_db(message, params=(title, content, mood, year, month, day))
    
    return {"msg": "Note modified successfully"}

def select_note(title, year, month, day):
    message = f"SELECT * FROM {MYSQL_DBNAME}.notes WHERE title = %s AND year = %s AND month = %s AND day = %s"
    result = setting_db(message, params=(title, year, month, day), fetch=True)
    
    if result:
        return result
    else:
        return None