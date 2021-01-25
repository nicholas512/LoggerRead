import pandas as pd
import re

from .AbstractReader import AbstractReader


class FG2(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"
    DELIMITER = ","

    def read(self, file):
        self.META['raw'] = list()
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
                    self.META['raw'].append(line)

        self.DATA = pd.DataFrame(self.DATA, columns=columns)
        self.DATA["TIME"] = pd.to_datetime(self.DATA["TIME"], format=self.DATEFMT)
        self.DATA = self.DATA.drop(["NO"], axis=1)

        return self.DATA

    def _is_metadata(self, line):
        return re.search("^<.*>$", line)

    def _is_observation(self, line):
        return re.search(fr"^\d*{self.DELIMITER}\d\d.\d\d", line)

    def _is_header(self, line):
        return re.search(f"NO{self.DELIMITER}TIME", line)
