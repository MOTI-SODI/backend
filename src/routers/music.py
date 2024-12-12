from flask import Flask, request, jsonify, abort, Blueprint
import datetime
import logging

from database import music
from utils.token import token
from utils.keyword import keywords
from utils.song import song

music_route = Blueprint("music", __name__, url_prefix='/api/music')

def token_parsing(auth_header, email):
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    result = token.verify_access_token(token, email)
    return result

@music_route.route('/recommend', methods=['POST'])
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
    
@music_route.route('/createmusic', methods=['POST'])
def add_music():
    try:
        auth_header = request.headers.get('Authorization')
        data = request.json
        email = data.get('email')
        thumbnail = data.get('thumbnail')
        song_title = data.get('song_title')
        artist = data.get('artist')

        date = datetime.date.today().strftime("%Y-%m-%d")

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

        result = music.create_music(thumbnail, song_title, artist, date, email)

        if result is None:
            return jsonify({"msg": "Email not found in users table"}), 400

        if not result:
            return jsonify({"msg": "Failed to create music"}), 400

        return jsonify({"msg": "Create Music Successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@music_route.route('/selectmusic', methods=['POST'])
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

        result = music.select_music(email, year, month)

        if not result:
            return jsonify({"msg": "No music found for the specified date"}), 404

        return jsonify({"msg": "Select Music Successfully", "data": result}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500