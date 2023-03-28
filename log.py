#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2023/2/14 14:19
# @Author       : Tridro
# @Email        : tridro@beneorigin.com
# @Project      : chatgpt-on-wxwork
# @File         : log.py
# @Software     : PyCharm
# All Copyright Reserved

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Union, Literal
import xml.etree.cElementTree as cET

import settings


def setup_logger():
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs).3d | %(name)s | %(levelname)s | %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    # chatgpt记录日志
    chatgpt_record_logger = logging.getLogger('chatgpt.record')
    chatgpt_record_logger.setLevel(logging.INFO)
    chatgpt_record_file_handler = logging.FileHandler(filename=os.path.join(settings.LOG_DIR, 'chatgpt_record.log'),
                                                      mode='a', encoding='utf-8')
    chatgpt_record_file_handler.setLevel(logging.INFO)
    chatgpt_record_file_handler.setFormatter(fmt=formatter)
    chatgpt_record_logger.addHandler(hdlr=chatgpt_record_file_handler)
    # chatgpt错误日志
    chatgpt_error_logger = logging.getLogger('chatgpt.error')
    chatgpt_error_logger.setLevel(logging.WARNING)
    chatgpt_error_file_handler = RotatingFileHandler(filename=os.path.join(settings.LOG_DIR, 'chatgpt_error.log'),
                                                     mode='a', encoding='utf-8')
    chatgpt_error_file_handler.setFormatter(fmt=formatter)
    chatgpt_error_logger.addHandler(hdlr=chatgpt_error_file_handler)
    # wxworkapi记录日志
    wxworkapi_record_logger = logging.getLogger('wxworkapi.record')
    wxworkapi_record_logger.setLevel(logging.INFO)
    wxworkapi_record_file_handler = logging.FileHandler(filename=os.path.join(settings.LOG_DIR, 'wxworkapi_record.log'),
                                                        mode='a', encoding='utf-8')
    wxworkapi_record_file_handler.setLevel(logging.INFO)
    wxworkapi_record_file_handler.setFormatter(fmt=formatter)
    wxworkapi_record_logger.addHandler(hdlr=wxworkapi_record_file_handler)
    # wxworkapi错误日志
    wxworkapi_error_logger = logging.getLogger('wxworkapi.error')
    wxworkapi_error_logger.setLevel(logging.WARNING)
    wxworkapi_error_file_handler = RotatingFileHandler(filename=os.path.join(settings.LOG_DIR, 'wxworkapi_error.log'),
                                                       mode='a', encoding='utf-8')
    wxworkapi_error_file_handler.setFormatter(fmt=formatter)
    wxworkapi_error_logger.addHandler(hdlr=wxworkapi_error_file_handler)


def log_error(text: str, logger: Union[str, logging.Logger] = 'wxworkapi.error', **kwargs):
    logger = logging.getLogger(logger) if isinstance(logger, str) else logger
    msg = '%(text)s'
    args = {'text': text}
    if kwargs:
        args.update(kwargs)
    logger.error(msg, args)


def log_wxwork_record(rec_body: cET.Element, logger: Union[str, logging.Logger] = 'wxworkapi.record', **kwargs):
    logger = logging.getLogger(logger) if isinstance(logger, str) else logger
    tags = [child.tag for child in rec_body]
    msg = ' | '.join([f'%({tag})s' for tag in tags])
    args = dict(zip(tags, [f'{tag}: {rec_body.findtext(tag)}' for tag in tags]))
    if kwargs:
        args.update(kwargs)
    logger.info(msg, args)


def log_chatgpt_qa(who: str, qa: Literal['Q', 'A'], text: str, logger: Union[str, logging.Logger] = 'chatgpt.record',
                   **kwargs):
    logger = logging.getLogger(logger) if isinstance(logger, str) else logger
    msg = '%(who)s | %(qa)5s | %(text)s'
    args = {'who': who, 'qa': qa, 'text': text}
    if kwargs:
        args.update(kwargs)
    logger.info(msg, args)
