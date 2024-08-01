import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, C2CMessage, Message

from script.weather import weather_search
from script.event import is_group_message, group_event_ids
import script.tarot.tarot_card as tarot

test_config = read(os.path.join(os.path.dirname(__file__), "./config/config.yaml"))

_log = logging.get_logger()


# Define a custom command decorator
def CustomCommand(name):
    def decorator(func):
        async def wrapper(api, message: GroupMessage, c2cmessage: C2CMessage, params=None):
            # 检查哪个消息对象是有效的，并执行相应的函数
            if message and name in message.content:
                await func(api, message=message, c2cmessage=c2cmessage, params=params)
            elif c2cmessage and name in c2cmessage.content:
                await func(api, message=message, c2cmessage=c2cmessage, params=params)

        return wrapper

    return decorator


@CustomCommand('菜单')
async def menu(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.info("menu")
    if message:
        await message.reply(content='正在开发中')
        _log.warning(f"收到的params是：{params}")
    elif c2cmessage:
        await c2cmessage.reply(content='正在开发中')


@CustomCommand('天气')
async def weather(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.info("天气")
    weather_output = await weather_search(params)
    if weather_output:
        if message:
            await message.reply(content=weather_output)
        elif c2cmessage:
            await c2cmessage.reply(content=weather_output)
    else:
        error_msg = "未能获取天气信息, 请检查查询格式，格式为 天气 + 地区（需要带省市县后缀）"
        if message:
            await message.reply(content=error_msg)
        elif c2cmessage:
            await c2cmessage.reply(content=error_msg)


@CustomCommand('塔罗牌')
async def tarot_card(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.warning(message.event_id if message else c2cmessage.event_id)
    if message and is_group_message(message.event_id, group_event_ids):
        output_tarot = await tarot.tarot_card()
        if output_tarot:
            media = await api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=output_tarot['image_url']
            )
            await api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                content=output_tarot['output_text'],
                media=media,
            )
    elif c2cmessage:
        output_tarot = await tarot.tarot_card()
        if output_tarot:
            media = await api.post_c2c_file(
                openid=c2cmessage.author.user_openid,
                file_type=1,
                url=output_tarot['image_url']
            )
            await api.post_c2c_message(
                openid=c2cmessage.author.user_openid,
                msg_type=7,
                msg_id=message.id,
                content=output_tarot['output_text'],
                media=media,
            )


@CustomCommand('鹿')
async def sega(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    event_id = message.event_id if message else c2cmessage.event_id
    _log.warning(f"Event ID: {event_id}")
    if message and is_group_message(event_id, group_event_ids):
        media = await api.post_group_file(
            group_openid=message.group_openid,
            file_type=3,
            url="https://8q9lug.dm.files.1drv.com/y4mhi44W9yc_bjyzpTA09BvQ_2HQZzSyp_spXwkg6P-qB7tAK3Unn-XAZkIQa8Lfm9-cx7WMkZkwqfZ-j_zVxoLsU1egue52ItBZXGTHAzxfuyCGoYBjY0DeT1GR0LDIhQRtCo5ltklhMtODJHCKrpwzxRi7SUXZpEAQl7gpkc0sjxGL9aP6LLEKPR79gKyYU060LZkUWJYPcPf6vpkZ8sLKA"
        )
        await api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7,
            msg_id=message.id,
            content="sega!",
            media=media,
        )
    elif c2cmessage:
        #await c2cmessage.reply(content="请在群聊内使用")
        media = await api.post_c2c_file(
            openid=c2cmessage.author.user_openid,
            file_type=3,
            url="https://8q9lug.dm.files.1drv.com/y4mhi44W9yc_bjyzpTA09BvQ_2HQZzSyp_spXwkg6P-qB7tAK3Unn-XAZkIQa8Lfm9-cx7WMkZkwqfZ-j_zVxoLsU1egue52ItBZXGTHAzxfuyCGoYBjY0DeT1GR0LDIhQRtCo5ltklhMtODJHCKrpwzxRi7SUXZpEAQl7gpkc0sjxGL9aP6LLEKPR79gKyYU060LZkUWJYPcPf6vpkZ8sLKA"
        )
        await c2cmessage.reply(content="sega!", msg_seq="2")
        await api.post_c2c_message(
            openid=c2cmessage.author.user_openid,
            msg_type=7,
            msg_id=c2cmessage.id,
            media=media,
            msg_seq="3",
        )


######################################################################################

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"Robot 「{self.robot.name}」 is ready!")

    async def on_group_at_message_create(self, message: Message):
        _log.info(f"Received group message: {message.content}")
        content = message.content.strip()
        if content:
            prefix = ''  # Define the command prefix, adjust as needed
            if content.startswith(prefix):
                command, *params = content[len(prefix):].split(maxsplit=1)
                params = params[0] if params else []

                _log.info(f"Received command: {command}, with params: {params}")

                handlers = [weather, menu, tarot_card, sega]
                for handler in handlers:
                    await handler(api=self.api, message=message, c2cmessage=None, params=params)
        else:
            _log.warning(f"Received empty message")

    async def on_c2c_message_create(self, message: Message):
        _log.info(f"Received c2cMessage message: {message.content}")
        content = message.content.strip()
        if content:
            prefix = ''
            if content.startswith(prefix):
                command, *params = content[len(prefix):].split(maxsplit=1)
                params = params[0] if params else []

                _log.info(f"Received command: {command}, with params: {params}")

                handlers = [weather, menu, tarot_card, sega]
                for handler in handlers:
                    await handler(api=self.api, c2cmessage=message, message=message, params=params)
        else:
            _log.warning(f"Received empty message")


if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    _log.info("Starting bot...")
    client.run(appid=test_config["appid"], secret=test_config["secret"])
