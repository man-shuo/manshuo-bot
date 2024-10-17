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
import pytz
import datetime
import os
import json
import httpx
import re
import json
import os
import random
import httpx as requests
import sys
import time
import hashlib
from multiprocessing import Process, Lock
import re
from asyncio import sleep
from io import BytesIO
import requests
from PIL import Image as Image1
from mirai import GroupMessage, At, Plain
from mirai import Image, Voice, Startup, MessageChain
from mirai.models import ForwardMessageNode, Forward

from plugins.toolkits import random_str, picDwn, group_manage_controller
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown, MessageChain


class SaveData():
    base_dir = None
    lock = Lock()

    def __init__(self, filename):
        self.filename = os.path.join(self.base_dir, filename + ".json")
        self.data = {}
        self.load()

    def load(self):
        with self.lock:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.data = json.load(f)

    def save(self):
        with self.lock:
            if not os.path.exists(self.base_dir):
                os.makedirs(self.base_dir)
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, separators=(',', ':'))

    @classmethod
    def set_base_dir(cls, base):
        cls.base_dir = base


DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join("config.json")
DATA_DIR = os.path.join("manshuo_data/MaiMai_search")
SaveData.set_base_dir(DATA_DIR)


def fetch_wahlap():  # 华立服务器获取机厅列表
    arcade_url = "http://wc.wahlap.net/maidx/rest/location"
    try:
        res = httpx.get(arcade_url)
        res.raise_for_status()
        # print(res)
        arcade_list = res.json()
        arcade_mp = {}
        for arcade in arcade_list:
            arcade_mp[arcade["id"]] = arcade
        arcade_file = SaveData("arcade")
        arcade_file.data = arcade_mp
        arcade_file.save()
        print("从华立服务器获取机厅列表成功，" + "机厅数量：" + str(len(arcade_mp)))
        return arcade_mp
    except Exception:
        print("从华立服务器获取机厅列表失败")
        return None


def init_data():  # 初始化文件
    arcade_file = SaveData("arcade")
    arcade_list = arcade_file.data
    if not arcade_list:
        fetch_wahlap()
    data_file = SaveData("data")
    if not data_file.data:
        data_file.data = {
            "arcades": {},
            "alias": {}
        }

    data_file.save()


def search_arc(keywords):
    arcade_file = SaveData("arcade")
    arcade_list = arcade_file.data
    result = []
    keywords = keywords.strip()
    if len(keywords) < 2:
        # print( '关键词长度过短，请输入至少两个字符')
        return '(˃ ⌑ ˂ഃ )关键词长度过短，请输入至少两个字符'
    kwds = keywords.split(' ')
    # print(keyword)
    for arcade in arcade_list.values():
        for keyword in kwds:
            if (keyword in arcade["arcadeName"]) or (keyword in arcade["address"]):
                result.append(
                    f"\n{arcade['arcadeName']} | ID：{arcade['id']} | 机台数：{arcade['machineCount']}\n地址：{arcade['address']}\n")
    if not result:
        return "未找到相关机厅"
    ret = "枫与岚找到了这些机厅哦：\n" + "".join(
        result) + "\n如需要在本群添加别名，请艾特bot+添加机厅别名\n注意ID上文已经给出，别名不可以带空格哟"
    # print(ret)
    return ret


def refresh_wahlap():
    arcade_list = fetch_wahlap()
    if arcade_list:
        # print("刷新华立机台数据成功，" + "当前登记机厅数量：" + str(len(arcade_list)))
        return f'刷新华立机台数据成功，当前登记机厅数量：{len(arcade_list)}'
        # await refreshwahlap.finish("刷新华立机台数据成功，" + "当前登记机厅数量：" + str(len(arcade_list)))
    else:
        # await refreshwahlap.finish("刷新华立机台数据失败，将继续返回上次数据")
        # print("刷新华立机台数据失败，将继续返回上次数据")
        return "刷新华立机台数据失败，将继续返回上次数据"


