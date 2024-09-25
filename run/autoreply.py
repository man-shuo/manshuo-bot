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




#from PIL import Image
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown,MessageChain

def read_paragraphs_from_file(filename):
    # 读取文件中的所有段落，并以字典形式返回，键为序号，值为段落内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        paragraphs = content.split('\n')  # 按照两个换行符拆分段落
        numbered_paragraphs = {i+1: para.strip() for i, para in enumerate(paragraphs)}  # 给每个段落加上序号
    return numbered_paragraphs
def get_random_paragraph(numbered_paragraphs):
    # 随机选择一个序号
    random_index = random.choice(list(numbered_paragraphs.keys()))
    return random_index, numbered_paragraphs[random_index]


filename = "variables.txt"

# 初始化文件内容，如果文件不存在则创建
def initialize_variables(variables_dict):
    with open(filename, 'w') as file:
        for key, value in variables_dict.items():
            file.write(f"{key}={value}\n")

# 读取变量值
def read_variables():
    variables_dict = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            variables_dict[key] = value
    return variables_dict

# 读取单个变量值
def read_variable(key):
    variables = read_variables()
    return variables.get(key, None)

# 修改单个变量值
def update_variable(key, new_value):
    variables = read_variables()
    variables[key] = str(new_value)
    initialize_variables(variables)

