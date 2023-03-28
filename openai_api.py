#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2023/2/15 13:08
# @Author       : Tridro
# @Email        : tridro@beneorigin.com
# @Project      : chatgpt-on-wxwork
# @File         : openai_api.py
# @Software     : PyCharm
# All Copyright Reserved

import os
import re
import time
import random
import json
from typing import List

import tiktoken
import openai

import log
import settings

user_session = dict()
user_settings = dict()


class Session:
    global user_session
    global user_settings

    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str = 'p50k_base') -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    @staticmethod
    def num_tokens_from_messages(messages, model=settings.CHAT_MODEL):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"num_tokens_from_messages() is not presently implemented for model {model}. See "
                                      f"https://github.com/openai/openai-python/blob/main/chatml.md "
                                      f"for information on how messages are converted to tokens.")

    @staticmethod
    def get_role_prompt(role: str) -> dict:
        """读取预设的角色和提示词"""
        with open(os.path.join(settings.BASE_DIR, 'prompts.json'), 'r', encoding='utf-8') as f:
            prompts = json.load(f)
            if role in prompts.keys():
                prompt = prompts.get(role)
                return {'role': role, 'prompt': prompt}
            else:
                prompt = prompts.get('ChatGPT')
                return {'role': 'ChatGPT', 'prompt': prompt}

    @staticmethod
    def set_role_prompt(user_id: str, role: str = None) -> dict:
        """设置自定义角色和提示词"""
        role_prompt = Session.get_role_prompt(role=role)
        if user_settings.get(user_id, None):
            user_settings[user_id].update(role_prompt)
        return user_settings[user_id]

    @staticmethod
    def set_model(user_id: str, model: str = None) -> dict:
        """设置自定义使用引擎"""
        if model not in settings.MODEL_LIST:
            model = settings.CHAT_MODEL
        if user_settings.get(user_id, None):
            user_settings[user_id].update(model=model)
        return user_settings[user_id]

    @staticmethod
    def apply_default(user_id) -> dict:
        user_settings[user_id] = {'model': settings.CHAT_MODEL}
        Session.set_role_prompt(user_id=user_id)
        return user_settings[user_id]

    @staticmethod
    def build_session_query(query, user_id):
        custom_setting = user_settings.get(user_id, None) or Session.apply_default(user_id=user_id)
        prompt = custom_setting['prompt']
        session = user_session.get(user_id, None)
        if custom_setting['model'] == settings.GPT3_MODEL:
            prompt += "<|endoftext|>\n\n\n"
            if isinstance(session, list):
                for conversation in session:
                    prompt += "Q: " + conversation["query"] + "\n\n\nA: " + conversation["answer"] + "<|endoftext|>\n"
                prompt += "Q: " + query + "\nA: "
                return prompt
            else:
                return prompt + "Q: " + query + "\nA: "
        elif custom_setting['model'] == settings.CHAT_MODEL:
            if isinstance(session, list):
                session.append({'role': 'user', 'content': query})
                return session
            else:
                user_session[user_id] = [{'role': 'system', 'content': prompt}]
                user_session[user_id].append({'role': 'user', 'content': query})
                return user_session[user_id]

    @staticmethod
    def save_gpt3_session(query: str, answer: str, user_id: str) -> None:
        session = user_session.get(user_id, None)
        if session:
            session.append({'query': query, 'answer': answer})
        else:
            user_session[user_id] = [{'query': query, 'answer': answer}]
        Session.discard_exceed_conversation(user_id=user_id, max_tokens=settings.MAX_TOKEN)

    @staticmethod
    def save_chat_session(content: str, user_id: str) -> None:
        session = user_session.get(user_id)
        session.append({'role': 'assistant', 'content': content})
        Session.discard_exceed_conversation(user_id=user_id, max_tokens=settings.MAX_TOKEN)

    @staticmethod
    def discard_exceed_conversation(user_id: str, max_tokens) -> None:
        count = 0
        count_list = list()
        model = user_settings.get(user_id)['model']
        session = user_session.get(user_id)
        if model == settings.GPT3_MODEL:
            for i in range(len(session)-1, -1, -1):
                count += Session.num_tokens_from_string(session[i]["query"])
                count += Session.num_tokens_from_string(session[i]["answer"])
                count_list.append(count)
            for c in count_list:
                if c > max_tokens:
                    session.pop(0)
        elif model == settings.CHAT_MODEL:
            while Session.num_tokens_from_messages(messages=session) >= max_tokens:
                session.pop(1)

    @staticmethod
    def clear_session(user_id) -> None:
        user_session.pop(user_id, None)
        user_settings.pop(user_id, None)


def retry_with_exponential_backoff(func, initial_delay: float = 1, exponential_base: float = 2, jitter: bool = True,
                                   max_retries: int = 10, errors: tuple = (openai.error.RateLimitError,)):
    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except errors as e:
                num_retries += 1
                log.log_error(e.args[0], logger='chatgpt.error')
                if num_retries > max_retries:
                    log.log_error(f"Maximum number of retries ({max_retries}) exceeded.", logger='chatgpt.error')
                    return "提问太快啦，请休息一下再问我吧"
                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
            except Exception as e:
                log.log_error(e.args[0], logger='chatgpt.error')
                return "遇到点问题，让工程师帮我看看吧"
    return wrapper


