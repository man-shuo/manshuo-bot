# -*- coding: utf-8 -*-
import asyncio
import matplotlib.pyplot as plt
import os
import json
import httpx
import re
import json
import os
import random
import httpx as requests
from multiprocessing import  Lock
import re
import requests
from datetime import datetime, timedelta
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown,MessageChain

buildingidcheck= {
    '1503975832':{'s1','S1','凤凰居1号楼','凤凰居一号楼','凤凰居1'} ,
    '1503975890':{'s2','S2','凤凰居2号楼','凤凰居二号楼','凤凰居2'},
    '1599193777': {'s11', 'S11', '凤凰居11号楼', '凤凰居十一号楼','凤凰居11','s11-13','s13','S11-13','凤凰居S11','凤凰居s11'},
    '1503975967': {'s5', 'S5', '凤凰居5号楼', '凤凰居五号楼', '凤凰居5'},
    '1503975980': {'s6', 'S6', '凤凰居6号楼', '凤凰居六号楼', '凤凰居6'},
    '1503975988': {'s7', 'S7', '凤凰居7号楼', '凤凰七号楼', '凤凰居7'},
    '1503975995': {'s8', 'S8', '凤凰居8号楼', '凤凰居八二号楼', '凤凰居8'},
    '1503976004': {'s9', 'S9', '凤凰居9号楼', '凤凰居九号楼', '凤凰居9'},
    '1503976037': {'s10', 'S10', '凤凰居10号楼', '凤凰居二号楼', '凤凰居10'},
    '1574231830': {'t1', 'T1'},
    '1574231835': {'t3', 'T3'},
    '1693031710': {'b10', 'B10', '阅海居10号楼', '阅海居十号楼', '阅海居10'},
    '1661835256': {'b2', 'B2', '阅海居2号楼', '阅海居二号楼', '阅海居2'},
    '1693031698': {'b9', 'B9', '阅海居9号楼', '阅海居九号楼', '阅海居9'},
    '1661835249': {'b1', 'B1', '阅海居1号楼', '阅海居一号楼', '阅海居1'}
}

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
DATA_DIR = os.path.join("manshuo_data/elect_check")
SaveData.set_base_dir(DATA_DIR)

def init_data():#初始化文件
    data_file = SaveData("user_data")
    if not data_file.data:
        data_file.data = {
            "user_info": {},
            "buildingid": {},
            "check_number": {}
        }
    data_file.save()

def elect_buildingid(building):
    print('yes')

def elect_check_internet(floor,campus,building,room):
    if campus =='您还没有进行注册喵' :
        return False
    elif campus == "您的信息有误，请重新注册喵～":
        return 'error'
    url = "https://mcard.sdu.edu.cn/charge/feeitem/getThirdData"
    headers = {
        "Host": "mcard.sdu.edu.cn",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Basic Y2hhcmdlOmNoYXJnZV9zZWNyZXQ=",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://mcard.sdu.edu.cn",
        "Content-Length": "192",  # 根据实际请求数据的长度来调整
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/Synjones-E-Campus/2.3.24/&cn&/schoolId=53",
        "Referer": "https://mcard.sdu.edu.cn/charge-app/",
        "Connection": "keep-alive",
        "synjones-auth": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOiIxIiwiZmxhZyI6IjAwMDEwIiwidXNlcl9uYW1lIjoiMjAyMTAwMTIwMDE5IiwibW9iaWxlIjoiMTM3NTM1NTUzMDYiLCJsb2dpbkZyb20iOiJhcHAiLCJ1dWlkIjoiY2M0MzFjMTBmYTBhMjg5MDg2ZTlhNzViOWY5M2RjNjEiLCJjbGllbnRfaWQiOiJtb2JpbGVfc2VydmljZV9wbGF0Zm9ybSIsImlzX3Bhc3N3b3JkX2V4cGlyZWQiOmZhbHNlLCJpc19maXJzdF9sb2dpbiI6dHJ1ZSwic25vIjoiMjAyMTAwMTIwMDE5Iiwic2NvcGUiOlsiYWxsIl0sImxvZ2ludHlwZSI6InNub05ld0FuZEFjY291bnRLZXlib2FyZCIsIm5hbWUiOiLnjovmnpfljZoiLCJpZCI6MTYxMDkyMzcsImV4cCI6MTczOTYzODQ3NywianRpIjoiNDU4NDA0YjAtZTdmNC00OTkyLWJmYTQtNjg2NmYwNDM2YjMwIn0.TTn3ysXi0iqyLtWwW4KUwDXDewMq9PWIT5YxK7SmrPU",
        "Sec-Fetch-Dest": "empty",
        "Cookie": "Domain=pass.sdu.edu.cn; TGC=\"third_login:TGT-ee34591bd32b4fd191d2bf3be75fa926\""
    }
    if int(campus) == 1:
        for check in buildingidcheck:
            if building in buildingidcheck[check]:
                buildingid=check
                #print(f'buildingid={buildingid}')
                data = {
                    f"feeitemid": "410",
                    f"type": "IEC",
                    f"campus": "青岛校区&青岛校区",
                    f"building": f"{buildingid}&{building}",
                    f"room": f"{room}",
                }
    if int(campus) == 2:
        room_check = str(room).zfill(3)
        #print(room_check)
        data = {
            f"feeitemid": "411",
            f"type": "IEC",
            f"campus": "主校区&主校区",
            f"building": f"{building}&{building}",
            f"room": f"{building}0{floor}{room_check}&{room}",
            f'floor': f"{building}0{floor}&{floor}",
        }
        #print(data)
    # 发送POST请求
    js = None

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        js = json.loads(response.text)
    else:return None
    #print(js)
    try:
        match = re.search(r"\d+\.\d+", js['map']["showData"].get("信息"))
        if match:
            # 将提取到的数字部分转换为浮点数
            remaining_power = float(match.group())
            return remaining_power
        else:
            return None
    except KeyError:
        return 'error'



