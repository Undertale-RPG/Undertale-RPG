import json
import logging
import os
from random import randint


class InvalidFileIO(Exception):
    pass


class DataIO:
    def __init__(self):
        self.logger = logging.getLogger("red")

    def load_json(self, filename):
        """Loads json file"""
        return self._read_json(filename)

    def _read_json(self, filename):
        with open(filename, encoding="utf-8", mode="r") as f:
            data = json.load(f)
        return data

    def _legacy_fileio(self, filename, IO, data=None):
        """Old fileIO provided for backwards compatibility"""
        if IO == "load" and data is None:
            return self.load_json(filename)
        elif IO == "check" and data is None:
            return self.is_valid_json(filename)
        else:
            raise InvalidFileIO("FileIO was called with invalid" " parameters")


def get_value(filename, key):
    with open(filename, encoding="utf-8", mode="r") as f:
        data = json.load(f)
    return data[key]


def set_value(filename, key, value):
    data = fileIO(filename, "load")
    data[key] = value
    fileIO(filename, "save", data)
    return True


dataIO = DataIO()
fileIO = dataIO._legacy_fileio  # backwards compatibility
