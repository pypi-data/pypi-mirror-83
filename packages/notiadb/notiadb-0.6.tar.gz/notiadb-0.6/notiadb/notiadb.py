import ast
import json

"""
~Project
Author: Kyshi (https://kyshi.github.io)
License: MIT
Version: 0.6
Status: alpha
Github: https://github.com/kyshi/NotiaDB

~Features (version 0.6 | alpha)
Added information section in main code.
Added logical operations in filter().
Added return dictionary feature in filter().
Both dictionary and str taking feature added to update() (It used to take str only in dictionary form.)
If in first line, writeNl() doesn't put newline character.
Removed key parameter in update(), key will to be set by the key of kwargs now.
Recommended parameter types set.
Fixed bugs.
"""


class NotiaDB:
    """
        -Write Operations
        *Methods
            -write: Writes to file, if file doesn't exist create a new the file
            -startFromScratch: Start from scratch.
            -update: Updates a value connected of key

        -Read Operations
        *Methods
            -read: Reads the file
            -readKeys: Reads only keys in the file
            -readValues: Reads only values in the file
            -readFile: Reads all the
            -filter(key, conditions): Returns the dictionary with the desired key and value, returns a list if there is
            more than one value to return
    """

    def __init__(self, file_name: str, auto_id: bool = False):
        self.name = file_name
        f = open(f"{self.name}.ndb", "a", encoding="utf8")
        f.close()
        self.id = self.readFile().count("'id'") + 1
        self.auto_id = auto_id

    def write(self, **kwargs):
        with open(f"{self.name}.ndb", "a", encoding="utf8") as f:
            f.seek(0)
            data = self.readFile()
            if data == "File is Empty":
                if self.auto_id:
                    f.write(str(kwargs)[:1] + f"'id': {self.id}, " + str(kwargs)[1:])
                    self.id += 1
                else:
                    f.write(str(kwargs))
            else:
                data = data.replace("}", ",")
                with open(f"{self.name}.ndb", "w"):
                    f.write(data + str(kwargs).replace("{", " "))

    def writeNl(self, **kwargs):
        with open(f"{self.name}.ndb", "a", encoding="utf8") as f:
            f.seek(0)
            f.seek(len(self.readFile()))
            if self.auto_id:
                if self.id != 1:  # If in first line
                    f.write("\n" + str(kwargs)[:1] + f"'id': {self.id}, " + str(kwargs)[1:])
                else:
                    f.write(str(kwargs)[:1] + f"'id': {self.id}, " + str(kwargs)[1:])
                self.id += 1
            else:
                if f.readline() != "":  # If in first line
                    f.write("\n" + str(kwargs))
                else:
                    f.write("\n" + str(kwargs))

    def filter(self, key: str or int, condition: str):
        with open(f"{self.name}.ndb", "r") as f:
            result = list()
            all_data = f.readlines()
            for data in all_data:
                exec(f"if ast.literal_eval(data)[key] {condition.split(' ')[0]} {condition.split(' ')[1]}: "
                     f"result.append(ast.literal_eval(data))")
            if len(result) > 1:
                return result
            elif len(result) == 1:
                return result[0]

    def startFromScratch(self, **kwargs):
        with open(f"{self.name}.ndb", "w", encoding="utf8") as f:
            f.write(str(kwargs))

    def update(self, data: str or dict, **kwargs):
        data_dict = dict()
        key = list(kwargs.keys())[0]
        if type(data) == str:
            data = data
            data_dict = ast.literal_eval(data)
        elif type(data) == dict:
            data_dict = data  # data already dict.
            data = json.dumps(data)  # data converted dict.
            # ! Tek tırnaklar çift tırnağa çevrilmedi
            data = data.replace("\"", "$").replace("\'", "\"").replace("$", "'")  # Quotation marks corrected. Because break down place of quotation marks.
        file = self.readFile().split(data)
        with open(f"{self.name}.ndb", "w", encoding="utf8") as f:
            if type(data_dict[key]) == str:
                f.seek(0)
                index = data.index(f"'{key}':")
                data_start = data[0:index + len(key) + 5]
                data_last = data[index + len(key) + 5 + len(data_dict[key]):]
                f.write(file[0])
                f.write(f"{data_start}{kwargs[key]}{data_last}")
                f.write(file[1])
            elif type(data_dict[key]) == int:
                f.seek(0)
                index = data.index(f"'{key}':")
                data_start = data[0:index + len(key) + 4]
                data_last = data[index + len(key) + 4 + len(str(data_dict[key])):]
                f.write(f"{data_start}{kwargs[key]}{data_last}")

    def read(self, key: str or int):
        with open(f"{self.name}.ndb", "r", encoding="utf8") as f:
            f.seek(0)
            if len(f.read()) > 0:
                f.seek(0)
                data = f.read()
                data_dict = ast.literal_eval(data)
                return data_dict[key]
            else:
                return "File is Empty"

    def readKeys(self):
        if len(self.readFile()) > 0:
            data = self.readFile()
            data_dict = ast.literal_eval(data)
            return data_dict.keys()
        else:
            return "File is Empty"

    def readValues(self):
        if len(self.readFile()) > 0:
            data = self.readFile()
            data_dict = ast.literal_eval(data)
            return data_dict.values()
        else:
            return "File is Empty"

    def readFile(self):
        with open(f"{self.name}.ndb", "r", encoding="utf8") as f:
            f.seek(0)
            if len(f.read()) > 0:
                f.seek(0)
                data = f.read()
                return data
            else:
                return "File is Empty"
