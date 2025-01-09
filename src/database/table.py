from dotenv import load_dotenv
import logging
import pymysql
import json
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

def create_database():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            charset='utf8'
        )
        cursor = conn.cursor()
        message = f"CREATE DATABASE IF NOT EXISTS {MYSQL_DBNAME}"
        cursor.execute(message)
        conn.commit()
        logging.info(f"Database {MYSQL_DBNAME} created successfully.")
    except Exception as e:
        logging.error(f"Error occurred while creating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_table():
    create_database()

    user_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        birth_date DATE NOT NULL,
        phone_address VARCHAR(255) NOT NULL,
        gender ENUM('F','M') NOT NULL,
        job VARCHAR(255) NOT NULL,
        status BOOLEAN
    );
    """

    note_table_query = """
    CREATE TABLE IF NOT EXISTS notes (
        note_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        mood VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """

    calendar_table_query = """
    CREATE TABLE IF NOT EXISTS calendar (
        calendar_id INT AUTO_INCREMENT PRIMARY KEY ,
        user_id INT NOT NULL,
        note_id INT,
        date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (note_id) REFERENCES notes(note_id) ON DELETE SET NULL
    );
    """

    music_table_query = """
    CREATE TABLE IF NOT EXISTS musics (
        music_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        thumbnail VARCHAR(255) NOT NULL,
        song_title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        music_url VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """

    inspection_table_query = """
    CREATE TABLE IF NOT EXISTS inspections (
        inspection_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        emotionality INT NOT NULL,
        extraversion INT NOT NULL,
        agreeableness INT NOT NULL,
        honesty INT NOT NULL,
        conscientiousness INT NOT NULL,
        open INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """

    mission_table_query = """
    CREATE TABLE IF NOT EXISTS missions (
        mission_id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(255) NOT NULL,
        content TEXT NOT NULL
    );
    """
    setting_db(user_table_query)
    setting_db(note_table_query)
    setting_db(calendar_table_query)
    setting_db(music_table_query)
    setting_db(inspection_table_query)
    setting_db(mission_table_query)

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
            check_query = f"SELECT COUNT(*) FROM {MYSQL_DBNAME}.missions WHERE category = %s AND content = %s"
            result = setting_db(check_query, params=(category, content), fetch=True)
            if result and result[0][0] == 0:
                insert_query = f"INSERT INTO {MYSQL_DBNAME}.missions (category, content) VALUES (%s, %s)"
                setting_db(insert_query, params=(category, content))
