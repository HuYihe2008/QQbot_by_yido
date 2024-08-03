# yido酱的QQ机器人

[![forthebadge](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMzQuNzE4NzYxNDQ0MDkxOCIgaGVpZ2h0PSIzNSIgdmlld0JveD0iMCAwIDEzNC43MTg3NjE0NDQwOTE4IDM1Ij48cmVjdCB3aWR0aD0iNzkuMzU5MzgyNjI5Mzk0NTMiIGhlaWdodD0iMzUiIGZpbGw9IiM2MGE3ZjgiLz48cmVjdCB4PSI3OS4zNTkzODI2MjkzOTQ1MyIgd2lkdGg9IjU1LjM1OTM3ODgxNDY5NzI2NiIgaGVpZ2h0PSIzNSIgZmlsbD0iI2ZmZmZmZiIvPjx0ZXh0IHg9IjM5LjY3OTY5MTMxNDY5NzI2NiIgeT0iMjEuNSIgZm9udC1zaXplPSIxMiIgZm9udC1mYW1pbHk9IidSb2JvdG8nLCBzYW5zLXNlcmlmIiBmaWxsPSIjMDAwMDAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBsZXR0ZXItc3BhY2luZz0iMiI+UFlUSE9OPC90ZXh0Pjx0ZXh0IHg9IjEwNy4wMzkwNzIwMzY3NDMxNiIgeT0iMjEuNSIgZm9udC1zaXplPSIxMiIgZm9udC1mYW1pbHk9IidNb250c2VycmF0Jywgc2Fucy1zZXJpZiIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC13ZWlnaHQ9IjkwMCIgbGV0dGVyLXNwYWNpbmc9IjIiPuKJpTMuOTwvdGV4dD48L3N2Zz4=)](https://forthebadge.com)

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