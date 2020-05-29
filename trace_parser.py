from trace_models import TraceModel
from error_handler import ErrorHandler
from trace_manager import TraceManager
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

class TraceParser:
    """description of class"""

    def __init__(self, error_handler: ErrorHandler, trace_manager: TraceManager):
        self.__error_handler = error_handler
        self.__trace_manager = trace_manager

    def parse(self, trace_str):
        trace = self.__try_parse(trace_str)
        print("\n")
        if trace[1]:
            self.__error_handler.handle_parse_error(trace_str)
        else:
            print(trace[0].to_json())
            self.__trace_manager.SetTrace(trace[0])

    def __try_parse(self, trace_str):
        """do parsing here"""
        model = TraceModel(None, None, None, None, None, None, datetime.now())
        if len(trace_str) > 0:
            trace = trace_str.split(' ')
            if len(trace) == 5:
                try:
                    model.start_time = datetime.strptime(trace[0], '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    print("date is not in valid format")
                    return None, True
                try:
                    model.end_time = datetime.strptime(trace[1], '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    print("date is not in valid format")
                    return None, True
                model.trace_id = trace[2]
                model.service_name = trace[3]
                spans = trace[4].split('->')
                model.span_received = spans[0]
                model.span_assigned = spans[1].strip('\n')
            else:
                print("wrong line")
                return None, True
        else:
            print("empty line")
            return None, True
        return model, False
