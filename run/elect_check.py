import time
import requests
import json
import urllib.parse
import re
# import schedule
import yaml
import os

import shutil
#import paramiko

from asyncio import sleep

import random
import httpx
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from mirai.models import MusicShare
from itertools import repeat
from plugins import weatherQuery
import datetime
from asyncio import sleep
from io import BytesIO
from PIL import Image as Image1
from mirai import GroupMessage, At, Plain
from mirai.models import ForwardMessageNode, Forward
from plugins.toolkits import random_str, picDwn
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown, MessageChain, \
    Voice

state = {}


# 初始化 YAML 文件（如果不存在则创建）
def initialize_yaml(file_path):
    if not os.path.exists(file_path):
        data = {'users': {}}
        write_yaml(file_path, data)


# 创建文件夹和初始化 YAML 文件（如果不存在则创建）
def initialize_yaml(directory, file_name):
    # 如果目录不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)

    # 如果文件不存在则创建
    if not os.path.exists(file_path):
        data = {'users': {}}
        write_yaml(file_path, data)

    return file_path


# 读取 YAML 文件
def read_yaml(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    else:

        return None


# 写入 YAML 文件
def write_yaml(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)


# 获取用户的所有数据
def get_user_data(file_path, user_id):
    data = read_yaml(file_path)
    if data and user_id in data['users']:
        return data['users'][user_id]
    else:

        return None


# 获取用户的某个字段数据
def get_user_field(file_path, user_id, field):
    user_data = get_user_data(file_path, user_id)
    if user_data and field in user_data:
        return user_data[field]
    else:

        return None


# 更新或添加用户的单个字段数据
def update_user_field(file_path, user_id, field, value):
    data = read_yaml(file_path)
    if data is None:
        data = {'users': {}}

    if user_id not in data['users']:
        data['users'][user_id] = {}  # 创建新用户

    data['users'][user_id][field] = value
    write_yaml(file_path, data)
    # print(f"用户 {user_id} 的 {field} 已更新为 {value}")


# 示例：读取和修改用户数据
def manage_user_data(base_directory, user_id, room=None, location=None, account=None):
    file_name = 'user_data.yaml'  # 定义每个用户的YAML文件名
    user_directory = os.path.join(base_directory, user_id)  # 每个用户的文件夹

    # 初始化文件（如果不存在则创建）
    file_path = initialize_yaml(user_directory, file_name)

    # 如果提供了房间号、位置或账号信息，则更新对应字段
    if room is not None:
        update_user_field(file_path, user_id, 'room', room)
    if location is not None:
        update_user_field(file_path, user_id, 'location', location)
    if account is not None:
        update_user_field(file_path, user_id, 'account', account)

    global test
    test = "Manyana"

    # 读取并返回用户的全部数据
    return get_user_data(file_path, user_id)


def json_check(directory, filename):
    file_path = os.path.join(directory, filename)
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 初始化的 JSON 数据
    init_data = {
        "account": "814272",
        "building": {
            "buildingid": "1503975832",
            "building": "凤凰居 S1"
        },
        "room": "B413",
        "sender": "example@foxmail.com",
        "password": "aaaaaaaaaaaaaaaa",
        "receiver": "example@163.com"
    }

    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 创建并初始化文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(init_data, f, ensure_ascii=False, indent=4)


def json_rewrite(directory, filename, name_id):
    file_path = os.path.join(directory, filename)
    # 从文件中读取 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    base_directory = directory
    # 修改对应键值对

    account = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'account')
    building = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'building')
    buildingid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                'buildingid')
    room = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'room')

    data['account'] = account  # 修改 account
    data['building']['buildingid'] = buildingid  # 修改 buildingid
    data['building']['building'] = building  # 修改 building 名称
    data['room'] = room  # 修改房间号

    # 打印修改后的 JSON 数据
    # print(json.dumps(data, indent=4, ensure_ascii=False))

    # 保存修改后的 JSON 数据到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def inquiry(directory, filename):
    file_path = os.path.join(directory, filename)
    # 读取查询信息
    with open(file_path, "rb") as memory_file:
        js = json.loads(memory_file.read())  # 读取并解析JSON文件
        account = js["account"]  # 获取校园卡账号
        building = js["building"]  # 获取建筑信息
        room = js["room"]  # 获取房间号

    print(f"查询 {building} {room}")

    session = requests.session()  # 创建一个会话对象
    # 设置请求头，Content-Type是必要的
    header = {
        "User-Agent": """Mozilla/5.0 (Linux; Android 10; SM-G9600 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36""",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    data = ""
    json_data = '''
    {
	    "query_elec_roominfo": {
		    "aid": "0030000000002505",
	    	"account": "000000",
	    	"room": {
		    	"roomid": "B999",
			    "room": "B999"
		    },
		    "floor": {
			    "floorid": "",
			    "floor": ""
    		},
    		"area": {
	    		"area": "青岛校区",
		    	"areaname": "青岛校区"
	    	},
		    "building": {
			    "buildingid": "1503975890",
			    "building": "S2从文书院"
		    }
    	}
    }
    '''
    js = json.loads(json_data)  # 将JSON字符串转换为Python对象

    # 更新请求数据
    js["query_elec_roominfo"]["account"] = account
    js["query_elec_roominfo"]["room"]["roomid"] = room
    js["query_elec_roominfo"]["room"]["room"] = room
    js["query_elec_roominfo"]["building"] = building

    js = json.dumps(js, ensure_ascii=False)  # 将Python对象转换为JSON字符串
    # print(js)

    js = urllib.parse.quote(js)  # 对JSON字符串进行URL编码
    data += js

    # 构建请求数据
    data = "jsondata=" + data + "&funname=synjones.onecard.query.elec.roominfo&json=true"
    # print(data)
    # 发送POST请求
    res = session.post(url="http://10.100.1.24:8988/web/Common/Tsm.html", headers=header, data=data)
    # print("res!!!!!!!!!!!!!!!")
    # print(res.text)
    js = json.loads(res.text)  # 解析响应内容
    time_now = time.localtime()

    # 使用正则表达式提取数字部分
    match = re.search(r"\d+\.\d+", js['query_elec_roominfo']['errmsg'])
    if match:
        # 将提取到的数字部分转换为浮点数
        global remaining_power
        remaining_power = float(match.group())




    else:
        return None


def schedule_tasks():
    # Schedule the task to run at every hour and half-hour
    schedule.every().hour.at(":00").do(inquiry)
    schedule.every().hour.at(":30").do(inquiry)

    while True:
        schedule.run_pending()
        time.sleep(1)




def move_file_to_directory(source_file, destination_directory):
    # 确保目标目录存在，如果不存在则创建
    os.makedirs(destination_directory, exist_ok=True)

    # 获取源文件的文件名
    file_name = os.path.basename(source_file)

    # 构建目标文件的完整路径
    destination_file = os.path.join(destination_directory, file_name)

    # 移动文件
    shutil.move(source_file, destination_file)

    print(f"文件已成功移动到: {destination_file}")





def send_file_via_sftp(local_file, remote_file, remote_folder, hostname, username, password, port=22):
    # 创建一个SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加远程主机的密钥
    ssh.connect(hostname, port=port, username=username, password=password)

    # 创建SFTP客户端
    sftp = ssh.open_sftp()

    # 确保远程目录存在
    try:
        sftp.chdir(remote_folder)
    except IOError:
        sftp.mkdir(remote_folder)
        sftp.chdir(remote_folder)

    # 上传文件
    sftp.put(local_file, f"{remote_folder}/{remote_file}")
    
    # 关闭SFTP和SSH连接
    sftp.close()
    ssh.close()





def main(bot, logger):
    @bot.on(GroupMessage)
    async def elect_check(event: GroupMessage):
        
        
        

            
            
            
            
            
            
            
        
        
        
        # 获取master信息
        with open('config.json', 'r', encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
        config = data
        botName = str(config.get('botName'))
        master = int(config.get('master'))
        mainGroup = int(config.get("mainGroup"))
        # 定义文件
        directory = 'manshuo_data'  # 文件夹路径
        data_json = 'data.json'  # 文件名
        # 示例：读取和修改用户数据
        base_directory = directory
        # 初始化文件
        user_data = manage_user_data(base_directory, 'elect_check', room='b666', location="abc", account="alice123")
        stateid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid')
        if stateid == None:
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'room', 'b413')
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'building',
                              '凤凰居 S1')
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'account',
                              '814272')
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'buildingid',
                              '1503975832')
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid',
                              '0')
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'sender_id',
                              '0')
        stateid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid')
        stateid = int(stateid)
        
        
        
        if ('查询' in str(event.message_chain) and '电费' in str(event.message_chain)) and event.group.id == 674822468 and int(event.sender.id) == master:
            #await bot.send(event, "master青岛电费查询（暂定）")
            pass

        if ('查询' in str(event.message_chain) and '电费' in str(event.message_chain)) and event.group.id == 674822469:
            logger.info("电费查询")
            name_id = int(str(event.sender.id))

            room = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'room')
            if room == None:
                #await bot.send(event, '您还未注册，请在bot群内发送"电费注册"以开始')
                pass
            else:

                #await bot.send(event, "当前功能限时上线," + str(botName) + "正在为您查询喵~")

                json_check(directory, data_json)
                json_rewrite(directory, data_json, name_id)
                inquiry(directory, data_json)
                #await bot.send(event, '您宿舍剩余的电量为' + str(remaining_power))

        if (('注册' in str(event.message_chain) and '电费' in str(event.message_chain)) or stateid == 1) and event.group.id == 674822469:

            state_id = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                      'sender_id')
            # await bot.send(event, '进入判断，state_id：'+str(state_id)+" stateid："+str(stateid))

            sb = 1

            # await bot.send_friend_message(master, '进入判断，state_id：'+str(state_id)+" stateid："+str(stateid))
            if stateid != 1:
                await bot.send(event, '本次注册需要您提交校园卡号以及宿舍号，若不同意请发送“终止注册”')
                user_id = str(event.sender.id)
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'sender_id',
                                  str(user_id))
                state_id = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'sender_id')
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid',
                                  '1')
                # await bot.send_friend_message(master, '开始注册，state_id：'+str(state_id)+" stateid："+str(stateid))
                # await bot.send(event, str(state_id))
            if '终止注册' in str(event.message_chain) or '停止注册' in str(event.message_chain):
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid',
                                  '0')
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'sender_id',
                                  "0")

                user_id = str(event.sender.id)
                # state[user_id] = "注册终止"
                state.clear()
                sb = 0
                await bot.send(event, '注册终止')
                state.clear()

            user_id = str(event.sender.id)

            # 判断用户是否在进程中
            if user_id in state:
                current_state = state[user_id]
                if current_state == "注册终止" and (
                        '注册' in str(event.message_chain) and '电费' in str(event.message_chain)):
                    # state[user_id] = "重新注册"
                    state.clear()

                if current_state == "等待卡号" and state_id == str(event.sender.id):
                    await sleep(0.1)
                    account = str(event.message_chain)
                    state[user_id] = "等待房间号"
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(user_id),
                                      'account', str(account))
                    await bot.send(event, f'卡号已收到，请发送房间号')


                elif current_state == "等待房间号" and state_id == str(event.sender.id):
                    room = str(event.message_chain)
                    state[user_id] = "等待建筑位置"
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(user_id),
                                      'room', str(room))
                    await bot.send(event, f'房间号已收到，请发送建筑位置')

                elif current_state == "等待建筑位置" and state_id == str(event.sender.id):
                    building = str(event.message_chain)
                    state[user_id] = "注册终止"
                    state.clear()
                    if 'S11' in str(event.message_chain) or 's11' in str(event.message_chain):
                        buildingid = 1599193777
                    elif 'S2' in str(event.message_chain) or 's2' in str(event.message_chain):
                        buildingid = 1503975890
                    elif 'S5' in str(event.message_chain) or 's5' in str(event.message_chain):
                        buildingid = 1503975967
                    elif 'S6' in str(event.message_chain) or 's6' in str(event.message_chain):
                        buildingid = 1503975980
                    elif 'S7' in str(event.message_chain) or 's7' in str(event.message_chain):
                        buildingid = 1503975988
                    elif 'S8' in str(event.message_chain) or 's8' in str(event.message_chain):
                        buildingid = 1503975995
                    elif 'S9' in str(event.message_chain) or 's9' in str(event.message_chain):
                        buildingid = 1503976004
                    elif 'S10' in str(event.message_chain) or 's10' in str(event.message_chain):
                        buildingid = 1503976037
                    elif 'S1' in str(event.message_chain) or 's1' in str(event.message_chain):
                        buildingid = 1503975832
                    elif 'T1' in str(event.message_chain) or 't1' in str(event.message_chain):
                        buildingid = 1574231830
                    elif 'T3' in str(event.message_chain) or 't2' in str(event.message_chain):
                        buildingid = 1574231835
                    else:
                        await bot.send(event, f'未能成功获取，请重试或联系master')
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                      'stateid', '0')
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                      'sender_id', "0")
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(user_id),
                                      'building', str(building))
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(user_id),
                                      'buildingid', str(buildingid))

                    await bot.send(event, f'位置已收到，该建筑代码为：{buildingid}，注册成功，谢谢！')

                    # await bot.send_friend_message(master, '完成注册，state_id：'+str(state_id)+" stateid："+str(stateid))



                elif current_state == "重新注册" and state_id == str(event.sender.id):
                    state[user_id] = "等待卡号"
                    if state_id == str(event.sender.id):
                        await bot.send(event, '请发送您的卡号')
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'stateid', '1')
            else:
                # 如果用户不在进程中，开始新的进程
                state[user_id] = "等待卡号"
                if state_id == str(event.sender.id):
                    if sb == 0:
                        state.clear()
                    else:
                        await bot.send(event, '请发送您的卡号')
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'stateid', '1')
                # update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'sender_id',str(user_id))
    @bot.on(FriendMessage)
    async def friend_message_listener(event: FriendMessage):
        # 获取发送者和消息内容
        sender = event.sender
        if '查询' in str(event.message_chain) and '电费' in str(event.message_chain):
            await bot.send(event, '本bot暂不支持查询青岛宿舍电费哦，请前往bot群添加bot二号机查询电费')
        if '注册' in str(event.message_chain) and '电费' in str(event.message_chain):
            await bot.send(event, '本bot暂不支持查询青岛宿舍电费哦，请前往bot群添加bot二号机查询电费')