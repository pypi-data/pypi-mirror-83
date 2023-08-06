import gunicorn.app.base

import foggy.avahi
import foggy.api.app

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=True,
    root={"level": "DEBUG", "handlers": ["console"]},
    loggers={
        "gunicorn.error": {
            "level": "DEBUG",
            "handlers": ["error_console"],
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stderr",
        },
    },
    formatters={
        "generic": {
            "format": "[%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
)


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    options = {
        "bind": "0.0.0.0:21210",
        "threads": 2,
        "reload": True,
        "logconfig_dict": LOGGING_CONFIG,
        "access_log_format": '%(h)s "%(r)s" %(s)s %(b)s "%(a)s"',
    }
    with foggy.avahi.broadcast_service():
        StandaloneApplication(foggy.api.app.get_app(), options).run()


if __name__ == "__main__":
    main()