class OpenAIBot:
    def __init__(self):
        log.setup_logger()
        openai.api_key = settings.OPENAI_API_KEY

    async def reply(self, query, user_id, q_type: str = 'text'):
        if q_type == 'text':
            if re.match(r'^#+', query):
                custom_setting = user_settings.get(user_id, None)
                if query[1:] == "角色列表":
                    return str(settings.PROMPT_ROLES)
                elif query[1:] == '模型列表':
                    return str(settings.MODEL_LIST)
                elif query[1:] == '清除记忆':
                    Session.clear_session(user_id)
                    return '[记忆已清除]'
                elif query[1:] == '当前角色':
                    if not custom_setting:
                        custom_setting = Session.apply_default(user_id=user_id)
                    return f"[{custom_setting['role']}]"
                elif query[1:] == '角色提示':
                    if not custom_setting:
                        custom_setting = Session.apply_default(user_id=user_id)
                    return f"[{custom_setting['prompt']}]"
                elif query[1:] == '当前模型':
                    if not custom_setting:
                        custom_setting = Session.apply_default(user_id=user_id)
                    return f"[{custom_setting['model']}]"
                elif query[1:] in settings.PROMPT_ROLES:
                    pre_model = None
                    if custom_setting:
                        pre_model = custom_setting['model']
                    Session.clear_session(user_id)
                    Session.apply_default(user_id=user_id)
                    Session.set_model(user_id=user_id, model=pre_model)
                    custom_setting = Session.set_role_prompt(user_id=user_id, role=query[1:])
                    return f"已启用[{custom_setting['role']}]角色"
                elif query[1:] in settings.MODEL_LIST:
                    pre_role = None
                    if custom_setting:
                        pre_role = custom_setting['role']
                    Session.clear_session(user_id)
                    Session.apply_default(user_id=user_id)
                    Session.set_role_prompt(user_id=user_id, role=pre_role)
                    custom_setting = Session.set_model(user_id=user_id, model=query[1:])
                    return f"已启用[{custom_setting['model']}]模型"
            new_query = Session.build_session_query(query=query, user_id=user_id)
            custom_setting = user_settings.get(user_id)
            if custom_setting['model'] == settings.GPT3_MODEL:
                log.log_chatgpt_qa(logger='chatgpt.record', who=user_id, qa='Q', text=query)
                reply_content = self.create_gpt3_completion(session=new_query)
                log.log_chatgpt_qa(logger='chatgpt.record', who=custom_setting['model'], qa='A', text=reply_content)
                if reply_content and query:
                    Session.save_gpt3_session(query, reply_content, user_id)
                return reply_content
            elif custom_setting['model'] == settings.CHAT_MODEL:
                log.log_chatgpt_qa(logger='chatgpt.record', who=user_id, qa='Q', text=query)
                reply_content = self.create_chat_completion(messages=new_query)
                log.log_chatgpt_qa(logger='chatgpt.record', who=custom_setting['model'], qa='A',
                                   text=reply_content)
                Session.save_chat_session(content=reply_content, user_id=user_id)
                return reply_content
        elif q_type == 'image':
            log.log_chatgpt_qa(logger='chatgpt.record', who=user_id, qa='Q', text=query)
            image_url = self.create_image(query)
            log.log_chatgpt_qa(logger='chatgpt.record', who=settings.GPT3_MODEL, qa='A', text='图片地址: ' + image_url)
            return image_url

    @retry_with_exponential_backoff
    def create_chat_completion(self, messages: List[dict]) -> openai.ChatCompletion.response_ms:
        completion = openai.ChatCompletion.create(
            model=settings.CHAT_MODEL,
            messages=messages,
        )
        content = completion['choices'][0]['message']['content']
        return content

    @retry_with_exponential_backoff
    def create_gpt3_completion(self, session: str):
        completion = openai.Completion.create(
            engine=settings.GPT3_MODEL,  # gpt3引擎, 默认为"text-davinci-003"
            prompt=session,  # 语句提示
            temperature=0.8,  # 采样温度，在0和1之间。较高的数值如0.8会使输出更加随机，而较低的数值如0.2会使其更加集中和确定。
            max_tokens=settings.MAX_TOKEN,  # 最大单词量
            # top_p=1,  # 采样温度另一种方法，称为核取样，模型考虑具有top_p概率质量的令牌的结果。所以0.1意味着只考虑由前10%的概率质量组成的标记。
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=['\n\n\n']
        )
        content = completion['choices'][0]['text'].strip().replace('<|endoftext|>', '')
        return content

    @retry_with_exponential_backoff
    def create_image(self, query):
        image = openai.Image.create(
            prompt=query,  # 图片描述
            n=1,  # 每次生成图片的数量
            size="256x256"  # 图片大小,可选有 256x256, 512x512, 1024x1024
        )
        image_url = image['data'][0]['url']
        return image_url
