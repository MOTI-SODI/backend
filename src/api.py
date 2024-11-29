from flask import Flask, request, jsonify, abort
import datetime
import logging
import random
import json

import utills.database.table as table
import utills.database.user as user
import utills.database.music as music
import utills.database.note as note
import utills.database.mission as mission
import utills.song.song as song
import utills.keyword.keyword as keywords
import utills.jwt.jwts as jwts

app = Flask(__name__)

def token_parsing(auth_header, email):
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    result = jwts.verify_access_token(token, email)
    return result

@app.route('/api/user/signup', methods=['POST'])
def add_user():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        if not email:
            return jsonify({"msg": "Email is Required"}), 400
        
        if not name:
            return jsonify({"msg": "Name is Required"}), 400
        
        if not password:
            return jsonify({"msg": "Password is Required"}), 400

        result = user.add_user(email, name, password)

        if not result:
            return jsonify({"msg": "User already exists"}), 400

        return jsonify({"msg": "User Added Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/api/user/signin', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email:
            return jsonify({"msg": "Email is Required"}), 400
        
        if not password:
            return jsonify({"msg": "Password is Required"}), 400

        access_token, refresh_token = user.login_user(email, password)

        if not access_token or not refresh_token:
            return jsonify({"msg": "Invalid credentials"}), 400

        return jsonify({"msg": "User Login Successfully", 'Access_Token': access_token, "Refresh_Token": refresh_token}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500    

@app.route('/api/user/password', methods=['POST'])
def change_password():
    try:
        data = request.json
        email = data.get('email')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not email:
            return jsonify({"msg": "Email is Required"}), 400
        
        if not current_password:
            return jsonify({"msg": "Password is Required"}), 400
        
        if not new_password:
            return jsonify({"msg": "New Password is Required"}), 400
        
        if not confirm_password:
            return jsonify({"msg": "Password Confirmation is Required"}), 400
        
        result = user.change_password(email, current_password, new_password, confirm_password)
        
        if not result:
            return jsonify({"msg": "Invalid credentials"}), 400

        return jsonify({"msg": "Change to Password Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/api/token/refresh', methods=['POST'])
def refresh_tokens():
    data = request.json
    refresh_token = data.get('refresh_token')

    if not refresh_tokens:
        return jsonify({"msg": "Refresh token is Required"}), 400
    
    result = jwts.refresh_access_token(refresh_token)

    if not result["success"]:
        return jsonify({"msg": "Refresh Token is Required"}), 400

    return jsonify({"msg": "Access token refreshed", "Access_Token": result["new_access_token"]}), 200

@app.route('/api/music/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        email = data.get('email')
        content = data.get('content')


        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400

        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not content:
            return jsonify({"msg": "Content is required"}), 400
        
        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400
        
        keyword = keywords.get_completion(content)

        if not keyword:
            return jsonify({"msg": "Keyword is required"}), 400

        result = song.get_music(keyword)

        if not result:
            return jsonify({"msg": "Failed to select music"}), 400

        return jsonify({"msg": "Select music successfully", "data": result}), 200
    except json.JSONDecodeError as e:
        return jsonify({'error': f'JSON parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/api/mission/selectmission', methods=['POST'])
def select_mission():
    try:
        id = random.randint(1, 60)

        result = mission.select_mission(id)

        if not result.get("data"):
            return jsonify({"msg": "No mission found for the specified date"}), 404

        return jsonify({"msg": "Select mission Successfully", "data": result["data"]}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/api/note/createnote', methods=['POST'])
def create_note():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        title = data.get('title')
        content = data.get('content')
        mood = data.get('mood')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400

        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not title:
            return jsonify({"msg": "Title is Required"}), 400
        
        if not content:
            return jsonify({"msg": "Content is Required"}), 400
        
        if not mood:
            return jsonify({"msg": "Mood is Required"}), 400
        
        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400

        result = note.create_note(title, content, mood, year, month, day)

        if result is None:
            return jsonify({"msg": "Failed to create note"}), 400

        if not result:
            return jsonify({"msg": "Failed to create note"}), 400

        return jsonify({"msg": "Create Note Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    
@app.route('/api/note/modifynote', methods=['POST'])
def modify_note():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        title = data.get('title')
        content = data.get('content')
        mood = data.get('mood')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400

        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not title:
            return jsonify({"msg": "Title is Required"}), 400
        
        if not content:
            return jsonify({"msg": "Content is Required"}), 400
        
        if not mood:
            return jsonify({"msg": "Mood is Required"}), 400
        
        if not year:
            return jsonify({"msg": "Year is Required"}), 400
        
        if not month:
            return jsonify({"msg": "Month is Required"}), 400
        
        if not day:
            return jsonify({"msg": "Day is Required"}), 400

        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400

        result = note.modify_note(title, content, mood, year, month, day)

        if not result:
            return jsonify({"msg": "Failed to modify note"}), 400

        return jsonify({"msg": "Modify Note Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/api/note/selectnote', methods=['POST'])
def modify_note():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        title = data.get('title')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400

        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not title:
            return jsonify({"msg": "Title is Required"}), 400
        
        if not year:
            return jsonify({"msg": "Year is Required"}), 400
        
        if not month:
            return jsonify({"msg": "Month is Required"}), 400
        
        if not day:
            return jsonify({"msg": "Day is Required"}), 400

        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400

        result = note.select_note(title, year, month, day)

        if not result:
            return jsonify({"msg": "Failed to select note"}), 400

        return jsonify({"msg": "Modify Note Successfully", "data": result["data"]}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/api/music/createmusic', methods=['POST'])
def add_music():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        thumbnail = data.get('thumbnail')
        song_title = data.get('song_title')
        artist = data.get('artist')
        
        year = datetime.datetime.now().strftime("%y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")

        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400
        
        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not thumbnail:
            return jsonify({"msg": "Thumbnail is Required"}), 400

        if not song_title:
            return jsonify({"msg": "Song Title is Required"}), 400
        
        if not artist:
            return jsonify({"msg": "Artist is Required"}), 400
        
        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400

        result = music.create_music(thumbnail, song_title, artist, year, month, day)

        if result is None:
            return jsonify({"msg": "Email not found in users table"}), 400

        if not result:
            return jsonify({"msg": "Failed to create music"}), 400

        return jsonify({"msg": "Create Music Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/api/music/selectmusic', methods=['POST'])
def add_music():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        year = data.get('year')
        month = data.get('month')
        
        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 400

        if not email:
            return jsonify({"msg": "Email is Required"}), 400

        if not year:
            return jsonify({"msg": "Year is Required"}), 400
        
        if not month:
            return jsonify({"msg": "Month is Required"}), 400
        
        auth_token = token_parsing(auth_header, email)

        if not auth_token["valid"]:
            return jsonify({"msg": "Invalid Token"}), 400

        result = music.select_month_music(year, month)

        if not result.get("data"):
            return jsonify({"msg": "No music found for the specified date"}), 404

        return jsonify({"msg": "Select Music Successfully", "data": result["data"]}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

if __name__ == '__main__':
    table.create_table()
    app.run(debug=True, host='0.0.0.0', port=8080)