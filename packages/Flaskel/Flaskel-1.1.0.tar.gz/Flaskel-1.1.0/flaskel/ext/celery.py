from celery import Celery


class FlaskCelery:
    def __init__(self, app=None, **kwargs):
        """

        :param app:
        :param kwargs:
        """
        self.session = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, name, **kwargs):
        """

        :param app:
        :param name:
        :param kwargs:
        :return:
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['celery'] = self

        self.session = Celery(name, **kwargs)
        self.session.conf.update(app.config)

        class ContextTask(self.session.Task):
            abstract = True

            def __call__(self, *args, **kw):
                with app.app_context():
                    return self.celery.Task.__call__(self, *args, **kw)

        # noinspection PyPropertyAccess
        self.session.Task = ContextTask


celery = FlaskCelery()
