#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2023/2/14 13:04
# @Author       : Tridro
# @Email        : tridro@beneorigin.com
# @Project      : chatgpt-on-wxwork
# @File         : settings.py
# @Software     : PyCharm
# All Copyright Reserved

import os

# ---------------------------------------------------System Settings----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

FASTAPI_ADDRESS = ('localhost', 8848)

LOG_DIR = os.path.join(BASE_DIR, 'log')

# ---------------------------------------------------OpenAI Settings----------------------------------------------------

OPENAI_API_KEY = "Your OpenAI API"  # OPENAI的API密钥

CHAT_MODEL = "gpt-3.5-turbo"

GPT3_MODEL = "text-davinci-003"

CODEX_MODEL = "code-davinci-002"

MODEL_LIST = [CHAT_MODEL, GPT3_MODEL, CODEX_MODEL]

MAX_TOKEN = 4000

PROMPT_ROLES = ['ChatGPT', 'Linux终端', '英语翻译', '面试官', 'JavaScript控制台', 'Excel表', '英语口语老师', '导游', '抄袭检查器',
                '广告商', '说书人', '足球评论员', '单口相声演员', '激励教练', '作曲家', '辩论者', '编剧', '小说作家', '电影评论员',
                '关系调解员', '诗人', '说唱歌手', '演说家', '哲学老师', '哲学家', '数学老师', '写作导师', 'UX/UI开发者', '网络安全专家',
                '生活教练', '词源学家', '评论员']

USER_GUIDE = "ChatGPT是由OpenAI开发的人工智能，会根据会话的内容进行回复，具体使用效果需要用户自行探索。\n\n" \
             "指令命令：\n" \
             "进行会话的基本配置，所有指令需要以‘#’为起始，如‘#使用指南’，当前可用指令包括以下指令，以及所有角色列表中列出的角色，如‘#英语翻译’\n\n" \
             "【使用指南】：用户使用指南\n" \
             "【清除记忆】：清除当前会话记录，并重置角色\n" \
             "【角色列表】：列出目前可启用的角色名称，不同角色有不同的效果\n" \
             "【模型列表】：列出目前可使用的模型名称，推荐使用[gpt-3.5-turbo]，其他模型支持fine-turn\n" \
             "【当前模型】：返回当前应用模型的名称\n" \
             "【当前角色】：返回当前应用的角色，如果之前没用启用过角色，将返回默认角色[ChatGPT]\n" \
             "【角色提示】：返回当前应用角色的提示词\n"

TOKEN_ENCODING = ['cl100k_base', 'p50k_base']
# ---------------------------------------------------Wxwork Settings----------------------------------------------------

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
