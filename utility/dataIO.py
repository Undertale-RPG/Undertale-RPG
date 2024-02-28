import json
import logging
import os
from random import randint


class InvalidFileIO(Exception):
    pass


class DataIO:
    """Class for automatic JSON file operations.

    This class provides methods for automatic saving and loading of JSON files,
    ensuring that the original file is unaltered if an error occurs during the process.

    Attributes:
        logger (Logger): The logger instance for logging messages related to file operations.
    """
    def __init__(self):
        self.logger = logging.getLogger("red")

    def load_json(self, filename):
        """Loads JSON file"""
        return self._read_json(filename)

    def _read_json(self, filename):
        with open(filename, encoding="utf-8", mode="r") as f:
            data = json.load(f)
        return data

    def _legacy_fileio(self, filename, IO, data=None):
        """Legacy fileIO provided for backwards compatibility"""
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
    data = fileIO(filename, "load") # <-- Unused Variable in set_value function? The data variable in the set_value function is assigned the result of fileIO(filename, "load") but never used. You can omit that line if it's not necessary. Worth testing first though.
    data[key] = value
    fileIO(filename, "save", data)
    return True


dataIO = DataIO()
fileIO = dataIO._legacy_fileio  # backwards compatibility
