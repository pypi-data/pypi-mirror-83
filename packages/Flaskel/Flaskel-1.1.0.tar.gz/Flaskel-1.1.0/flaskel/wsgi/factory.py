import sys
import traceback

from .base import WSGIBuiltin

try:
    from .gunicorn import WSGIGunicorn
except ImportError as exc:
    WSGIGunicorn = None
try:
    from .gevent import WSGIGevent
except ImportError as exc:
    WSGIGevent = None
try:
    from .tornado import WSGITornado
except ImportError as exc:
    WSGITornado = None
try:
    from .twisted import WSGITwisted
except ImportError as exc:
    WSGITwisted = None
try:
    from .waitress import WSGIWaitress
except ImportError as exc:
    WSGIWaitress = None


class WSGIFactory:
    DEFAULT_WSGI = {
        'builtin':  WSGIBuiltin,
        'gunicorn': WSGIGunicorn,
        'gevent':   WSGIGevent,
        'tornado':  WSGITornado,
        'twisted':  WSGITwisted,
        'waitress': WSGIWaitress,
    }

    @classmethod
    def getInstance(cls, name, **kwargs):
        """

        :param name:
        :param kwargs:
        :return:
        """
        return cls.getClass(name)(**kwargs)

    @classmethod
    def getClass(cls, name):
        """

        :param name:
        :return:
        """
        if name not in cls.DEFAULT_WSGI:
            raise ValueError("unable to find wsgi server: '{}'".format(name))

        wsgi_class = cls.DEFAULT_WSGI.get(name)

        if wsgi_class is None:
            raise ImportError(traceback.TracebackException)
            # print(traceback.format_exc(), file=sys.stderr)
            # sys.exit(-1)

        return wsgi_class
