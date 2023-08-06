from PIL import Image
import bottle
from karlovic.middleware import use_middleware
from karlovic.api import default_routes
from karlovic.execution_time import execution_time
from karlovic.request_logger import request_logger


def run_server(app, port, server_name='karlovic-server'):
    from cheroot.wsgi import Server

    server = Server(
        ('0.0.0.0', port),
        app,
        server_name=server_name,
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


def model_server(plugins, port=80, bottle_configuration_function=lambda bottle: None):
    from cheroot.wsgi import Server
    configure_bottle(bottle_configuration_function)
    app = bottle.app()
    use_middleware(app)
    use_plugins(app, plugins)
    default_routes(app)
    return app, run_server(app, port)
