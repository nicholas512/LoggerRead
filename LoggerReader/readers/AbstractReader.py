from abc import ABCMeta, abstractmethod


class AbstractReader(object):
    __metaclass__ = ABCMeta

    def __init__(self, datefmt=None):
        self.DATA = []
        self.META = dict()
        if datefmt:
            self.DATEFMT = datefmt

    @abstractmethod
    def read(self, file):
        """read data from a file"""

    def get_data(self):
        return self.DATA
