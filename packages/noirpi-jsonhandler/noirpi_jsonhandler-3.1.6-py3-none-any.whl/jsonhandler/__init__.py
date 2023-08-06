import json
import os
import traceback
import typing
from pathlib import Path
from random import randint
from typing import Dict


def validate(data: Dict):
    """
    Verifies json dict is readable
    :param data: json formatted data to validate
    """
    tmp_file = "./{}.tmp".format(randint(1000, 9999))
    with open(tmp_file, encoding='utf-8', mode="w") as f:
        json.dump(data, f, indent=4, sort_keys=True, separators=(',', ' : '))
    try:
        with open(tmp_file, encoding='utf-8', mode="r") as f:
            json.loads(f.read())
        os.remove(tmp_file)
        return True
    except json.decoder.JSONDecodeError as error:
        traceback.print_exception(type(error), error, error.__traceback__)
        os.remove(tmp_file)
        return False


class FileIO:
    def __init__(self, filepath: str, value=None):
        """
        Opens the file or creates the file with the given value
        :param filepath: Path to the file
        :param value: value if the file gets created. If None its an empty dict
        """
        self.filepath = filepath
        try:
            self.data = json.load(open(self.filepath, 'r', encoding='utf-8'))
        except FileNotFoundError:
            value = value if value else {}
            path, filename = filepath.rsplit('/', 1)
            Path(path).mkdir(parents=True, exist_ok=True)
            self.replace(value)
            self.data = value

    def __setitem__(self, key, value):
        """
        Sets a key to a value in the file
        :param key: key for the dict
        :param value: value for the dict
        :return:
        """
        keys = key if isinstance(key, tuple) else [key]
        _dict = self.data
        for part in keys:
            try:
                if part == keys[-1]:
                    _dict[part] = value
                elif not isinstance(_dict[part], dict):
                    _dict[part] = {}
                    _dict = _dict[part]
                else:
                    _dict = _dict[part]
            except KeyError:
                _dict[part] = {}
                _dict = _dict[part]
        self.save()
        return True

    def __getitem__(self, item):
        """
        Gets a value out of the file
        :param item: the keys to that specific value
        :return:
        """
        items = item if isinstance(item, tuple) else [item]
        _dict = self.data
        for part in items:
            _dict = _dict[part]
        return _dict

    def __delitem__(self, item):
        """
        Deletes a value out of the file
        :param item: the keys to that specific value
        :return:
        """
        items = item if isinstance(item, tuple) else [item]
        _dict = self.data
        for part in items:
            if part == items[-1]:
                _dict.pop(part)
            else:
                _dict = _dict[part]
        return _dict

    def __call__(self):
        """
        Returns the file data
        :return:
        """
        return self.data

    def __str__(self):
        """
        Prints you the Filepath of the given file
        :return:
        """
        return f"Filepath: {self.filepath}"

    def is_valid_json(self):
        """Verifies if json file exists / is readable"""
        try:
            self.read()
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return False

    def read(self):
        """internally used function to read a json File"""
        with open(self.filepath, encoding='utf-8', mode="r") as f:
            return json.loads(f.read())

    # noinspection PySameParameterValue
    def replace(self, data):
        """
        Replaces the data of the json with the given data
        :param data: json formatted data to replace
        """
        if validate(data):
            with open(self.filepath, encoding='utf-8', mode="w") as f:
                json.dump(data, f, indent=4, sort_keys=True, separators=(',', ' : '))
            return True

    def save(self):
        """Automically saves json file"""
        with open(self.filepath, encoding='utf-8', mode="w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True, separators=(',', ' : '))
            return True

    def delete(self, keys: typing.Union[tuple, str]):
        """
        Deletes a key from the json file
        :param keys: tuple of path and string of single key to delete
        """
        items = keys if isinstance(keys, tuple) else [keys]
        _dict = self.data
        for part in items:
            if part == items[-1]:
                _dict.pop(part)
            else:
                _dict = _dict[part]
        return self.save()
