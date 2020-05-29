from error_handler import ErrorHandler
from input_reader import InputReader
from output_writer import OutputWriter
from trace_manager import TraceManager
from trace_parser import TraceParser
from threading import Thread

error_handler = ErrorHandler()
writer = OutputWriter(error_handler)
trace_manager = TraceManager(writer)
parser = TraceParser(error_handler, trace_manager)
reader = InputReader(parser)

print("Start parsing")
clean_thread = Thread(target=trace_manager.clean_traces)
clean_thread.start()

reader.read()