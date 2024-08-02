# yido酱的QQ机器人

## 运行
```bash
pip install -r requirements.txt
python bot.py
```

## 目录

```
----bot
    |----config
    |    |    config.yaml
    |----features
    |    |----tarot
    |    |    |    tarot_card.py
    |    |----weather
    |    |    |    weather.py
    |----logs
    |----public
    |----script
    |    |    msg_send.py
    |----source
    |    |    MyGO!!!!! - 春日影.silk
    |    |    output.silk
    |    |    temp_audio.m4a
    |    |    空の箱.silk
    |----static
    |    |----json
    |    |    |----tarot
    |    |    |    |    batarot.json
    |    |    |    |    batarot_fortune.json
    |    |    |    |    batarot_spread.json
    |    |    |    |    batarot_url.json
    |    |    |    tableConvert.com_7k197d.json
    |----utils
    |    |    event.py
    |    |    path.py
    |    |    to_silk.py
    |    .gitignore
    |    botpy.log
    |    index.py
    |    README.md
```


## Todo
- [x] 塔罗牌开发
- [ ] 占卜开发
- [x] 完善菜单(已在帮助功能实现)
- [x] 添加天气查询
- [x] 帮助功能
- [x] 彩蛋功能
- [x] 签到功能