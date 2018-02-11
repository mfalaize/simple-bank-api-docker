import inspect
import json
import sys

import cherrypy
import datetime
import simplebank.bank # used by sys.modules


def default_serializer(o):
    if isinstance(o, datetime.date):
        return o.isoformat()
    return o.__dict__


def json_serialize(obj):
    return json.dumps(obj, default=default_serializer)


class Api(object):

    def __init__(self):
        self.bank = Bank()

    def _cp_dispatch(self, vpath):
        if len(vpath) == 2:
            cherrypy.request.params['bank'] = vpath.pop(0)
            cherrypy.request.params['method'] = vpath.pop(0)
            return self.bank

        return vpath


class Bank(object):
    @cherrypy.expose
    def index(self, bank, method, **kwargs):
        # Retrieve bank instance and call method by reflection
        for name, cls in inspect.getmembers(sys.modules['simplebank.bank']):
            if name.lower() == bank:
                params = {}
                for param in inspect.signature(cls).parameters:
                    if param in kwargs:
                        params[param] = kwargs.pop(param)

                with cls(**params) as api:
                    return json_serialize(getattr(api, method)(**kwargs))

        return ""


if __name__ == '__main__':
    cherrypy.quickstart(Api())