def sync_arcade_from_wahlap(id):  # 同步华立信息到 data
    data_file = SaveData("data")
    arcade_file = SaveData("arcade")
    arcade_list = arcade_file.data
    if len(id) < 2:
        return False, "(˃ ⌑ ˂ഃ )同步华立api失败：ID长度不能过短呢"
    if id not in arcade_list and id not in data_file.data["arcades"]:
        return False, "(˃ ⌑ ˂ഃ )同步华立api失败：ID不存在哦，请在看一眼吧"
    arc = arcade_list[id]
    if id in data_file.data["arcades"]:
        data_file.data["arcades"][id]["machineCount"] = arc["machineCount"]
        data_file.data["arcades"][id]["name"] = arc["arcadeName"]
        data_file.data["arcades"][id]["province"] = arc["province"]
        data_file.data["arcades"][id]["address"] = arc["address"]
    else:
        data_file.data["arcades"][id] = {
            "machineCount": arc["machineCount"],
            "name": arc["arcadeName"],
            "province": arc["province"],
            "address": arc["address"],
        }
    # print(data_file.data["arcades"][id])
    if not "lastMsg" in data_file.data["arcades"][id]:
        data_file.data["arcades"][id]["lastMsg"] = "系统初次同步机台信息"
    if not "personCount" in data_file.data["arcades"][id]:
        data_file.data["arcades"][id]["personCount"] = 0
    data_file.save()
    return True, "…>_<…同步华立api成功, 机厅名称：" + arc["arcadeName"]


def add_arc(arcade, group_id, permission, sender_id, master):  # 机厅别名添加

    if permission != "OWNER" and permission != "ADMINISTRATOR" and sender_id != master:
        # print("权限不足，仅群主和管理员支持添加机台！")
        return "¯\_(ツ)_/¯您好像不是管理员呢~~"
    # print(arcade)
    arcade = arcade.strip()
    # print(arcade)
    arcade = str(arcade)
    if not ' ' in arcade or (arcade.split(' ')[0].isdigit() == False):
        # print(":( 请按照格式发送消息！")
        return "•᷄ࡇ•᷅ 请发送正确的格式哦"
    if "[CQ:" in arcade and (not "face,id" in arcade):
        # print(":( 请不要整除了表情外的其他花活！")
        return "…>_<…喵喵喵！"
    try:
        # forbidwords = ["+", "＋", "-", "－", "=", "＝"]
        arc, alias = arcade.split(' ', 1)
        # for word in forbidwords:
        #    if word in alias:
        #        await Text(":( 为避免影响更新卡功能，请不要在别名中使用特殊符号！").finish()
        sync_status, sync_msg = sync_arcade_from_wahlap(arc)
        # print(f"addArc: {arc} {alias}")
        # print(f"addArc: {sync_status} {sync_msg}")
        if sync_status:
            data_file = SaveData("data")
            if str(group_id) not in data_file.data["alias"]:
                data_file.data["alias"][str(group_id)] = {}
            data_file.data["alias"][str(group_id)][alias] = arc
            data_file.save()
            # await addArc.finish(message=Message(":) 机厅添加成功\n别名：" + alias + "\n机厅名称：" + data_file.data["arcades"][arc]["name"]))
            # print(":) 机厅添加成功\n别名：" + alias + "\n机厅名称：" + data_file.data["arcades"][arc]["name"])
            # context=":) 机厅添加成功\n别名：" + alias + "\n机厅名称：" + data_file.data["arcades"][arc]["name"]
            context = '成功为' + data_file.data["arcades"][arc]["name"] + '添加别名：' + alias + ' ❛‿˂̵✧'
            return context

        else:
            context = "O_o?! 在同步api时发生错误：\n" + sync_msg
            return context
    except Exception as e:
        return "O_o?!好像出错了呢"


def del_arc(alias, group_id, permission, sender_id, master):
    if permission != "OWNER" and permission != "ADMINISTRATOR" and sender_id != master:
        return "¯\_(ツ)_/¯您好像不是管理员呢~~"
    alias = alias.strip()
    data_file = SaveData("data")
    if str(group_id) not in data_file.data["alias"]:
        return "＞_＜本群数据尚未初始化"
    if alias not in data_file.data["alias"][str(group_id)]:
        return "＞_＜该别名好像不存在的说"
    del data_file.data["alias"][str(group_id)][alias]
    data_file.save()
    return " ❛‿˂̵✧删除别名成功！"


