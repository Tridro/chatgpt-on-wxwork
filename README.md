# chatgpt-on-wxwork
***ChatGPT api backend ASGI server for Wxwork application***
<p align="left">
    <img src ="https://img.shields.io/badge/platform-windows|linux|-green.svg" />
    <img src ="https://img.shields.io/badge/python-3.8+-blue.svg" />
    <img src ="https://img.shields.io/badge/license-Apache2.0-orange" />
</p>
通过自建企业微信APP，绕过微信可能被屏蔽的限制，可以直接从微信中调用企业微信APP的接口使用ChatGPT API

## 配置流程
#### 1. 下载整个项目包, 并解压至目标目录
#### 2. 环境配置, 这里以Linux系统为例, 默认已安装python3
* 配置python虚拟环境, 默认环境配置在根目录下, 如需修改, 需要同步修改项目server.sh脚本
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
* 设置settings.py
```
# openai的API密钥
OPENAI_API_KEY = "Your OpenAI API"
```
```
# 以下填企业ID
WX_CORP_ID = 'Your Wxwork Corp ID'

# 以下填企业微信指定APP的ID
WX_APP_AGENT_ID = 1000002

# 以下填企业微信指定APP的Secret
WX_APP_API_SECRET = 'Your Wxwork App Secret'

# 以下填企业微信指定APP随机获取的Token, 用于回调配置
WX_APP_API_TOKEN = 'Your Wxwork App Token'

# 以下填企业微信指定APP随机获取的EncodingAESKey, 用于回调配置
WX_APP_API_ENCODING_AES_KEY = 'Your Wxwork App Encoding AES Key'
```
#### 3. 运行server.sh
* 启动服务
``` {.sourceCode .bash}
$ ./server.sh start
```
* 关闭服务
``` {.sourceCode .bash}
$ ./server.sh stop
```
* 重启服务
``` {.sourceCode .bash}
$ ./server.sh restart
```
#### 4. 进行wxwork的回调验证, 成功后就可以愉快的玩耍了
还不会在readme中贴图, 后面以图文形式再完善流程
