from karlovic.plugins.ensure_nonconflicting_plugins import ensure_nonconflicting_plugins
from karlovic.plugins.get_plugin_value import get_plugin_value
from workflow.ignite.handlers import ModelCheckpoint
from karlovic.request_logger import log


class ModelPlugin:
    name = 'model'
    api = 2

    def __init__(self, run_dir, config, device, architecture, keyword='model'):
        self.run_dir = run_dir
        self.config = config
        self.device = device

        self.keyword = keyword
        self.architecture = architecture

    def setup(self, app):
        ensure_nonconflicting_plugins(self, app)

        import time

        start_time = time.time()
        self.model = self.architecture.Model(
            self.config, pretrained=False,
        ).to(self.device)

        ModelCheckpoint.load(
            dict(model=self.model),
            dirname=self.run_dir / ModelCheckpoint.dirname,
            device=self.device,
        )
        end_time = time.time()

        log().info(f'Model loaded in {end_time-start_time:.3f} s')

    def apply(self, f, context):
        @get_plugin_value(f, context, self.keyword)
        def _f():
            return self.model

        return _f
