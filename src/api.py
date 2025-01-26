from flask import Flask, make_response
from flask_cors import CORS, cross_origin

import database.table as table
import routers.user as user
import routers.note as note
import routers.music as music
import routers.token as token
import routers.health as health
import routers.mission as mission
import routers.calendar as calendar

app = Flask(__name__)

CORS(app,
    resources={r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True,
        "expose_headers": ["Content-Range", "X-Content-Range"]
    }}
)

@app.after_request
def after_request(response):
    origin = "http://localhost:3000"
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/', methods=['OPTIONS'])
@cross_origin(origins=["http://localhost:3000"])
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

app.register_blueprint(user.user_route)
app.register_blueprint(note.note_route)
app.register_blueprint(music.music_route)
app.register_blueprint(token.token_route)
app.register_blueprint(health.health_route)
app.register_blueprint(mission.mission_route)
app.register_blueprint(calendar.calendar_route)

if __name__ == '__main__':
    table.create_table()
    app.run(debug=True, host='0.0.0.0', port=8080)                     