# -*- coding: utf-8 -*-
import os
import random
from mirai.models import ForwardMessageNode, Forward
import yaml
import httpx
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from mirai import GroupMessage, At
from mirai import Voice
from mirai.models import MusicShare

from itertools import repeat
from asyncio import sleep
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import yaml
import random
#from PIL import Image
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown,MessageChain

def manage_gal_status(user_id, status=None, file_path="manshuo_data/galgame_judge.yaml"):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            yaml.dump({}, file)
    with open(file_path, 'r') as file:
        try:
            users_data = yaml.safe_load(file) or {}
        except yaml.YAMLError:
            users_data = {}
    if status is not None:
        users_data[user_id] = status
        with open(file_path, 'w') as file:
            yaml.safe_dump(users_data, file)
        return status
    return users_data.get(user_id, False)


def get_game_description(url):
    # 发送请求获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确的编码

    # 解析网页
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找游戏介绍部分 (根据网页结构，这里假设游戏介绍在<p>标签中)
    game_description = ""
    paragraphs = soup.find_all('p')  # 找到所有的<p>标签
    number=0

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string
    title = title[:-13]
    #print(paragraphs)
    for para in paragraphs:
        if  "发行日期" in para.text or number==1:  # 假设含有"介绍"或"剧情"关键词的是游戏介绍
            game_description = str(game_description)+'\n'+str(para.text)

            if number==1:
                game_description = str(title) + str(game_description)
                break
            number = 1


    # 返回游戏介绍
    if game_description:
        return game_description
    else:
        return None

def get_game_image(url,filepath,number_url):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # 获取网页内容
    response = requests.get(url)

    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有的 <img> 标签
        images = soup.find_all('img')

        if manage_gal_status(number_url):
            if manage_gal_status(str(number_url)+'.jpg'):img_name=str(number_url)+'.jpg'
            elif manage_gal_status(str(number_url) + '.png'): img_name = str(number_url) + '.png'
            elif manage_gal_status(str(number_url) + '.webp'): img_name = str(number_url) + '.webp'
            else: img_name = None
            print("图片已存在，返回图片名称")
            return img_name
        else:
            state=False
            # 遍历每个图片标签
            for img in images:
                # 获取图片的 URL
                img_url = img.get('src')
                if img_url:
                    # 处理相对路径，补全成完整 URL
                    img_url = urljoin(url, img_url)
                    # 获取图片名称
                    img_name = os.path.basename(img_url)
                    #print('这是获取图片名称',img_name)
                    if  'main' in img_name:

                        # 下载图片并保存
                        if 'jpg' in img_name:
                            img_name_test=str(number_url)+'.jpg'
                        if 'png' in img_name:
                            img_name_test = str(number_url) + '.png'
                        if 'webp' in img_name:
                            img_name_test = str(number_url) + '.webp'
                        print(img_name_test)
                        img_name=img_name_test
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(filepath, img_name)
                            with open(img_path, 'wb') as f:
                                f.write(img_response.content)
                            manage_gal_status(number_url,True)
                            if 'jpg' in img_name:
                                manage_gal_status(str(number_url) + '.jpg', True)
                            if 'png' in img_name:
                                manage_gal_status(str(number_url) + '.png', True)
                            if 'webp' in img_name:
                                manage_gal_status(str(number_url) + '.webp', True)
                            state = True
                            print(f"图片下载完成: {img_name}")

                            return img_name

                    elif 'default' in img_name :
                        global state_gal
                        state_gal=True

                        # 下载图片并保存
                        if 'jpg' in img_name:
                            img_name_test=str(number_url)+'deflaut.jpg'
                        if 'png' in img_name:
                            img_name_test = str(number_url) + 'deflaut.png'
                        if 'webp' in img_name:
                            img_name_test = str(number_url) + 'deflaut.webp'
                        print(img_name_test)
                        img_name=img_name_test
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(filepath, img_name)
                            with open(img_path, 'wb') as f:
                                f.write(img_response.content)
                            manage_gal_status(str(number_url)+'deflaut',True)
                            if 'jpg' in img_name:
                                manage_gal_status(str(number_url) + 'deflaut.jpg', True)
                            if 'png' in img_name:
                                manage_gal_status(str(number_url) + 'deflaut.png', True)
                            if 'webp' in img_name:
                                manage_gal_status(str(number_url) + 'deflaut.webp', True)
                            state = True
                            print(f"图片下载完成: {img_name}")

                            return img_name


                    else:
                        if state:
                            print(f"无法下载图片: {img_url}")
                            return None


