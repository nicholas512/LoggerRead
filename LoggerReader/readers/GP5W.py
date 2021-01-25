
import pandas as pd
import re

from .AbstractReader import AbstractReader


class GP5W(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"

    def read(self, file):
        self.META['raw'] = list()
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
                    self.META['raw'].append(line)

        self.DATA = pd.DataFrame(self.DATA, columns=columns)
        self.DATA["Time"] = pd.to_datetime(self.DATA["Time"], format=self.DATEFMT)
        self.DATA = self.DATA.drop(["No"], axis=1)

        return self.DATA

    def _is_observation(self, line):
        return re.search(r"\d*,\d{2}\.\d{2}\.\d{4}", line)

    def _is_header(self, line):
        return re.search("No,Time", line)
