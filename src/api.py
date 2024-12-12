from flask import Flask

import database.table as table
import routers.user as user
import routers.note as note
# import routers.music as music
import routers.token as token
import routers.mission as mission
import routers.calendar as calendar

app = Flask(__name__)

app.register_blueprint(user.user_route)
app.register_blueprint(note.note_route)
# app.register_blueprint(music.music_route)
app.register_blueprint(token.token_route)
app.register_blueprint(mission.mission_route)
app.register_blueprint(calendar.calendar_route)

if __name__ == '__main__':
    table.create_table()
    app.run(debug=True, host='0.0.0.0', port=8080)