import requests
import os
import subprocess
import pilk

audio_url = 'https://m801.music.126.net/20240801185826/eb27705abb9249bd774d6c0704d03e10/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/33190764350/7dfb/42ba/a634/847878e08cefa56b21b154af8eed8689.m4a'
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
silk_output_path = '../source/MyGO!!!!! - 春日影.silk'
try:
    duration = pilk.encode(pcm_output_path, silk_output_path, pcm_rate=44100, tencent=True)
    print(f"Silk编码成功，文件已保存到：{silk_output_path}")
except Exception as e:
    print(f"Silk编码失败：{e}")

# 转换完成后，删除临时PCM文件
os.remove(pcm_output_path)
os.remove(input_file_path)