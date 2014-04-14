import humanize
import datetime as dt
import requests
from shred import Command


class MBTACommuterRailCommand(Command):
    COMMAND = "mbta"

    def __call__(self, *args, **kwargs):
        url = 'http://developer.mbta.com/lib/RTCR/RailLine_9.json'
        resp = requests.get(url)
        data = resp.json()
        descrs = []

        def format(train):
            delta = humanize.naturaltime(dt.datetime.now() - train['Scheduled'])
            return (" * Train {train} ({fro} => {to}) leaving {delt}. "
                    "Currently in status '{flag}'\n".format(
                        train=train['Trip'],
                        fro=train['Stop'],
                        to=train['Destination'],
                        flag=train['Flag'],
                        delt=delta))

        for train in data['Messages']:
            if train['Stop'] != "North Station":
                continue

            train['Scheduled'] = dt.datetime.fromtimestamp(
                float(train['Scheduled'])
            )

            descrs.append(train)
            if len(descrs) > 3:
                break

        return " ".join([format(x) for x in descrs])
