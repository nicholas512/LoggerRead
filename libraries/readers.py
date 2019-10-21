from abc import ABCMeta, abstractmethod
from datetime import datetime
import pandas as pd
import re

"""
Standard vocabulary
Timestamp
"""

class AbstractReader(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.DATA = []
        self.META = []
        self.DATEFMT = None

    @abstractmethod
    def read(self, file):
        """read data from a file"""

class FG2(AbstractReader):
    def read(self, file):
        pass


class GP5W(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"

    def read(self, file):
        with open(file, 'r') as f:
            for line in f:
                if re.search("No,Time", line):
                    delimiters = line.count(",")
                    columns = line.strip().split(',')

                elif re.search("\d*,\d{2}\.\d{2}\.\\d{4}", line):
                    line = line.strip()
                    line += "," * (delimiters - line.count(","))
                    self.DATA.append(line.split(','))

                else:
                    self.META.append(line)

        self.DATA = pd.DataFrame(self.DATA, columns = columns)
        self.DATA['Time'] = pd.to_datetime(self.DATA['Time'], format=self.DATEFMT)

"""if __name__ == "__main__":
    x = GP5W()

    x.read(r"C:\Users\Nick\src\Pyrmafrost\data\GP5W_270.csv")
    a = x.DATA
    #del(x)
    y = GP5W()
    y.read(r"C:\Users\Nick\src\Pyrmafrost\data\GP5W.csv")
    b = y.DATA"""