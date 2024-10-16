import httpx
import json
import random
import yaml
from pytubefix import Channel, YouTube, Playlist, Stream

from plugins.newsEveryDay import get_headers

with open('config/api.yaml', 'r', encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)
    proxy = result.get("proxy")
    proxies = {
        "http://": proxy,
        "https://": proxy
    }
    pyproxies = {       #pytubefix代理
        "http": proxy,
        "https:": proxy
    }

with open('config/settings.yaml', 'r', encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)
ASMR_channels = result.get("ASMR").get("channels")
 
with open('data/ASMR.yaml', 'r', encoding='utf-8') as f:
    ASMRpush = yaml.load(f.read(), Loader=yaml.FullLoader)
pushed_videos = ASMRpush.get("已推送ASMR")

client = httpx.AsyncClient(headers=get_headers(),timeout=100)

async def ASMR_today():
    global ASMR_channels     #ASMR频道列表
    global  pushed_videos    #已推送ASMR列表
    print(ASMR_channels)
    channel = random.choice(ASMR_channels)
    c = Channel(url=f'https://www.youtube.com/{channel}',proxies=pyproxies)
    print(f'https://www.youtube.com/{channel}')

    athor = c.channel_name
    video_idlist=[]
    for url in c.video_urls:
        video_id=str(url).split('=')[1].replace('>', '')
        video_idlist.append(video_id)
    # video_idlist=list(set(video_idlist)-set(pushed_videos))    #该方法可以去除重复ASMR,但是会导致ASMR顺序不确定
    for pushed_video in pushed_videos:      #去除已推送ASMR
        if pushed_video in video_idlist:
            video_idlist.remove(pushed_video)

    try:
        video_id = video_idlist[0]    #获取一个最新的未推送ASMR
        pushed_videos.append(video_id)
        ASMRpush["已推送ASMR"] = pushed_videos
        with open('data/ASMR.yaml', 'w', encoding="utf-8") as file:
            yaml.dump(ASMRpush, file, allow_unicode=True)
    except:
        print(f"{athor}频道没有未推送的ASMR,从投稿中随机选择")    #如果没有未推送的ASMR,从该频道投稿中随机选择
        video_id=str(random.choice(c.video_urls)).split('=')[1].replace('>', '')
    url='https://www.youtube.com/watch?v='+video_id
    yt = YouTube(url)
    title = yt.title
    length = yt.length
    return athor,title,video_id,length


# 函数：存储视频信息
def store_video_data(id, length, url, filename="video_data.yaml"):
    # 尝试读取现有的 YAML 文件数据
    try:
        with open(filename, "r") as file:
            data = yaml.safe_load(file)
            if data is None:  # 如果文件为空，初始化数据结构
                data = {}
    except FileNotFoundError:
        data = {}  # 如果文件不存在，创建一个空的字典

    data[id] = {
        "length": length,
        "url": url
    }
    # 将数据写回 YAML 文件
    with open(filename, "w") as file:
        yaml.dump(data, file)
    print(f"Video data for id {id} stored successfully.")

# 函数：随机获取一个视频数据
def information_get(filename="manshuo_data/ASMR_check/video_data.yaml"):
    try:
        with open(filename, "r") as file:
            data = yaml.safe_load(file)
            if not data:
                print("No data found in the file.")
                return None
        # 随机选择一个 id
        video_id = random.choice(list(data.keys()))
        video_data=data[video_id]
        title=video_data['title']
        url=video_data['url']
        length=video_data['length']
        athor=video_data['athor']
        return video_id, title, url, length,athor
    except FileNotFoundError:
        print("File not found.")
        return None





