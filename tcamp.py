import requests
from shred import Command


class TCampCommand(Command):

    COMMAND = 'tcamp'

    def __call__(self, *args, **kwargs):

        url = 'https://tcamp.sunlightfoundation.com/register/whos-going/'

        resp = requests.get(url)
        data = resp.json()
        
        attendees = data['attendees']

        return "%i people have registered for TransparencyCamp" % len(attendees)
