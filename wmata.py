import requests


STATION_CODE = 'A03'
LINE_CODE = 'RD'

class MetroCommand(object):

    def __init__(self, app=None, token=None, key=None):
        if app is not None:
            self.init_app(app)

        self.key = key
        self.token = token

    def init_app(self, app):
        app.extensions['MetroCommand'] = self
        app.config['SLASH_COMMANDS']['metro'] = self

    def __call__(self, *args, **kwargs):

        url = 'http://api.wmata.com/StationPrediction.svc/json/GetPrediction/A03'

        params = {'api_key': self.key}

        resp = requests.get(url, params=params)
        data = resp.json()

        trains = []

        for train in data['Trains'][:3]:
            if train['Min'] == 'BRD':
                pred = "%s is boarding." % (train['DestinationName'],)
            else:
                pred = "%s in %s minutes." % (train['DestinationName'], train['Min'])
            trains.append(pred)

        return " ".join(trains) if trains else "No predictions available."
