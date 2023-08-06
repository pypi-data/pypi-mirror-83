import os
import sys

import click
import yaml
from yaml.error import YAMLError

from flaskel import AppFactory, BASE_EXTENSIONS
from flaskel.utils.misc import parse_value
from flaskel.wsgi import BaseApplication, WSGIFactory

wsgi_types = click.Choice(WSGIFactory.DEFAULT_WSGI, case_sensitive=False)


def option_as_dict(ctx, param, value):
    """

    :param ctx:
    :param param:
    :param value:
    :return:
    """
    ret = {}
    for opt in value:
        k, v = opt.split("=", 2)
        ret.update({k: parse_value(v)})
    return ret


class Server:
    opt_config_attr = dict(
        default=None,
        help='app yaml configuration file'
    )
    opt_log_config_attr = dict(
        default=None,
        help='alternative log yaml configuration file'
    )
    opt_bing_attr = dict(
        default='127.0.0.1:5000',
        help='address to bind',
        show_default=True
    )
    opt_debug_attr = dict(
        is_flag=True,
        flag_value=True,
        default=False,
        help='enable debug mode'
    )
    opt_wsgi_server_attr = dict(
        default=None,
        type=wsgi_types,
        help='name of wsgi server to use'
    )
    option_wsgi_config_attr = dict(
        default={},
        multiple=True,
        callback=option_as_dict,
        metavar="KEY=VAL",
        help='wsgi configuration'
    )

    def __init__(self, app=None, blueprints=None, extensions=None, **kwargs):
        """

        :param app:
        :param blueprints:
        :param extensions:
        :param kwargs:
        :return:
        """
        self._app = app or AppFactory().getOrCreate(
            blueprints=blueprints,
            extensions={**BASE_EXTENSIONS, **extensions},
            **kwargs
        )

    def _register_options(self, func):
        """

        :param func:
        :return:
        """

        @click.command()
        @click.option('-b', '--bind', **self.opt_bing_attr)
        @click.option('-d', '--debug', **self.opt_debug_attr)
        @click.option('-c', '--config', **self.opt_config_attr)
        @click.option('-l', '--log-config', **self.opt_log_config_attr)
        @click.option('-w', '--wsgi-server', **self.opt_wsgi_server_attr)
        @click.option('-D', '--wsgi-config', **self.option_wsgi_config_attr)
        def _options(*args, **kwargs):
            return func(*args, **kwargs)

        return _options

    def run(self):
        """

        """
        @self._register_options
        def _forever(config, log_config, bind, debug, wsgi_server, wsgi_config):
            self._serve_forever(
                app=self._app,
                bind=bind,
                debug=debug,
                config=config,
                log_config=log_config,
                wsgi_server=wsgi_server,
                wsgi_config=wsgi_config
            )

        _forever()

    @staticmethod
    def _prepare_config(filename, **kwargs):
        """

        :param filename:
        :return: config
        """
        if filename is not None:
            try:
                with open(filename) as f:
                    config = yaml.safe_load(f)
            except (OSError, YAMLError) as e:
                print(e, file=sys.stderr)
                sys.exit(os.EX_OSFILE)
        else:
            env = os.environ.get('FLASK_ENV')
            env = env or ('development' if kwargs['debug'] else 'production')
            config = dict(
                app={'DEBUG': kwargs['debug'], 'ENV': env},
                wsgi={'bind': kwargs['bind'], 'debug': kwargs['debug']}
            )

        if kwargs['log_config'] is not None:
            config['app']['LOG_FILE_CONF'] = log_config

        # debug flag enabled overrides config file
        if kwargs['debug'] is True:
            config['app']['DEBUG'] = True

        return config

    def _serve_forever(self, config=None, log_config=None, bind=None, debug=None,
                       wsgi_class=None, wsgi_server=None, wsgi_config=None, **kwargs):
        """

        :param wsgi_class: optional a custom subclass of BaseApplication
        :param config: app and wsgi configuration file
        :param log_config: log configuration file
        :param bind: address to bind
        :param debug: enable debug mode
        :param wsgi_server: wsgi server chose
        :param wsgi_config: wsgi configuration
        :param kwargs: parameters passed to factory
        :return: never returns
        """
        config = self._prepare_config(config, debug=debug, bind=bind, log_config=log_config)

        if wsgi_server:
            wsgi_class = WSGIFactory.getClass(wsgi_server)
        elif wsgi_class and not issubclass(wsgi_class, BaseApplication):
            mess = '{} must be subclass of {}'
            raise TypeError(mess.format(wsgi_class, BaseApplication))
        else:
            wsgi_class = WSGIFactory.getClass('builtin')

        config.update(dict(wsgi=wsgi_config))
        kwargs['conf_map'] = config.get('app', {})
        wsgi = wsgi_class(self._app, options=config.get('wsgi', {}))

        wsgi.run()  # run forever
