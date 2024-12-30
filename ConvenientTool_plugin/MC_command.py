import os
import json
from mcdreforged.api.all import *
from typing import Dict

class Command_Data(Serializable):
    command_name: str
    command: str
    command_permission: int = 0	
    command_description: str = ""

class MC_Command:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.command_list: Dict[str, Command_Data] = {}
        self.command_init()
        
    def command_init(self):
        file_path = os.path.join(self.server.get_data_folder(), "MC_command.json")
        with open(file_path, "r") as command_file:
            command_data = json.load(command_file)
            for command in command_data:
                if self.command_check(command_data[command]):
                    self.command_list[command] = Command_Data(command_data[command])
                else:
                    self.server.logger.error(f"Command {command} is not valid")
                    
    def command_check(self, command: dict):
        if command.get("name") is None:
            return False
        if command.get("command") is None:
            return False
        return True
