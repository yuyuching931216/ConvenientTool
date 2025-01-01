import os
import json
from mcdreforged.api.all import *
from typing import Dict

class Command_Data(Serializable):
    name: str
    command: str
    permission: int = 0	
    description: str = ""

class MC_Command:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.command_init()
        
    def command_init(self):
        self.command_list: Dict[str, Command_Data] = {}
        file_path = os.path.join(self.server.get_data_folder(), "MC_command.json")
        if not os.path.exists(file_path):
            self.new_commandFile()

        with open(file_path, "r", encoding="utf-8") as command_file:
            command_data = json.load(command_file)
            for command in command_data:
                if self.command_check(command):
                    self.command_list[command["name"]] = Command_Data.deserialize(command)
                else:
                    raise ValueError(f"MC_Command.json is not valid")
                    
    def command_check(self, command: dict):
        if command.get("name") is None:
            return False
        if command.get("command") is None:
            return False
        if command.get("command")[0] != "/":
            command["command"] = "/" + command["command"]
        return True
    
    def new_commandFile(self):
        file_path = os.path.join(self.server.get_data_folder(), "MC_command.json")
        with open(file_path, "w") as command_file:
            json.dump("[]", command_file)
