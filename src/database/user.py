from dotenv import load_dotenv
import pymysql
import logging
import hashlib
import base64
import os

import utils.token.token as token

load_dotenv(dotenv_path="./config/.env")

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_DBNAME = os.environ.get('MYSQL_DBNAME')

def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()
    return base64.b64encode(salt + hashed_password.encode('utf-8')).decode('utf-8')

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

def setting_db(message, params=False, fetch=False):
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


def add_user(email, name, password, birth_date, phone_address, gender, job,):
    create_message = f"INSERT INTO {MYSQL_DBNAME}.users (email, name, password, birth_date, phone_address, gender, job) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    select_message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    
    existing_user = setting_db(select_message, params=(email,), fetch=True)
    if existing_user:
        return False
    
    password = hash_password(password)
    setting_db(create_message, params=(email, name, password, birth_date, phone_address, gender, job))
    
    return True


def login_user(email, password):
    select_message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(select_message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][3]
        status = result[0][8]
        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            access_token, refresh_token = token.create_tokens(email)
            if access_token and refresh_token:
                return access_token, refresh_token, status
            else:
                return False, False
        else:
            return False, False
    else:
        return False, False

def change_password(email, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        return False

    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][3]

        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + current_password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            new_hashed_password = hash_password(new_password)
            update_message = f"UPDATE {MYSQL_DBNAME}.users SET password = %s WHERE email = %s"
            setting_db(update_message, params=(new_hashed_password, email))

            return True
        else:
            return False
    else:
        return False

def change_name(email, password, name):
    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][3]

        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            update_message = f"UPDATE {MYSQL_DBNAME}.users SET name = %s WHERE email = %s"
            setting_db(update_message, params=(name, email))

            return True
        else:
            return False
    else:
        return False

def change_gender(email, password, gender):
    if gender not in ("F", "M"):
        return False

    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][3]

        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            update_message = f"UPDATE {MYSQL_DBNAME}.users SET gender = %s WHERE email = %s"
            setting_db(update_message, params=(gender, email))

            return True
        else:
            return False
    else:
        return False
    
def change_job(email, password, job):
    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][3]

        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            update_message = f"UPDATE {MYSQL_DBNAME}.users SET job = %s WHERE email = %s"
            setting_db(update_message, params=(job, email))

            return True
        else:
            return False
    else:
        return False
    
def select_user_email(user_id):
    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE user_id = %s"
    result = setting_db(message, params=(user_id), fetch=True)

    return result[0][1]