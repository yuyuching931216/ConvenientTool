from mcdreforged.api.all import *
from typing import Callable, Optional, Dict, List
import json
import os


class MCDR_CommandManeger:
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.get_config()
    
    def cmd_help(self, source: PlayerCommandSource):
        pass
    
    def cmd_executeCommand(self, source: PlayerCommandSource):
        pass
    
    def cmd_add_command(self, source: PlayerCommandSource):
        pass
    
    def cmd_remove_command(self, source: PlayerCommandSource):
        pass
    
    def cmd_reload_command(self, source: PlayerCommandSource):
        pass
    
    def cmd_list_command(self, source: PlayerCommandSource):
        pass
    
    def get_config(self):
        file_path = os.path.join(self.server.get_config_folder(), "MCDR_command.json")
        with open(file_path, "r") as config_file:
            config_data = json.load(config_file)
            if "Prefix" in config_data:
                self.prefix = config_data["Prefix"]
            else:
                self.prefix = "!!CT"
                
    #TODO:
    def register_command(self):
        self.server.register_command(
            Literal(self.prefix).
            runs(self.cmd_help).               
            then(Literal("help").
                runs(self.cmd_help)
            ).
            then(Literal("execute")
            ).
            then(Literal("add")
            )
        )
