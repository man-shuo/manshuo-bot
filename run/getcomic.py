# -*- coding:utf-8 -*-
import os
import shutil
import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
import random
import yaml
from mirai import GroupMessage, MessageChain, Image, FriendMessage
from mirai.models import ForwardMessageNode, Forward
from plugins.toolkits import group_manage_controller
from plugins.jmcomicDownload import queryJM, downloadComic, downloadALLAndToPdf, JM_search, JM_search_week, JM_search_comic_id
import json
import requests
import datetime
from mirai import GroupMessage, At, Plain,  Mirai, WebSocketAdapter, GroupMessage, Image, At,MessageChain
import re
from PIL import Image as PILImage


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


def check_for_new_pdfs(folder_path):
    # 获取当前文件列表
    current_files = set(os.listdir(folder_path))
    
    # 筛选出 PDF 文件
    pdf_files = [f for f in current_files if f.lower().endswith('.pdf')]
    
    if pdf_files:
        return pdf_files
    else:
        return None
def images_to_pdf(image_folder, output_pdf, quality=85):
    """
    将指定文件夹内的图片按照顺序压缩成 PDF 文件。
    :param image_folder: 包含图片的文件夹路径
    :param output_pdf: 输出 PDF 文件路径
    :param quality: 压缩质量（1-100），默认85
    """
    # 获取文件夹内的所有图片文件并按名称排序
    images = sorted(
        [os.path.join(image_folder, file) for file in os.listdir(image_folder) 
         if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    )
    
    if not images:
        print("文件夹中没有图片文件！")
        return
    
    # 打开第一个图片作为PDF的初始页
    with PILImage.open(images[0]) as img:
        img = img.convert('RGB')  # 转为RGB模式（确保兼容性）
        pdf_pages = []
        
        # 压缩并处理剩余的图片
        for image in images[1:]:
            with PILImage.open(image) as img_page:
                img_page = img_page.convert('RGB')
                pdf_pages.append(img_page)
        
        # 保存为PDF
        img.save(output_pdf, save_all=True, append_images=pdf_pages, quality=quality)
        print(f"PDF 已保存至 {output_pdf}")
        
def clear_pdfs(folder_path):
    # 获取文件夹内的所有文件
    files = os.listdir(folder_path)

    # 遍历文件，删除 PDF 文件
    for file in files:
        if file.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
        if file.lower().endswith('.zip'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            #print(f"Deleted: {file_path}")

import zipfile
import os

def compress_pdf_to_zip(pdf_path, zip_path):
    # 创建一个ZIP文件，准备写入数据
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # 获取PDF文件名（不带路径）
        pdf_filename = os.path.basename(pdf_path)
        # 将PDF文件写入ZIP文件中
        zipf.write(pdf_path, arcname=pdf_filename)

    #print(f"PDF 文件已压缩到 {zip_path}")

def main(bot, logger):
    with open('config/settings.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    friendsAndGroups = result.get("加群和好友")
    trustDays = friendsAndGroups.get("trustDays")
    with open('config.json', 'r', encoding='utf-8') as f:
        configData = yaml.load(f.read(), Loader=yaml.FullLoader)
    global userdict
    with open('data/userData.yaml', 'r', encoding='utf-8') as file:
        userdict = yaml.load(file, Loader=yaml.FullLoader)
    global superUser
    superUser = [str(configData.get('master')), ]
    for i in userdict.keys():
        data = userdict.get(i)
        times = int(str(data.get('sts')))
        if times > trustDays:
            superUser.append(str(i))
    with open('config/controller.yaml', 'r', encoding='utf-8') as f:
        controller = yaml.load(f.read(), Loader=yaml.FullLoader)
    jmcomicSettings = controller.get("JMComic")
    URLSource=jmcomicSettings.get("URLSource")
    if not jmcomicSettings.get("enable"):
        logger.warning("jmcomic相关功能已关闭。")
        return
    global operating
    operating=[]
    with open('config/api.yaml', 'r', encoding='utf-8') as f:
        resulttr = yaml.load(f.read(), Loader=yaml.FullLoader)
    proxy = resulttr.get("proxy")
    @bot.on(GroupMessage)
    async def querycomic(event: GroupMessage):
        global superUser,operating
        if str(event.message_chain).startswith("J123M搜"):
            if not group_manage_controller(f'{event.group.id}_JM'):
                return
            aim = str(event.message_chain).replace("JM搜", "")
            if jmcomicSettings.get("onlyTrustUser") and str(event.sender.id) not in superUser:
                await bot.send(event, "用户无权限",True)
                return
            if aim in operating:
                await bot.send(event,"相关文件占用中，等会再发吧",True)
                return
            logger.info(f"JM搜索: {aim}")
            operating.append(aim)
            # 分页查询，search_site就是禁漫网页上的【站内搜索】
            # 原先的执行方式将导致bot进程阻塞，任务添加到线程池，避免阻塞
            await bot.send(event, "在找了在找了，稍等一会哦(长时间不出就是被吞了)",True)
            try:
                loop = asyncio.get_running_loop()
                # 使用线程池执行器
                with ThreadPoolExecutor() as executor:
                    # 使用 asyncio.to_thread 调用函数并获取返回结果
                    results = await loop.run_in_executor(executor, queryJM,aim,5)
            except Exception as e:
                logger.error(e)
                logger.exception("详细错误如下：")
                operating.remove(aim)
            try:
                cmList = []
                cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine", message_chain=MessageChain(f" \n腾子吞图严重，bot仅提供本子部分页面预览。\n图片已经过处理，但不保证百分百不被吞。可能显示不出来")))
                for i in results:
                    cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine",message_chain=MessageChain(i[0])))
                    cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine",message_chain=MessageChain(Image(path=i[1]))))
                await bot.send(event, Forward(node_list=cmList))
                operating.remove(aim)
                #await bot.send(event, "好了喵", True)
                for i in results:
                    os.remove(i[1])
                logger.info("已清除预览缓存")
            except Exception as e:
                logger.error(e)
                await bot.send(event, "寄了喵", True)
                operating.remove(aim)

    @bot.on(GroupMessage)
    async def download(event: GroupMessage):
        if str(event.message_chain).startswith("jm搜索") or str(event.message_chain).startswith("JM搜索"):
            if not group_manage_controller(f'{event.group.id}_JM'):
                return
            keyword = str(event.message_chain)
            index = keyword.find("搜索")
            if index != -1:
                keyword = keyword[index + len("查询") :]
                if ':' in keyword or ' ' in keyword or '：' in keyword:
                    keyword = keyword[+1:]
                print(keyword)
                context=JM_search(keyword)
            if context=="":
                await bot.send(event, "枫与岚好像没有找到你说的本子呢~~~")
                return
            cmList = []
            cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine", message_chain=MessageChain(context)))
            await bot.send(event, Forward(node_list=cmList))

    @bot.on(GroupMessage)
    async def download(event: GroupMessage):
        if '本周jm' == str(event.message_chain) or '本周JM' == str(event.message_chain) or '今日jm' == str(event.message_chain) or '今日JM' == str(event.message_chain):
            if not group_manage_controller(f'{event.group.id}_JM'):
                return
            context=JM_search_week()
            cmList = []
            cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine", message_chain=MessageChain('本周的JM排行如下，请君过目\n')))
            cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine", message_chain=MessageChain(context)))
            await bot.send(event, Forward(node_list=cmList))


    @bot.on(GroupMessage)
    async def download(event: GroupMessage):
        if str(event.message_chain).startswith("验车") or str(event.message_chain).startswith("随机本子"):
            if not group_manage_controller(f'{event.group.id}_JM'):
                return
            global operating
            if jmcomicSettings.get("onlyTrustUser") and str(event.sender.id) not in superUser:
                await bot.send(event, "用户无权限",True)
                return
            if str(event.message_chain).startswith("验车") :
                try:
                    comic_id = int(str(event.message_chain).replace("验车", ""))
                except:
                    await bot.send(event, "无效输入 int，指令格式如下\n验车【车牌号】\n如：验车604142",True)
                    return

                if comic_id in operating:
                    await bot.send(event,"相关文件占用中，等会再试试吧")
                    return
                operating.append(comic_id)
                logger.info(f"JM验车 {comic_id}")
                await bot.send(event, "下载中...稍等喵")
                try:
                    loop = asyncio.get_running_loop()
                    # 使用线程池执行器
                    with ThreadPoolExecutor() as executor:
                        # 使用 asyncio.to_thread 调用函数并获取返回结果
                        png_files = await loop.run_in_executor(executor, downloadComic, comic_id, 1,
                                                               jmcomicSettings.get("previewPages"))
                except Exception as e:
                    logger.error(e)
                    await bot.send(event, "下载失败",True)
                    operating.remove(comic_id)
                    return
            else:
                context=['正在随机ing，请稍等喵~~','正在翻找好看的本子喵~','嘿嘿，JM，启动！！！！','正在翻找JM.jpg','有色色！我来了','hero来了喵~~','了解~','全力色色ing~']
                await bot.send(event, context[random.randint(1, len(context)) - 1])
                context=JM_search_comic_id()
                comic_id = context[random.randint(1, len(context)) - 1]
                logger.info(f"随机JM {comic_id}")
                try:
                    if comic_id in operating:
                        await bot.send(event,"相关文件占用中，等会再试试吧")
                        return
                    operating.append(comic_id)
                    loop = asyncio.get_running_loop()
                    with ThreadPoolExecutor() as executor:
                        png_files = await loop.run_in_executor(executor, downloadComic, comic_id, 1,
                                                               jmcomicSettings.get("previewPages"))
                except Exception as e:
                    await bot.send(event, "随机失败了喵~")

            cmList = []
            logger.info(png_files)
            cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine", message_chain=MessageChain(f"车牌号：{comic_id} \n腾子吞图严重，bot仅提供本子部分页面预览。\n图片已经过处理，但不保证百分百不被吞。可能显示不出来")))
            shutil.rmtree(f"data/pictures/benzi/temp{comic_id}")
            logger.info("移除预览缓存")
            for path in png_files:
                print(path)
                cmList.append(ForwardMessageNode(sender_id=bot.qq, sender_name="ninethnine",
                                                 message_chain=MessageChain(Image(path=path))))
            await bot.send(event, Forward(node_list=cmList))
            operating.remove(comic_id)
            for path in png_files:
                os.remove(path)
            logger.info("本子预览缓存已清除.....")
    @bot.on(GroupMessage)
    async def downloadAndToPdf(event: GroupMessage):
        if str(event.message_chain).startswith("JM下载"):
            if not group_manage_controller(f'{event.group.id}_JM'):
                return
            global operating
            if jmcomicSettings.get("onlyTrustUser") and str(event.sender.id) not in superUser:
                await bot.send(event, "用户无权限")
                return
            try:
                comic_id = int(str(event.message_chain).replace("JM下载",""))
                logger.info(f"JM下载启动 aim: {comic_id}")
            except:
                await bot.send(event,"非法参数，指令示例 JM下载601279")
                return
            if comic_id in operating:
                await bot.send(event,"相关文件占用中，等会再试试吧")
                return
            operating.append(comic_id)
            try:
                await bot.send(event,"已启用线程,请等待下载完成")
                loop = asyncio.get_running_loop()
                # 使用线程池执行器
                with ThreadPoolExecutor() as executor:
                    # 使用 asyncio.to_thread 调用函数并获取返回结果
                    r=await loop.run_in_executor(executor, downloadALLAndToPdf, comic_id, jmcomicSettings.get("savePath"))
                logger.info("pdf检测")
                folder_to_watch = "/home/qq/manshuo_bot_work/data/pictures/benzi"
                new_pdfs = check_for_new_pdfs(folder_to_watch)
                file_mounts=0
                file_mounts=int(file_mounts)
                if new_pdfs:
                    for pdf in new_pdfs :
                        file_mounts= file_mounts+1
                        if file_mounts ==1:
                        #folder_to_clear = "/home/qq/Manyana/data/pictures/benzi"
                            
                            pdf_name=pdf
                        else:
                            clear_pdfs(folder_to_watch)
                    

                #numbers = re.findall(r'\d+', pdf_name)
                numbers = re.sub(r'\D', '', pdf_name)
                
                logger.info("pdf修正")
                #await bot.send(event, "函数返回路径："+str(pdf_name))
                #await bot.send(event, f"下载路径如下{jmcomicSettings.get('savePath')}/{comic_id}.pdf")
                source_file = "/home/qq/manshuo_bot_work/data/pictures/benzi/"+str(numbers)+".zip"  # 源文件路径
                #await bot.send(event, "读取到源文件路径：/home/qq/Manyana/data/pictures/benzi/"+str(numbers)+".zip")
                destination_directory = "/www/wwwroot/www.manshuo.com/manshuo_data"  # 目标文件夹路径
                
                pdf_file_path = "/home/qq/manshuo_bot_work/data/pictures/benzi/"+str(numbers)+".pdf"
                
                 # 压缩后的ZIP文件路径
                zip_file_path = "/home/qq/manshuo_bot_work/data/pictures/benzi/"+str(numbers)+".zip"
                final_path="/www/wwwroot/www.manshuo.com/manshuo_data"+str(numbers)+".zip"
                # 调用函数进行压缩
                await wait_and_delete_file(f"{pdf_file_path}")
                image_folder = "/home/qq/manshuo_bot_work/data/pictures/benzi/"+str(numbers)  # 替换为你的图片文件夹路径
                images_to_pdf(image_folder, pdf_file_path,50)
                logger.info("图片转pdf成功")
                #await bot.send(event, "pdf功能测试:图片转pdf成功")
                logger.info("pdf转移")
                #await bot.send(event, str(pdf_file_path)+"\n"+str(zip_file_path))
                compress_pdf_to_zip(pdf_file_path, zip_file_path)
                logger.info("文件已成功压缩")
                #await bot.send(event, "pdf功能测试:文件已成功压缩")
                
                move_file_to_directory(source_file, destination_directory)
                #logger.info("pdf修正")
                #await bot.send(event, "pdf功能测试:文件转移成功")

                
                
                
                logger.info(f"下载完成，车牌号：{comic_id} \n下载链接：{r} ")
                await bot.send(event,"车牌号："+str(comic_id)+" \n下载链接：http://www.manshuo.ink/manshuo_data/"+str(numbers)+".zip\n因服务器为个人所有，下载速度极慢，bot随后会将文件发送至群里（")
                #await bot.send(event,f"下载完成，车牌号：{comic_id} \n下载链接：{r}\n请复制到浏览器打开，为避免失效请尽快使用",True)
            except Exception as e:
                logger.error(e)
                await bot.send(event, "下载失败",True)
            finally:
                try:
                    absolute_path=pdf_file_path
                    print('开始发送文件')
                    await sendFile(event,absolute_path,comic_id)
                    print('发送成功~~')
                    await wait_and_delete_file(f"{absolute_path}")
                except Exception as e: 
                    logger.error(e)
                finally:
                    operating.remove(comic_id)

    async def sendFile(event,path,comic_id):
        url="http://localhost:3000/upload_group_file"
        header = {
        "Authorization": "Bearer ff" 
        }
        data={
          "group_id": event.group.id,
          "file": path,
          "name": f"{comic_id}.pdf"
                }
        logger.info(data)
        async with httpx.AsyncClient(timeout=None,headers=header) as client:
            r = await client.post(url,json=data)
            #print(r.json())
            print(r)
    async def wait_and_delete_file(file_path, check_interval=30):
        for _ in range(10):
            try:
                shutil.os.remove(file_path)
                logger.info(f"文件 {file_path} 已成功删除")
                return
            except PermissionError:
                logger.warning(f"文件 {file_path} 被占用，等待重试...")
                await asyncio.sleep(interval)
            except FileNotFoundError:
                logger.warning(f"文件 {file_path} 已不存在")
                return
            except Exception as e:
                logger.error(f"删除文件时出现错误: {e}")
                return

