<div align="center">
  <img src="https://socialify.git.ci/avilliai/Manyana/image?description=1&descriptionEditable=based%20on%20mirai&font=Inter&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Favilliai%2FimgBed%2Fmaster%2Fimages%2FwWFSwF6A.png&name=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light" alt="Manyana" /></br>
</div>

----
# 🎆鸣谢

- [Mirai框架](https://github.com/mamoe/mirai)
- [petpet](https://github.com/Dituon/petpet) 
- [CjangCjengh-MoeGoe](https://github.com/CjangCjengh/MoeGoe) vits语音合成功能来源
- [coze-discord-proxy](https://github.com/deanxv/coze-discord-proxy) 通过discord白嫖gpt4(用户多不建议用这个。)
- [overflow](https://mirai.mamoe.net/topic/2565/overflow-%E5%B0%86-mirai-%E5%AE%9E%E7%8E%B0%E6%8D%A2%E6%88%90-onebot-%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%9A%84%E5%8F%88%E4%B8%80%E4%B8%AA%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88?_=1712421277845)     你懂的
- [arona api](https://doc.arona.diyigemt.com/)  提供blueArchive数据支持
- [star-rail-atlas](https://gitee.com/Nwflower/star-rail-atlas)  数据支持
- [Yiri-mirai](https://github.com/YiriMiraiProject/YiriMirai)  很好的python sdk
- [install_llob](https://github.com/super1207/install_llob) llob安装器，帮大忙了
- 如果遇到使用问题，请在QQ群623265372反馈


<div align="center">
   <img width="70%" height="70%" src="https://moe-counter.glitch.me/get/@:manyana" alt="logo"></br>
</div>

---

# 🚀linux部署
[linux部署脚本](https://github.com/lux-QAQ/Manyana_deploy)

# 🚀windows部署
**如果你没有代理，或git连接不稳定，可在搭建时选择【镜像源】，镜像源和git源完全同步更新。**<br>

 压缩包中附带了readme.txt 照做就行<br>
 能用Launcher改设置就用launcher改，不规范地修改文件导致的格式错误自行搜索解决。<br>
## 方法1：搭建工具部署(推荐)
**如果你觉得自己从零开始搭建bot比较困难，请使用此方案**<br>
对于windows用户，存在两款启动器，分别是[Manyana1.x](https://github.com/avilliai/Manyana/releases) 和[Manyana_deploy](https://github.com/lux-QAQ/Manyana_deploy/releases) 你可以根据自己的喜好选择<br>
[Manyana1.x](https://github.com/avilliai/Manyana/releases)使用方式如下。
- 从[release](https://github.com/avilliai/Manyana/releases)下载LAUNCHER-all-requirements.rar并解压
  - 如果下载过慢，你也可以从Q群623265372获得这个压缩包
- 运行launcher.exe<br>
- 点击主界面 克隆仓库(没有自己的onebot实现的，需要额外安装onebot文件夹下的两个文件，先qq后llob_install)
- 关闭launcher，重启launcher
- 此时可以看到主界面已经变化，填写主界面设置并保存。使用压缩包仅需修改前四项。<br>
- 在第二个页面，依次启动overflow和Manyana<br>

## 方法2：不使用release(不推荐，除非你有丰富bot搭建经验)
- 请确保py版本为3.9
- 请确保已安装[mirai-api-http](https://github.com/project-mirai/mirai-api-http) 并[正确配置](https://github.com/avilliai/wReply/blob/master/setting.yml)
- 强烈推荐使用[release](https://github.com/avilliai/Manyana/releases))的LAUNCHER_ALL_Requirements.rar进行部署，请参考 搭建工具部署 部分，这将省去大量折腾的时间。
### 如果你仍坚持不使用一键包
- 从[release](https://github.com/avilliai/wReply/releases/tag/yirimirai-Bot)下载python39_amd.exe并安装，(**安装python39的第一步一定要先勾选add to path**)
- 克隆本仓库。找一个你喜欢的目录(**不要带中文**)打开cmd或git bash执行
```
git clone --depth 1 https://github.com/avilliai/Manyana.git
或使用镜像源
git clone --depth 1 https://mirror.ghproxy.com/https://github.com/avilliai/Manyana
其他镜像源(推荐)
git clone --depth 1 https://github.moeyy.xyz/https://github.com/avilliai/Manyana
国内镜像(最快)
git clone --depth 1 https://www.gitlink.org.cn/lux-QAQ/Manyana
```
- 双击Manyana/一键部署脚本.bat即可
- 填写config.json(必做，填写方式见下方)

```
Manyana/config.json的填写示例如下。
{"botName": "机器人名字", "botQQ": "机器人QQ", "master": "你的QQ", "mainGroup": "你自己群的群号","vertify_key": "这里写你http-api的key,尖括号不用带", "port": "httpapi的ws运行端口"}
下面是一个config.json填写实例，如使用整合包，不要修改后两项
{"botName": "Manyana", "botQQ": "1283992481", "master": "1840094972","mainGroup": "623265372", "vertify_key": "1234567890", "port": "23456"}
```
`对于verify_key和port，如果你用了我上面给出的【正确配置】，那就不用动这两项。`
- 启动bot
  - 自行搭建：启动你自己的mirai或overflow，以及Manyana/启动脚本.bat

---
# 🍩功能
#### 功能列表

搭建后在群内发送@bot 帮助 以查看功能列表。其他相关问题请查看[Manyana wiki](https://github.com/avilliai/Manyana/wiki)

<details markdown='1'><summary>图片版菜单</summary>

<div align="center">
   <img width="70%" height="70%" src="data/fonts/help1.png" alt="logo"></br>
   <img width="70%" height="70%" src="data/fonts/help2.png" alt="logo"></br>
   <img width="70%" height="70%" src="data/fonts/help3.png" alt="logo"></br>
   <img width="70%" height="70%" src="data/fonts/help4.png" alt="logo"></br>
   <img width="70%" height="70%" src="data/fonts/master.png" alt="logo"></br>
</div>

</details>


#### 未来更新计划
由于学业繁忙，下面这些可能要到明年才能开始了，如果您有意向参与开发，欢迎pr🏵
- [x] 降低耦合度，进一步优化承载收发功能的run文件夹下各文件
- [ ] 适配tg、discord、微信等平台(完成上一目标后)
- [ ] 各大手游/端游数据查询
- [ ] 更换sdk
- [x] 词库优化
- [x] UI重制
- [x] 优化搭建引导
- [ ] jmcomic对接


# 🎲可选配置
<details markdown='1'><summary>填写配置文件</summary>

有关配置文件的填写，config文件夹每个yaml文件基本都有注释，每个yaml文件几乎都是可供修改的，默认的记事本即可打开yaml文件，但对于windows用户尤其是不熟悉yaml用户结构的用户来说，我们强烈建议在launcher的UI中进行配置文件的修改，而不是通过记事本。

不规范地修改配置文件将破坏yaml文件结构并最终导致bot无法运行。

</details>

<details markdown='1'><summary>ai回复配置方式</summary>

请查看[Manyana wiki](https://github.com/avilliai/Manyana/wiki/%E8%AE%BE%E7%BD%AEai%E5%AF%B9%E8%AF%9D%E6%A8%A1%E5%9E%8B)

</details>


# 🎄最后
如果觉得项目还不错的话给个star喵，给个star谢谢喵
![Star History Chart](https://api.star-history.com/svg?repos=avilliai/Manyana&type=Date)

其他相关项目如下
- [Enkianthus_tts](https://github.com/avilliai/Enkianthus_tts) 简单易用的语音合成工具
- [Petunia](https://github.com/avilliai/Petunia/releases) 轻量版Manyana，无需搭建环境，已打包
- [Amaranth](https://github.com/avilliai/Amaranth) 欢迎关注我们的新版启动器
- [Eridanus](https://github.com/avilliai/Eridanus) Manyana直接对接onebot实现的版本，欢迎参与开发

感谢JetBrains提供的开源项目license<br>
<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm_icon.png" alt="PyCharm logo." width="50">
