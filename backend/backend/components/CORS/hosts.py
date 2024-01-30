from decouple import config


class Hosts:

    def __init__(self, debug):
        if debug:
            self.backend = config("DEBUG_BACKEND_HOST", default="api.localhost", cast=str)
            self.frontend = config("DEBUG_FRONTEND_HOST", default="localhost", cast=str)

        else:
            self.backend = config('BACKEND_HOST', cast=str)
            self.frontend = config('FRONTEND_HOST', cast=str)

    @property
    def origin_domain(self):
        """return the original domain: www.example.com or one.www.example.com or example.com - return: example.com"""
        if self.backend.split('.')[-1] == 'localhost':
            return self.backend.split('.')[-1]
        return '.'.join(self.backend.split('.')[-2:])
