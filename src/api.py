from flask import Flask
from flask_cors import CORS

import database.table as table
import routers.user as user
import routers.note as note
import routers.music as music
import routers.token as token
import routers.health as health
import routers.mission as mission
import routers.calendar as calendar

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

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