def set_arc_person(reg, group_id, nickname, user_id):  # 查询机厅人数
    pattern = r'^(.+)?\s?(设置|设定|🟰|＝|=|加|➕|＋|\+|减|➖|－|-)\s?([0-9]+|＋|\+|－|-)(人|卡)?$'
    reg = re.findall(pattern, reg)
    if len(reg) == 0:
        return
    if len(reg[0]) != 4:
        return
    reg = reg[0]
    # print(f"setArcPerson: {reg}")
    gid = str(group_id)
    data_file = SaveData("data")
    arcName = reg[0].strip()
    # print(f"arcName: {arcName}")
    if arcName == None or (arcName not in data_file.data["alias"][gid]):  # 未找到时说明可能瞎匹配，直接静默处理
        return
    arc = data_file.data["alias"][gid][arcName]
    op = reg[1].strip()
    num = reg[2].strip()
    # op = op.replace("＋", "+").replace("－", "-").replace("增加", "+").replace("减少", "-").replace("添加", "+").replace("加", "+").replace("减", "-").replace("设定", "=").replace("＝", "=")
    opRepList = {
        "+": ["＋", "加", "➕"],
        "-": ["－", "减", "➖"],
        "=": ["设定", "＝", "🟰"]
    }
    for k, v in opRepList.items():
        if op in v:
            op = k
    if not op:
        return
    num = num.replace("＋", "+").replace("－", "-")
    if (not num.isdigit()) and num != "+" and num != "-":
        return
    if op == "+" and num == "+":
        num = 1
    if op == "-" and num == "-":
        num = 1
    if not str(num).isdigit():
        return
    else:
        num = int(num)
    if op == "+":
        if num < 0 or num > 30:
            return "请勿乱玩 bot！(╯‵□′)╯︵┻━┻"
        data_file.data["arcades"][arc]["personCount"] += num
        tm_string = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%H:%M")
        lastMsg = f"{tm_string} {nickname} 增加 {num} 人"
        data_file.data["arcades"][arc]["lastMsg"] = lastMsg
        data_file.save()
        arcRealName = data_file.data["arcades"][arc]["name"]
        context = f"{arcName} 人数已增加 {num} 人 ❛‿˂̵✧"
        return context

    if op == "-":
        if num < 0 or num > 30:
            # print(":( 请勿乱玩 bot！(╯‵□′)╯︵┻━┻")
            return "请勿乱玩 bot！(╯‵□′)╯︵┻━┻"
        num = min(num, data_file.data["arcades"][arc]["personCount"])
        data_file.data["arcades"][arc]["personCount"] -= num
        tm_string = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%H:%M")
        lastMsg = f"{tm_string} {nickname} 减少 {num} 人"
        data_file.data["arcades"][arc]["lastMsg"] = lastMsg
        data_file.save()
        arcRealName = data_file.data["arcades"][arc]["name"]
        # print(f":) {arcRealName} 人数已减少 {num} 人")
        context = f"{arcName} 人数已减少 {num} 人 ❛‿˂̵✧"
        return context
    if op == "=":
        if abs(data_file.data["arcades"][arc]["personCount"] - int(num)) > 30:
            # print(":( 请勿乱玩 bot！(╯‵□′)╯︵┻━┻")
            return "请勿乱玩 bot！(╯‵□′)╯︵┻━┻"
        data_file.data["arcades"][arc]["personCount"] = int(num)
        tm_string = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%H:%M")
        lastMsg = f"{tm_string} {nickname} 设定了人数为 {num} 人"
        data_file.data["arcades"][arc]["lastMsg"] = lastMsg
        data_file.save()
        arcRealName = data_file.data["arcades"][arc]["name"]
        # print(f":) {arcRealName} 人数已设定为 {num} 人")
        context = f"{arcName} 人数已设定为 {num} 人 ❛‿˂̵✧"
        return context
    return


