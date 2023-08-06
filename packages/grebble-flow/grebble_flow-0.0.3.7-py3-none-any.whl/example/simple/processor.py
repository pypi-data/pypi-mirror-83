from grebble_flow.processors.base import BaseFlowProcessor


class SimpleProcessor(BaseFlowProcessor):
    name = "simple-flow-processor"

    def execute(self, *args, **kwargs):
        for i in range(0, 100):
            yield {"test": i}