async def ASMR_random():
    global ASMR_channels     #ASMR频道列表
    channel = random.choice(ASMR_channels)

    pyproxies = {
        "http": 'http://127.0.0.1:7890',
        "https": 'https://127.0.0.1:7890'
    }
    try:
        raise Exception("这是一个手动引发的错误")
        print('开始获取')
        c = Channel(url=f'https://www.youtube.com/{channel}', proxies=pyproxies)
        # c = Channel(url=f'https://www.youtube.com/@emococh/videos')
        print(f'url=https://www.youtube.com/{channel}， proxies={pyproxies}')
        athor = c.channel_name
        video_id = str(random.choice(c.video_urls)).split('=')[1].replace('>', '')  # 从该频道投稿中随机选择
        url = 'https://www.youtube.com/watch?v=' + video_id
        yt = YouTube(url)
        title = yt.title
        length = yt.length
    except Exception:
        print('获取失败，尝试获取本地数据')
        try:
            video_id, title, url, length,athor = information_get()
        except Exception:
            print('本地数据获取失败。尝试直接赋值')
            url = f'https://www.youtube.com/@emococh/videos'
            athor='えもこちゃんねる'
            title='【密着甘々】友達以上恋人未満のクラスメイトと相合傘をしたら甘い空気になって…♡【KU100シチュボASMR】'
            video_id='I1rwPVoWHFs'
            length=442

    return athor,title,video_id,length,url

async def get_audio(video_id):
    url=f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(url=url,proxies=pyproxies)
    title = yt.title

    url=f"https://ripyoutube.com/mates/en/convert?id={video_id}"    #从ripyoutube获取音频下载地址
    data ={
        'platform': 'youtube',
        'url': f'https://www.youtube.com/watch?v={video_id}',
        'title': title,
        'id': 'iCMgE7C1JltWuflTeD0TJm==',
        'ext': 'mp3',
        'note': '128k',
        'format': ''
    }

    response = await client.post(url=url,data=data)
    audiourl = response.json()['downloadUrlX']
    response = await client.get(audiourl)
    path = f'data/music/musicCache/{video_id}.mp3'
    with open(path, 'wb') as f:
        f.write(response.content)
    audiourl =await file_chain(path)
    return audiourl

async def get_video(video_id):
    url=f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(url=url,proxies=pyproxies)
    title = yt.title

    url=f"https://ripyoutube.com/mates/en/convert?id={video_id}"    #从ripyoutube获取视频下载地址
    data ={
        'platform': 'youtube',
        'url': f'https://www.youtube.com/watch?v={video_id}',
        'title': title,
        'id': 'iCMgE7C1JltWuflTeD0TJn==',
        'ext': 'mp4',
        'note': '1080p',
        'format': 137
    }

    response = await client.post(url=url,data=data)
    videourl = response.json()['downloadUrlX']
    return videourl

async def get_img(video_id):
    path =f"data/pictures/cache/{video_id}.jpg"
    url=f"https://i.ytimg.com/vi/{video_id}/hq720.jpg"    #下载视频封面
    client = httpx.AsyncClient(headers=get_headers(),proxies=proxies,timeout=100)
    response = await client.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)
    imgurl =await file_chain(path)
    #print(imgurl)
    return imgurl

async def file_chain(path):     ##上传文件到ffsup.com并取得直链
    http_select=['https://www.manshuo.ink/usr/uploads/2024/10/3275509652.jpg',
                 'https://www.manshuo.ink/usr/uploads/2024/09/1038428739.png',
                 'https://www.manshuo.ink/usr/uploads/2024/06/3895161579.jpg',
                 'https://www.manshuo.ink/img/12.jpg',
                 'https://www.manshuo.ink/img/299.JPG',
                 'https://www.manshuo.ink/img/54cdb2cf9e53bf874041e159356a1282.png',
                 ]
    count_number = len(http_select)
    rnum1 = random.randint(0, count_number - 1)


    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Sec-Ch-Ua' : '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Fetch-Dest' : 'empty',
    'Sec-Fetch-Mode' : 'cors',
    'Sec-Fetch-Site' : 'same-site',
    }
    url = 'https://upload.ffsup.com/'
    file = {'file': open(path, 'rb')}
    response = await client.post(url, files=file, headers=headers)
    #print(response.status_code)
    if response.status_code == 200:
        if 'url' in response.json()['data']:
            print(response.json()['data']['url'])
            if str(response.json()['data']['url']) =='https://f0.0sm.com/node0/2024/10/86709FE6710F8F09-1ae7edcae257da47.jpg':
                return http_select[rnum1]
            return response.json()['data']['url']
        else:
            return http_select[rnum1]
    else:
        return 'https://www.manshuo.ink/usr/uploads/2024/09/1038428739.png'