def user_info_check(register_id):
    data_file = SaveData("user_data")
    if data_file.data["user_info"].get(f'{register_id}') is None:
        return "您还没有进行注册喵",None,None,None
    try:
        campus = data_file.data["user_info"][f'{register_id}']['campus']
        building = data_file.data["user_info"][f'{register_id}']['building']
        room = data_file.data["user_info"][f'{register_id}']['room']
        if int(campus) == 1:
            floor = None
        elif int(campus) == 2:
            floor = data_file.data["user_info"][f'{register_id}']['floor']
        return campus, building, room, floor
    except KeyError:
        return "您的信息有误，请重新注册喵～", None, None, None


def user_info_Re_register(register_id):
    global Team_list
    try:
        Team_list['campus'].pop(register_id, None)
        Team_list['room'].pop(register_id, None)
        Team_list['building'].pop(register_id, None)
        Team_list['floor'].pop(register_id, None)
    except KeyError:
        return
    pass

def add_elect_number(register_id):
    data_file = SaveData("user_data")
    if data_file.data["user_info"].get(f'{register_id}'):
        if data_file.data["user_info"][f'{register_id}'].get('times'):
            number_check = int(data_file.data["user_info"][f'{register_id}']['times'])
            number_check+=1
            data_file.data["user_info"][f'{register_id}']['times']=number_check
        else:
            data_file.data["user_info"][f'{register_id}']['times'] = 1
    data_file.save()
    return data_file.data["user_info"][f'{register_id}']['times']

