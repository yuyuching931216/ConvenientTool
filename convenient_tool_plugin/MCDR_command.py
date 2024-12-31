from mcdreforged.api.all import *
from typing import Dict, Any
from convenient_tool_plugin.MC_command import MC_Command, Command_Data

def tr(key: str, source: CommandSource) -> str:
    with source.preferred_language_context():
        message = source.get_server().tr(f'ConvenientTool_plugin.{key}')
        return message

class MCDR_CommandManeger:
    
    def __init__(self, server: PluginServerInterface, mc_command: MC_Command, config: Dict[str, Any]):
        self.server = server
        self.mc_command = mc_command
        self.config = config
        self.prefix = config["Prefix"]
    
    def cmd_welcome(self, source: CommandSource):
        source.reply(tr('text.welcome', source))

    def cmd_help(self, source: CommandSource):
        source.reply(tr('text.help', source))
    
    #TODO:
    def cmd_executeCommand(self, source: CommandSource, context: CommandContext):
        name = context["commandName"]
        command_id = self.mc_command.command_list.get(name)
        if command_id is None:
            source.reply(tr('message.command_not_found', source))
            return
        elif command_id.permission > source.get_permission_level():
            source.reply(tr('message.command_no_permission', source))
            return
        else:
            source.reply(tr('message.command_execute', source) + command_id.command)
            self.server.execute(command_id.command)
    
    def cmd_reload_command(self, source: CommandSource):
        self.config = self.server.load_config_simple("convenient_tool.json", self.config)
        self.mc_command.command_init()
        source.reply(tr('message.reload', source))
    
    def cmd_list_command(self, source: CommandSource):
        command_list: Dict[str, Command_Data] = {}
        for command in self.mc_command.command_list:
            if self.mc_command.command_list[command].permission > source.get_permission_level():
                continue
            command_list[command] = self.mc_command.command_list[command]
            
        if not command_list:
            source.reply(tr('message.command_list_empty', source))
            return
        
        literal_name = {}
        for literal in ["name", "command", "permission", "description"]:
            literal_name[literal] = tr('literal.' + literal, source)
        
        for command in command_list:
            text = f"§e{literal_name['name']}: §f{command_list[command].name}\n§b{literal_name['description']}: §f{command_list[command].description}\n§a{literal_name['command']}: §f{command_list[command].command}"
            
            if command != list(command_list)[-1]:
                text += "\n"
            source.reply(text)
                
    def register_command(self):
        permission_level: int = self.config["MCDR Command Permission Level"]

        def Permissed_Literal(literal: str):
            return Literal(literal).\
                requires(lambda src: src.has_permission(permission_level)).\
                on_error(RequirementNotMet, lambda src: src.reply(tr('message.no_permission', src)), handled=True)	


        self.server.register_command(
            Permissed_Literal(self.prefix).
            runs(self.cmd_welcome).               
            then(
                Literal("help").
                runs(self.cmd_help)
            ).
            then(
                Literal("run").
                then(
                    Text('commandName').
                    suggests(lambda: self.mc_command.command_list.keys()).
                    runs(self.cmd_executeCommand))
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

