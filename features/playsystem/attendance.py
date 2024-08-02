import os
import json
from datetime import datetime
import botpy
from botpy.message import GroupMessage, C2CMessage

# 确保data目录存在
os.makedirs('./data', exist_ok=True)

# 签到记录的文件路径
attendance_file = './data/attendance.json'

# 初始化 attendance_data 为默认的JSON结构
attendance_data = {'groups': {}}

# 尝试读取签到记录的JSON文件
try:
    with open(attendance_file, 'r', encoding='utf-8') as f:
        file_content = f.read().strip()  # 读取并去除空白字符
        if file_content:  # 如果文件内容不是空白
            attendance_data = json.loads(file_content)  # 使用json.loads加载JSON数据
            if 'groups' not in attendance_data:
                raise ValueError("JSON数据缺少'groups'键")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    # 文件不存在、文件内容不是有效的JSON或缺少'groups'键时，使用默认的JSON结构
    print(f"Error reading JSON, using default structure: {e}")


# 签到功能
async def attendance(message):
    """
    签到功能，记录到data/attendance.json中
    在用户字典中添加total字段记录累计签到次数，并在每次签到时删除之前的签到记录，只保留今天的签到记录
    同时检查是否已经签到过，如果签到过则提示用户
    """
    # 获取群组和用户的唯一标识符
    group_openid = message.group_openid
    user_openid = message.author.member_openid
    # 获取今天的日期字符串
    today = datetime.now().strftime('%Y-%m-%d')

    # 读取签到记录
    if not os.path.exists(attendance_file):
        attendance_data = {'groups': {}}
    else:
        with open(attendance_file, 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if file_content:
                attendance_data = json.loads(file_content)
            else:
                # 文件为空，使用默认结构
                attendance_data = {'groups': {}}

    # 检查群组是否存在，如果不存在则初始化
    if group_openid not in attendance_data['groups']:
        attendance_data['groups'][group_openid] = {'users': {}}

    # 获取群组用户的签到记录字典
    group_users = attendance_data['groups'][group_openid]['users']

    # 检查用户是否存在，如果存在则处理签到
    if user_openid in group_users:
        # 检查今天是否已经签到过
        if today in group_users[user_openid]:
            # 如果今天已经签到过，则提示用户
            await message.reply(content=f'您在本群今日已签到。')
            return  # 退出函数，不再执行后续操作
        else:
            # 如果今天没有签到过，则更新今天的签到记录并增加累计签到次数
            group_users[user_openid] = {
                'total': group_users[user_openid].get('total', 0) + 1,
                today: 1
            }
    else:
        # 如果是新用户，则初始化签到记录和累计签到次数
        group_users[user_openid] = {'total': 1, today: 1}

    # 发送签到成功的消息给用户
    total_sign_ins = group_users[user_openid]['total']
    await message.reply(content=f'签到成功！您在本群已累计签到{total_sign_ins}次。')

    # 更新签到记录文件
    with open(attendance_file, 'w', encoding='utf-8') as f:
        json.dump(attendance_data, f, ensure_ascii=False, indent=4)
