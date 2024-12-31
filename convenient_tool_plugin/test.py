import json
import os
from mcdreforged.api.all import *
                    
def command_check(self, command: dict):
    if command.get("name") is None:
        return False
    if command.get("command") is None:
        return False
    return True

def get_config():
    file_path = './command_simple_config.json'
    with open(file_path, "r") as config_file:
        return json.load(config_file)

dictionary = {}
for i in range(10):
    dictionary[i] = {"name": str(i) + "th test", "test": "test line"}

def get_commandID(dictionary: dict, command_name: str):
        for item in dictionary:
            if dictionary[item].get("name") == command_name:
                return item
        return -1

print(get_commandID(dictionary, "5th test"))
