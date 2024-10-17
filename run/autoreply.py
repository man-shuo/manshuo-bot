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
import asyncio
import datetime
from mirai import Startup, Shutdown
import json

import re
from asyncio import sleep
from io import BytesIO
import requests
from PIL import Image as Image1
from mirai import GroupMessage, At, Plain
from mirai import Image, Voice, Startup, MessageChain
from mirai.models import ForwardMessageNode, Forward

from plugins.toolkits import group_manage_controller

_task = None

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

def manage_group_status(user_id, status=None,file_name=None,target_group=None,type=None):
    if file_name:
        file_path = 'manshuo_data/wife_you_want_img'
        file_path=os.path.join(file_path,file_name)
    else:
        file_path = "manshuo_data/wife_you_want_img/wife_you_want.yaml"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            yaml.dump({}, file)
    with open(file_path, 'r') as file:
        try:
            users_data = yaml.safe_load(file) or {}
        except yaml.YAMLError:
            users_data = {}
    #print(users_data)
    if type is None:
        type='day'#0代表天数，1代表周，2代表月
    if status is not None:
        if target_group is not None:
            if type=='day':
                if type not in users_data:
                    users_data[type] = {}
                if target_group not in users_data[type]:
                    users_data[type][target_group] = {}
                if user_id not in users_data[type][target_group]:
                    users_data[type][target_group][user_id] = 0
                number = int(users_data[type][target_group][user_id])
                users_data[type][target_group][user_id] = number + 1
                type = 'week'
            if type == 'week':
                if type not in users_data:
                    users_data[type] = {}
                if target_group not in users_data[type]:
                    users_data[type][target_group] = {}
                if user_id not in users_data[type][target_group]:
                    users_data[type][target_group][user_id] = 0
                number = int(users_data[type][target_group][user_id])
                users_data[type][target_group][user_id] = number + 1
                type = 'moon'
            if type == 'moon':
                if type not in users_data:
                    users_data[type] = {}
                if target_group not in users_data[type]:
                    users_data[type][target_group] = {}
                if user_id not in users_data[type][target_group]:
                    users_data[type][target_group][user_id] = 0
                number=int(users_data[type][target_group][user_id])
                #print(number)
                users_data[type][target_group][user_id] = number + 1
        else:
            users_data[user_id] = status
        with open(file_path, 'w') as file:
            yaml.safe_dump(users_data, file)
        return status

    if target_group:
        return users_data.get(type, {}).get(target_group, {}).get(user_id, False)
    else:
        return users_data.get(user_id, False)

def sort_yaml(file_name,target_group,type=None):
    file_path = 'manshuo_data/wife_you_want_img'
    file_path = os.path.join(file_path, file_name)
    if not os.path.exists(file_path):
        return '还没有任何一位群友开过趴哦',None
    if type is None:
        type='day'#0代表天数，1代表周，2代表月
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    if type not in data:
        return '还没有任何一位群友开过趴哦',None
    if target_group not in data[type]:
        return '本群还没有任何一位群友开过趴哦',None
    data=data.get(type, {}).get(target_group, {})
        #print(data)
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    context=''
    king=None
    time=0
    for key, value in sorted_data:
        context +=f'【{key}】: {value}次~\n'
        if time != 0:
            continue
        time += 1
        king = key
    return context,king

filename = "variables.txt"

def get_game_image(url,filepath,id):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    id = str(id) + '.jpg'
    #print(str(id))
    # 获取指定文件夹下的所有文件
    files = os.listdir(filepath)
    if id in files:
        img_path = os.path.join(filepath, id)
        print('图片已存在，返回图片名称')
        return img_path
    # 过滤出文件名（不包含文件夹）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        #filename = url.split('/')[-1]
        id = str(id)
        img_path = os.path.join(filepath, id)
        #print(img_path)
        # 打开一个文件以二进制写入模式保存图片
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print("图片已下载并保存为 {}".format(img_path))
        return img_path
    else:
        print(f"下载失败，状态码: {response.status_code}")
        return None

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
def translate(text):
    #text=This is a test text&from=en&to=zh-CN
    params = {
        "text": text,
        "from": 'zh-CN',
        "to": "ja"
    }
    url = 'https://translate.appworlds.cn'
    # url="https://api.hikarinagi.com/random/v2/?tag=原神&num=1&r-18=false"
    response = httpx.get(url, params=params)
    # print(response)
    if response.status_code:
        # print(response.status_code)
        json_check = response.json()
        msg=json_check["msg"]
        data = json_check['data']
        #print(data)
        if msg == 'ok':
            return data
        else:
            return False
