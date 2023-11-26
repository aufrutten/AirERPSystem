from os import environ
from django.conf import settings


class Hosts:

    def __init__(self):
        if settings.DEBUG is True:
            self.backend = environ.get("DEBUG_BACKEND_HOST", 'api.aufrutten.local')
            self.frontend = environ.get("DEBUG_FRONTEND_HOST", 'aufrutten.local')

        else:
            self.backend = environ.get('BACKEND_HOST', 'api.aufrutten.com')
            self.frontend = environ.get('FRONTEND_HOST', 'aufrutten.com')
