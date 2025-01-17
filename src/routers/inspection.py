from flask import request, jsonify, Blueprint
import logging

import database.user as user
import database.inspection as inspection
import utils.token.token as token
import utils.error.error as error

inspection_route = Blueprint("inspection", __name__, url_prefix='/api/inspection')

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
    
@inspection_route.route('/results', methods=['POST'])
def insert_inspection_result():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'emotionality', 'extraversion', 'agreeableness', 'eonesty', 'eonscientiousness', 'open']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code

        result = inspection.insert_inspection_result(fields['user_id'], fields['emotionality'], fields['extraversion'], fields['agreeableness'], fields['eonesty'], fields['eonscientiousness'], fields['open'])

        if result is None:
            return jsonify({"msg": "Failed to insert inspection result"}), 400

        return jsonify({"msg": "Insert inspection result Successfully"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500