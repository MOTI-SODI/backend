from dotenv import load_dotenv
import datetime
import jwt
import os

load_dotenv(dotenv_path="./config/.env")

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

def create_tokens(email):
    kst_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

    access_payload = {
        "email": email,
        'iat': kst_now,
        'exp': kst_now + datetime.timedelta(minutes=30),
    }
    refresh_payload = {
        "email": email,
        'iat': kst_now,
        'exp': kst_now + datetime.timedelta(days=7),
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS512")
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS512")

    return access_token, refresh_token

def verify_access_token(token, requested_email):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS512"])
        token_email = decoded.get("email")
        exp = decoded.get("exp")

        if not token_email:
            return {"valid": False, "msg": "Invalid token payload"}
        
        if token_email != requested_email:
            return {"valid": False, "msg": "Email does not match the token"}

        kst_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        exp_time = datetime.datetime.fromtimestamp(exp, tz=datetime.timezone(datetime.timedelta(hours=9)))  # KST로 처리

        if exp_time < kst_now:
            return {"valid": False, "msg": "Token has expired"}
        
        return {"valid": True, "email": token_email}

    except jwt.ExpiredSignatureError:
        return {"valid": False, "msg": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "msg": "Invalid token"}

def refresh_access_token(refresh_token):
    try:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS512"])
        email = decoded.get("email")
        exp = decoded.get("exp")

        if not email:
            return {"success": False, "msg": "Invalid refresh token payload"}
        
        kst_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        if datetime.datetime.fromtimestamp(exp, datetime.timezone.utc) < kst_now:
            return {"success": False, "msg": "Refresh token has expired"}

        tokens = create_tokens(email)
        new_access_token = tokens[0]
        return {"success": True, "new_access_token": new_access_token}

    except jwt.ExpiredSignatureError:
        return {"success": False, "msg": "Refresh token has expired"}
    except jwt.InvalidTokenError:
        return {"success": False, "msg": "Invalid refresh token"}
