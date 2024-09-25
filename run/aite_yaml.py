# -*- coding: utf-8 -*-
import os
import random

import yaml
import httpx
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from mirai import GroupMessage, At
from mirai import Voice
from mirai.models import MusicShare

from itertools import repeat

from plugins import weatherQuery

import datetime
import json

import re
from asyncio import sleep
from io import BytesIO
import requests
from PIL import Image as Image1
from mirai import GroupMessage, At, Plain
from mirai import Image, Voice, Startup, MessageChain
from mirai.models import ForwardMessageNode, Forward

from plugins.toolkits import random_str,picDwn
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown,MessageChain

#master=1270858640


# 数据存储路径
DATA_DIR = 'manshuo_data/ait_list.yaml'
os.makedirs(DATA_DIR, exist_ok=True)

# 读取 YAML 数据
def load_group_data(group_id):
    file_path = os.path.join(DATA_DIR, f'{group_id}.yaml')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

# 保存 YAML 数据
def save_group_data(group_id, data):
    file_path = os.path.join(DATA_DIR, f'{group_id}.yaml')
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True)

def main(bot, logger):
    @bot.on(GroupMessage)
    async def handle_message(event):
        #if isinstance(event, Plain):
            group_id = event.sender.group.id
            user_id = event.sender.id
            msg = '你猜我放这里是干什么的'
            if '订阅' in str(event.message_chain) or '召唤阵' in str(event.message_chain) or '订阅' in str(event.message_chain):
                msg = event.message_chain[Plain][0].text.strip()

            # 读取群数据
            group_data = load_group_data(group_id)

            # 创建大召唤阵
            if msg.startswith("创建大召唤阵"):
                
                _, summon = msg.split("创建大召唤阵", 1)
                #await bot.send(event, '正在创建大召唤阵，请稍等1')
                summon = summon.strip()
                #await bot.send(event, '正在创建大召唤阵，请稍等2')
                if summon:
                    #await bot.send(event, 'summon：'+str(summon))
                    if "召唤阵" not in group_data:
                        group_data["召唤阵"] = {}
                    if summon not in group_data["召唤阵"]:
                        group_data["召唤阵"][summon] = {}
                        #await event.sender.group.send(f"大召唤阵 {summon} 已创建！")
                        await bot.send(event, f"大召唤阵 {summon} 已创建！")
                        #await bot.send(event, "大召唤阵 {summon} 已创建！")
                    else:
                        #await event.sender.group.send(f"大召唤阵 {summon} 已经存在！")
                        await bot.send(event, f"大召唤阵 {summon} 已经存在！")
                    save_group_data(group_id, group_data)

            # 订阅大召唤阵
            elif msg.startswith("订阅"):
                _, summon = msg.split("订阅", 1)
                summon = summon.strip()
                if summon in group_data.get("召唤阵", {}):
                    group_data["召唤阵"][summon][user_id] = 1  # 设置订阅状态为1
                    save_group_data(group_id, group_data)
                    await bot.send(event, f"{event.sender.member_name} 已订阅 {summon}！")
                else:
                    await bot.send(event, f"大召唤阵 {summon} 不存在！")

            # 取消订阅大召唤阵
            elif msg.startswith("取消订阅"):
                _, summon = msg.split("取消订阅", 1)
                summon = summon.strip()
                if summon in group_data.get("召唤阵", {}):
                    if user_id in group_data["召唤阵"][summon]:
                        group_data["召唤阵"][summon][user_id] = 0  # 设置订阅状态为0
                        save_group_data(group_id, group_data)
                        await bot.send(event, f"{event.sender.member_name} 已取消订阅 {summon}！")
                    else:
                        await bot.send(event, f"{event.sender.member_name} 未订阅 {summon}！")
                else:
                    await bot.send(event, f"大召唤阵 {summon} 不存在！")

            # 执行大召唤阵
            elif msg.startswith("大召唤阵"):
                _, summon = msg.split("大召唤阵", 1)
                summon = summon.strip()
                if summon in group_data.get("召唤阵", {}):
                    # 过滤出订阅状态为1的用户
                    subscribed_users = [user for user, status in group_data["召唤阵"][summon].items() if status == 1]
                    if subscribed_users:
                        at_list = [At(user) for user in subscribed_users]
                        #await bot.send(event, [*at_list, Plain(f"\n召唤阵 {summon} 开启！")])
                        await bot.send(event, [f"{summon}大召唤阵——开启！\n",*at_list])
                        # 移除订阅状态为0的用户
                        group_data["召唤阵"][summon] = {user: status for user, status in group_data["召唤阵"][summon].items() if status == 1}
                        save_group_data(group_id, group_data)
                    else:
                        await bot.send(event, f"当前没有人订阅 {summon}！")
                else:
                    await bot.send(event, f"大召唤阵 {summon} 不存在！")


         
     
        
        
        
        



    
    
    
    