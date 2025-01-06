#MCDR-ConvenientTool
--------------------

一個專門為了自己的伺服器而寫的插件

需要 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)  版本`v2.1.0` 以上

##命令說明

`!!CT` 顯示歡迎訊息

`!!CT help` 顯示幫助訊息

`!!CT reload` 重載此插件

`!!CT list` 列出所有指令

`!!CT run <command_name>` 執行名稱為`<command_name>`的指令集

`!!CT skull <player_name>` 獲得名稱為`<command_name>`的玩家頭顱

##配置文件

配置文件位於`./config/convenient_tool_plugin/convenient_tool.json`

#### `Prefix`

插件指令預設前綴

預設為`!!CT`

#### `MCDR Command Permission Level`

插件指令的執行權限

預設為`1`

## Minecraft指令集

自訂指令文件位於`./config/convenient_tool_plugin/MC_command.json`

指令格式為

```
{
  "name": "指令名稱",
  "command": "指令內容",
  "permission": 需要權限,
  "description": "指令敘述"
}
```
#### `name`

指令的名稱，也是執行`run`指令的輸入參數，不得為空，也不得重複

#### `command`

欲執行的Minecraft指令內容，可以為`str`或是`list`，不得為空

#### `permission`

執行者的Minecraft權限需求，預設為`0`

#### `description`

指令的介紹，預設為空
