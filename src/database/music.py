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
    cursor = conn.cursor(pymysql.cursors.DictCursor)
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

def create_music(thumbnail, song_title, artist, date, email):
    message = f"INSERT INTO {MYSQL_DBNAME}.musics (thumbnail, song_title, artist, date, email) VALUES (%s, %s, %s, %s, %s)"
    setting_db(message, params=(thumbnail, song_title, artist, date, email))
    return {"msg": "Create Song Successfully"}

def select_music(email, year, month):
    message = f"SELECT id, thumbnail, song_title, artist, DATE_FORMAT(date, '%Y-%m-%d') as date FROM {MYSQL_DBNAME}.musics WHERE email = %s AND YEAR(date) = %s AND MONTH(date) = %s"
    result = setting_db(message, params=(email, year, month), fetch=True)
    return result
