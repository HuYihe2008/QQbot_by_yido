import os
import botpy
import asyncio
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage, C2CMessage, Message
from pyppeteer import launch


def is_group_message(event_id, group_event_ids):
    # 检查 event_id 是否以 group_event_ids 列表中的任何字符串开头

    return any(event_id.startswith(event) for event in group_event_ids)


# 定义群聊相关的事件ID列表
group_event_ids = ["GROUP_MSG_RECEIVE", "GROUP_ADD_ROBOT", "GROUP_AT_MESSAGE_CREATE"]
