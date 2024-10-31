# midi 游乐园
方块弹跳视频，开源版和游戏化版

[English](./README.md) | [简体中文](./README-ZH.md)
## 公告

### 对于内容创作者：

如果您上传视频平台的视频用了此软件，请尝试将此存储库的链接放入您的视频简介中，这就是我所要求的

### 对于开发者：

****此代码根据GPL3获得许可，未经要求提供源代码就公开分发此软件的修改副本是违法的！***

（但是，如果您不向公众发布修改后的版本，则可以修改代码而不发布源代码。）

## 如何制作自定义歌曲？

参照 [docs/SONGS.md](https://github.com/quasar098/midi-playground/blob/master/docs/SONGS.md) 获取自定义歌曲教程

## 开发指南

这是教您如何设置代码以从源代码运行它，而不是从捆绑的 PyInstaller 可执行文件运行它

从[这里](https://python.org)下载 Python（3.11.0 可以工作）。请勿从 Windows 应用商店下载。那个版本真的很糟糕，对于具有大量依赖项的更复杂的 Python 程序来说效果不佳

使用`python3 -m pip install -r requirements.txt`安装依赖

使用`python3 main.py`来启动程序

打包命令: `pyinstaller main.py --noconsole --onefile --clean --hidden-import glcontext`

## 鸣谢

详见[docs/CREDITS.md](https://github.com/quasar098/midi-playground/blob/master/docs/CREDITS.md)

## 贡献者

- [quasar098](https://github.com/quasar098)
- [TheCodingCrafter](https://github.com/TheCodingCrafter) - 主题 + QOL
- [PurpleJuiceBox](https://github.com/PurpleJuiceBox) - 重置为默认值按钮
- [sled45](https://github.com/sled45) - 高DPI显示器的鼠标修复
- [Times0](https://github.com/Times0) - dark_modern主题，发光，彩色弹钉
- [Spring-Forever-with-me](https://github.com/Spring-Forever-with-me) - 修复配置中屏幕分辨率的错误键名
- [sj-dan](https://github.com/sj-dan) - mac操作系统上的opengl修复
- [zetlen](https://github.com/zetlen) - 更新着色器以使用现代opengl api

- [cangerjun](https://github.com/cangerjun) - 中文翻译
- [lucmsilva651](https://github.com/lucmsilva651) - 巴西葡萄牙语和西班牙语翻译
- [leo539](https://github.com/leo539) - 法语翻译
- [simpansoftware](https://github.com/simpansoftware) - 瑞典语翻译
- [slideglide](https://github.com/slideglide) - 土耳其语翻译
- [Guavvva](https://github.com/Guavvva) - 俄语翻译
- [SpeckyYT](https://github.com/SpeckyYT) - 意大利语翻译
- [suzuuuuu09](https://github.com/suzuuuuu09) - 日语翻译

## 翻译指南

想添加其他语言的翻译吗？
请在标题中使用“translations”一词创建一个github pull请求
如果是这样，请为尽可能多的文本添加翻译（它们列在translations.py中）

- "play"
- "config"
- "contribute"
- "open songs folder"
- "quit"
- "back"
- "midi-playground" text (this is the title of the software)
- the marquee on the title screen (the moving text that appears underneath the title on the main screen; see translations.py file for english example)
- "restart required"

(更多的内容在translations.py)

如果你对任何文本的含义有任何疑问，在发出github pull请求之前，请参阅translations.py以获取英文示例
如果你对文本的含义有疑问，也可以参考translations.py中其他语言翻译的内容，可能会对你有所帮助。
另外，我们只添加真实的语言（没有海盗语言或像《我的世界》这样的颠倒语言）

## (旧的) 需要完成的列表

详见[docs/TODO.md](https://github.com/quasar098/midi-playground/blob/master/docs/TODO.md)

