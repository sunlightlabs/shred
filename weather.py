import requests
from shred import Command

FORECAST_URL = 'https://api.forecast.io/forecast/%s/%s,%s'


class WeatherCommand(Command):

    COMMAND = 'weather'

    def __call__(self, *args, **kwargs):

        url = FORECAST_URL % (self.key, '38.8904', '-77.0320')

        params = {
            'exclude': 'minutely,daily,flags',
        }

        resp = requests.get(url, params=params)
        data = resp.json()

        currently = data['currently']
        forecast = "Currently %0.0f and %s." % (currently['temperature'], currently['summary'].lower())

        if len(data['hourly']) > 1:
            next_hour = data['hourly']['data'][1]
            forecast = "%s %0.0f and %s in the next hour." % (forecast, next_hour['temperature'], next_hour['summary'].lower())

        return forecast