def get_arc_person(keywords, group_id):
    lookupSuffix = ['有多少人', '有几人', '有几卡', '多少人', '多少卡', '几人', 'jr', '几卡', '几']
    gid = str(group_id)
    data_file = SaveData("data")
    # rawMsg = event.raw_message.strip()
    rawMsg = keywords
    arcName, suffix = None, None
    for s in lookupSuffix:
        if rawMsg.endswith(s):
            arcName = rawMsg[:-len(s)].strip()
            suffix = s
            break
    # print(f"getArcPerson: {arcName} {suffix}")
    if gid not in data_file.data["alias"]:
        return '(˃ ⌑ ˂ഃ )诶呀——本群还没有别名哦'
    if arcName == None or (arcName not in data_file.data["alias"][gid]):
        return
    arc = data_file.data["alias"][gid][arcName]
    arcRealName = data_file.data["arcades"][arc]["name"]
    personCount = data_file.data["arcades"][arc]["personCount"]
    lastMsg = data_file.data["arcades"][arc]["lastMsg"]
    # print(f"{arcRealName} 当前人数为 {personCount} 人\n最近更新：{lastMsg}\n\n可发送 {arcName}+1 {arcName}-1 {arcName}=2 等维护排卡数量\n发送 .maiarc.help 获取帮助链接")
    # context = f"{arcRealName} 当前人数为 {personCount} 人\n最近更新：{lastMsg}\n\n可发送 {arcName}+1 {arcName}-1 {arcName}=2 等维护排卡数量\n发送 .maiarc.help 获取帮助链接"
    context = f'{arcName} 现有 {personCount} 卡，由{lastMsg}\n可发送{arcName}+1/-1/=2 以维护排卡'
    return context


def get_arc_person_multi(group_id):
    gid = str(group_id)
    data_file = SaveData("data")
    result = []
    if gid in data_file.data["alias"]:
        subscribed = data_file.data["alias"][gid]
        arcades = {}
        for alias, arc in subscribed.items():
            if arc not in arcades:
                arcades[arc] = alias
            else:
                arcades[arc] += "、" + alias
        for arc, alias in arcades.items():
            arcRealName = data_file.data["arcades"][arc]["name"]
            personCount = data_file.data["arcades"][arc]["personCount"]
            lastMsg = data_file.data["arcades"][arc]["lastMsg"]
            result.append(f"{arcRealName}({alias}) 当前人数为 {personCount} 人\n最近更新：{lastMsg}")
    if not result:
        # print(":( 本群尚未绑定任何机厅" + "\n\n查看插件使用帮助：" + HelpLink)
        context = "(˃ ⌑ ˂ഃ )本群尚未绑定任何机厅" + "\n可艾特bot+maimai排卡 查看帮助"
        return context
    # await addArc.finish(message=Message("本群目前绑定的机厅：\n" + "\n\n".join(result) + "\n\n查看插件使用帮助：" + HelpLink))
    # print("本群目前绑定的机厅：\n" + "\n\n".join(result) + "\n\n查看插件使用帮助：")
    context = "本群目前绑定的机厅：\n" + "\n".join(result)
    return context


def clear_arc_person():
    data_file = SaveData("data")
    for arc in data_file.data["arcades"]:
        data_file.data["arcades"][arc]["personCount"] = 0
        tm_string = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("'%M:%S")
        lastMsg = f"{tm_string} 凌晨维护，系统自动清空人数"
        data_file.data["arcades"][arc]["lastMsg"] = lastMsg
    data_file.save()


