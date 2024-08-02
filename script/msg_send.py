import os
from logging import Logger

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, C2CMessage

from features.weather.weather import weather_search
from utils.event import is_group_message, group_event_ids
import features.tarot.tarot_card as tarot


# 读取配置文件
def load_config():
    test_config = read(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))
    return test_config


config = load_config()

# 日志记录器
_log: Logger = logging.get_logger()


# 自定义命令装饰器
def CustomCommand(name, ignore_commands=None):
    if ignore_commands is None:
        ignore_commands = []

    def decorator(func):
        async def wrapper(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
            # 检查是否为指定的命令，且参数不以忽略的命令开头
            if (message and message.content.strip().lower().startswith(f"{name}")) or \
                    (c2cmessage and c2cmessage.content.strip().lower().startswith(f"{name}")):
                if params and any(params.lower().startswith(f"{cmd}") for cmd in ignore_commands):
                    return  # 如果参数以忽略的命令开头，则不执行函数
                await func(api, message=message, c2cmessage=c2cmessage, params=params)
            elif (message and message.content.strip().lower().startswith(f"/{name}")) or \
                    (c2cmessage and c2cmessage.content.strip().lower().startswith(f"/{name}")):
                if params and any(params.lower().startswith(f"/{cmd}") for cmd in ignore_commands):
                    return  # 如果参数以忽略的命令开头，则不执行函数
                await func(api, message=message, c2cmessage=c2cmessage, params=params)

        return wrapper

    return decorator


# 菜单命令
@CustomCommand('菜单')
async def menu(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.info("菜单命令被调用")
    if message:
        _log.warning(f"发送菜单信息到群聊：{message.group_openid}")
        await message.reply(content='菜单功能正在开发中...（群聊）')
    elif c2cmessage:
        _log.warning(f"发送菜单信息到私聊：{c2cmessage.author.user_openid}")
        await c2cmessage.reply(content='菜单功能正在开发中...（私聊）')


# 天气命令
@CustomCommand('天气')
async def weather(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.info("天气命令被调用")
    try:
        weather_output = await weather_search(params)
        if weather_output:
            if message:
                await message.reply(content=weather_output)
                _log.warning(f"发送天气信息到群聊：{message.group_openid}")
            elif c2cmessage:
                await c2cmessage.reply(content=weather_output)
                _log.warning(f"发送天气信息到私聊：{c2cmessage.author.user_openid}")
        else:
            error_msg = "未能获取天气信息，请检查查询格式。"
            if message:
                await message.reply(content=error_msg)
                _log.warning(f"发送错误信息到群聊：{message.group_openid}")
            elif c2cmessage:
                await c2cmessage.reply(content=error_msg)
                _log.warning(f"发送错误信息到私聊：{c2cmessage.author.user_openid}")
    except Exception as e:
        _log.error(f"获取天气信息失败: {e}")
        error_msg = "获取天气信息时发生错误，请稍后再试。"
        if message:
            await message.reply(content=error_msg)
            _log.warning(f"发送错误信息到群聊：{message.group_openid}")
        elif c2cmessage:
            await c2cmessage.reply(content=error_msg)
            _log.warning(f"发送错误信息到私聊：{c2cmessage.author.user_openid}")


# 塔罗牌命令
@CustomCommand('塔罗牌')
async def tarot_card(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    _log.warning(f"塔罗牌命令调用，事件ID: {message.event_id if message else c2cmessage.event_id}")
    try:
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
                _log.warning(f"发送塔罗牌到群聊：{message.group_openid}")
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
                    msg_id=c2cmessage.id,
                    content=output_tarot['output_text'],
                    media=media,
                )
                _log.warning(f"发送塔罗牌到私聊：{c2cmessage.author.user_openid}")
    except Exception as e:
        _log.error(f"塔罗牌命令失败: {e}")


# 鹿命令
@CustomCommand('鹿')
async def sega(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    event_id = message.event_id if message else c2cmessage.event_id
    _log.warning(f"鹿命令调用，事件ID: {event_id}")
    try:
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
            _log.warning(f"发送鹿到群聊：{message.group_openid}")
        elif c2cmessage:
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
            _log.warning(f"发送鹿到私聊：{c2cmessage.author.user_openid}")
    except Exception as e:
        _log.error(f"鹿命令失败: {e}")


@CustomCommand('为什么要弹春日影')
async def why_show_cry(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    event_id = message.event_id if message else c2cmessage.event_id
    _log.warning(f"春日影命令调用，事件ID: {event_id}")
    try:
        if message and is_group_message(event_id, group_event_ids):
            media = await api.post_group_file(
                group_openid=message.group_openid,
                file_type=3,
                url="https://raw.gitcode.com/yido/QQbot_by_yido/blobs/642b82d971fd8369f37b8138706468d096043179/MyGO!!!!!%20-%20%E6%98%A5%E6%97%A5%E5%BD%B1.silk"
            )
            media2 = await api.post_group_file(
                group_openid=message.group_openid,
                file_type=3,
                url="https://raw.gitcode.com/yido/QQbot_by_yido/blobs/381b85f63a9acab7f290c9bd2f966ddfb506a3cc/%E7%A9%BA%E3%81%AE%E7%AE%B1.silk"
            )
            await message.reply(content="为什么要演奏春日影!", msg_seq="2")
            await api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                content="为什么要演奏春日影!",
                media=media,
                msg_seq=3
            )
            await api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=media2,
                msg_seq=4
            )
            user = await api.me()
            _log.warning(f"发送春日影到群聊：{message.group_openid},{user['username']}")
        elif c2cmessage:
            media = await api.post_c2c_file(
                openid=c2cmessage.author.user_openid,
                file_type=3,
                url="https://9k9lug.dm.files.1drv.com/y4muLe3LLY-vdvZSHWjcimBNu19CztWfmtlhXiiPn-poC-XS2TpTEGsB-QiGcnMOo1pCkiv5UMIjlG6LSUXsegYs5naiP6CRRtJIksLJIhk_hscHw-5LdQa5zpCqYG_dUqBmwiuaSslMA5nA-3b4hs-Oc6V_rXDMXiYK43LtLFIkXpx1fJfoXXXOmFRQOv_DppHWajjhu3AHVvC_O9TsiX-gQ"
            )
            media2 = await api.post_c2c_file(
                openid=c2cmessage.author.user_openid,
                file_type=3,
                url="https://869lug.dm.files.1drv.com/y4m5lC9o9y4OYs5ElROxAstmnjxtM9VJbllbnEfG0vx6dsZZVNaIWcLup-IjH1hcC-7KC9AWIhKTleKMogkw80lgwosEtL7rg6gWJuwTC_z7oUtYUOJlylFY4BrljFw-NEIdcZRm96jJZ5w7A4hagxqxde8R6Z3HE6mf5V_m0-RM8aM2PlhaqSazdktNV7-cFCHsyp59wGAZa2p94Y5AteshQ"
            )
            await c2cmessage.reply(content="为什么要演奏春日影!", msg_seq="2")
            await api.post_c2c_message(
                openid=c2cmessage.author.user_openid,
                msg_type=7,
                msg_id=c2cmessage.id,
                media=media,
                msg_seq="3",
            )
            await api.post_c2c_message(
                openid=c2cmessage.author.user_openid,
                msg_type=7,
                msg_id=c2cmessage.id,
                media=media2,
                msg_seq="4",
            )
            user = await api.me()
            _log.warning(f"{user}")
            _log.warning(f"发送春日影到私聊：{user['username']}")
    except Exception as e:
        _log.error(f"春日影命令失败: {e}")


@CustomCommand('为什么要演奏春日影')
async def why_show_cry2(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    event_id = message.event_id if message else c2cmessage.event_id
    _log.warning(f"春日影命令调用，事件ID: {event_id}")
    try:
        if message and is_group_message(event_id, group_event_ids):
            media = await api.post_group_file(
                group_openid=message.group_openid,
                file_type=3,
                url="https://9k9lug.dm.files.1drv.com/y4muLe3LLY-vdvZSHWjcimBNu19CztWfmtlhXiiPn-poC-XS2TpTEGsB-QiGcnMOo1pCkiv5UMIjlG6LSUXsegYs5naiP6CRRtJIksLJIhk_hscHw-5LdQa5zpCqYG_dUqBmwiuaSslMA5nA-3b4hs-Oc6V_rXDMXiYK43LtLFIkXpx1fJfoXXXOmFRQOv_DppHWajjhu3AHVvC_O9TsiX-gQ"
            )
            media2 = await api.post_group_file(
                group_openid=message.group_openid,
                file_type=3,
                url="https://869lug.dm.files.1drv.com/y4m5lC9o9y4OYs5ElROxAstmnjxtM9VJbllbnEfG0vx6dsZZVNaIWcLup-IjH1hcC-7KC9AWIhKTleKMogkw80lgwosEtL7rg6gWJuwTC_z7oUtYUOJlylFY4BrljFw-NEIdcZRm96jJZ5w7A4hagxqxde8R6Z3HE6mf5V_m0-RM8aM2PlhaqSazdktNV7-cFCHsyp59wGAZa2p94Y5AteshQ"
            )
            await api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                content="为什么要演奏春日影!",
                media=media,
                msg_seq=2
            )
            await api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=media2,
                msg_seq=3
            )
            _log.warning(f"发送春日影到群聊：{message.group_openid}")
        elif c2cmessage:
            media = await api.post_c2c_file(
                openid=c2cmessage.author.user_openid,
                file_type=3,
                url="https://9k9lug.dm.files.1drv.com/y4muLe3LLY-vdvZSHWjcimBNu19CztWfmtlhXiiPn-poC-XS2TpTEGsB-QiGcnMOo1pCkiv5UMIjlG6LSUXsegYs5naiP6CRRtJIksLJIhk_hscHw-5LdQa5zpCqYG_dUqBmwiuaSslMA5nA-3b4hs-Oc6V_rXDMXiYK43LtLFIkXpx1fJfoXXXOmFRQOv_DppHWajjhu3AHVvC_O9TsiX-gQ"
            )
            media2 = await api.post_c2c_file(
                openid=c2cmessage.author.user_openid,
                file_type=3,
                url="https://869lug.dm.files.1drv.com/y4m5lC9o9y4OYs5ElROxAstmnjxtM9VJbllbnEfG0vx6dsZZVNaIWcLup-IjH1hcC-7KC9AWIhKTleKMogkw80lgwosEtL7rg6gWJuwTC_z7oUtYUOJlylFY4BrljFw-NEIdcZRm96jJZ5w7A4hagxqxde8R6Z3HE6mf5V_m0-RM8aM2PlhaqSazdktNV7-cFCHsyp59wGAZa2p94Y5AteshQ"
            )
            await c2cmessage.reply(content="为什么要演奏春日影!", msg_seq="2")
            await api.post_c2c_message(
                openid=c2cmessage.author.user_openid,
                msg_type=7,
                msg_id=c2cmessage.id,
                media=media,
                msg_seq="3",
            )
            await api.post_c2c_message(
                openid=c2cmessage.author.user_openid,
                msg_type=7,
                msg_id=c2cmessage.id,
                media=media2,
                msg_seq="4",
            )
            _log.warning(f"发送春日影到私聊：{c2cmessage.author.user_openid}")
    except Exception as e:
        _log.error(f"春日影命令失败: {e}")


# 帮助命令
@CustomCommand('帮助')
async def help_command(api: botpy.BotAPI, message: GroupMessage, c2cmessage: C2CMessage, params=None):
    help_text = """可用命令列表：
    - 💩菜单：显示菜单
    - 🌥️天气：查询天气信息
    - 🃏塔罗牌：抽取塔罗牌
    - 🦌鹿：小彩蛋
    - 🎸为什么要弹春日影/为什么要演奏春日影：小彩蛋2"""
    if message:
        await message.reply(content=help_text)
        _log.info(f"发送帮助信息到群聊：{message.group_openid}")
    elif c2cmessage:
        await c2cmessage.reply(content=help_text)
        _log.info(f"发送帮助信息到私聊：{c2cmessage.author.user_openid}")
