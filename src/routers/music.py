from flask import Flask, request, jsonify, abort, Blueprint
import datetime
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
        print(word)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500