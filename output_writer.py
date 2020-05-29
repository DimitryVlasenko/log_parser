from trace_models import TraceModel
from trace_models import RootOutputModel
from trace_models import ChildOutputModel
from error_handler import ErrorHandler
from json import dumps
from dataclasses import asdict
from dataclasses_json import dataclass_json
from typing import (Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar,
                    Union)

class OutputWriter:
    """description of class"""
    def __init__(self, error_handler: ErrorHandler):
        self.__error_handler = error_handler
    
    def write(self, traces):
        """ create json and write to default output"""
        print(f'OUTPUT trace_id = {traces[0].trace_id}')
        #print(traces.to_json())
        output_model = RootOutputModel(traces[0].trace_id, None)
        finish_trace = self.__get_finish_trace(traces)
        if finish_trace == None:
            self.__error_handler\
                .handle_parse_error(f'traces with id={traces[0].trace_id} has no one root trace')
            return
        output_model.root = finish_trace
        #output_model.root.cals = self.__get_childs(finish_trace.span, traces)
        #print(output_model.to_json())
        output_dict = asdict(output_model)
        output_json = dumps(output_dict)
        print(output_json)

    def __get_finish_trace(self, traces) -> ChildOutputModel:
        for trace in traces:
            if trace.span_received == "null":
                cals = self.__get_childs(trace.span_assigned, traces)
                return self.__create_child(trace, cals)
        return None

    def __get_childs(self, span_assigned: str, traces):
        children = []
        for trace in traces:
            if trace.span_received == span_assigned:
                cals = self.__get_childs(trace.span_assigned, traces)
                child = self.__create_child(trace, cals)
                children.append(child)
        return children

    def __create_child(self, trace: TraceModel, cals) -> ChildOutputModel:
        return ChildOutputModel(
            trace.service_name,
            trace.start_time.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
            trace.end_time.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
            trace.span_assigned,
            cals)