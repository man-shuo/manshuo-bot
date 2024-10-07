import time
import requests
import json
import urllib.parse
import re
#import schedule
import yaml
import os

import asyncio
import datetime
from mirai import Startup, Shutdown
from asyncio import sleep

import random
import httpx
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from mirai.models import MusicShare
from itertools import repeat
from plugins import weatherQuery
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


# 遍历所有用户目录并获取账号列表
def get_all_user_accounts(base_directory):
    accounts = []
    if os.path.exists(base_directory):
        # 遍历目录中的每个文件夹
        for user_folder in os.listdir(base_directory):
            user_directory = os.path.join(base_directory, user_folder)
            if os.path.isdir(user_directory):
                user_file = os.path.join(user_directory, 'user_data.yaml')
                user_data = read_yaml(user_file)
                #print("user_data:", user_data)
                if user_data and 'users' in user_data:
                    #print("user_data:", user_data)
                    # 提取每个用户的账号信息
                    for user_id, user_info in user_data['users'].items():
                        if 'account_number' in user_info:
                            accounts.append(user_info['account_number'])
    return accounts



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

    #print(f"查询 {building} {room}")

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

def elect_check_schedule():
    print("定时任务，开始执行")

def get_all_user_accounts_test(base_directory):
    accounts = []
    if os.path.exists(base_directory):
        # 遍历目录中的每个文件夹
        if base_directory:
            user_directory = base_directory
            if os.path.isdir(user_directory):
                user_file = os.path.join(user_directory, 'user_data.yaml')
                user_data = read_yaml(user_file)
                #print("user_data:", user_data)
                if user_data and 'users' in user_data:
                    #print("user_data:", user_data)
                    # 提取每个用户的账号信息
                    for user_id, user_info in user_data['users'].items():
                        if 'account_number' in user_info:
                            accounts.append(user_info['account_number'])
    return accounts

_task = None

