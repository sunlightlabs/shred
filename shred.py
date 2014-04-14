
class Command(object):

    def __init__(self, app=None, token=None, **kwargs):
        if app is not None:
            self.init_app(app)

        self.token = token

        if kwargs:
            self.__dict__.update(kwargs)

    def init_app(self, app):
        app.extensions[self.__class__.__name__] = self
        app.config['SLASH_COMMANDS'][self.COMMAND] = self
