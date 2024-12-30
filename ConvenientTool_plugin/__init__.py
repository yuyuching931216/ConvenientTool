from mcdreforged.api.all import *
from MCDR_command import MCDR_CommandManeger
from MC_command import MC_Command
from typing import Dict, Any
import json
import os

simple_config = {
    "Prefix": "!!CT",
    "MCDR Command Permission Level": 0
}

MCDR_server: PluginServerInterface
command_manager: MCDR_CommandManeger
mc_command: MC_Command
config: Dict[str, Any] = simple_config.copy()

def tr(key: str) -> str:
    return ServerInterface.get_instance().tr(f'ConvenientTool_plugin.{key}')

def on_load(server: PluginServerInterface, old):
    global MCDR_server, command_manager, mc_command
    MCDR_server = server
    get_config()
    mc_command = MC_Command(server)
    command_manager = MCDR_CommandManeger(server, mc_command)
    command_manager.register_command()

def get_config():
    global config, MCDR_server, simple_config
    MCDR_server.load_config_simple(config, simple_config)