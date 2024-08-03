import os
from logging import Logger

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, C2CMessage
from botpy.logging import DEFAULT_FILE_HANDLER

from script import msg_send


# 读取配置文件
def load_config():
    test_config = read(os.path.join(os.path.dirname(__file__), "config/config.yaml"))
    return test_config


config = load_config()

# 日志记录器
_log: Logger = logging.get_logger()
# 修改日志路径
DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")


# 自定义客户端类
class MyClient(botpy.Client):
    handlers = [
        msg_send.weather,
        msg_send.menu,
        msg_send.tarot_card,
        msg_send.sega,
        msg_send.help_command,
        msg_send.why_show_cry,
        msg_send.why_show_cry2,
        msg_send.group_manner,
    ]

    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」 准备就绪!")

    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(f"收到群聊消息: {message.content}")
        content = message.content.strip()
        if content:
            prefix = ''  # Define the command prefix, adjust as needed
            if content.startswith(prefix):
                command, *params = content[len(prefix):].split(maxsplit=1)
                params = params[0] if params else []

                _log.info(f"收到命令: {command}, 携带指令: {params}")

                for handler in self.handlers:
                    await handler(api=self.api, message=message, c2cmessage=None, params=params)
        else:
            _log.warning(f"收到空消息")

    async def on_c2c_message_create(self, message: C2CMessage, ):
        _log.info(f"收到私聊消息: {message.content}")
        content = message.content.strip()
        if content:
            prefix = ''
            if content.startswith(prefix):
                command, *params = content[len(prefix):].split(maxsplit=1)
                params = params[0] if params else []

                _log.info(f"收到命令: {command}, 携带指令: {params}")

                for handler in self.handlers:
                    await handler(api=self.api, c2cmessage=message, message=None, params=params)
        else:
            _log.warning(f"收到空消息")


# 程序入口
if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    _log.info("启动机器人...")
    client.run(appid=config["appid"], secret=config["secret"])
