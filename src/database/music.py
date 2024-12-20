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

def create_music(user_id, artist, song_title, thumbnail, music_url, date):
    create_message = f"INSERT INTO {MYSQL_DBNAME}.musics (user_id, artist, song_title, thumbnail, music_url, date) VALUES (%s, %s, %s, %s, %s, %s)"
    setting_db(create_message, params=(user_id, artist, song_title, thumbnail, music_url, date))
    
    return True

def select_music(user_id, date):
    select_message = f"SELECT * FROM {MYSQL_DBNAME}.musics WHERE user_id = %s AND date = %s"
    result = setting_db(select_message, params=(user_id, date), fetch=True)
    
    if result:
        return result
    else:
        return None