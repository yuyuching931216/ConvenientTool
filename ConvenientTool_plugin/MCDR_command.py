from mcdreforged.api.all import *
from typing import Callable, Optional, Dict, List
import json
import os
from MC_command import MC_Command
from __init__ import get_config, tr

class MCDR_CommandManeger:
    
    def __init__(self, server: PluginServerInterface, mc_command: MC_Command):
        self.server = server
        self.mc_command = mc_command
        self.get_config()

    def get_commandID(self, command_name: str):
        for command in self.mc_command.command_list:
            if self.mc_command.command_list[command].command_name == command_name:
                return command
        return None
    
    def cmd_welcome(self, source: PlayerCommandSource):
        source.reply(tr('text.welcome'))

    def cmd_help(self, source: PlayerCommandSource):
        source.reply(tr('text.help'))
    
    def cmd_executeCommand(self, source: PlayerCommandSource, context: CommandContext):
        name: str = context["command_name"]
        command_id = self.get_commandID(name)
        if command_id is None:
            source.reply(tr('message.command_not_found'))
            return
        self.server.execute_command(self.mc_command.command_list[command_id].command)
    
    def cmd_reload_command(self, source: PlayerCommandSource):
        self.mc_command.command_init()
        get_config()
        source.reply(tr('message.reload'))
    
    def cmd_list_command(self, source: PlayerCommandSource):
        for command in self.mc_command.command_list:
            if command.command_permission > source.get_permission_level():
                continue
            text = command.command_name + "\n" + command.command_description + "\n\n"
            source.reply(text)
                
    #TODO:
    def register_command(self):
        permission_level = self.config["Command setting Permission"]

        def Permissed_Literal(literal: Literal):
            return Literal(literal).\
                requires(lambda src: src.has_permission(permission_level)).\
                on_error(RequirementNotMet, lambda src: src.reply(tr('message.no_permission')))	


        self.server.register_command(
            Permissed_Literal(self.prefix).
            runs(self.cmd_welcome).               
            then(
                Literal("help").
                requires(lambda src: src.has_permission(PermissionLevel)).
                runs(self.cmd_help)
            ).
            then(
                Literal("execute").
                Text("command_name").
                suggests(lambda: self.mc_command.command_list.keys()).
                runs(self.cmd_executeCommand)
            ).
            then(
                Literal("reload").
                runs(self.cmd_reload_command)
            ).
            then(
                Literal("list").
                runs(self.cmd_list_command)
            )
        )

