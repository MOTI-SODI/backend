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

def select_note_by_date(user_id, date):
    select_message = f"SELECT * FROM {MYSQL_DBNAME}.notes WHERE user_id = %s AND date = %s"
    result = setting_db(select_message, params=(user_id, date), fetch=True)

    if result:
        return result
    else:
        return None

def create_note(user_id, title, content, mood, date):
    create_message = f"INSERT INTO {MYSQL_DBNAME}.notes (user_id, title, content, mood, date) VALUES (%s, %s, %s, %s, %s)"
    setting_db(create_message, params=(user_id, title, content, mood, date))
    
    return True

def modify_note(user_id, title, content, mood, date):
    modify_message = f"UPDATE {MYSQL_DBNAME}.notes SET title = %s, content = %s, mood = %s WHERE user_id = %s AND date = %s"
    setting_db(modify_message, params=(title, content, mood, user_id, date))
    
    return {"msg": "Note modified successfully"}

def select_note(user_id, date):
    select_message = f"SELECT * FROM {MYSQL_DBNAME}.notes WHERE user_id = %s AND date = %s"
    result = setting_db(select_message, params=(user_id, date), fetch=True)
    
    if result:
        return result
    else:
        return None