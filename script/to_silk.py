import requests
import os
import subprocess
import pilk

audio_url = 'https://m701.music.126.net/20240801103751/1037cf22796aef00e6e2a84be71fa7ba/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/44460910191/e8d9/3943/4df9/d09e14b332fafc08aed471d4ec8199b1.m4a'
response = requests.get(audio_url)
audio_data = response.content

# 将音频数据写入文件
with open('../source/temp_audio.m4a', 'wb') as audio_file:
    audio_file.write(audio_data)

# 原始音频文件路径
input_file_path = '../source/temp_audio.m4a'

# PCM输出文件路径
pcm_output_path = '../source/temp_audio.pcm'


# 执行ffmpeg命令
ffmpeg_command = [
    'ffmpeg',
    '-i', input_file_path,               # 输入文件
    '-f', 's16le',              # 强制使用PCM格式编码
    '-ar', '44100',                     # 设置采样率为44100Hz
    '-ac', '1',                          # 设置为单声道
    pcm_output_path,                      # 输出文件
    '-y'
]

# 使用subprocess.run执行ffmpeg命令
try:
    subprocess.run(ffmpeg_command, check=True)
    print(f"转换成功，PCM文件已保存到：{pcm_output_path}")
except subprocess.CalledProcessError as e:
    print(f"转换失败：{e}")

# 接下来使用pilk进行编码
silk_output_path = '../source/output.silk'
try:
    duration = pilk.encode(pcm_output_path, silk_output_path, pcm_rate=44100, tencent=True)
    print(f"Silk编码成功，文件已保存到：{silk_output_path}")
except Exception as e:
    print(f"Silk编码失败：{e}")

# 转换完成后，删除临时PCM文件
os.remove(pcm_output_path)