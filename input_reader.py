import sys


class InputReader:
    """description of class"""

    def __init__(self, trace_parser):
        self.__trace_parser = trace_parser

    def read(self):
        for line in sys.stdin:
            #print(line)
            self.__trace_parser.parse(line)
