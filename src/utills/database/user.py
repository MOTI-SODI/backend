from dotenv import load_dotenv
import pymysql
import logging
import hashlib
import base64
import jwt
import os

import utills.jwt.jwts as jwts

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

def add_user(email, nicname, password):
    message = f"INSERT INTO {MYSQL_DBNAME}.users (email, nicname, password) VALUES (%s, %s, %s)"
    password = hash_password(password)
    setting_db(message, params=(email, nicname, password))
    
    return {"msg": "User added successfully"}

def login_user(email, password):
    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][2]
        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            access_token, refresh_token = jwts.create_tokens(email)
            if access_token and refresh_token:
                return access_token, refresh_token
            else:
                return None, None
        else:
            return None, None
    else:
        return None, None

def change_password(email, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        message = {"msg": "New password and re-entered password do not match"}, 400
        return message

    message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE email = %s"
    result = setting_db(message, params=(email,), fetch=True)

    if result:
        stored_password = result[0][2]

        stored_password_bytes = base64.b64decode(stored_password)
        salt = stored_password_bytes[:16]
        hashed_password = stored_password_bytes[16:].decode('utf-8')

        hashed_input_password = hashlib.sha512(salt + current_password.encode('utf-8')).hexdigest()

        if hashed_password == hashed_input_password:
            new_hashed_password = hash_password(new_password)
            update_message = f"UPDATE {MYSQL_DBNAME}.users SET password = %s WHERE email = %s"
            setting_db(update_message, params=(new_hashed_password, email))

            message = {"msg": "Password changed successfully"}
            return message
        else:
            return None
    else:
        return None
