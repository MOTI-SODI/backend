from flask import jsonify
import logging

def validate_and_extract_fields(data, required_fields):
    for field in required_fields:
        if not data.get(field):
            return jsonify({"msg": f"{field} is Required"}), 400
    return None, {field: data.get(field) for field in required_fields}

def handle_error(error):
    logging.error(f"Error occurred: {error}")
    return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500
