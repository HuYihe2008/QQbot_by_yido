import json
import os
from botpy.ext.cog_yaml import read
import asyncio
import aiohttp
import logging
from botpy import logging  # 确保这个路径是正确的

# 读取配置
config = read(os.path.join(os.path.dirname(__file__), "../../config/config.yaml"))

# 定义日志记录器
_log = logging.get_logger()

# 这是提供的JSON数据
with open('./static/json/tableConvert.com_7k197d.json', 'r') as file:
    json_data = json.load(file)


async def get_weather_forecast(city_code):
    # API请求部分使用aiohttp
    url_api = config["weather"]["base_url"]
    params_url = {
        'key': config["weather"]["key"],  # 应该从环境变量或配置文件中获取
        'city': city_code,
        'extensions': 'all',
        'output': 'JSON'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url_api, params=params_url) as response:
            if response.status == 200:
                data = await response.json()
                _log.info("成功获取天气数据")
                return data
            else:
                _log.warning(f"请求失败，状态码：{response.status}")
                return None


async def weather_search(params):
    for item in json_data:
        if params in item:  # 假设params是城市名称，item是包含城市名称的子列表
            city_code = item[0]
            _log.info(f"找到城市代码：{city_code}，正在获取天气信息...")
            weather_data = await get_weather_forecast(city_code)
            if weather_data:
                forecasts = weather_data['forecasts'][0]
                casts = forecasts['casts']
                output = ""
                for cast in casts:
                    output += f"\n"
                    output += f"日期：{cast['date']}\n"
                    output += f"白天天气：{cast['dayweather']}，气温：{cast['daytemp']}°C\n"
                    output += f"夜间天气：{cast['nightweather']}，气温：{cast['nighttemp']}°C\n"
                    output += "-" * 20 + "\n"
                _log.info("成功获取天气信息")
                return output
            else:
                _log.warning("未能获取天气信息")
                return None
    _log.warning(f"未找到城市：{params}")
    return None
