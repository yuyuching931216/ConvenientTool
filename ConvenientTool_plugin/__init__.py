from mcdreforged.api.all import *
from testing_plugin.MCDR_command import MCDR_CommandManeger

MCDR_server: PluginServerInterface
config = {
    "Prefix": "!!CT",
    "Command execute Permission": 0,
    "Command setting Permission": 3
}

def on_load(server: PluginServerInterface, old):
    command_manager = MCDR_CommandManeger(server)
    global MCDR_server
    MCDR_server = server
    
def save_config():
    MCDR_server.save_config_simple(config)
