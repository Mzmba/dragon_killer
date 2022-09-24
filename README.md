# GGNMSL
此插件对机器性能需求稍高，请在2H4G主机上使用

基于pcrsealkiller(另一个插件)思路制作的Hoshinobot反广告插件

## 目录
- [插件简介](#插件简介)
- [部署插件](#部署插件)
- [版权声明](#版权声明)
- [鸣谢](#鸣谢)

![image](https://github.com/Akagicv/GGNMSL/blob/main/test/test.jpg)




### 插件简介
没有指令控制此插件

-----gg.jpg

用于撤回后提示消息发送的图片

-----ggnmsl.py

关键词匹配，如果匹配则撤回广告消息并且禁言10分钟

-----ggnmslocr.py

使用ocr进行关键词识别广告，禁言同上处理

-----ggnmslopencv.py 

在ocr未识别到任何广告信息的情况下进行图片二维码识别，查看二维码对应网站标题，进行关键词对照标题识别

-----Keyword.txt 

检测使用的关键词列表，如需要添加关键词只需要输入 "空格"关键词 即可

### 部署插件

1.安装opencv 命令  pip3 install opencv-python

2.把插件放到HoshinoBot/hoshino/modules 目录下

3.在HoshinoBot/hoshino/modules/config/__bot__.py 文件内MODULES_ON内添加「 'ggnmsl', 」开启插件

### 版权声明

该项目签署了GPL3.0授权许可

### 鸣谢

- [GWYOG大佬的pcrsealkiller项目](https://github.com/GWYOG/GWYOG-Hoshino-plugins/tree/master/pcrsealkiller)


