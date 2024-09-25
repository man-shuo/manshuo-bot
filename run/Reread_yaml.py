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

master=1270858640



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




def main(bot, logger):
    @bot.on(GroupMessage)
    async def Reread_yaml(event: GroupMessage):
        
        initial_data = {'群复读开关': 1, 'var2': 20}
        manager = YamlManager('manshuo_data/Rereadlist.yaml', initial_data)
        #manager = YamlManager('config/Rereadlist.yaml')
        
        
        # 读取群聊变量
        #loaded_variables = load_variables(file_path)
        group_id=str(event.group.id)
        #var_value = read_variable(file_path, 'group_id')
        #group_id_judge=int(read_variable(file_path, str(group_id)))
        group_id_judge=int(manager.get_variable(str(group_id)))
        #group_id_judge=read_variable(file_path, str(group_id))
        
        
        #若列表没有该群，则新增该群变量
        if group_id_judge != 1:
            manager.add_new_variables({str(group_id): 1, 'fudu1_'+str(group_id): 404, 'fudu2_'+str(group_id): 404, 'fudu3_'+str(group_id): 404})
            

        
        if str(event.message_chain) == "初始化":
            # 初始化变量，如果报错大概率初始化一下就就好了
            manager.clear_yaml()
            initial_data = {'群复读开关': 1, 'var2': 20}
            manager = YamlManager('config/Rereadlist.yaml', initial_data)
            
            
            
        #若列表有该群，则获取其变量值
        if group_id_judge == 1:
            fudu1=str(manager.get_variable('fudu1_'+str(group_id)))
            fudu2=str(manager.get_variable('fudu2_'+str(group_id)))
            fudu3=str(manager.get_variable('fudu3_'+str(group_id)))
            
            
            #这样bot获取图片获取到的是[图片]，那就新增一个判断（
            if '[图片]' in str(event.message_chain) or '@' in str(event.message_chain) :
                pass
            else:
                
            #if event.sender.id == master :
                #await bot.send(event, "收到master消息")
                    
                context=str(event.message_chain)
                fudu1=context
                #update_variable("fudu1", str(context))
                #update_variable(file_path, 'fudu1_'+str(group_id), str(context))
                manager.modify_variable('fudu1_'+str(group_id), str(context))
            #await bot.send(event, str(context))
                if fudu1 != fudu3:
                    if fudu1 == fudu2:
                        rnum0=random.randint(1,100)
                        if rnum0 < 45 :
                            await bot.send(event, str(context))
                            #update_variable("fudu3", str(context))
                            #update_variable(file_path, 'fudu3_'+str(group_id), str(context))
                            manager.modify_variable('fudu3_'+str(group_id), str(context))
                #update_variable("fudu2", str(context))
                #update_variable(file_path, 'fudu2_'+str(group_id), str(context))
                manager.modify_variable('fudu2_'+str(group_id), str(context))
        if event.sender.id == master :
            pass
            fudu1=str(manager.get_variable('fudu1_'+str(group_id)))
            fudu2=str(manager.get_variable('fudu2_'+str(group_id)))
            fudu3=str(manager.get_variable('fudu3_'+str(group_id)))
        #if event.sender.id == master :
            #await bot.send(event, str(fudu1)+"\n"+str(fudu2)+"\n"+str(fudu3)+"\n")
            #pass
        
        
        
        
        if str(event.message_chain) == "演示示例":
                # 使用示例
            if __name__ == "__main__":
            # 创建一个管理器，指定YAML文件的路径和初始数据
                initial_data = {'var1': 10, 'var2': 20}
                manager = YamlManager('config/variables.yaml', initial_data)

            # 获取变量值
            print(manager.get_variable('var1'))  # 输出: 10
            print(manager.get_variable('var3'))  # 输出: 0 (因为 var3 不存在)

            # 修改变量
            manager.modify_variable('var1', 150)
            print(manager.get_variable('var1'))  # 输出: 150

            # 添加新变量
            manager.add_new_variables({'var3': 300, 'var4': 400})
            print(manager.get_variable('var3'))  # 输出: 300
            print(manager.get_variable('var4'))  # 输出: 400


    
    
    
    