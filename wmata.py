import requests
from shred import Command

STATION_CODE = 'A03'
LINE_CODE = 'RD'


class MetroCommand(Command):

    COMMAND = 'metro'

    def __call__(self, *args, **kwargs):

        url = 'http://api.wmata.com/StationPrediction.svc/json/GetPrediction/A03'

        params = {'api_key': self.key}

        resp = requests.get(url, params=params)
        data = resp.json()

        trains = []

        for train in data['Trains']:
            if train['Min'] == 'BRD':
                pred = "%s is boarding." % (train['DestinationName'],)
            elif train['Min'] == 'ARR':
                pred = "%s is arriving." % (train['DestinationName'],)
            else:
                unit = 'minute' if train['Min'] == '1' else 'minutes'
                pred = "%s in %s %s." % (train['DestinationName'], train['Min'], unit)
            trains.append(pred)

        return " ".join(trains) if trains else "No predictions available."
