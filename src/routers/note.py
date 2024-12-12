from flask import request, jsonify, Blueprint
import logging

import database.user as user
import database.note as note
import utils.token.token as token
import utils.error.error as error

note_route = Blueprint("note", __name__, url_prefix='/api/note')

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

@note_route.route('/createnote', methods=['POST'])
def create_note():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'title', 'content', 'mood', 'year', 'month', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code

        year, month, day = fields['year'], fields['month'], fields['day']
        try:
            date_str = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400

        existing_note = note.select_note_by_date(fields['user_id'], date_str)
        if existing_note:
            return jsonify({"msg": "Note already exists for the specified date"}), 400

        result = note.create_note(fields['user_id'], fields['title'], fields['content'], fields['mood'], date_str)

        if result is None:
            return jsonify({"msg": "Failed to create note"}), 400

        return jsonify({"msg": "Create Note Successfully"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@note_route.route('/modifynote', methods=['POST'])
def modify_note():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'title', 'content', 'mood', 'year', 'month', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        year, month, day = fields['year'], fields['month'], fields['day']
        try:
            date_str = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400

        result = note.modify_note(fields['user_id'], fields['title'], fields['content'], fields['mood'], date_str)

        if not result:
            return jsonify({"msg": "Failed to modify note"}), 400

        return jsonify({"msg": "Modify Note Successfully"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@note_route.route('/selectnote', methods=['POST'])
def select_note():
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

        result = note.select_note(fields['user_id'], date_str)

        if not result:
            return jsonify({"msg": "Note Not Found"}), 400

        return jsonify({"msg": "Select Note Successfully", "title": result[0][2], "content": result[0][3], "mood": result[0][4]}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500