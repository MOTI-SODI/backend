from flask import Blueprint, jsonify
import utils.error.error as error

health_route = Blueprint("health", __name__, url_prefix='/api')

@health_route.route('/healthcheck', methods=['GET'])
def get_health():
    try:
        ret = {'status': 'ok'}

        return jsonify(ret), 200
    except Exception as e:
        return error.handle_error(e)