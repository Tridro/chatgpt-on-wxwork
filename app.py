#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2023/2/14 9:37
# @Author       : Tridro
# @Email        : tridro@beneorigin.com
# @Project      : chatgpt-on-wxwork
# @File         : app.py
# @Software     : PyCharm
# All Copyright Reserved

import os
import asyncio
import json
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Body, Depends, BackgroundTasks, __version__
from fastapi.responses import PlainTextResponse
from uvicorn import Config, Server
import xml.etree.cElementTree as cET
import requests

import settings
import log
from WXBizMsgCrypt3 import WXBizMsgCrypt
import openai_api

command = re.compile(r'^#[\s\S]+')


async def create_wxwork_crypt_token():
    return WXBizMsgCrypt(settings.WX_APP_API_TOKEN, settings.WX_APP_API_ENCODING_AES_KEY, settings.WX_CORP_ID)


def request_wxwork_access_token():
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={settings.WX_CORP_ID}" \
          f"&corpsecret={settings.WX_APP_API_SECRET}"
    response = requests.get(url=url)
    response_dict = response.json()
    if response.status_code == 200 and response_dict['errcode'] == 0:
        token_file = os.path.join(settings.BASE_DIR, 'access_token.json')
        if os.path.splitext(os.path.basename(token_file))[1] == '.json':
            with open(token_file, 'w+', encoding='utf-8') as f:
                try:
                    pending_dump = json.load(f)
                except json.JSONDecodeError:
                    pending_dump = dict()
                pending_dump['wxwork'] = response_dict['access_token']
                json.dump(pending_dump, f)
            return pending_dump['wxwork']
    else:
        return response


def wxwork_pusher(msg, to_user: str, access_token: str = None, msgtype: str = 'text', **kwargs):
    if msgtype not in ['text', 'image', 'voice', 'video', 'file', 'textcard', 'news', 'mpnews', 'markdown',
                       'miniprogram_notice', 'template_card']:
        raise ValueError('不支持的msgtype')
    if access_token is None:
        if os.path.exists(os.path.join(settings.BASE_DIR, 'access_token.json')):
            token_file = os.path.join(settings.BASE_DIR, 'access_token.json')
            with open(token_file, 'r', encoding='utf-8') as f:
                load_dict = json.load(f)
            access_token = load_dict['wxwork']
        else:
            access_token = request_wxwork_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    msg_content = {}
    if msgtype == 'text':
        msg_content['content'] = msg
    elif msgtype == 'image':
        msg_content['media_id'] = msg
    msg_pack = {"touser": f"{to_user}", "toparty": "", "totag": "", "msgtype": msgtype,
                "agentid": settings.WX_APP_AGENT_ID, "safe": 0, "enable_id_trans": 0,  "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800, msgtype: msg_content}
    response = requests.post(url=url, json=msg_pack)
    if response.json()['errcode'] == 0:
        return response.json()
    elif response.json()['errcode'] == 42001 or response.json()['errcode'] == 40014:
        access_token = request_wxwork_access_token()
        wxwork_pusher(msg=msg, to_user=to_user, access_token=access_token, msgtype=msgtype, **kwargs)
    else:
        print("errcode", response.json()['errcode'])
        return response


async def send_prompt_query(application, user_id, query):
    application.in_progress[user_id] = True
    if re.match(command, query):
        if query[1:] == '使用指南':
            bot_response = settings.USER_GUIDE
        else:
            bot_response = await application.bot.reply(user_id=user_id, query=query)
    else:
        bot_response = await application.bot.reply(user_id=user_id, query=query)
    wxwork_pusher(bot_response, to_user=user_id)
    application.in_progress.pop(user_id, False)


@asynccontextmanager
async def lifespan(application: FastAPI):
    log.setup_logger()
    application.bot = openai_api.OpenAIBot()
    application.in_progress = dict()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def index():
    return f'FastAPI {__version__} is running'


@app.get('/cgi-bin/wxpush', response_class=PlainTextResponse)
async def wxwork_callback(wxcpt=Depends(create_wxwork_crypt_token), msg_signature: str = Query(),
                          timestamp: str = Query(), nonce: str = Query(), echostr: str = Query()):
    """

    Args:
        wxcpt:
        msg_signature:
        timestamp:
        nonce:
        echostr:

    Returns:

    """
    ret, v_echostr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    if ret != 0:
        log.log_error(f'VerifyURL ret: {ret}', logger='wxworkapi.error')
    else:
        return PlainTextResponse(status_code=200, content=v_echostr)


@app.post('/cgi-bin/wxpush', response_class=PlainTextResponse)
async def wxwork_passive_response(background_tasks: BackgroundTasks, wxcpt=Depends(create_wxwork_crypt_token),
                                  rec_data=Body(), msg_signature: str = Query(), timestamp: str = Query(),
                                  nonce: str = Query()):
    """

    Args:
        background_tasks:
        wxcpt:
        rec_data:
        msg_signature:
        timestamp:
        nonce:

    Returns:

    """
    ret, decrypted_msg = wxcpt.DecryptMsg(rec_data, msg_signature, timestamp, nonce)
    if ret != 0:
        log.log_error(f'DecryptMsg ret: {ret}', logger='wxworkapi.error')
    tree = cET.fromstring(decrypted_msg)
    log.log_wxwork_record(tree)
    if tree.findtext('MsgType') != 'event':
        if not getattr(app, 'in_progress').get(tree.findtext('FromUserName'), False) and tree.findtext('Content'):
            background_tasks.add_task(func=send_prompt_query, application=app, user_id=tree.findtext('FromUserName'),
                                      query=tree.findtext('Content'))
    return PlainTextResponse(status_code=200, content='')
    # res_body = WxworkResponseBody()
    # res_body.from_rec_build(tree, content='测试成功:)')
    # ret, encrypted_msg = wxcpt.EncryptMsg(ET.tostring(res_body.tree).decode(), nonce)
    # if ret != 0:
    #     log.log_error(f'EncryptMsg ret: {ret}', logger='wxworkapi.error')
    # return Response(status_code=200, media_type='application/xml', content=encrypted_msg)


def start_fastapi(address: tuple = settings.FASTAPI_ADDRESS):
    """
    启动

    Args:
        address (tuple): 服务地址和端口，默认为settings模块中的FASTAPI_ADDRESS

    Returns:

    """
    ser_loop = asyncio.new_event_loop()
    config = Config(app=app, host=address[0], port=address[1], log_level="info", reload=True)
    ser = Server(config=config)
    ser_loop.run_until_complete(ser.serve())
    # uvicorn.run(app='app:app', host="127.0.0.1", port=8000, reload=True)