def main(bot, logger):
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):






        rnum00=2;

        if ('测试' in str(event.message_chain) or 'test' in str(event.message_chain) ) and At(bot.qq) in event.message_chain:
            logger.info("测试")
            pass
            
            #await bot.send(event, At(name_id) +" 这也是测试的一部分")
            #name_nickname = str(event.sender.member_name)
            #await bot.send(event, "测试者QQ昵称："+str(name_nickname))
            #await bot.send(event, "@"+str(name_nickname))
            

            #print(f"被艾特成员的昵称: {nickname}")

        #if ('可用角色' in str(event.message_chain) ) and At(bot.qq) in event.message_chain:
            #logger.info("测试")

            #await bot.send(event, '访问此网站以查看' + botName + '的功能列表\nヾ(≧▽≦*)o\n发送 pet 以查看制图功能列表')
        if '你好' in str(event.message_chain) and At(bot.qq) in event.message_chain :
            logger.info("你好")
            await bot.send(event, '你好哟~~~')
        if '打卡' in str(event.message_chain) in event.message_chain:
            s=[Image(path='manshuo_data/fonts/daka.png')]
            #for i in s:
            await bot.send(event, s)
            #logger.info("制图菜单")
            #await bot.send(event, '发送 pet 以查看制图功能列表')
        if '柚子处' in str(event.message_chain) or '柚子除' in str(event.message_chain) or '柚子厨' in str(event.message_chain) or 'yuzusoft' in str(event.message_chain) :
            logger.info("yuzu自定义回复")
            rnum0=random.randint(1,6)
            if rnum0 == 1:
                logger.info("yuzu自定义回复成功触发，type1")
                
                s=[Image(path='manshuo_data/fonts/ciallo.jpg')]
                await bot.send(event, s)
            if rnum0 == 2:
                logger.info("yuzu自定义回复成功触发，type2")
                await bot.send(event, 'Ciallo～(∠・ω< )⌒☆')
            if rnum0 == 3:
                logger.info("yuzu自定义回复成功触发，type3")
                s=[Image(path='manshuo_data/fonts/yuzusoft1.png')]
                await bot.send(event, s)
            if rnum0 == 4:
                logger.info("yuzu自定义回复成功触发，type4")
                s=[Image(path='manshuo_data/fonts/yuzusoft2.png')]
                await bot.send(event, s)
            if rnum0 == 5:
                logger.info("yuzu自定义回复成功触发，type5")
                
                
        if 'bot群' in str(event.message_chain) :
            logger.info("自定义回复")
            await bot.send(event, '欢迎来到bot群发电🤪：674822468')
        if '谁家机器人' in str(event.message_chain) :
            logger.info("自定义回复")
            await bot.send(event, '我可是高性能机器人哦！ʕ •ᴥ•ʔ')
        if '/help' in str(event.message_chain) :
            logger.info("自定义回复")
            await bot.send(event, '请发送@bot+help获取帮助菜单')
        if '你不准打断' in str(event.message_chain) :
            logger.info("自定义回复")
            await bot.send(event, '你好像没有权利来规定我啊（生气')
        if ('败犬女主' in str(event.message_chain) or '败犬一号' in str(event.message_chain) or '八奈见' in str(event.message_chain) or '老八伟大' in str(event.message_chain)):
            logger.info("自定义回复")
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                await bot.send(event, '我八胃大，无需多盐！！')
        if '不理' in str(event.message_chain) :
            logger.info("自定义回复")
            await bot.send(event, '不理笨蛋（哼！',True)
            
            
        if '几卡' in str(event.message_chain) and At(bot.qq) in event.message_chain:
            logger.info("自定义回复")
            rnum=random.randint(1,12)+random.randint(0,135)//100*999
            
            await bot.send(event, str(rnum)+'卡')
            
            
        if '哪勤' in str(event.message_chain) and At(bot.qq) in event.message_chain:
            logger.info("自定义回复")
            rnum1=random.randint(1,7)
            rnum=random.randint(1,12)+random.randint(0,135)//100*999
            
            if rnum1==7 :
                await bot.send(event, '在李万勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==1:
                await bot.send(event, '在李大猫勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==2:
                await bot.send(event, '在金狮勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==3:
                await bot.send(event, '在李大狗勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==4:
                await bot.send(event, '在书院路万达勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==5:
                await bot.send(event, '在乐客城勤！'+str(rnum)+'卡'+'速来!!!')
            if rnum1==6:
                await bot.send(event, '在朗玩勤！'+str(rnum)+'卡'+'速来!!!')
            
            
            #await bot.send(event, str(rnum1)+'卡')
        
        
        if '音趴' in str(event.message_chain) and At(bot.qq) in event.message_chain:
            logger.info("自定义回复开学音趴")
            rnum1=random.randint(1,8)
            rnum2=random.randint(1,12)+random.randint(0,105)//100*999
            rnum3=random.randint(1,31)+random.randint(0,105)//100*999
            if rnum1==1:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，振声院!!!')
            if rnum1==2:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，图书馆!!!')
            if rnum1==3:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，你心里（嘿嘿',True)
            if rnum1==4:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，金狮广场!!!')
            if rnum1==5:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，李沧万达!!!')
            if rnum1==6:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，李大猫!!!')
            if rnum1==7:
                await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+'，我家!!!')
            if rnum1==8:
                await bot.send(event, '可以在你家里开趴嘛（嘻嘻',True)
            

                
            #await bot.send(event, '开学音趴将在'+str(rnum2)+'月'+str(rnum3)+'日'+速来!!!')
        
        
        if ('qiqi' in str(event.message_chain)) and ('男娘' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/qiqinanniang.png')]
            await bot.send(event, s)
        if ('qiqi' in str(event.message_chain)) and ('杂鱼' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/qiqizayu.png')]
            await bot.send(event, s)
        if ('点燃大海' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/burn.png')]
            await bot.send(event, s)
        if ('¿' in str(event.message_chain) or '不是哥们' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/atri.png')]
            await bot.send(event, s)
        if ('想要了' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/tafei.png')]
            await bot.send(event, s)
        if ('杂鱼杂鱼' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/zayu.png')]
            await bot.send(event, s)
        if ('杂鱼' in str(event.message_chain)) and At(bot.qq) in event.message_chain:
            s=[Image(path='manshuo_data/fonts/zayu2.png')]
            await bot.send(event, s)
        if ('异议' in str(event.message_chain) or 'objection' in str(event.message_chain) or '逆转' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/yiyi.png')]
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                await bot.send(event, s)
        if ('欸嘿' in str(event.message_chain) or '诶嘿' in str(event.message_chain)):
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                s=[Image(path='manshuo_data/fonts/eihei.png')]
                await bot.send(event, s)
        if ('乖巧' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/guaiqiao.png')]
            await bot.send(event, s)
        if ('啊啊' in str(event.message_chain) or '苦恼' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/shengqi.gif')]
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                await bot.send(event, s)
        if ('我爱你' in str(event.message_chain) or '你爱我' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/woaini.jpg')]
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                await bot.send(event, s)
        if ('我没意见' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/womeiyijian.png')]
            await bot.send(event, s)
        if ('红温' in str(event.message_chain)):
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                s=[Image(path='manshuo_data/fonts/hongwen.png')]
            await bot.send(event, s)
        if ('生气' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/shengqi2.gif')]
            await bot.send(event, s)
        if ('喂我' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/weini.gif')]
            await bot.send(event, s)
        if ('我勒个' in str(event.message_chain)):
            rnum0=random.randint(1,rnum00)
            #await bot.send(event, '测试rum00='+str(rnum00)+'，随机数'+str(rnum0))
            if rnum0 == 1:
                s=[Image(path='manshuo_data/fonts/woleige.jpg')]
                await bot.send(event, s)
                #await bot.send(event, '成功触发')
        if ('这辈子' in str(event.message_chain)):
            logger.info("自定义回复:这辈子")
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                logger.info("自定义回复：这辈子，成功触发")
                s=[Image(path='manshuo_data/fonts/zhebeizi.jpg')]
                await bot.send(event, s)
        if ('喂我' in str(event.message_chain)):
            logger.info("自定义回复：喂我")
            s=[Image(path='manshuo_data/fonts/weini.gif')]
            await bot.send(event, s)
        if ('兄弟你' in str(event.message_chain)):
            logger.info("自定义回复：兄弟你")
            rnum0=random.randint(1,rnum00)
            if rnum0 == 1:
                s=[Image(path='manshuo_data/fonts/xiongdi.jpg')]
                await bot.send(event, s)
                
        
        
        
        
      