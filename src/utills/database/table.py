from dotenv import load_dotenv
import pymysql
import os
import json
import logging

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
        charset='utf8'
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

def create_table():
    user_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        email VARCHAR(255) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """

    mission_table_query = """
    CREATE TABLE IF NOT EXISTS missions (
        id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        category VARCHAR(255) NOT NULL,
        content VARCHAR(255) NOT NULL
    );
    """

    music_table_query = """
    CREATE TABLE IF NOT EXISTS music (
        id VARCHAR(255) NOT NULL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL
    );
    """

    setting_db(user_table_query)
    setting_db(mission_table_query)
    setting_db(music_table_query)
    insert_missions()

def insert_missions():
    try:
        with open("./config/mission.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("Mission file not found at mission.json")
        return
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from mission file.")
        return

    for category, contents in data.items():
        for content in contents:
            message = f"INSERT INTO {MYSQL_DBNAME}.missions (category, content) VALUES (%s, %s)"
            setting_db(message, params=(category, content))
