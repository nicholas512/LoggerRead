import pandas as pd
import re

from .AbstractReader import AbstractReader
from .HOBO import HOBO, HOBOProperties

"""
Standard vocabulary
Timestamp
"""


class FG2(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"
    DELIMITER = ","

    def read(self, file):
        with open(file, "r") as f:
            for line in f:
                if self._is_header(line):
                    delimiters = line.count(self.DELIMITER)
                    columns = line.strip().split(self.DELIMITER)

                elif self._is_observation(line):
                    line = line.strip()
                    line += self.DELIMITER * (delimiters - line.count(self.DELIMITER))
                    self.DATA.append(line.split(self.DELIMITER))

                else:
                    self.META.append(line)

        self.DATA = pd.DataFrame(self.DATA, columns=columns)
        self.DATA["TIME"] = pd.to_datetime(self.DATA["TIME"], format=self.DATEFMT)
        self.DATA = self.DATA.drop(["NO"], axis=1)

    def _is_metadata(self, line):
        return re.search("^<.*>$", line)

    def _is_observation(self, line):
        return re.search(rf"^\d*{self.DELIMITER}\d\d.\d\d", line)

    def _is_header(self, line):
        return re.search(f"NO{self.DELIMITER}TIME", line)


class GP5W(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"

    def read(self, file):
        with open(file, "r") as f:
            for line in f:
                if self._is_header(line):
                    delimiters = line.count(",")
                    columns = line.strip().split(",")

                elif self._is_observation(line):
                    line = line.strip()
                    line += "," * (delimiters - line.count(","))
                    self.DATA.append(line.split(","))

                else:
                    self.META.append(line)

        self.DATA = pd.DataFrame(self.DATA, columns=columns)
        self.DATA["Time"] = pd.to_datetime(self.DATA["Time"], format=self.DATEFMT)
        self.DATA = self.DATA.drop(["No"], axis=1)

    def _is_observation(self, line):
        return re.search(r"\d*,\d{2}\.\d{2}\.\\d{4}", line)

    def _is_header(self, line):
        return re.search("No,Time", line)


class RBR(AbstractReader):
    def read(self, file):
        raise NotImplementedError


if __name__ == "__main__":
    x = GP5W()

    x.read(r"E:\Users\Nick\Documents\src\Pyrmafrost\data\GP5W_270.csv")
    a = x.DATA

    #  del(x)
    y = GP5W()
    y.read(r"E:\Users\Nick\Documents\src\Pyrmafrost\data\GP5W.csv")
    b = y.DATA
