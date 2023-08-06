import inspect
import sys

from grebble_flow.processors.base import BaseFlowProcessor


def import_processors():
    module = "processors"
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=[module])


def find_all_processors():
    import_processors()
    results = inspect.getmembers(import_processors())

    result = []
    for cls in results:
        try:
            assert cls[1].is_flow_processor
            result.append(cls[1])
        except:
            pass
    return result
