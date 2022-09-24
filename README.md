# 龙图检测插件

基于[dragon-pic-detect](https://github.com/zyddnys/dragon-pic-detect)和[Akagicv](https://github.com/Akagicv)大佬的[GGNMSL](https://github.com/Akagicv/GGNMSL)插件暴力缝合而成的Hoshinobot 龙图检测插件

## 目录

- [插件简介](#插件简介)
- [部署插件](#部署插件)
- [版权声明](#版权声明)
- [鸣谢](#鸣谢)

### 插件简介

没有指令，可在lssv中控制开关。

py文件内有相应注释可修改检测到龙图后机器人做出的操作和检测力度方式等。

* [ ] TODO:dragon-pic-detect实现了检测gif图，但是这边插件需要稍微修改一下代码才行，等有时间再弄吧

### 部署插件

1. 安装依赖.

```
python3.8 -m pip install -r requirements.txt
```

3.在HoshinoBot/hoshino/modules/config/__bot__.py 文件内MODULES_ON内添加

```
 'dragon_killer', 
```

### 版权声明

该项目签署了GPL3.0授权许可.

### 鸣谢

- [Acagicv大佬的GGNMSL插件](https://github.com/Akagicv/GGNMSL "reademe都是抄的()")
