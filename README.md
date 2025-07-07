# Steam Authenticator 多账号管理器

本项目是一个基于 Python + Tkinter 的图形界面工具，支持批量管理 Steam 手机令牌（maFile）文件，快速获取 Steam 令牌验证码。适合拥有多个 Steam 账号、需要频繁获取动态验证码的用户。

## 主要功能

- 支持批量导入和管理多个 maFile 文件
- 账号列表自动读取 maFile 文件夹下的所有账号
- 支持账号搜索与过滤
- 双击账号弹出验证码窗口，显示动态验证码和倒计时
- 一键复制验证码到剪贴板
- 界面简洁，支持窗口靠右显示
- 底部带有简易使用说明和版权信息

##Win平台

请直接下载 `Steam_Authenticator.exe` 即可使用。

## 使用方法

1. **准备 maFile 文件**  
   将所有 Steam 手机令牌导出的 maFile 文件放入本程序同目录下的 `maFile` 文件夹内（如没有请自行创建）。

2. **运行程序**  
   双击或命令行运行 `steam_single_code_gui_pro.py`。

3. **浏览/搜索账号**  
   程序会自动读取 maFile 文件夹下的所有账号，并在主界面显示。支持关键词搜索。

4. **获取验证码**  
   在主界面双击账号列表中的任意账号，即可弹出验证码窗口，显示当前动态验证码和倒计时，并支持一键复制。

5. **刷新账号列表**  
   增删 maFile 文件后，点击“刷新账号列表”按钮即可。

## 环境要求

- Python 3.7+
- 依赖库：`steam-totp`、`tkinter`
- 建议在 Windows 10/11 下使用（支持中文字体）

安装依赖（如未安装）：
```bash
pip install steam-totp
```

## 目录结构
```
Steam_Authenticator.py
maFile/
    |- 你的账号1.maFile
    |- 你的账号2.maFile
    |- ...
```


## 版权信息

© 2025 灯火通明（济宁）网络有限公司

如有改进建议或 Bug，欢迎 Issue！
