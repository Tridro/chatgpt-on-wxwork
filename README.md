# chatgpt-on-wxwork
ChatGPT api backend ASGI server for wxwork application
<p align="left">
    <img src ="https://img.shields.io/badge/platform-windows|linux|-green.svg" />
    <img src ="https://img.shields.io/badge/python-3.8+-blue.svg" />
    <img src ="https://img.shields.io/badge/license-Apache2.0-orange" />
</p>

## 配置流程
### 下载整个项目包, 并解压至任意目录。
### 环境配置, 这里以Linux系统为例, 默认已安装python3
* 配置python虚拟环境, 默认环境配置在根目录下, 如需修改, 需要修改bash脚本 
``` {.sourceCode .bash}
$ pip3 install virtualenv
$ cd /
$ virtualenv -p python3 venv
```
* 进入项目目录，安装依赖库
``` {.sourceCode .bash}
$ cd <Project DIR>
$ source /venv/bin/activate
$ pip3 install -r requirements.txt
```
* 设置settings.py, 完成wxwork setting和openai api setting
* 运行server
``` {.sourceCode .bash}
$ ./server.sh start
```
* 进行wxwork的回调, 成功后就可以愉快的玩耍了
* 还不会在readme中贴图, 后面以图文形式再完善流程
