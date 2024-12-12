from flask import request, jsonify, Blueprint
import logging

import database.user as user
import database.calendar as calendar
import utils.token.token as token
import utils.error.error as error

calendar_route = Blueprint("calendar", __name__, url_prefix='/api/calendar')

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

@calendar_route.route('/createcalendar', methods=['POST'])
def create_calendar():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'note_id', 'year', 'month', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code

        year, month, day = fields['year'], fields['month'], fields['day']
        try:
            date_str = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400
        
        existing_note = calendar.select_note_id(fields['user_id'], fields['note_id'])
        if not existing_note:
            return jsonify({"msg": "Note Not Found"}), 400
        
        existing_calendar = calendar.select_calendar_by_date(fields['user_id'], date_str)
        if existing_calendar:
            return jsonify({"msg": "calendar already exists for the specified date"}), 400

        result = calendar.create_calendar_by_day(fields['user_id'], fields['note_id'], date_str)

        if result is None:
            return jsonify({"msg": "Failed to create calendar"}), 400

        return jsonify({"msg": "Create calendar Successfully"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@calendar_route.route('/year', methods=['POST'])
def select_calendar_by_year():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'year']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        result = calendar.select_calendar_by_year(fields['user_id'], fields['year'])

        if not result:
            return jsonify({"msg": "Calendar not found for the given year"}), 404
        
        return jsonify({"msg": "Select calendar with year successfully", "data": result}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    
@calendar_route.route('/month', methods=['POST'])
def select_calendar_by_month():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'month']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        result = calendar.select_calendar_by_month(fields['user_id'], fields['month'])

        if not result:
            return jsonify({"msg": "Calendar not found for the given month"}), 404
        
        return jsonify({"msg": "Select calendar with month successfully", "data": result}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    
@calendar_route.route('/day', methods=['POST'])
def select_calendar_by_day():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        required_fields = ['user_id', 'day']

        fields, error_response, status_code = validate_request(data, required_fields, auth_header)
        if error_response:
            return error_response, status_code
        
        result = calendar.select_calendar_by_day(fields['user_id'], fields['day'])

        if not result:
            return jsonify({"msg": "Calendar not found for the given day"}), 404
        
        return jsonify({"msg": "Select calendar with day successfully", "data": result}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500