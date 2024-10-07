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



class YamlManager:
    def __init__(self, file_path, initial_data=None):
        """
        初始化YAML管理器，接受YAML文件的路径和可选的初始数据。
        如果YAML文件不存在，则使用初始数据创建文件。
        """
        self.file_path = file_path
        if initial_data is None:
            initial_data = {}
        # 初始化 YAML 文件
        self.initialize_yaml(initial_data)

    def initialize_yaml(self, initial_data):
        """初始化 YAML 文件，若文件不存在则创建并写入初始数据"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                yaml.dump(initial_data, file)
        else:
            # 如果文件存在，但初始数据没有写入，则合并数据
            data = self.read_yaml()
            data.update(initial_data)
            self.write_yaml(data)

    def read_yaml(self):
        """读取 YAML 文件并返回数据"""
        with open(self.file_path, 'r') as file:
            return yaml.safe_load(file) or {}

    def write_yaml(self, data):
        """将数据写入 YAML 文件"""
        with open(self.file_path, 'w') as file:
            yaml.dump(data, file)

    def get_variable(self, var_name):
        """获取变量值，如果变量不存在则返回 0"""
        data = self.read_yaml()
        return data.get(var_name, 0)

    def set_variable(self, var_name, value):
        """设置变量值，如果文件中没有该变量则新增"""
        data = self.read_yaml()
        data[var_name] = value
        self.write_yaml(data)

    def modify_variable(self, var_name, new_value):
        """修改已存在的变量值，如果变量不存在则新增"""
        self.set_variable(var_name, new_value)

    def add_new_variables(self, variables):
        """批量新增或修改变量"""
        data = self.read_yaml()
        data.update(variables)
        self.write_yaml(data)
    
    def clear_yaml(self):
        """清空 YAML 文件内容"""
        self.write_yaml({})  # 将空字典写入文件，相当于清空文件

#随机读取yaml文件内容
def random_yaml_get(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_list = yaml.safe_load(file)
    return random.choice(text_list)

#攻击无效化的时候保留特定变量，删除其余所有变量
def delete_and_remain(file_path, specific_keys):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    filtered_data = {key: value for key, value in data.items() 
                     if key.startswith("white_list") or key in specific_keys}
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(filtered_data, file, allow_unicode=True)



def save_to_yaml(file_path, element):
    data = []
    # 检查文件是否存在，如果存在则加载已有数据
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or []

    # 添加新元素到数据列表中
    data.append(element)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)


def main(bot, logger):
    @bot.on(GroupMessage)
    async def Reread_yaml(event: GroupMessage):
        
        #获取master信息
        with open('config.json', 'r', encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
        config = data
        botName = str(config.get('botName'))
        master = int(config.get('master'))
        mainGroup = int(config.get("mainGroup"))
        
        
        
        #初始化文件
        initial_data = {'attack_group_switch': 1, 'limit_of_times': 2, "white_list_"+str(master): 1}
        manager = YamlManager('manshuo_data/attack_sb_list.yaml', initial_data)
        
        
        # 读取群聊变量
        group_id=str(event.group.id)
        group_id_judge=int(manager.get_variable(str(group_id)))
        
        #attack_name_id=int(event.sender.id)
        #若列表没有该群，则新增该群变量
        #attack_name_id是被攻击者，attack_state是攻击状态，attack_member是发起者id
        if group_id_judge != 1:
            manager.add_new_variables({str(group_id): 1, 'attack_name_id_'+str(group_id): 404, 'attack_name_id2_'+str(group_id): 404, 'attack_state_'+str(group_id): 0, 'attack_member_'+str(group_id): 404, 'times_'+str(group_id): 0})
            group_id_judge=int(manager.get_variable(str(group_id)))
            

        
        if str(event.message_chain) == "初始化" and int(event.sender.id) == master :
            # 初始化变量，如果报错大概率初始化一下就就好了
            file_path = 'manshuo_data/attack_sb_list.yaml'
            specific_keys = ['attack_group_switch', 'limit_of_times']  # 保留特定元素的键
            delete_and_remain(file_path, specific_keys)
            await bot.send(event, "初始化完成~")
            
            
        #若在bot群内发送攻击无效化则解除被攻击者的攻击状态
        if event.group.id == mainGroup and str(event.message_chain) == "攻击无效化":
            #await bot.send(event, '已经解除你的攻击状态啦')
            file_path = 'manshuo_data/attack_sb_list.yaml'
            specific_keys = ['attack_group_switch', 'limit_of_times']  # 保留特定元素的键
            delete_and_remain(file_path, specific_keys)
            await bot.send(event, '已经解除你的攻击状态啦')
            
            
        if str(event.message_chain).startswith("添加攻击文本") :
            #message=event.message_chain
            #msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
            #m = re.match(r'^添加攻击文本\s*(\w+)\s*$', msg.strip())
            msg = event.message_chain[Plain][0].text.strip()
            new_text = msg[len("添加攻击文本："):].strip()
            #new_text = m  # 获取 "添加:" 后面的内容
            if new_text:
                file_path = 'manshuo_data/attack_elements.yaml'
                save_to_yaml(file_path, new_text)
                await bot.send(event, f"已添加攻击文本: {new_text}")
            else:
                await bot.send(event, "无法添加空文本")
            
            
        # 被攻击者白名单，以防有人滥用
        #if str(event.message_chain).startswith("攻击白名单") :
        if '攻击白名单' in str(event.message_chain) and int(event.sender.id) == master:
            # 初始化变量，如果报错大概率初始化一下就就好了
            context=str(event.message_chain)
            name_id_number=re.search(r'\d+', context)
            if name_id_number:
                name_id_number = int(name_id_number.group())
                if '添加' in str(event.message_chain) in event.message_chain:
                    manager.add_new_variables({"white_list_"+str(name_id_number): 1})
                    await bot.send(event, "成功添加攻击白名单")
                if '删除' in str(event.message_chain) in event.message_chain:
                    manager.add_new_variables({"white_list_"+str(name_id_number): 0})
                    await bot.send(event, "成功删除")
        elif '攻击白名单' in str(event.message_chain) and int(event.sender.id) != master:
            await bot.send(event, "非master不可以操作哟")
            
        #若列表有该群，则获取其变量值
        if group_id_judge == 1:
            attack_name_id=int(manager.get_variable('attack_name_id_'+str(group_id)))
            attack_name_id2=int(manager.get_variable('attack_name_id2_'+str(group_id)))
            attack_name_id2=attack_name_id
            attack_state=int(manager.get_variable('attack_state_'+str(group_id)))
            attack_member=int(manager.get_variable('attack_member_'+str(group_id)))
            times=int(manager.get_variable('times_'+str(group_id)))
            limit_of_times=int(manager.get_variable('limit_of_times'))
            



        #指定人攻击模块
        if str(event.message_chain).startswith("开始攻击") :
            #获取被攻击者的id
            context=str(event.message_chain)
            attack_name_id=re.search(r'\d+', context)
            attack_member=int(event.sender.id)
            manager.modify_variable('attack_member_'+str(group_id), int(attack_member))
            
            
            if attack_name_id:
                attack_name_id = int(attack_name_id.group())
                manager.modify_variable('attack_name_id_'+str(group_id), str(attack_name_id))
                attack_name_id=int(manager.get_variable('attack_name_id_'+str(group_id)))
                white_list_state=int(manager.get_variable("white_list_"+str(attack_name_id)))
                attack_name_id2=int(manager.get_variable('attack_name_id2_'+str(group_id)))
                if attack_name_id == master :
                    manager.modify_variable('attack_name_id_'+str(group_id), str(attack_name_id2))
                    manager.modify_variable('attack_state_'+str(group_id), "0")
                    await bot.send(event, 'bot不可以攻击主人喵~')
                elif white_list_state == 1 :
                    manager.modify_variable('attack_name_id_'+str(group_id), str(attack_name_id2))
                    manager.modify_variable('attack_state_'+str(group_id), "0")
                    await bot.send(event, str(botName)+'不会攻击好孩子的喵~')
                else:
                        
                        if attack_name_id == master :
                            await bot.send(event, 'bot不可以攻击主人喵~')
                            
                        else:
                            if attack_name_id2 == attack_name_id and attack_state==1:
                                await bot.send(event, str(botName)+'从刚才就一直监听到现在了喵！')
                            if attack_name_id2 != attack_name_id and attack_state==1:
                                manager.modify_variable('times_'+str(group_id), "0")
                                manager.modify_variable('attack_name_id2_'+str(group_id), int(attack_name_id))
                                await bot.send(event, str(botName)+'收到！正在转移目标！')
                            if attack_state==0:
                                name_nickname = str(event.sender.member_name)
                                await bot.send(event, "@"+str(name_nickname)+" "+"收到！！即刻开始攻击！！！")
                                manager.modify_variable('times_'+str(group_id), "0")
                                manager.modify_variable('attack_state_'+str(group_id), "1")
                                manager.modify_variable('attack_name_id2_'+str(group_id), int(attack_name_id))
        if str(event.message_chain).startswith("停止攻击"):
            if event.sender.id == attack_name_id :
                await bot.send(event, "被攻击的孩子不可以自己取消哦，请到bot群："+str(mainGroup)+" 内发送“攻击无效化”哦")
            else:
                manager.modify_variable('attack_state_'+str(group_id), "0")
                name_nickname = str(event.sender.member_name)
                await bot.send(event, "@"+str(name_nickname)+" "+'好的主人，这就先放他一马')
        if str(event.message_chain) == "查询攻击状态":
            if attack_state ==0:
                await bot.send(event, str(botName)+'正在休息喵')
            if attack_state ==1:
                name_nickname = str(event.sender.member_name)
                #await bot.send(event, [At(attack_name_id), " "+'发言并攻击'])
                await bot.send(event, [str(botName)+'正在等待目标',At(attack_name_id), " "+'发言并攻击'])
                #await bot.send(event, str(botName)+'正在等待目标'+str(name_nickname)+'发言并攻击')







        #判断并发送攻击文本
        if event.sender.id == attack_name_id and attack_state == 1 :
            attack_state=int(manager.get_variable('attack_state_'+str(group_id)))
            attack_name_id=int(event.sender.id)
            white_list_state=int(manager.get_variable("white_list_"+str(attack_name_id)))
            rnum1=random.randint(1,100)
            if str(event.message_chain).startswith("停止攻击") :
                #await bot.send(event, "被攻击的孩子不可以自己取消哦，请到bot群："+str(mainGroup)+" 内发送“攻击无效化”哦")
                pass
            else:
                if '漫朔' in str(event.message_chain) or 'manshuo' in str(event.message_chain) or'漫溯' in str(event.message_chain) or'漫说' in str(event.message_chain) or'慢说' in str(event.message_chain):
                    await bot.send(event, "不可以欺负漫朔哥哥哦~~")
                                    
                elif white_list_state == 1 :
                    manager.modify_variable('attack_state_'+str(group_id), "0")
                    await bot.send(event, str(botName)+'不会攻击好孩子的喵~')
                    
                else:
                    if rnum1 < 51:
                        if times > limit_of_times:
                            times=times+1
                            #update_variable("times", str(times))
                            manager.modify_variable('times_'+str(group_id), int(times))
                            limits=limit_of_times+3
                            if times < limits:
                                await bot.send(event, "攻击次数太多啦，"+str(botName)+"要做个好孩子喵~")
                                manager.modify_variable('attack_state_'+str(group_id), "0")
                        else:
                            file_path = 'manshuo_data/attack_elements.yaml'
                            attack_context = random_yaml_get(file_path)
                            await bot.send_group_message(event.sender.group.id, [At(attack_name_id), " "+str(attack_context)])
                            times=times+1
                            #update_variable("times", str(times))
                            manager.modify_variable('times_'+str(group_id), int(times))
                            
            
            
        
        
        
        
        if str(event.message_chain).startswith("攻击") :
            logger.info('攻击触发！，bot开始攻击啦')
            check = random.randint(1, 100)
            logger.info(str(check))
            if check>75:
                type = random.randint(1, 6)
                name_nickname = str(event.sender.member_name)
                if type == 1:
                    #name_nickname = str(event.sender.member_name)
                    logger.info('攻击切换自定义回复，type1')
                    await bot.send(event, '攻击什么攻击'+str(name_nickname) + '个笨蛋（哼！')
                elif type == 2:
                    logger.info('攻击切换自定义回复，type2')
                    s = [Image(path='manshuo_data/fonts/shengqibaozha.gif')]
                    await bot.send(event, s)
                elif type == 3:
                    logger.info('攻击切换自定义回复，type3')
                    await bot.send(event, '天天就知道攻击人家，' + str(name_nickname) + '太坏了！')
                elif type == 4:
                    logger.info('攻击切换自定义回复，type4')
                    await bot.send(event, str(botName) + '不干啦，撒泼打滚又上吊~~~~（嘎了')
                elif type == 5:
                    logger.info('攻击切换自定义回复，type5')
                    await bot.send(event, str(name_nickname) +'又要指挥'+str(botName) + '干坏事情了，'+str(botName)+'才不要呢.')
                elif type == 6:
                    logger.info('攻击切换自定义回复，type6')
                    s = [Image(path='manshuo_data/fonts/zayuzayu.gif')]
                    await bot.send(event, s)
            else:


                msg = "".join(map(str, event.message_chain[Plain]))
            # 匹配指令
                #m = re.match(r'^攻击\s*(\w+)\s*$', msg.strip())
                m=0
            #m = re.match(r'^攻击@\s*(\w+)\s*$', msg.strip())
                if m:
                # 取出指令中的地名
                    #await bot.send(event, '成功匹配')
                    name_user = m.group(1)
                    if str(name_user) != "无效化":
                        file_path = 'manshuo_data/attack_elements.yaml'
                        attack_context = random_yaml_get(file_path)

                        name_id = int(str(event.sender.id))
                        name_nickname = str(event.sender.member_name)
                        await bot.send(event,  "@"+str(name_user)+" "+str(attack_context))




                context=str(event.message_chain)
                name_id_number=re.search(r'\d+', context)

                if name_id_number:
                    number = int(name_id_number.group())
                    white_list_state=int(manager.get_variable("white_list_"+str(number)))

                    if number == master :
                        file_path = 'manshuo_data/attack_elements.yaml'
                        attack_context = random_yaml_get(file_path)
                        await bot.send_group_message(event.sender.group.id, [At(number), " " + str(attack_context)])
                        #await bot.send(event, "不可以攻击master哦~~")

                    elif white_list_state == 1 :
                        manager.modify_variable('attack_state_'+str(group_id), "0")
                        await bot.send(event, str(botName)+'不会攻击好孩子的喵~')
                    else:
                        file_path = 'manshuo_data/attack_elements.yaml'
                        attack_context = random_yaml_get(file_path)
                        await bot.send_group_message(event.sender.group.id, [At(number), " "+str(attack_context)])
                    #await bot.send(event, '测试开始，开始输出结果：')
                    #name_id = int(str(event.sender.id))
                    #await bot.send(event, "测试者QQID："+str(number))
                    #group_id = event.sender.group.id
                    #await bot.send(event, "测试者所在群："+str(group_id))
                    #await bot.send(event, "发送内容："+str(message_chain))
                    #await bot.send_group_message(event.sender.group.id, [At(number),"\n提问前请翻阅：。"])
                    #await bot.send_group_message(event.sender.group.id, [At(number), " "+str(attack_context)])
                    #await bot.send(event, "@"+str(name_user)+" "+str(random_paragraph))
                    #name_id = int(str(event.sender.id))
                    #await bot.send(event, "测试者QQID："+str(name_id))
                    #name_nickname = str(event.sender.member_name)
                    #await bot.send(event, "测试者QQ昵称："+str(name_nickname))











    
    
    
    