from mcdreforged.api.all import *
from typing import Dict, Any, Union
from convenient_tool_plugin.MC_command import MC_Command, Command_Data

def tr(key: str, source: Union[CommandSource, PluginServerInterface], **kwargs) -> str:
    if type(source) == PluginServerInterface:
        return source.tr(f'ConvenientTool_plugin.{key}', **kwargs)
    else:
        with source.preferred_language_context():
            message = source.get_server().tr(f'ConvenientTool_plugin.{key}', **kwargs)
        return message

def getPlayerID(source: InfoCommandSource) -> Union[str, None]:
        if source.is_console:
            return None
        return source.get_info().player

class MCDR_CommandManeger:
    def __init__(self, server: PluginServerInterface, mc_command: MC_Command, config: Dict[str, Any]):
        self.server = server
        self.mc_command = mc_command
        self.config = config
        self.prefix = config["Prefix"]
    
    def run_command(self, source: CommandSource, command:str):
        player = getPlayerID(source)
        if "@p" in command or "@s" in command:
            if source.is_console:
                source.reply(tr('message.not_console', source))
                return
            command.replace("@p", player)
            command.replace("@s", player)
        self.server.execute(command)
        return
    
    def cmd_welcome(self, source: CommandSource):
        source.reply(tr('text.welcome', source, prefix=self.prefix))

    def cmd_help(self, source: CommandSource):
        source.reply(tr('text.help', source, prefix=self.prefix))
    
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
            source.reply(tr('message.command_execute', source) + command_id.name)
            for command_line in command_id.command:
                self.run_command(source, command_line)
    
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
            
    def cmd_getSkull(self, source: InfoCommandSource, context: CommandContext):
        if source.is_console:
            source.reply(tr('message.not_console', source))
            return
        player = getPlayerID(source)
        self.server.execute(f'/give {player} minecraft:player_head[profile={context["playerName"]}]')   
                
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
            ).
            then(
                Literal("skull").
                then(
                    Text('playerName').
                    runs(self.cmd_getSkull))
            )
        )