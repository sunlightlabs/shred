import os

import weather
import wmata
from flask import Flask, abort, jsonify, request

COMMAND_PARAMS = ('team_id', 'channel_id', 'channel_name',
                  'user_id', 'user_name', 'text')


app = Flask(__name__)
app.config['SLACK_TOKEN'] = os.environ.get('SLACK_TOKEN')
app.config['SLASH_COMMANDS'] = {}

app.config['FORECASTIO_KEY'] = os.environ.get('FORECASTIO_KEY')
weather.WeatherCommand(app)

app.config['WMATA_KEY'] = os.environ.get('WMATA_KEY')
wmata.MetroCommand(app)


@app.route('/command', methods=['GET', 'POST'])
def slash_command():

    if request.values.get('token') != app.config['SLACK_TOKEN']:
        return abort(403)

    command = request.values.get('command', '')[1:]

    if not command or command not in app.config['SLASH_COMMANDS']:
        return abort(400)

    params = {key: request.values.get(key) for key in COMMAND_PARAMS}

    return app.config['SLASH_COMMANDS'][command](**params)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
