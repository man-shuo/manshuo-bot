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

#from PIL import Image
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown,MessageChain

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
            if flag == 0:
                rnum1=random.randint(1,number1)
            if flag == 1:
                flag=0
                await bot.send(event, '请输入你想查询的序号')
                await sleep(0.1)
                rnum1 = int(str(event.message_chain))
            #await bot.send(event, str(rnum1))
            if rnum1:
                logger.info("有玩Gal的下头男，一股味！")
                #await bot.send(event, '测试开始，开始输出结果：')
                paragraphs = read_paragraphs_from_file(filename)
                random_index, random_paragraph = get_random_paragraph(paragraphs)
                #此处偷懒
                name=str(random_index)+".png"
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



                
                
                
                
            else:
                logger.info("有玩Gal的下头男，一股味！")
                if rnum1==1:
                    logger.info("《兰斯》系列")
                    s=[Image(path='data/galgame/lansi.jpg')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《兰斯》系列\n起手抛出暴论（纯属个人拙见），兰斯系列是整个galgame史上最伟大的系列作品，并且几乎可以肯定，业界不会再孕育出能够与之匹敌的宝藏级作品了。伟大的鬼畜王兰斯，在系列持续更新30年后，终于在2018年推出的兰斯10中完结了他此生的旅程。曾经那个初出茅庐、鲁莽好色的鬼畜勇者，在完成一系列传奇般的冒险历程后，成长为那个在魔物大举入侵、人类四大国岌岌可危之时，手提魔剑卡奥斯、背负全人类最后希望而战的人类最强战士。\n该系列剧情张弛有度，风格总体比较诙谐，但在重大事件的历史节点则很有史诗感，千人千面的优秀角色设计也对剧情的发展有着不小的助力，为避免剧透，此处不作赘述。')
                if rnum1==2:
                    logger.info("《交响乐之雨》")
                    s=[Image(path='data/galgame/jiaoxiangyue.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《交响乐之雨》\n“库里斯，你那边现在也在下着雨吗？\n我这里依旧是晴朗的好天气。”\n降雨永不停歇的城镇琵欧伯，为了即将到来的毕业演奏，属于符德鲁系的主人公库里斯必须与负责歌唱的伙伴一起合奏原创曲目。本作初始共有三条线，或是寻迹旧校舍中的歌声，陪伴黎瑟追求心中的梦想；或是接过雨中法珞的伞，在雨的幻影中为她极尽自己的才华；或是选择陪伴三年的朵鲁妲，即便心怀愧疚也要为她演奏。在三条线路之后则是Al fine线，以朵鲁妲的视角陈述朵鲁妲线，由她之口揭示所有的秘密。最后则是芙铃线，和这位一直陪伴在身边的小妖精迎来真正的ge。\n即便是距今已有20年的作品，sr仍能让我沉浸在雨城的氛围中。它所带来的情感冲突并不强烈，但就像雨一般下在心中。')
                if rnum1==3:
                    logger.info("《NOeSIS》系列")
                    s=[Image(path='data/galgame/NOeSIS.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《NOeSIS》系列\n首先惊悚，tmd回到设置界面大半夜我直接心梗，先不说他那个阴间设置界面，闪回这种百试不爽的发明的人一定是个栽种。\n这玩意好像没r18内容顺便一提\n然后剧情，虽然说立绘看着普通不过剧情确实过关，不过坑还是有的。虽然说角色就几个不过悬疑色彩渲染的不错，不过确实没想到那货是凶手……或者说从我目前只推了一条线来看，幕后黑手另有其人，不过那估计就是新角色了（但是很遗憾第二部是梦醒）不过主角的幼驯染涉及的画风有点偏搞了，怎么说呢，就像恐怖电影里出现了高达，徒手将横梁直接扔向三层多的高楼并贯穿墙壁，不过幼驯染的剧情存在一个坑就是家里埋着的尸体为什么除了浮木还有一个（第二部里被人找出后没有深入）等等')
                if rnum1==4:
                    logger.info("纯白交响曲")
                    s=[Image(path='data/galgame/love-is-pure-white.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '纯白交响曲\n《纯白交响曲》是一部有些年头了的废萌。虽然不都是全线通关，笔者psp版、pc版和高清重置，算来已是三刷，算是玩的次数最多的了\n初见纯白，正是充满幻想与希望的年龄。初动的男性本能让我立志成为日系亚萨西男主，希望能够受欢迎。纯白的主人公瓜生新吾是察言观色、温柔待人的典范，顺势成为我当时学习的目标。张扬与自信随着时间消磨，泪水为虚拟流尽后更漠视现实。二刷时我依然记得想要变得温柔，不过愿望从纯粹的希望变得温柔，到掺杂了希望被温柔对待的欲望。以前憧憬着，希望与人在爱的纯白画布上落下我们的颜色；现在确实love is pure white了，只不过这个白是空白。嘛，也不全是空的，里面装的是些其他人的故事。')
                if rnum1==5:
                    logger.info("樱之刻")
                    s=[Image(path='data/galgame/OIP.jpg')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'樱之刻\n先说结论:樱之刻是一部完成度蛮高的续作。它具有出色（有几首吵死了）的音乐，还算丰富的人设（除了女学生），一直抓在手里的主旨，虽说比不上前作、但也算是精彩的剧情展开的设计。玩的时候虽然有些地方还是很想c过去（比如futa自改不掉的不管怎么样都想掺一脚的荤段子和一些过于反常识的哲学讨论），而且很多线的一些描写感到牵强，很难不去想肯定会有更好的处理，他首先确实还是一部续作，樱之诗、樱之刻加在一起才是一个完整的故事，所以绕开樱之诗去谈樱之刻我觉得是很难得。')
                if rnum1==6:
                    logger.info("ever17")
                    s=[Image(path='data/galgame/ever17.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ 'ever17\n一部全年龄向悬疑作品，一部没玩完就等于没玩的作品。游玩该作品建议严格按照攻略顺序进行选项，以获得最佳游戏体验。\n作品核心诡计为叙述性诡计，是一种推理小说常用手法。在小说中体现为作者通过文字技巧或文章结构来刻意的对读者进行隐瞒或误导，在此基础上编织一个在被误导的读者眼里是绝对不可能有解的谜题，而在作品最后揭露诡计。只需一句话来纠正对读者的误导，所有看似无解的谜题将会自动溶解')
                if rnum1==7:
                    logger.info("乌有乡")
                    s=[Image(path='data/galgame/erewhom.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '乌有乡\n钟表社最佳作品，在我心目中是强于euphoria的存在，猎奇程度也不算很高（同是钟表社的妖蛆之饵，把我恶心的不行）。\n本作属于日式民俗类拔作，剧本还算优良，大致是男主作为外来的普通人进入落后的迷信小村后发生的一系列故事，')
                if rnum1==8:
                    logger.info("Chaos:Child")
                    s=[Image(path='data/galgame/ChaosChild.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Chaos:Child\n浅谈Chaos:Child：于混沌之中的救赎与重生;在正式开始吐槽之前，先讲一下混沌之子（Chaos;Child, 下文简称cc）的概况。混沌之子是5pb.开发的游戏，为MAGES所开发的“科学ADV” 系列的第四款作品，并于2015年发售。该作虽然是《混沌之脑》的正统续作.')
                if rnum1==9:
                    logger.info("君与彼女与彼女之恋")
                    s=[Image(path='data/galgame/junbi.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '君与彼女与彼女之恋\n大名鼎鼎的十二神器之一，“次元牢笼”《君与彼女与彼女之恋》绝对能狠狠敲打gal玩家的心灵，玩的越多，伤害越高（暴论）！\n在牛头人和纯爱战士之间反复横跳的你，是被她心甘情愿抓回囚于次元牢笼，书写纯爱，还是放弃深爱你的她，追逐那个注定不能独享的她？')
                if rnum1==10:
                    logger.info("海市蜃楼之馆")
                    s=[Image(path='data/galgame/haishishenlou.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'海市蜃楼之馆\n爱与罪的悲剧诗:海馆的画风，无论人物、背景都有着厚重的油彩感，前几章依次呈现不同时代的故事，充满了历史气息，同时与本作的音乐非常搭配，带玩家沉浸在那座若隐若现，庄严又悲寂的馆中。海馆的音乐在我玩过的gal里绝对是一流水平，情绪调动和氛围营造非常强，略显简单的曲调满溢着真挚的感情，像少女纯洁的吟唱，像吟游诗人在酒馆唱的歌，像底噪略大的留声机流露的旧朝之音。不同时代的音乐也有着强烈时代特色，是馆最突出的亮点之一了.')
                if rnum1==11:
                    logger.info("带我去地下城吧")
                    s=[Image(path='data/galgame/daiwoqudixiacheng.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '带我去地下城吧\n一款很不错的国产SLG，画面流畅精美，女主人设讨人喜欢，探图出现的各类随机事件也挺有新意（虽然在一次次闯关后有些重复），最大的缺点可能就是关卡太少、流程太短了\n本作背景设定十分简单粗暴，男主穿越到异世界，与女主一同闯荡地下城，打算借潜藏在地下城最深处的神器回家，而女主也为找寻走丢的妹妹与男主共同冒险（虽然实际只有女主自己在打）。')
                if rnum1==12:
                    logger.info("Hirahira Hihiru")
                    s=[Image(path='data/galgame/Hirahira-Hihiru.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Hirahira Hihiru\n以青年医生千种正光和男学生天间武雄的两个视角，展开关于架空疾病“风腐症”（hihiru，夕零）的医学伦理学探讨。\n濑户口一贯优秀的文笔，令医学生也能认同的医学讨论，水平扎实的作画和音乐，可以说前面一直很享受，但是打完总觉得后劲不足，可能是缺了点……再多发发疯啊濑户口。')
                if rnum1==13:
                    logger.info("Chaos:Child")
                    s=[Image(path='data/galgame/ChaosChild (2).png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Chaos:Child\n科学adv系列妄想科学chaos;head(后续简称为chn,石头门简称sg)同世界观续作，时间设定在涩谷大地震(chn，2009)的六年后，发生了被称作“新时代疯狂(new generation,chn的事件)的再袭”的连续猎奇杀人事件，就读于涩谷私立高中"碧朋学园"并担任新闻部部长的高三生宫代拓留，乐此不疲的进行着追查事件的“社团活动”，从旁观者逐渐卷入事件漩涡，真相究竟怎样，他与“她”的命运将会如何...')
                if rnum1==14:
                    logger.info("少女领域")
                    s=[Image(path='data/galgame/shaonvlingyu.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '少女领域\n这部游戏往往因为男主飞鸟湊的男妈妈属性和调色板社这一被分割商法毒害的公司而知名，因此我反而想强调一下日向的萌点——中二病. 比较奇葩的一点是我玩 Galgame 比追番还早，所以《少女*领域》就神奇地让我第一次  get 到中二病的属性.')
                if rnum1==15:
                    logger.info("星空列车与白的旅行")
                    s=[Image(path='data/galgame/xingkongliehce.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '星空列车与白的旅行\n“这场旅行，究竟会在她身上，留下什么呢”\n一个夏日，一辆列车，一次旅途，一场重生。燥热的夏日傍晚，踏上老旧的蒸汽列车，这场梦与现实交织的旅行，会带给几位绝望之人，怎样的思考呢？\n游戏的整体氛围十分温馨，前期剧情缓慢而放松，温馨的日常旅途，逐渐解开各位的心结，而后期被隐藏在主线之下的冲突逐渐浮上水面，节奏紧张而快速。整部作品没有各种玄乎其玄的具体设定支撑，更偏向于感性的散文的味道，能够直接触动人的心弦，像一个温馨的童话，温暖治愈着现实中的我们，给我们思考与希望。')
                if rnum1==16:
                    logger.info("Rewrite")
                    s=[Image(path='data/galgame/Rewrite.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ 'Rewrite\n熬过去共通之后的故事部分真的还可以\n虽然前半段共通线的日常一点也不有趣\n推荐程度的话，额，真的是故事很好的一个全年龄作品，算得上老少咸宜吧，共通线日常以外的地方可以很高分，忍一忍还是能有一段很不错的经历的，还是建议嘎鲁给老手或者像看故事的人玩一玩，入坑的话不好推荐')
                if rnum1==17:
                    logger.info("想要传达给你的爱恋")
                    s=[Image(path='data/galgame/xiangyaochuandadeailian.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '想要传达给你的爱恋\n想要传达给你的爱恋，简称恋彼女，这是一部对我影响颇深的作品。\n推这部作品的时候正是高三下学期，我首先推的彩音线。我惊叹于男主表白时，剧本家对回收先前伏笔的高超处理，这让我对这部作品的剧本水平有了很大的信心。\nTrue Ending实实在在地让我破防了，推完TE的时候是凌晨四点，\n转天是一模考试，最后我的数学取得了全班倒数第二的好成绩，我的数学老师第一次主动和我的父母取得了联系')
                if rnum1==18:
                    logger.info("古色迷宫轮舞曲")
                    s=[Image(path='data/galgame/guse.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '古色迷宫轮舞曲\n闲静住宅街一角的茶馆『红茶馆・童话之森』。\n主人公・名波行人被难以言喻的既视感所诱惑，成为了在这打工的一员――而就在同一天，店里送来了一只大木箱。\n装在木箱里的，是大量的兔子玩偶……还有，一名银发红瞳的谜样少女。\n自称saki的少女向行人作出如下宣告。\n『“命运之轮”陷入错乱』\n『一周后，行人的“死”将是既成事实』\n『行人身边的人将陆续遭遇“不幸”』\n>>>>')
                if rnum1==19:
                    logger.info("夏娃年代记")
                    s=[Image(path='data/galgame/xiawa.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '夏娃年代记\n由Alicesoft出品，是一款挺不错的RPG，无缝大世界探索冒险收集游戏，尽管无法扛起前辈兰斯系列的大旗，但该作品的优良程度是毋庸置疑的。\n该系列世界框架搭建宏大精良（因为毕竟要出续作），至少做到了完美支撑起十余个小时的故事情节发展和转折，且留有很多有意思的小细节供玩家探索，')
                if rnum1==20:
                    logger.info("《缘之空》及续作《悠之空》")
                    s=[Image(path='data/galgame/yuanzhikong.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《缘之空》及续作《悠之空》\n相信各位资深或者萌新二次元们都早已耳闻穹妹的大名，不过真正玩过缘之空的有多少呢？\n恐怕更多人只是了解了梗（德国骨科，玄关之战这类的吧），或者仅仅只是看过番剧。\n但是缘之空的番剧改编其实是很烂的，剧情发展完全体现不出来，更像是里番，男主当推土机。\n因此要推荐各位去玩缘之空，体验原汁原味的剧情。')
                if rnum1==21:
                    logger.info("Kud Wafter")
                    s=[Image(path='data/galgame/kudwafter.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Kud Wafter\n首先，我不是萝莉控，只是我喜欢的角色刚好是一个萝莉而已（）\n')
                if rnum1==22:
                    logger.info("《baldr sky dive》系列")
                    s=[Image(path='data/galgame/brladrsky.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'《baldr sky dive》系列\n“我不会忘记，那里曾有着无可替代的天空”\nbaldr sky dive并非普通的ADV类型游戏，而是一部ACT类型的硬核作品，机甲对战的玩法设计贯穿游戏始终，战斗系统深度较高，繁多的技能可以拼凑起花式的连招,真正掌握精髓后会特别有趣。')
                if rnum1==23:
                    logger.info("生命的备件")
                    s=[Image(path='data/galgame/shengming.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '生命的备件\n一部让正常人抑郁，让抑郁症患者重拾对生活的信心的游戏。该作环境代入感很强，樱纹病的压迫充斥着全作品的每个字节，死亡已成既定的事实，男主和女友惠璃的生命空间随时间流逝逐步缩小，最后樱花树下的告别让人痛彻心扉\n作愿天堂无樱纹病，但有樱花，“我爱你，真的至死不渝”。故事进行到最后，压根不需要考虑游戏结尾的画面精美与否，因为泪水早把眼睛盖住了。')
                if rnum1==24:
                    logger.info("壳之少女")
                    s=[Image(path='data/galgame/kezhishaonv.png')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '壳之少女\n不知道有多少人是被一首《琉璃之鸟》骗来的，反正我是（\n少女三部曲也算名作了，一大原因是剧情设计确实优秀，但另一大原因是游戏系统非常复杂，即使完全按攻略也要耗费相当精力才能达成全结局全 CG')
                if rnum1==25:
                    logger.info("网站推送")
                    await bot.send(event, '欢迎来到我的小站观看，这里有很多东西哦~~：http://www.manshuo.ink/')
                
                if rnum1==26:
                    logger.info("恋爱，我借走了")
                    s=[Image(path='data/galgame/恋爱，我借走了main.webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '恋爱，我借走了\n「请和我交往！」\n「不、不能随便摸哟？你会注意的对吧！？」\n「性癖和姐姐不一样。」\n「我想让你做我的“情人”呢。」\n「给，这是朋友费。」\n「为什么会变成这样……」\n这是妹控男主角，新海幸的故事///')
                if rnum1==27:
                    logger.info("寄宿之恋")
                    s=[Image(path='data/galgame/280px-寄宿之恋.webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '寄宿之恋\n主人公濑户田拓真回到了他小时候生活的小镇。\n这是为了离开双亲而独自生活。\n这座小镇充满了他小时候的回忆，为了正常生活和上学，拓真想在某个地方先暂住下来，\n然而身无分文的他走投无路。\n就在这时，儿时的青梅竹马们\n向拓真伸出了援助之手！\n虽然不能一直住下去，但如果是暂时轮换地寄住在青梅竹马们的家里，家人应该会同意的吧。')
                if rnum1==28:
                    logger.info("劈腿之恋")
                    s=[Image(path='data/galgame/300px-恋爱成双.webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '劈腿之恋\n浑身舒爽地醒来，伴随着朝阳……以及某人的体温。\n“你要负起责任啊……那个……跟我交往吧。\n联谊时遇到的女人·十色煌，原本只是想照顾一下，结果一起过了一夜。\n主人公古贺凪青在彼此都不太了解的情况下，承担起了责任。\n“和我交往吧！开不开心，古贺君?”\n与此同时他的单恋对象，信田结爱也单方面地宣布了交往。\n一直保持着对她的喜欢，事到如今想拒绝也拒绝不了————\n就这样，主人公交了两个女朋友，脚踏两条船的渣男诞生了。')
                if rnum1==29:
                    logger.info("八卦恋爱")
                    s=[Image(path='data/galgame/300px-Koibana.webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '八卦恋爱\n因为少子化什么的那些大人的原因，就读的学校关闭、从今年开始配合附近作为大小姐学校而闻名的樱华学园的共学化而编入其中的主人公叶太和他的朋友们。\n「「「机会难得，想交个女朋友！！！」」」\n怀着这样平凡的欲望，他们期待着与清纯系大小姐女生们的新生活。「「「好像和想象中的不一样！！！」」」')
                if rnum1==30:
                    logger.info("《千恋＊万花》")
                    s=[Image(path='data/galgame/280px-千戀＊萬花遊戲封面 (1).webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《千恋＊万花》\n春假时被母亲拜托到外公于温泉街“穗织”开的旅馆帮忙的男主角有地将臣，在参加建实神社举办的拔出神刀“丛雨丸”的活动时无意中折断了刀，并被建实神社的神主朝武安晴要求和女儿朝武芳乃结婚。\n因为这场意外而就此于穗织居住的将臣，逐渐发现了穗织诅咒的秘密。')
                if rnum1==31:
                    logger.info("《魔女的夜宴》")
                    s=[Image(path='data/galgame/280px-Img_prize22 (1).webp')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '《魔女的夜宴》\n绫地宁宁!!!!!!!!!!!!!!!\n🥵是、是的…♡我想绫地宁宁!我真的想要很多绫地宁宁♡🥵给我…好想要…想要见到绫地宁宁…♡呜呜、不行了,我已经变成看不到绫地宁宁就不行的笨蛋了……啊啊♡好喜欢♡更多的、可爱的绫地宁宁…是、哪怕有绫地宁宁也会觉得不够,什么时候都想要好多好多的绫地宁宁,除了绫地宁宁已经什么都想不了了……🥵')
                if rnum1==32:
                    logger.info("Summer Pockets")
                    s=[Image(path='data/galgame/280px-Sprb_main_img.webp')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Summer Pockets\n唯有那份眩目　未曾忘却。\n无论何时，我都会记得夏天的蓝……。\n与眺望大海的少女相遇，\n与寻找不可思议蝴蝶的少女相遇，\n与寻找回忆与海盗船的少女相遇，\n与住在宁静灯塔中的少女相遇，\n在岛上结识了新的伙伴——\n当时的他想，如果这个暑假永远都不结束就好了。')
                if rnum1==33:
                    logger.info("时廻者")
                    s=[Image(path='data/galgame/loppers.jpg')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '时廻者\n一日黄粱一场梦，一生游戏一生情\n相信奇迹的人，本来就是一个奇迹。由这些奇迹的结合才造就了《时廻者》。在我看来，《时廻者》就像小时候放在床头的童话书，你没有理由去相信，但你会这么做。它会回荡在你的思想里，只留下一点小小的回声。在你思想成熟之后，在你遇见相同的故事时，会逐渐温暖你，让你会心一笑')
                if rnum1==34:
                    logger.info("9-nine-九次九日九重色")
                    s=[Image(path='data/galgame/9nine.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'9-nine-九次九日九重色\n作为整部系列的第一部作品，只能说中规中矩，但是，感情线与人物塑造写真的挺好，嘛，谁会拒绝一个经常来你家做饭，而极其温柔，呆萌却又富有正义感的，庶民大小姐呢？总体下来感情线非常细腻，人物塑造也非常的成功！综合评价：8.6/10 \n个人吐槽：九条可爱捏！！甜甜的日常太少辣！还有九条能力居然用在那种地方........确实非常的方便！（玩过的懂得都懂）')
                if rnum1==35:
                    logger.info("9-nine-天色天歌天籁音")
                    s=[Image(path='data/galgame/9-nine-天色天歌天籁音.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'9-nine-天色天歌天籁音\n本作对妹妹天的塑造可以说是相当成功，在声优桐谷华的倾情演绎之下，将天的活泼可爱，爱开玩笑，天真烂漫，兄控，爱看电视玩游戏，经常和哥哥掰嘴，在表面的精神焕发下其实也隐藏着胆小和孤独的一面，惹人怜爱的形象完美的呈现！然后再加上由和泉绘制的精美的立绘与CG，直接绝杀！天是这9nine系列里最喜欢角色，嘛，谁会拒绝一个爱跟你掰嘴的妹妹呢，妹妹是天！妹妹是天！！妹妹是天！！！（双关）')
                if rnum1==36:
                    logger.info("9-nine-春色春恋春熙风")
                    s=[Image(path='data/galgame/9-nine-春色春恋春熙风.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'9-nine-春色春恋春熙风\nCG相比于前两作，个人觉得有比较大的进步，尤其在后面打伊莉丝那里，春的高光CG居然是动态的！！以及后续翔与春的约会CG，都让我眼前一亮，十分的精致唯美，看来调色板是真的狠狠砸钱了。ed是我已经推完三作里最喜欢的歌了，ed画面明显更加用心')
                if rnum1==37:
                    logger.info("9-nine-雪色雪花雪余痕")
                    s=[Image(path='data/galgame/9-nine-雪色雪花雪余痕.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'9-nine-雪色雪花雪余痕\n雪雪雪中女主希亚作为囊括了废萌中二反差萌为一体的女主，她的人设上可以说是跳出了以往的风格套路，惹人喜爱。比起前三作，第四作可谓是制作精良，不仅填补了许多前作的坑，而且整体剧情更是爽快而又令人震撼，尤其是将玩家带入剧情的迭代设定让人身临其境体会到故事的变化与发展')
                if rnum1==38:
                    logger.info("9-nine")
                    s=[Image(path='data/galgame/a7ff884ce764b92fcee3d8d30c756874.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'9-nine全系列！！！！\n9-nine-九次九日九重色\n9-nine-天色天歌天籁音\n9-nine-春色春恋春熙风\n9-nine-雪色雪花雪余痕')
                if rnum1==39:
                    logger.info("ラブピカルポッピー！")
                    s=[Image(path='data/galgame/0005847151_B.jpg')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ 'ラブピカルポッピー！\n10小时推完妹妹线，日常有意思不瞌睡，妹妹线甜死我了，这作妹妹真是又可爱又有意思又涩还是实妹特戳我，最后的婚纱推得差点掉小珍珠了，涼花我的涼花我妹妹太可爱了嘿嘿嘿嘿嘿嘿嘿嘿嘿')
                if rnum1==40:
                    logger.info("大逆转裁判")
                    s=[Image(path='data/galgame/R-C.jpg')]
                    await bot.send(event, s)
                    await bot.send(event,"序号:"+str(rnum1)+";"+ '大逆转裁判编年史\n本作剧情总的来说相当出色，故事的大小反转都做到了意料之外、情理之中。相比起系列其他作品，本作少了些天马行空的设定，但也在故事发展上更加大胆。唯一的遗憾就是一代的叙事节奏稍显拖沓。\n人设方面，用一个词概括的话就是讨喜。无论是主角团或是反派，诸如可爱、帅气、成熟、善良、聪慧等等词汇都可以安插在大部分人身上，但又不会完美到令人反感。')
                if rnum1==41:
                    logger.info("clannad")
                    s=[Image(path='data/galgame/clanned.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'clannad\n即使它已经出圈，即使它已经有一定年代，它永远都是我个人心中当之无愧的NO1。\n 家族，亲情，爱情，友情，奇迹，未来，希望——KEY的作品永远闪耀着人性的光辉,绝大多数人看了KEY的作品都会落泪，可是落泪的同时我们却在幸福的微笑着，在温馨而美好的音乐中我们潸然泪下，留在心头的却是让人无法释怀的美丽与爱，还有对未来的憧憬')
                if rnum1==42:
                    logger.info("素晴日")
                    s=[Image(path='data/galgame/suqingri.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'素晴日-美好的每一天～不连续的存在\n在这里可都得好好感谢下SCA自了，你可是真的干得好啊！（各种意义上），开头的温馨百合日常很甜，接着就是SCA自的独特传教时间了，用将近一半的充斥着电波的篇幅和近乎无视常理的剧情对玩家的精神进行不间断的轰炸，可以说对很多人来说都直接劝退了，不得不说这段SCA自的电波轰炸着实够猛，游玩完当晚剧情的笔者直接睡不着了，只觉得胸口压了大石，满脑袋充斥着愤怒、悲伤等各种混杂在一起的情绪，如今再度回望整个剧情和当时的自己，还真的会有种莫名的沧桑感')
                if rnum1==43:
                    logger.info("Eden*")
                    s=[Image(path='data/galgame/eden.png')]
                    await bot.send(event, s)
                    await bot.send(event, "序号:"+str(rnum1)+";"+'Eden*\n《Eden*》的演出方式比较特殊，galgame常见有重复利用人物立绘+不同背景+对话框，这种第一人称的叙事角度因身临其境的让我比较有代入感，只有少数几张CG才会gal里面的“我”的身影。\n 《Eden*》中天門还大量使用了八音盒音色增加轻盈、静谧、宁静的感觉，配上游戏下半部田园生活期的精致背景和CG，使这段地球上最后二人的爱情故事更为动人')
                await bot.send(event, '详情请前往以下网站查看：http://www.manshuo.ink/index.php/archives/294/')