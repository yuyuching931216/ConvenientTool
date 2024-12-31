from mcdreforged.api.all import *
from convenient_tool_plugin.MCDR_command import MCDR_CommandManeger
from convenient_tool_plugin.MC_command import MC_Command
from typing import Dict, Any
import json
import os

simple_config = {
    "Prefix": "!!CT",
    "MCDR Command Permission Level": 1
}

MCDR_server: PluginServerInterface
command_manager: MCDR_CommandManeger
mc_command: MC_Command
config: Dict[str, Any] = simple_config.copy()

def on_load(server: PluginServerInterface, old):
    global MCDR_server, command_manager, mc_command
    MCDR_server = server
    get_config()
    mc_command = MC_Command(server)
    command_manager = MCDR_CommandManeger(server, mc_command, config)
    command_manager.register_command()

def get_config():
    global config, MCDR_server, simple_config
    config = MCDR_server.load_config_simple("convenient_tool.json", simple_config)
    
def on_player_command(server: PluginServerInterface, player: str, command: str):
    if command.startswith('!!'):
        server.execute(command)
        return False
    return True