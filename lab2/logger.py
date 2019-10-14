import csv
import re
import time
import sys
from enum import Enum
from datetime import datetime

class OutputModes(Enum):
    FILE = 0
    CONSOLE = 1

class LogLevels(Enum):
    ERROR = 0
    TRACE = 1
    INFO = 2

DefaultFormat = '%p %m %d %t'

class Logger:
    def __init__(self, filename = None):
        if filename is not None:
            self.__outputMode = OutputModes.FILE
            self.filename = filename
        else:
            self.__outputMode = OutputModes.CONSOLE
        self.__format = ''

    def __matcher(self, priority, message):
        def replacer(match):
            if match.group() == '%m':
                return message
            elif match.group() == '%d':
                return str(datetime.now().date())
            elif match.group() == '%t':
                return str(datetime.now().time())
            elif match.group() == '%p':
                return priority.name

        return replacer

    def __log(self, priority, message):
        row = re.sub(r'(%m|%d|%t|%p)', self.__matcher(priority, message), self.__format)
        if self.__outputMode is OutputModes.CONSOLE:
            print(row)
        elif self.__outputMode is OutputModes.FILE:
            try:
                with open(self.filename, 'a+', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(row.split(' '))
            except:
                print(sys.exc_info())
        else:
            raise 'Desired output mode is not supported'

    def setFormat(self, format):
        self.__format = str(format)

    def trace(self, message):
        self.__log(LogLevels.TRACE, message)

    def error(self, message):
        self.__log(LogLevels.ERROR, message)

    def info(self, message):
        self.__log(LogLevels.INFO, message)