def main(bot, logger):
    with open('config.json', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    config = data
    botName = str(config.get('botName'))
    master = int(config.get('master'))
    mainGroup = int(config.get("mainGroup"))
    init_data()
    global nameget
    nameget = {}
    global namedel
    namedel = {}
    global namesearch
    namesearch = {}

    @bot.on(GroupMessage)
    async def MaiMai_wait(event: GroupMessage):
        if not group_manage_controller(f'{event.group.id}_maimai'):
            pass
            # return

        keywords = str(event.message_chain)
        group_id = int(event.group.id)
        sender_id = int(event.sender.id)
        nickname = str(event.sender.member_name)
        flag = None
        flag_send = None
        permission = None

        # flag数字各个代表的意思如下：
        # flag = 1 , 添加机厅别名
        # flag = 2 , 删除别名
        # flag = 3 , 查询本群绑定机厅
        # flag = 4 , 搜索机厅
        # flag = 5 , 查询当前人数
        # flag = 6 , 设定维护当前人数
        # flag = 7 , 更新数据
        # flag = 8 , 排卡帮助

        if '添加别名' in str(event.message_chain) and At(bot.qq) in event.message_chain:
            logger.info(f'添加机厅别名')
            flag = 1
        elif '删除别名' in str(event.message_chain) and At(bot.qq) in event.message_chain:
            logger.info(f'删除别名')
            flag = 2
        elif '本群' in str(event.message_chain) and '绑定' in str(event.message_chain) and '机厅' in str(
                event.message_chain):
            logger.info(f'查询本群绑定机厅')
            flag = 3
        elif '搜索' in str(event.message_chain) and '机厅' in str(event.message_chain) and At(
                bot.qq) in event.message_chain:
            logger.info(f'搜索机厅')
            flag = 4
        lookupSuffix = ['有多少人', '有几人', '有几卡', '多少人', '多少卡', '几人', 'jr', '几卡', '几']
        for i in range(len(lookupSuffix)):
            if str(lookupSuffix[i]) in str(event.message_chain):
                logger.info(f'查询当前人数')
                flag = 5
        pattern = r'^(.+)?\s?(设置|设定|🟰|＝|=|加|➕|＋|\+|减|➖|－|-)\s?([0-9]+|＋|\+|－|-)(人|卡)?$'
        reg = keywords
        reg = re.findall(pattern, reg)
        if len(reg) != 0:
            if len(reg[0]) == 4:
                logger.info(f'设定维护当前人数')
                flag = 6
        if '更新' in str(event.message_chain) and '华立' in str(event.message_chain) and '数据' in str(
                event.message_chain):
            context = refresh_wahlap()
            logger.info(f'更新数据')
            flag = 7
        if '排卡' in str(event.message_chain) and (
                'mai' in str(event.message_chain) or 'Mai' in str(event.message_chain) or '舞蒙' in str(
                event.message_chain) or '乌蒙' in str(event.message_chain)) and At(bot.qq) in event.message_chain:
            context = f'快捷指令菜单：\n① 艾特bot 添加别名\n② 艾特bot 删除别名\n③ 查询机厅人数：别名+几卡\n④ 更新机厅人数：别名 +/-/= number\n⑤ 本群绑定机厅\n⑥ 艾特bot 搜索机厅'
            flag = 8
            logger.info(f'排卡帮助')

        if flag == 1 or event.sender.id in nameget:
            if event.sender.id not in nameget:
                await bot.send(event, "请发送要添加机厅的别名，注意格式 “ID 别名”")
                nameget[event.sender.id] = []
                flag = None
            elif event.sender.id in nameget:
                nameget.pop(event.sender.id)
                flag = 1
        elif flag == 2 or event.sender.id in namedel:
            if event.sender.id not in namedel:
                await bot.send(event, "请发送要删除的别名")
                namedel[event.sender.id] = []
                flag = None
            elif event.sender.id in namedel:
                namedel.pop(event.sender.id)
                flag = 2
        elif flag == 4 or event.sender.id in namesearch:
            if event.sender.id not in namesearch:
                await bot.send(event, "请发送机厅名称")
                namesearch[event.sender.id] = []
                flag = None
            elif event.sender.id in namesearch:
                namesearch.pop(event.sender.id)
                flag = 4

        if flag == 1 or flag == 2:
            permission_check = await bot.get_group_member(event.group.id, event.sender.id)
            permission_check = permission_check.json()
            permission_check = json.loads(permission_check)
            permission = permission_check['permission']

        if flag == 1:
            context = add_arc(keywords, group_id, permission, master, sender_id)
        elif flag == 2:
            context = del_arc(keywords, group_id, permission, sender_id, master)
        elif flag == 3:
            context = get_arc_person_multi(group_id)
        elif flag == 4:
            context = search_arc(keywords)
        elif flag == 5:
            context = get_arc_person(keywords, group_id)
        elif flag == 6:
            context = set_arc_person(keywords, group_id, nickname, sender_id)

        if not group_manage_controller(f'{event.group.id}_maimai'):
            return

        if flag == None:
            pass
        elif flag == 3 or flag == 4:
            cmList = []
            await bot.send(event, str(context))
            b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                    message_chain=MessageChain(
                                        f'{context}'))
            cmList.append(b1)
            b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                    message_chain=MessageChain(
                                        f'快捷指令菜单：\n① 艾特bot 添加别名\n② 查询机厅人数：别名+几卡\n③ 更新机厅人数：别名 +/-/= number\n④ 艾特bot 删除别名\n⑤ 本群绑定机厅\n⑥ 搜索机厅'))
            cmList.append(b1)
            await bot.send(event, str(context))
            b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                    message_chain=MessageChain(
                                        f'更多详细指令请前往查看'))
            cmList.append(b1)
            await bot.send(event, Forward(node_list=cmList))
            pass
        else:
            await bot.send(event, str(context))



