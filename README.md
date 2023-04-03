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
* 进入企业微信后台

![进入企业微信后台](https://user-images.githubusercontent.com/42351086/229404910-69a6adb7-e8d2-44f2-80eb-0c1c39f1f4bb.png)
* 自建APP

![自建APP配置](https://user-images.githubusercontent.com/42351086/229405021-419e0005-e46b-46a6-84d7-ffada4365697.png)
* 回调配置验证

![回调配置](https://user-images.githubusercontent.com/42351086/229405119-5450029c-6f56-4106-b423-4b9f90c73a0c.png)

## 应用效果
* 企业微信App效果图

![企业微信App效果图](https://user-images.githubusercontent.com/42351086/229401944-6efb073b-1198-493b-b556-982c21e7ccdd.png)
* 同时支持微信接口调用

![同时支持微信接口调用](https://user-images.githubusercontent.com/42351086/229401985-cb78aa8b-0842-42d2-90a6-d416e06fc768.png)
* 微信App效果图

![微信App效果图](https://user-images.githubusercontent.com/42351086/229402126-756861d9-5932-4e3b-9e16-762d9403c06b.png)

