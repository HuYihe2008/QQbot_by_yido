import os
import botpy
import asyncio
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage, C2CMessage
from pyppeteer import launch
from script.weather import weather_search

test_config = read(os.path.join(os.path.dirname(__file__), "./config/config.yaml"))

_log = logging.get_logger()

@Commands('菜单')
async def menu(api: botpy.BotAPI, message: GroupMessage, params=None):
    _log.info(f"menu")
    if message:
        await message.reply(content=f'正在开发中')
        _log.warning(f"收到的params是：{params}")
@Commands('天气')
async def weather(api: botpy.BotAPI, message: GroupMessage, params=None):
    _log.info(f"天气")
    # 调用 weather_search 函数并接收返回值
    weather_output = await weather_search(params)
    if weather_output:  # 检查是否有返回值
        await message.reply(content=weather_output)  # 使用返回值作为回复内容
    else:
        await message.reply(content="未能获取天气信息")












######################################################################################

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"Robot 「{self.robot.name}」 is ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(f"Received group message: {message.content}")
        content = message.content.strip()
        if content.startswith(''):
            command, *params = content[1:].split(maxsplit=1)
            params = params[0].split() if params else []

            _log.info(f"Received command: {command}, with params: {params}")

            handlers = [weather, menu]
            for handler in handlers:
                if await handler(api=self.api, message=message, params=params):
                    _log.info(f"Handler {handler.__name__} processed the message.")
                    return
        else:
            _log.warning(f"Received non-command message: {content}")   
    async def on_c2c_message_create(self, message: C2CMessage):
        _log.info(f"Received c2cMessage message: {message.content}")
        content = message.content.strip()
        if content.startswith(''):
            command, *params = content[1:].split(maxsplit=1)
            params = params[0].split() if params else []

            _log.info(f"Received command: {command}, with params: {params}")

            handlers = [weather, menu]
            for handler in handlers:
                if await handler(api=self.api, message=message, params=params):
                    _log.info(f"Handler {handler.__name__} processed the message.")
                    return
        else:
            _log.warning(f"Received non-command message: {content}")   
if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    _log.info("Starting bot...")
    client.run(appid=test_config["appid"], secret=test_config["secret"])
