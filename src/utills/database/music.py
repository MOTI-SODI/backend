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
    finally:
        cursor.close()
        conn.close()

def create_music(thumbnail, song_title, artist, year, month, day):
    message = f"INSERT INTO {MYSQL_DBNAME}.musics (thumbnail, song_title, artist, year, month, day) VALUES (%s, %s, %s, %s, %s, %s)"
    setting_db(message, params=(thumbnail, song_title, artist, year, month, day))
    
    return {"msg": "Create Song Successfully"}

def select_music(year, month):
    message = f"SELECT * FROM {MYSQL_DBNAME}.musics WHERE year = %s AND month = %s"
    result = setting_db(message, params=(year, month), fetch=True)

    return result