def main(bot, logger):
    with open('config.json', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    config = data
    botName = str(config.get('botName'))
    master = int(config.get('master'))
    mainGroup = int(config.get("mainGroup"))

    directory_img_check = 'manshuo_data/today_wife'
    files_img_check = os.listdir(directory_img_check)
    files_img_check = [f for f in files_img_check if os.path.isfile(os.path.join(directory_img_check, f))]
    logger.info("今日老婆列表读取完毕")
    rnum00 = 2

    @bot.on(GroupMessage)#各种自定义回复
    async def help(event: GroupMessage):
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
        if ('漫朔' in str(event.message_chain))and('查询' in str(event.message_chain) or '今日' in str(event.message_chain)):
            type = random.randint(1, 7)
            name_nickname = str(event.sender.member_name)
            if type == 1:
                # name_nickname = str(event.sender.member_name)
                logger.info('漫朔自定义回复，type1')
                await bot.send(event, '不给' + str(name_nickname) + '今天的漫朔哦，这可是秘密~')
            elif type == 2:
                logger.info('漫朔自定义回复，type2')
                #await bot.send(event, '这是今天的漫朔哦~~')
                rnum0 = random.randint(1, 3)
                if rnum0 == 1:
                    #s = [Image(path='manshuo_data/fonts/guaiqiao.png')]
                    await bot.send(event, ['这是今天的漫朔哦~~',Image(path='manshuo_data/fonts/guaiqiao.png')])
                else:
                    count_number = len(files_img_check)
                    rnum1 = random.randint(0, count_number - 1)
                    img_rnum = files_img_check[rnum1]
                    # print(img_rnum)
                    img_path = os.path.join(directory_img_check, img_rnum)
                    logger.info(f"获取到漫朔图片地址{img_path}")
                    #s = [Image(path=img_path)]
                    await bot.send(event, ['这是今天的漫朔哦~~', Image(path=img_path)])
                    #await bot.send(event, s)
            elif type == 3:
                logger.info('漫朔自定义回复，type3')
                await bot.send(event, '你怎么天天想着人家？' + str(name_nickname) + '好怪哦')
            elif type == 4:
                logger.info('漫朔自定义回复，type4')
                await bot.send(event, str(botName) + '才不允许你看我家哥哥呢')
            elif type == 5:
                logger.info('漫朔自定义回复，type5')
                count_number = len(files_img_check)
                rnum1 = random.randint(0, count_number - 1)
                img_rnum = files_img_check[rnum1]
                # print(img_rnum)
                img_path = os.path.join(directory_img_check, img_rnum)
                logger.info(f"获取到漫朔图片地址{img_path}")
                # s = [Image(path=img_path)]
                await bot.send(event, ['这是今天的漫朔哦~~', Image(path=img_path)])
            elif type == 6:
                logger.info('漫朔自定义回复，type6')
                s = [Image(path='manshuo_data/fonts/momobendan.png')]
                await bot.send(event, s)
            else:
                await bot.send(event,'您想要什么样的漫朔呢（歪头')
        if '打卡' in str(event.message_chain) in event.message_chain:
            s=[Image(path='manshuo_data/fonts/daka.png')]
            #for i in s:
            await bot.send(event, s)
            #logger.info("制图菜单")
            #await bot.send(event, '发送 pet 以查看制图功能列表')

        if '亲' in str(event.message_chain) and '漫朔' in str(event.message_chain):
            logger.info("漫朔自定义回复")
            rnum0 = random.randint(1, 5)
            if rnum0 == 1:
                logger.info("漫朔自定义回复成功触发，type1")

                await bot.send(event, '不准你亲QAQ')
                #await bot.send(event, s)
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
        if 'help' == str(event.message_chain) :
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
            rnum0 = random.randint(1, 4)
            if rnum0 == 1:
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
        if str(event.message_chain).startswith("今"):
            if ('今日' in str(event.message_chain) or '今天' in str(event.message_chain) or '今日' in str(event.message_chain)) and '老婆' in str(event.message_chain):
                logger.info("今日老婆开启！")
                count_number = len(files_img_check)
                if group_manage_controller(f'{event.group.id}_today_wife'):
                    if'张' in str(event.message_chain) or '个' in str(event.message_chain) or '位' in str(event.message_chain):
                        cmList=[]
                        context = str(event.message_chain)
                        name_id_number = re.search(r'\d+', context)
                        if name_id_number:
                            number = int(name_id_number.group())
                            if number >5:
                                await bot.send(event, '数量过多，渣男！！！！')
                            else:
                                #number=5
                                for i in range(number):
                                    rnum1 = random.randint(0, count_number - 1)
                                    img_rnum = files_img_check[rnum1]
                                    # print(img_rnum)
                                    img_path = os.path.join(directory_img_check, img_rnum)
                                    logger.info(f"获取到老婆图片地址{img_path}")
                                    s = [Image(path=img_path)]
                                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                                            message_chain=MessageChain(Image(path=img_path)))
                                    cmList.append(b1)
                                await bot.send(event, Forward(node_list=cmList))
                    else:
                        rnum1 = random.randint(0, count_number-1)
                        img_rnum=files_img_check[rnum1]
                        #print(img_rnum)
                        img_path=os.path.join(directory_img_check,img_rnum)
                        logger.info(f"获取到老婆图片地址{img_path}")
                        s=[Image(path=img_path)]
                        await bot.send(event, s)

        if ('qiqi' in str(event.message_chain)) and ('男娘' in str(event.message_chain)):
            s=[Image(path='manshuo_data/fonts/qiqinanniang.png')]
            await bot.send(event, s)
        if '哼哼' in str(event.message_chain):
            s=[Image(path='manshuo_data/fonts/atri_kaixin.gif')]
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

    @bot.on(GroupMessage)#劝小白看文档
    async def help(event: GroupMessage):

        if event.group.id == 251807019 or event.group.id == 623265372:
            if '怎么' in str(event.message_chain) or '大佬' in str(event.message_chain):  # 前置触发词
                rnum0 = random.randint(1, 100)
                logger.info(f"小白蒙蔽拳！！！typr={rnum0}")
                if rnum0 < 60:
                    await bot.send(event, [f'{botName}提示您，遇到问题先看文档哟',Image(path='manshuo_data/fonts/wendang.png')
                        ,f'看完文档后还请自行百度确定自己无法独立解决该问题\n然后在提问群友时请描述清楚问题并附上控制台报错截图，谢谢\n文档备用地址：https://www.manshuo.ink/index.php/archives/149/'])

    @bot.on(GroupMessage)#来点图图
    async def help(event: GroupMessage):
        if group_manage_controller(f'{event.group.id}_P_select_search'):
            if str(event.message_chain).startswith("来点"):
            #if ('来点' in str(event.message_chain)):#前置触发词
                flag_wife = 0
                filepath = 'manshuo_data/wife_random'
                context=str(event.message_chain)
                test_context = context.replace("来点", "")
                logger.info(f"色图搜索开启！tag：{test_context}")
                if test_context=='色图':
                    params = {
                        "format": "json",
                        "num": '1',
                        "type": "auto",
                        "size": "regular",
                        'tag': '美しい',
                        'ex-tag':'創作BL',
                        'r-18': False
                    }
                elif '美' in test_context:
                    params = {
                        "format": "json",
                        "num": '1',
                        "type": "auto",
                        "size": "regular",
                        'tag': '美しい',
                        'ex-tag':'創作BL',
                        'r-18': False
                    }
                elif '18' in test_context:
                    params = {
                        "format": "json",
                        "num": '1',
                        "type": "auto",
                        "size": "regular",
                        'tag': 'R-18',
                        'ex-tag':'創作BL',
                        'r-18': True
                    }
                else:
                    if test_context:

                        try:
                            test_context_translate = translate(test_context)
                            if test_context_translate:
                                logger.info(f"中译日成功，返回数据：{test_context_translate}")
                                logger.info(f"尝试进行日文tag搜索{test_context_translate}")
                                params = {
                                    "format": "json",
                                    "num": '1',


                                    'tag': test_context_translate
                                }
                                url = 'https://api.hikarinagi.com/random/v2/?'
                                response = httpx.get(url, params=params)
                                data = response.json()
                                if 'error' in data:
                                    raise Exception("这是一个手动引发的错误")
                        except Exception:
                            try:
                                logger.error("日文tag搜索失败")
                                logger.info(f"尝试进行中文tag搜索:{test_context}")
                                params = {
                                    "format": "json",
                                    "num": '1',


                                    'tag': test_context
                                }
                                url = 'https://api.hikarinagi.com/random/v2/?'
                                # url="https://api.hikarinagi.com/random/v2/?tag=原神&num=1&r-18=false"
                                response = httpx.get(url, params=params)
                                data = response.json()
                                #print(data)
                                if 'error' in data:
                                    raise Exception("这是一个手动引发的错误")
                            except Exception:
                                try:
                                    logger.error("中文tag搜索失败")
                                    pass
                                    logger.info(f"尝试进行中文title搜索: {test_context}")
                                    params = {
                                        "format": "json",
                                        "num": '1',
                                        "type": "auto",
                                        "size": "regular",

                                        'title': test_context
                                    }
                                    #raise Exception("这是一个手动引发的错误")
                                    url = 'https://api.hikarinagi.com/random/v2/?'
                                    #response = httpx.get(url, params=params)
                                    #data = response.json()
                                except Exception:
                                    pass
                                    logger.error("中文title搜索失败")
                                    test_context_translate = translate(test_context)
                                    logger.info(f"尝试进行日文title搜索: {test_context_translate}")
                                    try:
                                        params = {
                                            "format": "json",
                                            "num": '1',
                                            "type": "auto",
                                            "size": "regular",

                                            'title': test_context_translate
                                        }
                                        url = 'https://api.hikarinagi.com/random/v2/?'
                                        #response = httpx.get(url, params=params)
                                        #data = response.json()

                                    except Exception:
                                        logger.error("日文title搜索失败")
                                        flag_wife = 1



                url = 'https://api.hikarinagi.com/random/v2/?'
                # url="https://api.hikarinagi.com/random/v2/?tag=原神&num=1&r-18=false"
                try:
                    response = httpx.get(url, params=params)
                    if response.status_code == 200:
                    #print(response.status_code)
                        data = response.json()
                    if 'error' in data:
                        await bot.send_group_message(event.sender.group.id,
                                                     [f'{botName}好像找不到您所说{test_context}的照片哦'])
                    else:
                        test = data[0]
                        url = test['url']
                        pid = test['pid']
                        tags = test['tags']
                        print(tags)
                        proxy_url = url.replace("https://i.pximg.net/", "https://i.yuki.sh/")
                        logger.info(f"搜索成功，作品pid：{pid}，反代url：{proxy_url}")
                        img_path = get_game_image(proxy_url, filepath, pid)
                        if '18' in test_context:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'这是{botName}为您找到的图片哟\nurl：{proxy_url}\ntags:{tags}'])
                        else:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'这是{botName}为您找到的图片哟',
                                                          Image(path=img_path)])

                except Exception:
                    logger.error("搜索失败")
                    await bot.send_group_message(event.sender.group.id,
                                                 [f'{botName}好像找不到您所说{test_context}的照片哦'])

    @bot.on(GroupMessage)#透群友合集
    async def help(event: GroupMessage):

        if ('/' in str(event.message_chain)):#前置触发词
            if group_manage_controller(f'{event.group.id}_wife_you_want'):
                pass
            else:
                return
            flag_persona = 0
            flag_aim = 0
            if ('透群主' in str(event.message_chain)):
                flag_persona=1
                check='OWNER'
                pass
            elif ('透管理' in str(event.message_chain)):
                flag_persona = 2
                check = 'ADMINISTRATOR'
                pass
            elif ('透群友' in str(event.message_chain)):
                flag_persona = 3
                pass
            elif ('娶群友' in str(event.message_chain)):
                flag_persona = 4
                from_id = int(event.sender.id)
                if manage_group_status(from_id) :
                    target_group = int(event.group.id)
                    target_id_aim=manage_group_status(from_id)
                    flag_aim = 1
                else:
                    flag_aim = 0
                pass
            elif ('离婚' in str(event.message_chain)):
                from_id = int(event.sender.id)
                manage_group_status(from_id,False)
                manage_group_status(f'{from_id}_name', False)
                await bot.send(event, '离婚啦，您现在是单身贵族咯~')
            else:
                flag_persona=0

            if flag_persona == 3 or flag_persona == 4:

                context=str(event.message_chain)
                name_id_number=re.search(r'\d+', context)
                if name_id_number:
                    if flag_aim == 1:
                        await bot.send(event, '渣男！吃着碗里的想着锅里的！', True)
                        flag_persona = 0
                        flag_aim = 0
                    else:
                        number = int(name_id_number.group())
                        target_id_aim=number
                        #print(target_id_aim)
                        rnum1 = random.randint(1, 10)
                        if rnum1 > 3:
                            #await bot.send(event, '不许瑟瑟！！！！', True)
                            target_group = int(event.group.id)
                            group_member_check = await bot.get_group_member(target_group, target_id_aim)
                            #print(group_member_check)
                            if group_member_check:
                                flag_aim=1
                    #print(rnum1)
                    #print(flag_aim)



                rnum0 = random.randint(1, 10)
                if rnum0 == 1:
                    await bot.send(event, '不许瑟瑟！！！！')
                    flag_persona = 0

            if flag_persona != 0:
                logger.info("透群友任务开启")
                filepath = 'manshuo_data/wife_you_want_img'
                friendlist = []
                target_name = None
                target_id = None
                target_img = None
                # target_nikenamne=None
                from_name = str(event.sender.member_name)
                from_id = int(event.sender.id)
                #flag_aim = 0
                target_group = int(event.group.id)
                friendlist_get = await bot.member_list(target_group)
                data = friendlist_get.json()
                data = json.loads(data)
                data_count = len(data["data"])
                for i in range(data_count):
                    data_test=None
                    data_check = data['data'][i]['permission']
                    if flag_persona == 1 or flag_persona == 2:
                        if data_check == check:
                            data_test = data['data'][i]['id']
                    elif flag_persona == 3 or flag_persona == 4:
                        data_test = data['data'][i]['id']
                    if data_test != None:
                        friendlist.append(data_test)
                    #print(data_test)
                #print(friendlist)
                number_target = len(friendlist)
                target_number = random.randint(1, number_target)
                target_id = friendlist[target_number - 1]

                if flag_aim == 1 :
                    target_id=target_id_aim

                #print(target_id)
                logger.info(f'群：{target_group}，透群友目标：{target_id}')
                group_member_check = await bot.get_group_member(target_group, target_id)
                # target_id = extract_between_symbols(str(group_member_check), 'id=', ' member')
                if manage_group_status(f'{from_id}_name') and flag_persona == 4:
                    target_name=manage_group_status(f'{from_id}_name')
                else:
                    group_member_check = group_member_check.json()
                    group_member_check = json.loads(group_member_check)
                    target_name=group_member_check['member_name']
                    #target_name = extract_between_symbols(str(group_member_check), 'member_name=', ' permission')


                if flag_persona == 4:
                    if manage_group_status(from_id):
                        flag_aim = 0
                    manage_group_status(from_id, target_id)
                    manage_group_status(f'{from_id}_name', target_name)

                # 下面是获取对应人员头像的代码
                target_img_url = f"https://q1.qlogo.cn/g?b=qq&nk={target_id}&s=640"  # QQ头像 URL 格式
                target_img_path = get_game_image(target_img_url, filepath, target_id)

                from_name=str(from_name)
                target_name = str(target_name)
                target_times=manage_group_status(f'{target_name} ({target_id})',True,target_group=target_group,file_name='wife_you_want_week_check_target.yaml')
                from_times=manage_group_status(f'{from_name} ({from_id})',True,target_group=target_group,file_name='wife_you_want_week_check_from.yaml')
                #print(f'target_times: {target_times} , from_times: {from_times}')




                if group_manage_controller(f'{event.group.id}_wife_you_want'):
                    if flag_persona == 1:
                        if manage_group_status(f'{target_id}_ower_time'):
                            times = int(manage_group_status(f'{target_id}_ower_time'))
                            times += 1
                            manage_group_status(f'{target_id}_ower_time', times)
                        else:
                            times = 1
                            manage_group_status(f'{target_id}_ower_time', 1)
                        await bot.send_group_message(event.sender.group.id,
                                                     [f'@{from_name} 恭喜你涩到群主！！！！',
                                                      Image(path=target_img_path),
                                                      f'群主【{target_name}】今天这是第{times}次被透了呢'])
                    if flag_persona == 2:
                        await bot.send_group_message(event.sender.group.id,
                                                     [f'@{from_name} 恭喜你涩到管理！！！！',
                                                      Image(path=target_img_path),
                                                      f'【{target_name}】 ({target_id})哒！'])
                    if flag_persona == 3:
                        if flag_aim == 1:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'@{from_name} 恭喜你涩到了群友！！！！',
                                                          Image(path=target_img_path),
                                                          f'【{target_name}】 ({target_id})哒！'])
                        else:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'@{from_name} 今天你的色色对象是',
                                                          Image(path=target_img_path),
                                                          f'【{target_name}】 ({target_id})哒！'])
                    if flag_persona == 4:
                        if flag_aim == 1:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'@{from_name} 恭喜你娶到了群友！！！！',
                                                          Image(path=target_img_path),
                                                          f'【{target_name}】 ({target_id})哒！'])
                        else:
                            await bot.send_group_message(event.sender.group.id,
                                                         [f'@{from_name} 今天你的结婚对象是',
                                                          Image(path=target_img_path),
                                                          f'【{target_name}】 ({target_id})哒！'])
            if '记录' in str(event.message_chain) and (
                    '色色' in str(event.message_chain) or '瑟瑟' in str(event.message_chain) or '涩涩' in str(
                    event.message_chain)):
                target_group = int(event.group.id)
                cmList = []
                if '本周' in str(event.message_chain) or '每周' in str(event.message_chain) or '星期' in str(event.message_chain):
                    logger.info(f'本周色色记录启动！')
                    type_context='以下是本周色色记录：'
                    target_context,target_king = sort_yaml('wife_you_want_week_check_target.yaml',target_group,'week')
                    from_context,from_king = sort_yaml('wife_you_want_week_check_from.yaml',target_group,'week')
                elif '本月' in str(event.message_chain) or '月份' in str(event.message_chain) or '月' in str(event.message_chain):
                    logger.info(f'本周色色记录启动！')
                    type_context = '以下是本月色色记录：'
                    target_context,target_king = sort_yaml('wife_you_want_week_check_target.yaml',target_group,'moon')
                    from_context,from_king = sort_yaml('wife_you_want_week_check_from.yaml',target_group,'moon')
                else:
                    logger.info(f'本日色色记录启动！')
                    type_context = '以下是本日色色记录：'
                    target_context,target_king = sort_yaml('wife_you_want_week_check_target.yaml',target_group)
                    from_context,from_king = sort_yaml('wife_you_want_week_check_from.yaml',target_group)
                if '没有任何一位' in target_context or '没有任何一位' in from_context:
                    await bot.send(event, f'{target_context}')
                else:
                    filepath = 'manshuo_data/wife_you_want_img'
                    target_king_name, inside_with_parens = target_king.split(" (")
                    target_king_id = inside_with_parens.rstrip(")")  # 去除右括号
                    from_king_name, inside_with_parens = from_king.split(" (")
                    from_king_id = inside_with_parens.rstrip(")")  # 去除右括号
                    target_img_url = f"https://q1.qlogo.cn/g?b=qq&nk={target_king_id}&s=640"  # QQ头像 URL 格式
                    from_img_url = f"https://q1.qlogo.cn/g?b=qq&nk={from_king_id}&s=640"
                    target_img_path = get_game_image(target_img_url, filepath, target_king_id)
                    from_img_path = get_game_image(from_img_url, filepath, from_king_id)
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(str(type_context)))
                    cmList.append(b1)
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain([f'被群友透最多的人诞生了！！',
                                                          Image(path=target_img_path),
                                                          f'是【{target_king_name}】 ({target_king_id})哦~']))
                    cmList.append(b1)
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(f'群友被透的次数如下哦：\n{target_context}'))
                    cmList.append(b1)
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain([f'群最涩色魔，透群友大王出现了！',
                                                          Image(path=from_img_path),
                                                          f'【{from_king_name}】 ({from_king_id})的说~~']))
                    cmList.append(b1)
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(f'群友透别人的次数如下哦：\n{from_context}'))
                    cmList.append(b1)
                    await bot.send(event, Forward(node_list=cmList))

    @bot.on(GroupMessage)#部分功能权限管理
    async def function_manager(event: GroupMessage):
        if '测试' in str(event.message_chain):
            context = await bot.get_group_member(event.group.id, event.sender.id)
            data = context.json()
            data = json.loads(data)
            permission = data['permission']
            if permission == 'OWNER' or permission == 'ADMINISTRATOR':
                print(f"检测到管理员：{permission}")
        if '权限列表' in str(event.message_chain):
            context = await bot.get_group_member(event.group.id, event.sender.id)
            data = context.json()
            data = json.loads(data)
            permission = data['permission']
            if permission == 'OWNER' or permission == 'ADMINISTRATOR' or event.sender.id == master:
                wife_you_want=group_manage_controller(f'{event.group.id}_wife_you_want')
                today_wife=group_manage_controller(f'{event.group.id}_today_wife')
                ing_search=group_manage_controller(f'{event.group.id}_ing_search')
                P_select_search=group_manage_controller(f'{event.group.id}_P_select_search')
                tarot=group_manage_controller(f'{event.group.id}_tarot')
                Reload=group_manage_controller(f'{event.group.id}_Reload')
                maimai=group_manage_controller(f'{event.group.id}_maimai')
                await bot.send(event, f'目前支持单独开关的功能权限：\n'
                                      f'①透群友功能: {wife_you_want}\n'
                                      f'②今日老婆: {today_wife}\n'
                                      f'③搜图识图功能： {ing_search}\n'
                                      f'④P站图片搜索（来点XX）： {P_select_search}\n'
                                      f'⑤今日运势or塔罗： {tarot}\n'
                                      f'⑥复读功能： {Reload}\n'
                                      f'⑦MaiMai排卡: {maimai}\n'
                                      f'请管理员搭配 “开启" or "关闭" 食用')
        if str(event.message_chain).startswith("开启"):
            context = await bot.get_group_member(event.group.id, event.sender.id)
            data = context.json()
            data = json.loads(data)
            permission = data['permission']
            if permission == 'OWNER' or permission == 'ADMINISTRATOR' or event.sender.id == master:
                #await bot.send(event, f'目前支持单独开关的功能权限：\n①透群友功能；②今日老婆；\n请搭配“开启"or"关闭"食用')
                if '透群友' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_wife_you_want',True)
                    await bot.send(event, f'透群友功能开启！')
                if '今日老婆' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_today_wife', True)
                    await bot.send(event,f'今日老婆功能开启！')
                if '搜图识图' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_ing_search', True)
                    await bot.send(event,f'搜图识图功能功能开启！')
                if 'P站图片' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_P_select_search', True)
                    await bot.send(event,f'P站图片搜索功能开启！')
                if '今日运势or塔罗' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_tarot', True)
                    await bot.send(event,f'今日运势or塔罗搜索功能开启！')
                if '复读功能' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_Reload', True)
                    await bot.send(event,f'复读功能搜索功能开启！')
                if 'MaiMai排卡' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_maimai', True)
                    await bot.send(event,f'MaiMai排卡功能开启！')
        if str(event.message_chain).startswith("关闭"):
            context = await bot.get_group_member(event.group.id, event.sender.id)
            data = context.json()
            data = json.loads(data)
            permission = data['permission']
            if permission == 'OWNER' or permission == 'ADMINISTRATOR' or event.sender.id == master:
                #await bot.send(event, f'目前支持单独开关的功能权限：\n①透群友功能；②今日老婆；\n请搭配“开启"or"关闭"食用')
                if '透群友' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_wife_you_want',False)
                    await bot.send(event, f'透群友功能已关闭~~')
                elif '今日老婆' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_today_wife', False)
                    await bot.send(event, f'今日老婆功能已关闭~~')
                elif '搜图识图' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_ing_search', False)
                    await bot.send(event,f'搜图识图功能已关闭~~')
                elif 'P站图片' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_P_select_search', False)
                    await bot.send(event,f'P站图片搜索已关闭~~')
                elif '今日运势or塔罗' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_tarot', False)
                    await bot.send(event,f'今日运势or塔罗搜索功能已关闭~~')
                elif '复读功能' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_Reload', False)
                    await bot.send(event,f'复读功能搜索功能已关闭~~')
                elif 'MaiMai排卡' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_maimai', False)
                    await bot.send(event,f'MaiMai排卡功能已关闭~~')
                elif '所有' in str(event.message_chain):
                    group_manage_controller(f'{event.group.id}_wife_you_want', False)
                    group_manage_controller(f'{event.group.id}_today_wife', False)
                    group_manage_controller(f'{event.group.id}_ing_search', False)
                    group_manage_controller(f'{event.group.id}_P_select_search', False)
                    group_manage_controller(f'{event.group.id}_tarot', False)
                    group_manage_controller(f'{event.group.id}_Reload', False)
                    await bot.send(event, f'执行完毕')


    @bot.on(Startup)#部分文件指定删除，用以实现循环
    async def start_scheduler(_):
        async def timer():
            today_finished = False  # 设置变量标识今天是会否完成任务，防止重复发送
            while True:
                await asyncio.sleep(1)
                now = datetime.datetime.now()
                today = datetime.datetime.today()
                weekday = today.weekday()
                month = datetime.datetime.now().month
                day = datetime.datetime.now().day
                if now.hour == 00 and now.minute == 00 and not today_finished:  # 每天早上 7:30 发送早安
                    file_path_check="manshuo_data/wife_you_want_img/wife_you_want.yaml"
                    if os.path.exists(file_path_check):
                        os.remove(file_path_check)
                    file_path="manshuo_data/wife_you_want_img/wife_you_want_week_check_target.yaml"
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as file:
                            users_data = yaml.safe_load(file) or {}
                            type='day'
                            users_data[type] = {}
                        if int(weekday) == 0:
                            type = 'week'
                            users_data[type] = {}
                        if int(day) == 1:
                            type = 'moon'
                            users_data[type] = {}
                        with open(file_path, 'w') as file:
                            yaml.safe_dump(users_data, file)
                    print('娶群友事件已重置')
                    today_finished = True
                if now.hour == 00 and now.minute == 1:
                    today_finished = False  # 早上 7:31，重置今天是否完成任务的标识

        global _task
        _task = asyncio.create_task(timer())

    @bot.on(Shutdown)
    async def stop_scheduler(_):
        # 退出时停止定时任务
        if _task and not task.done():
            _task.cancel()






        
      