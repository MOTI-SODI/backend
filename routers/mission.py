from flask import Flask, jsonify, Blueprint
import random

import database.mission as mission

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

mission_route = Blueprint("mission", __name__, url_prefix='/api/mission')


@mission_route.route('/mission', methods=['GET'])
def select_mission():
    id = random.randint(1, 60)

    result = mission.select_mission(id)

    return jsonify({"msg": "Select Mission Successfully", "mission": result})
