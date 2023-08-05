import warnings
from PIL import Image
import bottle
from karlovic.middleware import use_middleware
from karlovic.api import default_routes
from karlovic.execution_time import execution_time
from karlovic.request_logger import request_logger


def arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=80, type=int)
    parser.add_argument('--model', default='model', type=str)

    try:
        __IPYTHON__
        return parser.parse_known_args()[0]
    except NameError:
        return parser.parse_args()


def run_server(app):
    from cheroot.wsgi import Server

    args = arguments()
    server = Server(
        ('0.0.0.0', args.port),
        app,
        server_name='<Server name from env implemented in the future>',
        numthreads=4,
    )

    def _run_server():
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()

    return _run_server


def use_plugins(app, plugins):
    default_plugins = [
        execution_time,
        request_logger,
    ]

    for plugin in default_plugins + plugins:
        app.install(plugin)


def configure_bottle(configuration_function):
    # Allow the request body to be 10Mb
    bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10
    return configuration_function(bottle)


def model_server(plugins, bottle_configuration_function):
    from cheroot.wsgi import Server
    configure_bottle(bottle_configuration_function)
    app = bottle.app()
    use_middleware(app)
    use_plugins(app, plugins)
    default_routes(app)
    return app, run_server(app)
