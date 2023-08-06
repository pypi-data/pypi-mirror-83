class BaseFlowProcessor(object):
    is_flow_processor = True

    def initialize(self, *args, **kwargs):
        raise NotImplemented()

    def execute(self, *args, **kwargs):
        raise NotImplemented()
