import os

import weather
import wmata
import mbta
import nextbus_dc
from flask import Flask, abort, jsonify, request

COMMAND_PARAMS = ('team_id', 'channel_id', 'channel_name',
                  'user_id', 'user_name', 'text')


app = Flask(__name__)
app.config['SLASH_COMMANDS'] = {}

weather.WeatherCommand(app,
    token=os.environ.get('WEATHER_TOKEN'),
    key=os.environ.get('FORECASTIO_KEY'))

wmata.MetroCommand(app,
    token=os.environ.get('METRO_TOKEN'),
    key=os.environ.get('WMATA_KEY'))

mbta.MBTACommuterRailCommand(app,
    token=os.environ.get('MBTA_TOKEN'))

nextbus_dc.NextbusCommand(app,
    token=os.environ.get('NEXTBUS_TOKEN'))


@app.route('/command', methods=['GET', 'POST'])
def slash_command():

    command = request.values.get('command', '')[1:]

    if not command or command not in app.config['SLASH_COMMANDS']:
        return abort(400)

    params = {key: request.values.get(key) for key in COMMAND_PARAMS}

    cmd = app.config['SLASH_COMMANDS'][command]

    if request.values.get('token') != cmd.token:
        return abort(403)

    return cmd(**params)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