def read_paragraphs_from_file(filename):
    # 读取文件中的所有段落，并以字典形式返回，键为序号，值为段落内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        paragraphs = content.split('\n\n')  # 按照两个换行符拆分段落
        numbered_paragraphs = {i+1: para.strip() for i, para in enumerate(paragraphs)}  # 给每个段落加上序号
    return numbered_paragraphs


def get_random_paragraph(numbered_paragraphs):
    # 随机选择一个序号
    random_index = random.choice(list(numbered_paragraphs.keys()))
    return random_index, numbered_paragraphs[random_index]


def main(bot, logger):
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        
        
        filename = 'manshuo_data/galgamelist/galgamelist.txt'  # 替换为你的TXT文件名
        number=8
        number1=number+43
        flag = 0
        state_gal=False
        
        if str(event.message_chain) == "gal查询":
            flag=1
            await sleep(0.1)
            
        global galgame
        galgame = 1
        if str(event.message_chain) == "开启galgame推荐":
            galgame = 1
            
            logger.info("开启Galgame推荐")
            await bot.send(event, 'Ciallo～(∠・ω< )⌒☆，galgame推荐已开启喵')
        if str(event.message_chain) == "关闭galgame推荐":
            galgame = 0
            logger.info("关闭Galgame推荐")
            await bot.send(event, '关闭Galgame推荐')
        
        if str(event.message_chain) == "galgame推荐" or str(event.message_chain) == "Galgame推荐" or(
                At(bot.qq) in event.message_chain and "gal" in str(event.message_chain)) or flag == 1:
            logger.info("Galgame推荐")



            filepath = 'manshuo_data/galgame_image'
            for i in range(5):
                number_url = random.randint(1, 4000)
                # number_url=2302
                url = 'https://www.hikarinagi.com/p/' + str(number_url)
                #print('第'+str(i)+ '次尝试')
                logger.info('第'+str(i)+ '次尝试')
                logger.info(url)
                #print(url)
                description = get_game_description(url)
                if description:
                    break
            img_name = get_game_image(url, filepath, number_url)





            if flag == 0:
                rnum1=random.randint(1,number1)
            if flag == 1:
                flag=0
                await bot.send(event, '请输入你想查询的序号')
                await sleep(0.1)
                rnum1 = int(str(event.message_chain))
            #await bot.send(event, str(rnum1))


            if description and img_name:
                if img_name:
                    logger.info("有玩Gal的下头男，一股味！")

                    cmList = []
                    s = [Image(path=filepath + '/'+img_name)]
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(s))
                    cmList.append(b1)
                    #await bot.send(event, s)

                    if 'def' in img_name:
                        b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                                message_chain=MessageChain(
                                                    '网页图片获取失败，默认使用default'))
                        cmList.append(b1)


                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(
                                                str(description)+'\n详情请前往以下网站查看：'+str(url)))
                    cmList.append(b1)
                    #await bot.send(event, "序号:"+str(random_index_1)+str(random_paragraph)+'\n详情请前往以下网站查看：http://www.manshuo.ink/index.php/archives/294/')
                    await bot.send(event, Forward(node_list=cmList))



            else:
                if rnum1:
                    logger.info("有玩Gal的下头男，一股味！")
                    logger.info("网络获取失败，调用本地数据")
                    #await bot.send(event, '测试开始，开始输出结果：')
                    paragraphs = read_paragraphs_from_file(filename)
                    random_index, random_paragraph = get_random_paragraph(paragraphs)
                    #此处偷懒
                    name=str(random_index)+".webp"
                    logger.info(str(random_index))
                    cmList = []
                    s=[Image(path='manshuo_data/galgamelist/'+name)]
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(s))
                    cmList.append(b1)
                    #await bot.send(event, s)
                    random_index_1=random_index
                    b1 = ForwardMessageNode(sender_id=bot.qq, sender_name="Manyana",
                                            message_chain=MessageChain(
                                                "序号:"+str(random_index_1)+str(random_paragraph)+'\n详情请前往以下网站查看：http://www.manshuo.ink/index.php/archives/294/'))
                    cmList.append(b1)
                    #await bot.send(event, "序号:"+str(random_index_1)+str(random_paragraph)+'\n详情请前往以下网站查看：http://www.manshuo.ink/index.php/archives/294/')
                    await bot.send(event, Forward(node_list=cmList))



                
                
                
