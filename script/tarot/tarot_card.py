import json
import random
import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read

# 读取配置
config = read(os.path.join(os.path.dirname(__file__), "../../config/config.yaml"))

_log = logging.get_logger()

# 读取塔罗牌图片 URL JSON 数据
with open(config["tarot"]["batarot_url"], 'r', encoding='utf-8') as file:
    tarot_url_data = json.load(file)

# 读取塔罗牌含义 JSON 数据
with open(config["tarot"]["batarot"], 'r', encoding='gbk') as file:
    tarot_data = json.load(file)

# 读取塔罗牌语录 JSON 数据
with open(config["tarot"]["batarot_fortune"], 'r', encoding='gbk') as file:
    tarot_fortune_data = json.load(file)


async def tarot_card():
    # 准备塔罗牌编号列表，用于随机选择
    tarot_keys = list(tarot_data['cards'].keys())

    # 随机抽取一张塔罗牌
    selected_tarot = random.choice(tarot_keys)
    selected_card_info = tarot_data['cards'][selected_tarot]  # 将selected_tarot转换为整数
    image_url = tarot_url_data[f'tarot_{selected_tarot}']

    # 准备fortune_range变量，这里我们根据塔罗牌编号来决定语录区间
    if int(selected_tarot) <= 10:
        fortune_range = '1-10'
    elif int(selected_tarot) <= 20:
        fortune_range = '11-20'
    elif int(selected_tarot) <= 30:
        fortune_range = '21-30'
    elif int(selected_tarot) <= 40:
        fortune_range = '31-40'
    elif int(selected_tarot) <= 50:
        fortune_range = '41-50'
    elif int(selected_tarot) <= 60:
        fortune_range = '51-60'
    elif int(selected_tarot) <= 70:
        fortune_range = '61-70'
    elif int(selected_tarot) <= 80:
        fortune_range = '71-80'
    elif int(selected_tarot) <= 90:
        fortune_range = '81-90'
    elif int(selected_tarot) <= 100:
        fortune_range = '91-100'
    # 继续添加更多的elif语句来覆盖所有可能的塔罗牌编号区间

    # 使用异常处理来安全地获取语录
    try:
        fortunes = tarot_fortune_data[fortune_range]
    except KeyError:
        _log.error(f"The fortune range '{fortune_range}' was not found in the tarot fortune data.")
        fortunes = []  # 或者其他默认值

    # 输出结果
    print(f"抽取的塔罗牌编号: {selected_tarot}")
    print(f"塔罗牌名称（中文）: {selected_card_info['name_cn']}")
    print(f"图片地址: {image_url}")
    print("塔罗牌描述:")
    for description in selected_card_info['description']:
        print(description)
    print("塔罗牌含义（正位）:", selected_card_info['meaning']['up'])
    if 'down' in selected_card_info['meaning']:
        print("塔罗牌含义（逆位）:", selected_card_info['meaning']['down'])
    print("抽取的语录:")
    for fortune in fortunes:
        print(fortune)

    # 将结果收集到一个字典中
    result = {
        "image_url": image_url,
        "selected_tarot": selected_tarot,
        "name_cn": selected_card_info['name_cn'],
        "description": selected_card_info['description'],
        "meaning": selected_card_info['meaning'],
        "fortunes": fortunes
    }

    output_tarot = ""
    output_tarot += f"\n"
    output_tarot += f"⭐抽取的塔罗牌编号: {selected_tarot}\n"
    output_tarot += f"⭐塔罗牌名称（中文）: {selected_card_info['name_cn']}\n"
    output_tarot += "⭐塔罗牌描述:\n"
    for description in selected_card_info['description']:
        output_tarot += f"{description}\n"
    output_tarot += f"⭐塔罗牌含义（正位）: \n{selected_card_info['meaning']['up']}\n"
    if 'down' in selected_card_info['meaning']:
        output_tarot += f"⭐塔罗牌含义（逆位）: \n{selected_card_info['meaning']['down']}\n"
    output_tarot += f"⭐抽取的语录:\n"
    for fortune in fortunes:
        output_tarot += f"{fortune}\n"
    result['output_text'] = output_tarot

    return result
