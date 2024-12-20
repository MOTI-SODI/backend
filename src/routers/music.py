from flask import Flask, request, jsonify, abort, Blueprint
import logging

import database.user as user
import database.music as music
import utils.song.song as song
import utils.error.error as error
import utils.token.token as token
import utils.keyword.keyword as keyword

music_route = Blueprint("music", __name__, url_prefix='/api/music')

def token_parsing(auth_header, email):
    access_token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    result = token.verify_access_token(access_token, email)
    return result

def validate_request(data, required_fields, auth_header):
    error_response, fields = error.validate_and_extract_fields(data, required_fields)
    if error_response:
        return None, jsonify({"msg": error_response[0]}), error_response[1]
    
    if not auth_header:
        return None, jsonify({"msg": "Authorization header is missing"}), 400
    
    email = user.select_user_email(fields['user_id'])
    
    auth_token = token_parsing(auth_header, email)
    
    if not auth_token["valid"]:
        return None, jsonify({"msg": auth_token["msg"]}), 400
    
    return fields, None, None

@music_route.route('/recommend', methods=['POST'])
def get_recommend():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'content']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        word = keyword.generate_keyword(fields['content'])
        result = song.get_music(word)
        return jsonify({'msg': "Recommend Music Successfully", "artist": result['artist'], "song_title": result['song_title'], "thumbnail": result['thumbnail'], "music_url": result['music_url']}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    
@music_route.route('/createmusic', methods=['POST'])
def create_music():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'artist', 'song_title', 'thumbnail', 'music_url', 'year', 'month', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code

        year, month, day = fields['year'], fields['month'], fields['day']
        try:
            date_str = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400

        result = music.create_music(fields['user_id'], fields['artist'], fields['song_title'], fields['thumbnail'], fields['music_url'], date_str)

        if result is None:
            return jsonify({"msg": "Failed to create music"}), 400

        return jsonify({"msg": "Create music Successfully"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    

@music_route.route('/selectmusic', methods=['POST'])
def select_music():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'year', 'month', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        year, month, day = fields['year'], fields['month'], fields['day']
        try:
            date_str = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400

        result = music.select_music(fields['user_id'], date_str)
        if not result:
            return jsonify({"msg": "music Not Found"}), 400

        return jsonify({"msg": "Select music Successfully", "artist": result[0]['artist'], "song_title": result[0]['song_title'], "thumbnail": result[0]['thumbnail'], "music_url": result[0]['music_url']}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500