def main(bot, logger):
    @bot.on(GroupMessage)
    async def elect_check(event: GroupMessage):
        # 获取master信息

        if '遍历' in str(event.message_chain):
            base_directory_test='manshuo_data/elect_check'
            all_accounts = get_all_user_accounts_test(base_directory_test)
            print("所有用户的账号:", all_accounts)


            #for account_number in all_accounts:



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

        stateid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid')
        if stateid == None:
            manage_user_data(base_directory, 'elect_check', room='b666', location="abc", account="alice123")
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
            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'elect_check_state',
                              '0')
        stateid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'stateid')
        elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'elect_check_state')
        stateid = int(stateid)




                            #await bot.send_friend_message(name_id,'您的电费过低：' + str(remaining_power) + " \n请及时为宿舍补充电费")

        if '提醒' in str(event.message_chain) and ('开启' in str(event.message_chain) or '打开' in str(event.message_chain))and '电费' in str(event.message_chain):
            name_id = int(str(event.sender.id))
            stateid_check_number=get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'stateid_check')

            if stateid_check_number:
                stateid_check_number = int(stateid_check_number)
                if stateid_check_number==1:
                    await bot.send(event, '您已订阅过此服务')
                elif stateid_check_number==0:
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'stateid_check', '1')
                    await bot.send(event, '已订阅，电费过低时候将通知您')
            else:
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'stateid_check', '1')
                await bot.send(event, '已订阅，电费过低时候将通知您')


        if '提醒' in str(event.message_chain) and ('关闭' in str(event.message_chain) or '取消' in str(event.message_chain) or '停止' in str(event.message_chain))and '电费' in str(event.message_chain):
            name_id = int(str(event.sender.id))
            stateid_check_number=get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'stateid_check')

            if stateid_check_number:
                stateid_check_number = int(stateid_check_number)
                if stateid_check_number==1:
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'stateid_check', '0')
                    await bot.send(event, '已为您取消该服务')
                else:
                    await bot.send(event, '该服务一直是停止状态')


        if '查询' in str(event.message_chain) and '电费' in str(event.message_chain):
            elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','elect_check_state')
            if ('开启' in str(event.message_chain)or '打开' in str(event.message_chain)) and int(event.sender.id)==master:
                logger.info("已开启电费查询功能")
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                  'elect_check_state', '1')
                await bot.send(event, '已开启电费查询功能，请确保bot部署在山青内网')
            if ('关闭' in str(event.message_chain) or '取消' in str(event.message_chain)) and int(event.sender.id)==master:
                logger.info("已关闭电费查询功能")
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                  'elect_check_state', '0')
                elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),
                                                   'manshuo', 'elect_check_state')
                await bot.send(event, '已关闭电费查询功能')


            if elect_check_state==None:
                elect_check_state=0
            if int(elect_check_state)==1:
                logger.info("电费查询")
                name_id = int(str(event.sender.id))
                context = str(event.message_chain)
                name_id_number = re.search(r'\d+', context)
                if name_id_number:
                    name_id_number = int(name_id_number.group())
                    name_id = name_id_number

                room = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'room')

                if room == None:
                    await bot.send(event, '您还未注册，请在群内或私聊发送"电费注册"以开始')
                else:
                    check = random.randint(1, 100)
                    logger.info("开始电费查询，check="+str(check))
                    if check > 81:
                        name_nickname = str(event.sender.member_name)
                        times = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),str(name_id),'times')
                        if times == None:
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),
                                              str(name_id), 'times', '1')
                        elif times:
                            times = int(times)
                            times += 1
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),
                                              str(name_id), 'times', str(times))

                        type = random.randint(1, 7)
                        name_nickname = str(event.sender.member_name)
                        if type == 1:
                            # name_nickname = str(event.sender.member_name)
                            logger.info('电费查询切换自定义回复，type1')
                            await bot.send(event, '查询什么查询' + str(name_nickname) + '个笨蛋（哼！')
                        elif type == 2:
                            logger.info('电费查询切换自定义回复，type2')
                            s = [Image(path='manshuo_data/fonts/shengqibaozha.gif')]
                            await bot.send(event, s)
                        elif type == 3:
                            logger.info('电费查询切换自定义回复，type3')
                            await bot.send(event, '天天就知道使唤人家，' + str(name_nickname) + '太坏了！')
                        elif type == 4:
                            logger.info('电费查询切换自定义回复，type4')
                            await bot.send(event, str(botName) + '不干啦，撒泼打滚又上吊~~~~（嘎了')
                        elif type == 5:
                            logger.info('电费查询切换自定义回复，type5')
                            await bot.send(event, str(name_nickname) + '又要指挥' + str(botName) + '干活了，' + str(
                                botName) + '才不要呢.')
                        elif type == 6:
                            logger.info('攻击切换自定义回复，type6')
                            s = [Image(path='manshuo_data/fonts/zayuzayu.gif')]
                            await bot.send(event, s)
                        else:
                            await bot.send(event, str(name_nickname) + '是要让'+str(botName)+'查什么呢，刚才好像忘记了，再试一次吧（嘻嘻')
                    else:
                        times = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                              'times')
                        if times == None:
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'times','1')
                        elif times:
                            times = int(times)
                            times+=1
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'times',str(times))
                        account_number = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                              'account_number')

                        if account_number == None:
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'account_number',str(name_id))

                        stateid_check = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),str(name_id),'stateid_check')
                        if stateid_check == None:
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                              'stateid_check', '0')

                        json_check(directory, data_json)
                        json_rewrite(directory, data_json, name_id)
                        inquiry(directory, data_json)
                        if name_id_number:

                            await bot.send_group_message(event.sender.group.id, [At(name_id), ' 所在的宿舍剩余的电量为' + str(remaining_power)])
                        else:
                            await bot.send(event, '该项目为测试功能，您宿舍剩余的电量为' + str(remaining_power))
            else:
                if ('开启' in str(event.message_chain) or '打开' in str(event.message_chain)) or ('关闭' in str(event.message_chain) or '取消' in str(event.message_chain)):
                    pass
                else:

                    await bot.send(event, '本bot暂未开启电费查询功能')




        if ('注册' in str(event.message_chain) and '电费' in str(event.message_chain)) or stateid == 1:
            elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','elect_check_state')
            if elect_check_state==None:
                elect_check_state=0
            if int(elect_check_state) == 1:
                state_id = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'sender_id')
                # await bot.send(event, '进入判断，state_id：'+str(state_id)+" stateid："+str(stateid))

                sb = 1

                # await bot.send_friend_message(master, '进入判断，state_id：'+str(state_id)+" stateid："+str(stateid))
                if stateid != 1:

                    user_id = str(event.sender.id)
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo', 'sender_id',
                                      str(user_id))
                    context = str(event.message_chain)
                    name_id_number = re.search(r'\d+', context)
                    if name_id_number:
                        name_id_number = int(name_id_number.group())
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','member_id',str(name_id_number))
                        #print(f"name_id长度: {name_id}")
                        await bot.send(event, '您正在为他人注册~')
                    else:
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'member_id', str(user_id))
                        await bot.send(event, '本次注册需要您提供校园卡卡号以及宿舍号，若不同意请发送“终止注册”')

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
                    sb = 0
                    state.clear()

                    await bot.send(event, '注册终止')
                    state.clear()

                user_id = str(event.sender.id)
                member_id=get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                              'member_id')

                # 判断用户是否在进程中
                if user_id in state:
                    current_state = state[user_id]
                    if current_state == "注册终止" and (
                            '注册' in str(event.message_chain) and '电费' in str(event.message_chain)):
                        # state[user_id] = "重新注册"
                        state.clear()

                    if current_state == "等待卡号" and state_id == str(event.sender.id):
                        await sleep(0.1)

                        context = str(event.message_chain)
                        account_number = re.search(r'\d+', context)
                        if account_number:
                            account_number_check = int(account_number.group())
                        else:
                            account_number_check = 1

                        if len(str(account_number_check)) ==6:
                            account = str(event.message_chain)
                            state[user_id] = "等待房间号"
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(member_id),
                                              'account', str(account))
                            await bot.send(event, f'卡号已收到，请发送房间号')
                        else:
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','stateid','0')
                            update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','sender_id',"0")
                            sb = 0
                            state.clear()
                            await bot.send(event, f'请确认发送的为6位校园卡卡号，注册已终止')


                    elif current_state == "等待房间号" and state_id == str(event.sender.id):
                        room = str(event.message_chain)
                        state[user_id] = "等待建筑位置"
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(member_id),
                                          'room', str(room))
                        await bot.send(event, f'房间号已收到，请发送建筑位置')

                    elif current_state == "等待建筑位置" and state_id == str(event.sender.id):
                        building = str(event.message_chain)
                        state[user_id] = "注册终止"
                        state.clear()
                        if 'S11' in str(event.message_chain) or 's11' in str(event.message_chain) or ('凤凰居' in str(event.message_chain) and '11' in str(event.message_chain)):
                            buildingid = 1599193777
                        elif 'S2' in str(event.message_chain) or 's2' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '2' in str(event.message_chain)):
                            buildingid = 1503975890
                        elif 'S5' in str(event.message_chain) or 's5' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '5' in str(event.message_chain)):
                            buildingid = 1503975967
                        elif 'S6' in str(event.message_chain) or 's6' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '6' in str(event.message_chain)):
                            buildingid = 1503975980
                        elif 'S7' in str(event.message_chain) or 's7' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '7' in str(event.message_chain)):
                            buildingid = 1503975988
                        elif 'S8' in str(event.message_chain) or 's8' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '8' in str(event.message_chain)):
                            buildingid = 1503975995
                        elif 'S9' in str(event.message_chain) or 's9' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '9' in str(event.message_chain)):
                            buildingid = 1503976004
                        elif 'S10' in str(event.message_chain) or 's10' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '10' in str(event.message_chain)):
                            buildingid = 1503976037
                        elif 'S1' in str(event.message_chain) or 's1' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '1' in str(event.message_chain)):
                            buildingid = 1503975832
                        elif 'T1' in str(event.message_chain) or 't1' in str(event.message_chain):
                            buildingid = 1574231830
                        elif 'T3' in str(event.message_chain) or 't2' in str(event.message_chain):
                            buildingid = 1574231835
                        elif 'B10' in str(event.message_chain) or 'b10' in str(event.message_chain):
                            buildingid = 1693031710
                        elif 'B2' in str(event.message_chain) or 'b2' in str(event.message_chain):
                            buildingid = 1661835256
                        elif 'B9' in str(event.message_chain) or 'b9' in str(event.message_chain):
                            buildingid = 1693031698
                        elif 'B1' in str(event.message_chain) or 'b1' in str(event.message_chain):
                            buildingid = 1661835249

                        else:
                            await bot.send(event, f'未能成功获取，请重试或联系master')
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'stateid', '0')
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'sender_id', "0")
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                          'member_id', "0")
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(member_id),
                                          'building', str(building))
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(member_id),
                                          'buildingid', str(buildingid))

                        await bot.send(event, f'您注册成功，谢谢！\n若开启bot提醒，请发送“开启电费提醒”')

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

            else:
                await bot.send(event, '本bot暂未开启电费查询以及注册功能')








    @bot.on(FriendMessage)
    async def friend_message_listener(event: FriendMessage):
        # 获取发送者和消息内容
        sender = event.sender
        message_content = event.message_chain.get(Plain)

        #print(f"收到来自 {sender.id} 的消息: {message_content}")
        #print(f"收到来自 {sender} 的消息: {message_content}")
        # 回复消息
        #await bot.send(event, "accept message")



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

        stateid = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo',
                                 'stateid')
        if stateid == None:
            user_data = manage_user_data(base_directory, 'elect_check', room='b666', location="abc", account="alice123")
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

        if '提醒' in str(event.message_chain) and ('开启' in str(event.message_chain) or '打开' in str(event.message_chain))and '电费' in str(event.message_chain):
            name_id = int(str(event.sender.id))
            stateid_check_number=get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'stateid_check')
            stateid_check_number=int(stateid_check_number)
            if stateid_check_number:
                await bot.send(event, '您已订阅过此服务')
            else:
                update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'stateid_check', '1')
                await bot.send(event, '已订阅，电费过低时候将通知您')


        if '提醒' in str(event.message_chain) and ('取消' in str(event.message_chain) or '停止' in str(event.message_chain))and '电费' in str(event.message_chain):
            name_id = int(str(event.sender.id))
            stateid_check_number=get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'stateid_check')
            if stateid_check_number:
                if stateid_check_number==1:
                    update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                      'stateid_check', '0')
                    await bot.send(event, '已为您取消该服务')
                else:
                    await bot.send(event, '该服务一直是停止状态')



        if '电费查询' == str(event.message_chain):
            elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','elect_check_state')
            if elect_check_state==None:
                elect_check_state=0
            if int(elect_check_state) == 1:
                logger.info("个人电费查询")
                name_id = int(str(event.sender.id))

                room = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'room')
                if room == None:
                    await bot.send(event, '您还未注册，请发送"电费注册"以开始')
                else:
                    times = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                          'times')
                    if times == None:
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id), 'times','1')
                    if times:
                        times=int(times)
                        times+=1
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),'times',str(times))
                    #await bot.send(event, "当前功能限时上线," + str(botName) + "正在为您查询喵~")
                    account_number = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),str(name_id),'account_number')

                    if account_number == None:
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                          'account_number', str(name_id))

                    stateid_check = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),
                                                   str(name_id), 'stateid_check')
                    if stateid_check == None:
                        update_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), str(name_id),
                                          'stateid_check', '0')
                    json_check(directory, data_json)
                    json_rewrite(directory, data_json, name_id)
                    inquiry(directory, data_json)
                    await bot.send(event, '该项目为测试功能，您宿舍剩余的电量为' + str(remaining_power))
            else:
                await bot.send(event, '本bot暂未开启电费查询功能，请前往bot群获取最细消息')


        if ('注册' in str(event.message_chain) and '电费' in str(event.message_chain)) or stateid == 1:
            elect_check_state = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'), 'manshuo','elect_check_state')
            if elect_check_state==None:
                elect_check_state=0
            if int(elect_check_state) == 1:
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
                        if 'S11' in str(event.message_chain) or 's11' in str(event.message_chain) or ('凤凰居' in str(event.message_chain) and '11' in str(event.message_chain)):
                            buildingid = 1599193777
                        elif 'S2' in str(event.message_chain) or 's2' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '2' in str(event.message_chain)):
                            buildingid = 1503975890
                        elif 'S5' in str(event.message_chain) or 's5' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '5' in str(event.message_chain)):
                            buildingid = 1503975967
                        elif 'S6' in str(event.message_chain) or 's6' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '6' in str(event.message_chain)):
                            buildingid = 1503975980
                        elif 'S7' in str(event.message_chain) or 's7' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '7' in str(event.message_chain)):
                            buildingid = 1503975988
                        elif 'S8' in str(event.message_chain) or 's8' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '8' in str(event.message_chain)):
                            buildingid = 1503975995
                        elif 'S9' in str(event.message_chain) or 's9' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '9' in str(event.message_chain)):
                            buildingid = 1503976004
                        elif 'S10' in str(event.message_chain) or 's10' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '10' in str(event.message_chain)):
                            buildingid = 1503976037
                        elif 'S1' in str(event.message_chain) or 's1' in str(event.message_chain)or ('凤凰居' in str(event.message_chain) and '1' in str(event.message_chain)):
                            buildingid = 1503975832
                        elif 'T1' in str(event.message_chain) or 't1' in str(event.message_chain):
                            buildingid = 1574231830
                        elif 'T3' in str(event.message_chain) or 't2' in str(event.message_chain):
                            buildingid = 1574231835
                        elif 'B10' in str(event.message_chain) or 'b10' in str(event.message_chain):
                            buildingid = 1693031710
                        elif 'B2' in str(event.message_chain) or 'b2' in str(event.message_chain):
                            buildingid = 1661835256
                        elif 'B9' in str(event.message_chain) or 'b9' in str(event.message_chain):
                            buildingid = 1693031698
                        elif 'B1' in str(event.message_chain) or 'b1' in str(event.message_chain):
                            buildingid = 1661835249
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

                        await bot.send(event, f'您注册成功，谢谢！\n若开启bot提醒，请发送“开启电费提醒”')

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
            else:
                await bot.send(event, '本bot暂未开启电费查询以及注册功能，请前往bot群获取最细消息')

    @bot.on(Startup)
    async def start_scheduler(_):
        async def timer():
            today_finished = False # 设置变量标识今天是会否完成任务，防止重复发送
            while True:
                await asyncio.sleep(1)
                now = datetime.datetime.now()
                state_elect_check = 0

                if now.hour == 20 and now.minute == 00 and not today_finished: # 每天早上 7:30 发送早安
                    state_elect_check=1
                if now.hour == 20 and now.minute == 1:
                    today_finished = False # 早上 7:31，重置今天是否完成任务的标识
                if now.hour == 8 and now.minute == 00 and not today_finished:
                    state_elect_check = 1
                if now.hour == 8 and now.minute == 1:
                    today_finished = False # 早上 7:31，重置今天是否完成任务的标识


                if state_elect_check==1:
                    state_elect_check = 0
                    directory = 'manshuo_data'  # 文件夹路径
                    data_json = 'data.json'  # 文件名
                    base_directory = directory
                    all_accounts = get_all_user_accounts(base_directory)
                    print("所有用户的账号:", all_accounts)

                    for account_number in all_accounts:
                        # print(account_number)
                        name_id = int(account_number)
                        json_check(directory, data_json)
                        json_rewrite(directory, data_json, name_id)
                        inquiry(directory, data_json)
                        stateid_check = get_user_field(os.path.join(base_directory, 'elect_check', 'user_data.yaml'),
                                                       str(name_id),
                                                       'stateid_check')
                        #print("用户", name_id, "的电费:", remaining_power)
                        remaining_power_check = int(remaining_power)
                        if remaining_power_check < 20:
                            if stateid_check:
                                stateid_check = int(stateid_check)
                                friend_check = await bot.get_friend(name_id)
                                group_member_check = await bot.get_group_member(674822468, name_id)
                                if stateid_check == 1:
                                    print("用户", name_id, "的电费过低，将为其发送通知提醒")
                                    if group_member_check:
                                        await bot.send_group_message(674822468,[At(name_id), '您的电费过低：' + str(remaining_power) + " \n请及时为宿舍补充电费"])
                                    if friend_check:
                                        await bot.send_friend_message(name_id,'您的电费过低：' + str(remaining_power) + " \n请及时为宿舍补充电费")
                    #await bot.send_friend_message(1270858640, '定时开启')
                    today_finished = True
                if now.hour == 20 and now.minute == 1:
                    today_finished = False # 早上 7:31，重置今天是否完成任务的标识
                if now.hour == 19 and now.minute == 59:
                    today_finished = False
        global _task
        _task = asyncio.create_task(timer())

    @bot.on(Shutdown)
    async def stop_scheduler(_):
        # 退出时停止定时任务
        if _task and not task.done():
            _task.cancel()