def main(bot, logger):
    init_data()
    _task = None
    global Team_list
    Team_list = {'campus':{}, 'building':{}, 'room':{},'floor':{},'register':{}}
    print('初始化')
    @bot.on(GroupMessage)
    async def elect_check(event: GroupMessage):
        data_file = SaveData("user_data")
        register_flag=0
        if not str(event.message_chain).startswith("电费查询"):
            return
        register_id = event.sender.id
        context = str(event.message_chain)
        number_check = re.search(r'\d+', context)
        if number_check:
            register_id = int(number_check.group())
            register_flag = 1

        campus, building, room, floor=user_info_check(register_id)
        try:
            remaining_power = elect_check_internet(floor, campus, building, room)
        except Exception as e:
            await bot.send(event, "无法获取，请检查个人信息是否正确")
            return
        print(remaining_power)
        if remaining_power == False:
            await bot.send(event, f'您还没有进行注册喵')
            return
        elif remaining_power == 'error':
            await bot.send(event, f'您的个人信息有误，请重新注册喵～')
            return
        elif remaining_power is None:
            await bot.send(event, f'枫与岚暂时无法查询喵，请稍后再试')
            return
        if register_flag==0:
            await bot.send(event, f'该项目为测试功能，您宿舍的剩余电量为{remaining_power}')
        elif register_flag == 1:
            await bot.send_group_message(event.sender.group.id, [At(register_id), ' 所在的宿舍剩余的电量为' + str(remaining_power)])
        add_elect_number(register_id)
        data_file.save()

    @bot.on(GroupMessage)
    async def elect_user_info_check(event: GroupMessage):
        data_file = SaveData("user_data")
        if '电费个人信息查询' not in str(event.message_chain):
            return
        register_id = event.sender.id
        if data_file.data["user_info"].get(f'{register_id}') is None:
            await bot.send(event, "您还没有进行注册喵")
            return
        try:
            campus, building, room, floor=user_info_check(register_id)
            await bot.send(event, f'您的个人信息为：\n校区：{campus}，建筑：{building}，房间号：{room},楼层：{floor}')
        except Exception as e:
            await bot.send(event, f'您的个人信息出错了喵～')

    @bot.on(GroupMessage)
    async def elect_user_info_plt(event: GroupMessage):
        data_file = SaveData("user_data")
        register_flag = 0
        if '创建虚拟数据' == str(event.message_chain):
            try:
                register_id = int(event.sender.id)
                today = datetime.today()
                first_day_of_this_month = today.replace(day=1)
                last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
                try:
                    start_date = today.replace(month=today.month - 1, day=today.day)
                except ValueError:
                    start_date = last_day_of_last_month
                current_date = start_date
                while current_date <= today:
                    date = str(current_date.strftime('%Y-%m-%d'))
                    remaining_power = random.randint(120, 130)
                    if data_file.data["check_number"].get(f'{register_id}') is None:
                        data_file.data["check_number"][f'{register_id}'] = {}
                    data_file.data["check_number"][f'{register_id}'][f'{date}'] = remaining_power
                    print(remaining_power, date)
                    current_date += timedelta(days=1)
                    data_file.save()
                await bot.send(event, "虚拟数据创建成功喵")
            except Exception as e:
                await bot.send(event, "虚拟数据创建失败~")

        if not (str(event.message_chain).startswith("本周电费绘图") or str(event.message_chain).startswith("本月电费绘图")or str(event.message_chain).startswith("电费绘图")):
            return
        register_id = int(event.sender.id)
        context = str(event.message_chain)
        number_check = re.search(r'\d+', context)
        if number_check:
            register_id = int(number_check.group())
            register_flag = 1
        logger.info(f'查询人：{register_id}')
        if data_file.data["user_info"].get(f'{register_id}') is None:
            await bot.send(event, "您还没有进行注册喵")
            return
        if data_file.data["user_info"][f'{register_id}'].get(f'stateid_check'):
            stateid_check = int(data_file.data["user_info"][f'{register_id}']['stateid_check'])
        else:stateid_check = 0
        if stateid_check != 1:
            await bot.send(event, "您还未开启电费提醒，无法记录电费喵")
            return
        x = []
        y = []
        try:
            if '电费绘图' == str(event.message_chain) or '本周电费绘图' == str(event.message_chain):
                register_flag_check=0
                today = datetime.today()
                start_date = today - timedelta(days=7)
                current_date = start_date
                while current_date <= today:
                    date = str(current_date.strftime('%Y-%m-%d'))
                    if data_file.data["check_number"][f'{register_id}'].get(f'{date}') is None:
                        remaining_power=0
                    else:
                        remaining_power = data_file.data["check_number"][f'{register_id}'][f'{date}']
                    result = date[5:]
                    x.append(f'{result}')
                    y.append(remaining_power)
                    current_date += timedelta(days=1)
            elif '本月电费绘图' in str(event.message_chain):
                register_flag_check = 1
                
                today = datetime.today()
                first_day_of_this_month = today.replace(day=1)
                last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
                try:
                    start_date = today.replace(month=today.month - 1, day=today.day)
                except ValueError:
                    start_date = last_day_of_last_month
                current_date = start_date
                while current_date <= today:
                    date = str(current_date.strftime('%Y-%m-%d'))
                    if data_file.data["check_number"][f'{register_id}'].get(f'{date}') is None:
                        remaining_power=0
                    else:
                        remaining_power = data_file.data["check_number"][f'{register_id}'][f'{date}']
                    result = date[5:]
                    x.append(f'{result}')
                    y.append(remaining_power)
                    current_date += timedelta(days=1)
                #print(x,y)
        except Exception as e:
            await bot.send(event, "电费记录时长不够喵~请耐心等待喵~~")
            return

        try:
            # 创建画布
            plt.figure(figsize=(8, 6))
            # 绘制折线图
            plt.plot(x, y, marker='o', linestyle='-', color='dodgerblue', linewidth=2, label='ELECTION')
            plt.gca().set_facecolor('#f9f9f9')
            plt.title('elect_check_PIL', fontsize=16, fontweight='bold', color='darkblue')
            plt.xlabel('date', fontsize=12)
            plt.ylabel('elect_check', fontsize=12)
            plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
            plt.legend(fontsize=12, loc='upper left')
            if '本周电费绘图' in str(event.message_chain):plt.xticks(fontsize=10)
            elif '本月电费绘图' in str(event.message_chain):plt.xticks(fontsize=10,rotation=45)
            plt.yticks(fontsize=10)
            output_path = "manshuo_data/elect_check/elect_check.png"
            plt.savefig(output_path, dpi=300)
            #plt.show()
            #s = [Image(path='manshuo_data/fonts/xiongdi.jpg')]
            #await bot.send(event, [Image(path=output_path)])
            if register_flag_check == 0:
                await bot.send_group_message(event.sender.group.id,
                                         [At(register_id),f' 本周你的电费图像为',Image(path=output_path)])
            if register_flag_check == 1:
                await bot.send_group_message(event.sender.group.id,
                                         [At(register_id),f' 本月你的电费图像为',Image(path=output_path)])
        except Exception as e:
            await bot.send(event, "绘图失败了喵~")
            return


    @bot.on(GroupMessage)
    async def elect_user_number_check(event: GroupMessage):
        data_file = SaveData("user_data")
        if '电费次数查询' not in str(event.message_chain):
            return
        register_id = event.sender.id
        context = str(event.message_chain)
        number_check = re.search(r'\d+', context)
        if number_check:
            register_id = int(number_check.group())

        if data_file.data["user_info"].get(f'{register_id}') is None:
            await bot.send(event, "您还没有进行注册喵")
            return
        try:
            number=add_elect_number(register_id)
            await bot.send(event, f'您的电费查询次数为：{number}')
        except Exception as e:
            await bot.send(event, f'您的个人信息出错了喵～')


    @bot.on(GroupMessage)
    async def elect_register(event: GroupMessage):
        global Team_list
        register_flag=0
        number_check = 0
        data_file = SaveData("user_data")

        register_id = event.sender.id
        if event.sender.id in Team_list['register']:
            register_id=Team_list['register'][event.sender.id]
        if data_file.data["user_info"].get(f'{register_id}'):
            if data_file.data["user_info"][f'{register_id}'].get('campus'):
                number_check=int(data_file.data["user_info"][f'{register_id}']['campus'])

        if '电费提醒' in str(event.message_chain):
            if data_file.data["user_info"].get(f'{register_id}'):
                if '开启' in str(event.message_chain):
                    data_file.data["user_info"][f'{register_id}']['stateid_check']=1
                    await bot.send(event, "电费提醒已开启")
                elif '关闭' in str(event.message_chain):
                    data_file.data["user_info"][f'{register_id}']['stateid_check']=0
                    await bot.send(event, "电费提醒已关闭")


        if '电费注册' in str(event.message_chain) or '重新注册' == str(event.message_chain):
            if event.group.id == 6748224681:
                await bot.send(event, '该群非bot群，请前往bot群：674822468 开启注册，以免刷屏，谢谢')
                return
            Team_list['register'][event.sender.id] = register_id
            context = str(event.message_chain)
            number_check = re.search(r'\d+', context)
            if number_check:
                register_id = int(number_check.group())
                register_flag = 1
                Team_list['register'][event.sender.id] = register_id

            if data_file.data["user_info"].get(f'{register_id}') is None:
                data_file.data["user_info"][f'{register_id}'] = {}
            if register_flag == 1:
                await bot.send(event, "您正在为他人注册")
            elif register_flag ==0:
                await bot.send(event, "即将开始进行电费注册，建议前往bot群进行，若拒绝请发送'终止注册'")
            await bot.send(event, "请确认您所在的校区\n青岛扣1，威海扣2，不知道的扣眼珠子")
            Team_list['campus'][event.sender.id] = {}
        elif '终止注册' == str(event.message_chain):
            user_info_Re_register(event.sender.id)
            await bot.send(event, "开溜开溜~~")
        elif event.sender.id in Team_list['campus']:
            number_check = str(event.message_chain)
            number_check = re.search(r'\d+', number_check)
            if number_check:
                number_check = int(number_check.group())
                if not (number_check==1 or number_check==2):
                    await bot.send(event, "调戏bot的滚啊～～～")
                    Team_list['campus'].pop(event.sender.id, None)
                    return
            else:
                await bot.send(event, "调戏bot的滚啊～～～")
                Team_list['campus'].pop(event.sender.id, None)
                return
            data_file.data["user_info"][f'{register_id}']['campus'] = int(number_check)
            Team_list['campus'].pop(event.sender.id,None)
            if number_check == 1:
                await bot.send(event, "请发送您的房间号，如b111")
            elif number_check == 2:
                await bot.send(event, "请发送您的房间号,如13，不要加楼层")
            Team_list['room'][event.sender.id] = {}
        elif event.sender.id in Team_list['room'] and number_check == 1 :
            data_file.data["user_info"][f'{register_id}']['room'] = str(event.message_chain)
            Team_list['room'].pop(event.sender.id,None)
            await bot.send(event, "请发送您的建筑位置，如s1")
            Team_list['building'][event.sender.id] = {}
        elif event.sender.id in Team_list['building'] and number_check ==1:
            data_file.data["user_info"][f'{register_id}']['building'] = str(event.message_chain)
            Team_list['building'].pop(event.sender.id,None)
            await bot.send(event, "您已经完成注册\n若开启bot提醒和电费绘图，请发送“开启电费提醒”")

        elif event.sender.id in Team_list['room'] and number_check == 2 :
            data_file.data["user_info"][f'{register_id}']['room'] = str(event.message_chain)
            Team_list['room'].pop(event.sender.id,None)
            await bot.send(event, "请发送您的建筑位置,如15")
            Team_list['building'][event.sender.id] = {}
        elif event.sender.id in Team_list['building'] and number_check == 2 :
            data_file.data["user_info"][f'{register_id}']['building'] = str(event.message_chain)
            Team_list['building'].pop(event.sender.id,None)
            await bot.send(event, "请发送您的楼层，如4")
            Team_list['floor'][event.sender.id] = {}
        elif event.sender.id in Team_list['floor'] and number_check ==2:
            data_file.data["user_info"][f'{register_id}']['floor'] = str(event.message_chain)
            Team_list['floor'].pop(event.sender.id,None)
            await bot.send(event, "您已经完成注册\n若开启bot提醒和电费绘图，请发送“开启电费提醒”\n同时确保您有bot好友或在bot群内，谢谢")
        data_file.save()
        #print(data_file.data)
        #print(Team_list)



    @bot.on(Startup)
    async def start_scheduler(_):
        async def timer():
            today_finished = False  # 设置变量标识今天是会否完成任务，防止重复发送
            while True:
                await asyncio.sleep(1)
                now = datetime.now()
                state_elect_check = 0

                if now.hour == 00 and now.minute == 1 and not today_finished:
                    state_elect_check = 1
                if now.hour == 00 and now.minute == 2:
                    today_finished = False
                if now.hour == 12 and now.minute == 00 and not today_finished:
                    state_elect_check = 1
                if now.hour == 12 and now.minute == 1:
                    today_finished = False


                if state_elect_check == 1:
                    print('开始执行')
                    date = str(now.strftime('%Y-%m-%d'))
                    data_file = SaveData("user_data")
                    print(f'{date}')
                    for register_id in data_file.data["user_info"]:
                        if data_file.data["user_info"][f'{register_id}'].get(f'stateid_check'):
                            stateid_check=int(data_file.data["user_info"][f'{register_id}']['stateid_check'])
                        else:stateid_check=0
                        #print(f'register_id={register_id},stateid_check={stateid_check}')
                        if stateid_check == 0:continue
                        elif stateid_check ==1:
                            try:
                                campus, building, room, floor = user_info_check(register_id)
                                #print(campus, building, room, floor)
                                remaining_power = elect_check_internet(floor, campus, building, room)
                                remaining_power_check = int(remaining_power)
                                if data_file.data["check_number"].get(f'{register_id}') is None:
                                    data_file.data["check_number"][f'{register_id}'] = {}
                                data_file.data["check_number"][f'{register_id}'][f'{date}'] = remaining_power_check
                            except Exception as e:
                                continue
                        if remaining_power_check < 20:
                            register_id = int(register_id)
                            friend_check = await bot.get_friend(register_id)
                            group_member_check = await bot.get_group_member(674822468, register_id)
                            print("用户", register_id, "的电费过低，将为其发送通知提醒")
                            if group_member_check:
                                await bot.send_group_message(674822468, [At(register_id), '您的电费过低：' + str(
                                    remaining_power_check) + " \n请及时为宿舍补充电费"])
                            if friend_check:
                                await bot.send_friend_message(register_id, '您的电费过低：' + str(
                                    remaining_power_check) + " \n请及时为宿舍补充电费")
                    data_file.save()
                    today_finished = True
                if now.hour == 20 and now.minute == 1:
                    today_finished = False  # 早上 7:31，重置今天是否完成任务的标识
                if now.hour == 19 and now.minute == 59:
                    today_finished = False

        global _task
        _task = asyncio.create_task(timer())

    @bot.on(Shutdown)
    async def stop_scheduler(_):
        # 退出时停止定时任务
        if _task and not task.done():
            _task.cancel()
