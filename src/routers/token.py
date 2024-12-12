from flask import request, jsonify, Blueprint

from utils.token import token

token_route = Blueprint("token", __name__, url_prefix='/api/token')

@token_route.route('/refresh', methods=['POST'])
def refresh_tokens():
    data = request.json
    refresh_token = data.get('refresh_token')

    if not refresh_tokens:
        return jsonify({"msg": "Refresh token is Required"}), 400
    
    result = token.refresh_access_token(refresh_token)

    if not result["success"]:
        return jsonify({"msg": "Refresh Token is Required"}), 400

    return jsonify({"msg": "Access token refreshed", "Access_Token": result["new_access_token"]}), 200
