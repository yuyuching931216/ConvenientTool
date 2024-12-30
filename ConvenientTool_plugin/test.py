import json
from MCDR_Testing.testing_plugin.MCDR_command import MCDR_Command

def command_init():
    with open("./MCDR_Testing/testing_plugin/MCDR_command.json", "r") as command_file:
        command_data = json.load(command_file)
        print(command_data.keys())
        print(type(command_data))
        for command in command_data:
            command_list[command] = MCDR_Command.deserialize(command_data[command])
                
command_init()

print(command_list)
print(command_list["help"].command_description)

def command_init(self):
        file_path = self.server.open_bundled_file("MCDR_command.json")
        with open(file_path, "r") as command_file:
            command_data = json.load(command_file)
            for command in command_data:
                if self.command_check(command_data[command]):
                    self.command_list[command] = MCDR_Command(command_data[command])
                else:
                    self.server.logger.error(f"Command {command} is not valid")
                    
def command_check(self, command: dict):
    if command.get("name") is None:
        return False
    if command.get("command") is None:
        return False
    return True