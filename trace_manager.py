from trace_models import TraceModel
from output_writer import OutputWriter
from time import sleep
from datetime import datetime
from datetime import timedelta

class TraceManager:
    """description of class"""
    __traces = dict()

    def __init__(self, writer: OutputWriter):
        self.__writer = writer


    def SetTrace(self, trace: TraceModel):
        print("Set Trace start")
        if trace.trace_id in self.__traces :
            print(f'trace id {trace.trace_id} already exist')
            self.__update_trace(trace)
        else:
            print(f'new trace {trace.trace_id}')
            self.__add_trace(trace)

    def clean_traces(self):
        while True:
            #print('clean traces')
            for key in list(self.__traces):
                max_created_time = max(self.__traces[key], key=lambda x: x.created).created
                max_end_time = max_created_time + timedelta(seconds=15)
                if max_end_time <= datetime.now():
                    final_trace_list = self.__traces.pop(key)
                    self.__writer.write(final_trace_list)
            sleep(1)

    def __add_trace(self, trace: TraceModel):
        self.__traces[trace.trace_id] = [trace]

    def __update_trace(self, trace: TraceModel):
        if self.__check_trace(trace):
            self.__traces[trace.trace_id].append(trace)
            final_trace_list = self.__traces.pop(trace.trace_id)
            self.__writer.write(final_trace_list)
        else:
            self.__traces[trace.trace_id].append(trace)

    def __check_trace(self, trace: TraceModel) -> bool:
        if trace.span_received != "null":
            return False
        trace_list = self.__traces[trace.trace_id]
        min_start_time = min(trace_list, key=lambda x: x.start_time)
        max_end_time = max(trace_list, key=lambda x: x.end_time)
        if min_start_time.start_time > trace.start_time and \
                max_end_time.end_time < trace.end_time:
            print(f'final trace trace_id = {trace.trace_id}')
            return True
        return False
